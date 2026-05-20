"""PDF -> Excel / Word / PowerPoint tool (Mistral OCR) as a Flask Blueprint."""
import os
import re
import io
from flask import Blueprint, request, jsonify, send_file, render_template
from mistralai import Mistral

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

from docx import Document
from docx.shared import Pt as DocxPt
from docx.enum.text import WD_BREAK

from pptx import Presentation
from pptx.util import Inches, Pt as PptxPt
from pptx.dml.color import RGBColor

TOOL = {
    "slug": "pdf-converter",
    "name": "PDF Converter",
    "description": "Convert any PDF to Excel, Word, or PowerPoint using Mistral OCR.",
    "icon": "📄",
    "url": "/tools/pdf-converter",
}

bp = Blueprint(
    "pdf_converter",
    __name__,
    url_prefix="/tools/pdf-converter",
)


# --- Shared OCR + markdown parsing ---------------------------------------

def parse_markdown_page(markdown_text):
    """Split a page's markdown into blocks: 'table' or 'text'."""
    blocks = []
    lines = markdown_text.split("\n")
    i = 0
    while i < len(lines):
        if re.match(r"^\s*\|", lines[i]):
            table_lines = []
            while i < len(lines) and re.match(r"^\s*\|", lines[i]):
                table_lines.append(lines[i])
                i += 1
            blocks.append({"type": "table", "content": table_lines})
        else:
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
        if re.match(r"^\s*\|[\s\-:]+\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def run_ocr(pdf_file):
    """Upload PDF to Mistral, run OCR, return (pages, base_name)."""
    api_key = os.environ.get("MISTRAL_API_KEY", "")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY not configured on server")

    pdf_bytes = pdf_file.read()
    client = Mistral(api_key=api_key)

    uploaded = client.files.upload(
        file={"file_name": pdf_file.filename, "content": pdf_bytes},
        purpose="ocr",
    )
    signed_url = client.files.get_signed_url(file_id=uploaded.id)
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={"type": "document_url", "document_url": signed_url.url},
    )

    try:
        client.files.delete(file_id=uploaded.id)
    except Exception:
        pass

    base_name = os.path.splitext(pdf_file.filename)[0]
    return ocr_response.pages, base_name


# --- Excel builder -------------------------------------------------------

def _write_page_to_sheet(ws, blocks):
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
            current_row += 1
        else:
            for line in block["content"].split("\n"):
                line = line.strip()
                if line:
                    ws.cell(row=current_row, column=1, value=line)
                    current_row += 1
            current_row += 1


def _auto_fit_columns(ws):
    for col in ws.columns:
        max_len = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = min(max_len + 4, 60)


def build_excel(pages):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for page_idx, page in enumerate(pages):
        ws = wb.create_sheet(title=f"Page {page_idx + 1}")
        blocks = parse_markdown_page(page.markdown)
        _write_page_to_sheet(ws, blocks)
        _auto_fit_columns(ws)
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output


# --- Word builder --------------------------------------------------------

def build_word(pages):
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = DocxPt(11)

    for page_idx, page in enumerate(pages):
        if page_idx > 0:
            doc.add_page_break()
        doc.add_heading(f"Page {page_idx + 1}", level=1)

        blocks = parse_markdown_page(page.markdown)
        for block in blocks:
            if block["type"] == "table":
                rows = parse_table_rows(block["content"])
                if not rows:
                    continue
                n_cols = max(len(r) for r in rows)
                table = doc.add_table(rows=len(rows), cols=n_cols)
                table.style = "Light Grid Accent 1"
                for r_idx, row in enumerate(rows):
                    for c_idx, cell_val in enumerate(row):
                        if c_idx >= n_cols:
                            continue
                        cell = table.cell(r_idx, c_idx)
                        cell.text = cell_val
                        if r_idx == 0:
                            for para in cell.paragraphs:
                                for run in para.runs:
                                    run.bold = True
                doc.add_paragraph()
            else:
                for line in block["content"].split("\n"):
                    line = line.strip()
                    if line:
                        doc.add_paragraph(line)

    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    return output


