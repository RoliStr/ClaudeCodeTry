import os
import re
import uuid
import io
from flask import Flask, request, jsonify, send_file, render_template
from mistralai import Mistral
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB limit

MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")


def parse_markdown_page(markdown_text):
    """
    Split a page's markdown into blocks: 'table' or 'text'.
    Returns list of {'type': 'table'|'text', 'content': ...}
    """
    blocks = []
    lines = markdown_text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detect start of a markdown table (line contains |)
        if re.match(r"^\s*\|", line):
            table_lines = []
            while i < len(lines) and re.match(r"^\s*\|", lines[i]):
                table_lines.append(lines[i])
                i += 1
            blocks.append({"type": "table", "content": table_lines})
        else:
            # Accumulate plain text until next table or end
            text_lines = []
            while i < len(lines) and not re.match(r"^\s*\|", lines[i]):
                text_lines.append(lines[i])
                i += 1
            text = "\n".join(text_lines).strip()
            if text:
                blocks.append({"type": "text", "content": text})

    return blocks


def parse_table_rows(table_lines):
    """Parse markdown table lines into list of row lists."""
    rows = []
    for line in table_lines:
        # Skip separator rows like |---|---|
        if re.match(r"^\s*\|[\s\-:]+\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def write_page_to_sheet(ws, blocks):
    """Write parsed blocks to an openpyxl worksheet."""
    current_row = 1
    header_font = Font(bold=True)
    header_fill = PatternFill("solid", fgColor="D9E1F2")

    for block in blocks:
        if block["type"] == "table":
            rows = parse_table_rows(block["content"])
            for r_idx, row in enumerate(rows):
                for c_idx, cell_val in enumerate(row):
                    cell = ws.cell(row=current_row, column=c_idx + 1, value=cell_val)
                    if r_idx == 0:
                        cell.font = header_font
                        cell.fill = header_fill
                        cell.alignment = Alignment(horizontal="center")
                current_row += 1
            current_row += 1  # blank row after table

        elif block["type"] == "text":
            for line in block["content"].split("\n"):
                line = line.strip()
                if line:
                    ws.cell(row=current_row, column=1, value=line)
                    current_row += 1
            current_row += 1  # blank row after text block


def auto_fit_columns(ws):
    for col in ws.columns:
        max_len = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = min(max_len + 4, 60)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF file provided"}), 400

    pdf_file = request.files["pdf"]
    if not pdf_file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "File must be a PDF"}), 400

    if not MISTRAL_API_KEY:
        return jsonify({"error": "MISTRAL_API_KEY not configured"}), 500

    pdf_bytes = pdf_file.read()
    client = Mistral(api_key=MISTRAL_API_KEY)

    # Upload PDF to Mistral and get signed URL
    uploaded = client.files.upload(
        file={"file_name": pdf_file.filename, "content": pdf_bytes},
        purpose="ocr",
    )
    signed_url = client.files.get_signed_url(file_id=uploaded.id)

    # Run OCR
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": signed_url.url},
    )

    # Build Excel workbook
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # remove default sheet

    for page_idx, page in enumerate(ocr_response.pages):
        sheet_name = f"Page {page_idx + 1}"
        ws = wb.create_sheet(title=sheet_name)
        blocks = parse_markdown_page(page.markdown)
        write_page_to_sheet(ws, blocks)
        auto_fit_columns(ws)

    # Stream Excel back to client
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    base_name = os.path.splitext(pdf_file.filename)[0]
    excel_filename = f"{base_name}_ocr.xlsx"

    # Clean up uploaded file from Mistral
    try:
        client.files.delete(file_id=uploaded.id)
    except Exception:
        pass

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=excel_filename,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
