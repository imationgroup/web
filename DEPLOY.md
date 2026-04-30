# Despliegue de imationgroup.com en el VPS

Mismo flujo que **autolinked-saas**: cada push a `main` dispara
`.github/workflows/deploy.yml`, que se conecta por SSH al VPS y ejecuta
`scripts/deploy.sh`.

El sitio se sirve **desde el VPS** (no desde GitHub Pages).

## Componentes en el VPS

| Servicio | Subdominio | Origen |
| --- | --- | --- |
| Web estática | `imationgroup.com` (+ `www`) | Nginx → archivos en `/var/www/imationgroup.com` |
| API de contacto | `api.imationgroup.com` | Nginx → `127.0.0.1:8001` (contenedor `contact-api`) |

## Setup inicial (UNA sola vez)

### 1. Secretos en GitHub

`Settings → Secrets and variables → Actions` del repo `imationgroup/web`:

| Secret | Valor |
| --- | --- |
| `VPS_HOST` | `76.13.56.232` |
| `VPS_USER` | `deploy` |
| `VPS_SSH_KEY` | la **clave privada** ed25519 que el usuario `deploy` tiene autorizada en el VPS |
| `VPS_PORT` | (opcional) `22` |

### 2. Clonar el repo en el VPS

```bash
ssh deploy@76.13.56.232
mkdir -p ~/apps && cd ~/apps
git clone https://github.com/imationgroup/web.git imationgroup-web
cd imationgroup-web
cp .env.example .env
nano .env   # rellena los SMTP_* (mismos valores que autolinked)
```

### 3. Permitir a `deploy` ejecutar `rsync` con sudo sin contraseña

El deploy escribe en `/var/www/imationgroup.com`, así que el usuario
necesita poder hacer `sudo mkdir` y `sudo rsync` sin que pida password:

```bash
sudo visudo -f /etc/sudoers.d/imationgroup-deploy
```

Pega esta línea exactamente:

```
deploy ALL=(root) NOPASSWD: /bin/mkdir, /usr/bin/rsync
```

Guarda y sal. Comprueba con `sudo -n mkdir -p /var/www/imationgroup.com`.

### 4. Nginx

#### Vhost del sitio estático

`/etc/nginx/sites-available/imationgroup.com`

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name imationgroup.com www.imationgroup.com;

    root /var/www/imationgroup.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # Long-cache para assets versionados (si los hay)
    location ~* \.(?:css|js|woff2|svg|png|jpg|jpeg|webp|ico)$ {
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/imationgroup.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d imationgroup.com -d www.imationgroup.com
```

#### Vhost del API de contacto

`/etc/nginx/sites-available/api.imationgroup.com`

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name api.imationgroup.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 30s;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/api.imationgroup.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d api.imationgroup.com
```

### 5. DNS

En el panel del registrador (Hostinger / Cloudflare):

| Tipo | Nombre | Valor |
| --- | --- | --- |
| `A` | `imationgroup.com` | `76.13.56.232` |
| `A` | `www.imationgroup.com` | `76.13.56.232` |
| `A` | `api.imationgroup.com` | `76.13.56.232` |

Si tenías GitHub Pages configurado, **desactívalo** desde
`Settings → Pages → Source = None`. El archivo `CNAME` del repo
ya no se sirve (lo excluye `deploy.sh`).

### 6. Primer deploy

Empuja a `main` o ejecuta el workflow manualmente desde la pestaña
**Actions** del repo. Comprueba después:

```bash
curl -I https://imationgroup.com
curl https://api.imationgroup.com/api/health
```

## Despliegues siguientes

Cada `git push` a `main` lanza el workflow automáticamente. Si quieres
forzar uno, `Actions → Deploy to VPS → Run workflow`.

## Rollback

```bash
ssh deploy@76.13.56.232
cd ~/apps/imationgroup-web
git log --oneline -10           # localiza el commit estable
git reset --hard <COMMIT_HASH>
bash scripts/deploy.sh          # reaplica
```
