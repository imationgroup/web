#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# Deploy de imationgroup.com en el VPS, ejecutado por GitHub Actions.
# Asume:
#   - El repo está clonado en ~/apps/imationgroup-web
#   - Existe ~/apps/imationgroup-web/.env (no versionado, con SMTP_*)
#   - El usuario deploy pertenece al grupo docker
#   - Existe el directorio web a servir (lo creamos si no): WEB_ROOT
#   - Nginx tiene un vhost que apunta a WEB_ROOT y otro que hace proxy
#     a 127.0.0.1:8001 para api.imationgroup.com
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/apps/imationgroup-web}"
WEB_ROOT="${WEB_ROOT:-/var/www/imationgroup.com}"
COMPOSE_FILE="docker-compose.yml"

echo "▶ Deploy iniciado: $(date -u +%FT%TZ)"
cd "$APP_DIR"

echo "▶ Fetch + reset a origin/main"
git fetch --prune origin
git reset --hard origin/main

# Estáticos: todo el repo salvo backend/, scripts/, .git, .github, .env, CNAME
# CNAME es de GitHub Pages, no hace falta servirlo desde Nginx.
echo "▶ Sincronizando estáticos en $WEB_ROOT"
sudo mkdir -p "$WEB_ROOT"
sudo rsync -a --delete \
  --exclude='.git' \
  --exclude='.github' \
  --exclude='backend' \
  --exclude='scripts' \
  --exclude='.env' \
  --exclude='.env.example' \
  --exclude='.gitignore' \
  --exclude='CNAME' \
  --exclude='docker-compose.yml' \
  --exclude='README.md' \
  ./ "$WEB_ROOT/"

# Backend de contacto: docker compose up
echo "▶ Build + up del backend de contacto"
docker compose -f "$COMPOSE_FILE" up -d --build --remove-orphans

echo "▶ Prune de imágenes huérfanas"
docker image prune -f

echo "▶ Estado del backend:"
docker compose -f "$COMPOSE_FILE" ps

echo "✅ Deploy OK: $(date -u +%FT%TZ)"
