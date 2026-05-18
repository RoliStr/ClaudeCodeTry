# PDF → Excel (Mistral OCR)

Upload a PDF, get a structured Excel file back. Uses Mistral OCR to extract tables and text — one Excel sheet per PDF page.

## Quick start

**1. Add your Mistral API key**
```bash
cp .env.example .env
# Edit .env and paste your MISTRAL_API_KEY
```

**2. Run with Docker**
```bash
docker compose up --build
```

**3. Open** `http://localhost:5000` in your browser, drop in a PDF, download Excel.

## Getting a Mistral API key

Sign up at [console.mistral.ai](https://console.mistral.ai) → API Keys → Create new key.

## Excel output format

| Content type | Where it goes |
|---|---|
| Tables | Extracted as a grid with bold blue headers |
| Plain text | Each line in column A |
| Multiple pages | One sheet per page (`Page 1`, `Page 2`, …) |

## Run locally without Docker

```bash
pip install -r requirements.txt
cp .env.example .env   # add your key
python app.py
```
