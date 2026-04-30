#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# Deploy de imationgroup.com en el VPS, ejecutado por GitHub Actions.
# Asume:
#   - El repo está clonado en ~/apps/imationgroup-web
#   - Existe ~/apps/imationgroup-web/.env (no versionado, con SMTP_*)
#   - El usuario deploy pertenece al grupo docker
#   - Nginx sirve estáticos directamente desde ~/apps/imationgroup-web
#     (root /home/deploy/apps/imationgroup-web;) y hace proxy a 127.0.0.1:8001
#     para api.imationgroup.com.
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/apps/imationgroup-web}"
COMPOSE_FILE="docker-compose.yml"

echo "▶ Deploy iniciado: $(date -u +%FT%TZ)"
cd "$APP_DIR"

echo "▶ Fetch + reset a origin/main"
git fetch --prune origin
git reset --hard origin/main

# Estáticos: el propio directorio del repo es el root de Nginx, así que con
# git reset ya están servidos. Solo hay que asegurarse de que el bloque
# location bloquee .git/, backend/, scripts/, .github/, .env, etc.
# (ver DEPLOY.md).

echo "▶ Build + up del backend de contacto"
docker compose -f "$COMPOSE_FILE" up -d --build --remove-orphans

echo "▶ Prune de imágenes huérfanas"
docker image prune -f

echo "▶ Estado del backend:"
docker compose -f "$COMPOSE_FILE" ps

echo "✅ Deploy OK: $(date -u +%FT%TZ)"
