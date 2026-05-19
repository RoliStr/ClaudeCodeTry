# Tools Portal

A multi-tool web portal. The landing page lists every available tool; pick one to use it.

**Available tools**

| Tool | What it does |
|---|---|
| **PDF → Excel** | Upload a PDF, get a structured Excel back (Mistral OCR). One sheet per page; tables as grids, text in column A. |

More tools can be added easily (see "Adding a tool" below).

## Quick start (local)

**1. Add your Mistral API key**
```bash
cp .env.example .env
# Edit .env and paste your MISTRAL_API_KEY
```

**2. Run with Docker**
```bash
docker compose up --build
```

**3. Open** `http://localhost:5000` — pick a tool from the portal.

Get a Mistral key at [console.mistral.ai](https://console.mistral.ai) → API Keys.

### Run locally without Docker
```bash
pip install -r requirements.txt
cp .env.example .env   # add your key
python app.py
```

## Production (Lightsail + Caddy)

The container listens on `8080`. On the server it runs bound to `127.0.0.1:8082`,
with Caddy reverse-proxying `tools.sebastianclaw.com` → `127.0.0.1:8082` (auto-HTTPS).

Deploy / redeploy:
```bash
./deploy_tools.sh
```
This pulls latest, rebuilds the image, and restarts the `tools-portal` container.
`MISTRAL_API_KEY` lives only in `~/ClaudeCodeTry/.env` on the server (never committed).

## Adding a tool

1. Create `tools/<your_tool>.py` defining a Flask `bp` (Blueprint, `url_prefix=/tools/<slug>`)
   and a `TOOL = {slug, name, description, icon, url}` dict.
2. Register it in `tools/__init__.py` by appending `(module.TOOL, module.bp)` to `REGISTRY`.

The portal landing page and routing pick it up automatically.

## Architecture

```
app.py              portal: landing page (/), /health, registers blueprints
tools/__init__.py   tool registry
tools/pdf_to_excel.py   PDF → Excel tool (Blueprint, /tools/pdf-to-excel)
templates/portal.html       tool grid landing page
templates/pdf_to_excel.html PDF tool UI
Dockerfile          gunicorn on :8080
deploy_tools.sh     server deploy script
```
