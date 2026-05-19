#!/usr/bin/env bash
# Deploy the Tools Portal container on the Lightsail server.
# Mirrors the convention used by deploy_myapp.sh (git pull -> build -> run),
# but isolated: own image, own container name, own port (8082).
set -euo pipefail

REPO_DIR="$HOME/ClaudeCodeTry"
IMAGE="tools-portal:latest"
NAME="tools-portal"
HOST_PORT="8082"   # Caddy reverse-proxies tools.sebastianclaw.com -> 127.0.0.1:8082

cd "$REPO_DIR"
git pull

APP_VERSION="$(git rev-parse --short HEAD)"

docker build -t "$IMAGE" .
docker rm -f "$NAME" 2>/dev/null || true

# --env-file loads MISTRAL_API_KEY (kept on the server only, never in git).
docker run -d --name "$NAME" --restart unless-stopped \
  -e APP_VERSION="$APP_VERSION" \
  --env-file "$REPO_DIR/.env" \
  -p 127.0.0.1:${HOST_PORT}:8080 "$IMAGE"

echo "Deployed OK:"
docker ps --filter "name=${NAME}"
sleep 2
curl -s "http://127.0.0.1:${HOST_PORT}/health" ; echo
