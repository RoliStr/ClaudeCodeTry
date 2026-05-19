FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Server convention: containers listen on 8080, Caddy reverse-proxies to them.
EXPOSE 8080

# 1 worker + threads keeps memory low (small Lightsail box) while still
# handling concurrent uploads, since OCR is I/O-bound on the Mistral API.
# Long timeout: large/scanned PDFs can take a while to OCR.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "--timeout", "300", "app:app"]