# --- PowerPoint builder --------------------------------------------------

def _pick_font_size(total_lines):
    """Pick a font size so total_lines fit one 16:9 slide body."""
    # body area ~6.5" tall, line height ~= 1.4 * font_pt (in points; 72pt = 1in)
    if total_lines <= 22:
        return 14
    if total_lines <= 32:
        return 11
    if total_lines <= 45:
        return 9
    if total_lines <= 65:
        return 7
    return 6


def _estimate_lines(blocks):
    total = 0
    for block in blocks:
        if block["type"] == "table":
            total += max(1, len(parse_table_rows(block["content"])))
        else:
            for line in block["content"].split("\n"):
                if line.strip():
                    total += 1
    return total


def build_pptx(pages):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for page_idx, page in enumerate(pages):
        slide = prs.slides.add_slide(blank_layout)
        blocks = parse_markdown_page(page.markdown)

        # Title bar
        title_box = slide.shapes.add_textbox(
            Inches(0.3), Inches(0.15), Inches(12.7), Inches(0.5)
        )
        title_tf = title_box.text_frame
        title_tf.text = f"Page {page_idx + 1}"
        title_run = title_tf.paragraphs[0].runs[0]
        title_run.font.size = PptxPt(20)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)

        # Body — flatten everything into one text frame, scale font to fit
        total_lines = _estimate_lines(blocks)
        font_pt = _pick_font_size(total_lines)

        body_box = slide.shapes.add_textbox(
            Inches(0.3), Inches(0.75), Inches(12.7), Inches(6.6)
        )
        body_tf = body_box.text_frame
        body_tf.word_wrap = True

        first_para = True

        def add_line(text, bold=False):
            nonlocal first_para
            p = body_tf.paragraphs[0] if first_para else body_tf.add_paragraph()
            first_para = False
            p.text = text
            for run in p.runs:
                run.font.size = PptxPt(font_pt)
                if bold:
                    run.font.bold = True

        for block in blocks:
            if block["type"] == "table":
                rows = parse_table_rows(block["content"])
                for r_idx, row in enumerate(rows):
                    add_line("  |  ".join(row), bold=(r_idx == 0))
                add_line("")
            else:
                for line in block["content"].split("\n"):
                    if line.strip():
                        add_line(line.strip())
                add_line("")

    output = io.BytesIO()
    prs.save(output)
    output.seek(0)
    return output


# --- Routes --------------------------------------------------------------

@bp.route("/")
def index():
    return render_template("pdf_converter.html", tool=TOOL)


_FORMATS = {
    "excel": {
        "builder": build_excel,
        "ext": "xlsx",
        "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    },
    "word": {
        "builder": build_word,
        "ext": "docx",
        "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    },
    "pptx": {
        "builder": build_pptx,
        "ext": "pptx",
        "mime": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    },
}


def _convert(fmt):
    if "pdf" not in request.files:
        return jsonify({"error": "No PDF file provided"}), 400

    pdf_file = request.files["pdf"]
    if not pdf_file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "File must be a PDF"}), 400

    spec = _FORMATS[fmt]

    try:
        pages, base_name = run_ocr(pdf_file)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    output = spec["builder"](pages)
    download_name = f"{base_name}_ocr.{spec['ext']}"

    return send_file(
        output,
        mimetype=spec["mime"],
        as_attachment=True,
        download_name=download_name,
    )


@bp.route("/convert/excel", methods=["POST"])
def convert_excel():
    return _convert("excel")


@bp.route("/convert/word", methods=["POST"])
def convert_word():
    return _convert("word")


@bp.route("/convert/pptx", methods=["POST"])
def convert_pptx():
    return _convert("pptx")
