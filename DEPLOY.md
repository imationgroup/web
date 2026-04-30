# Despliegue de imationgroup.com en el VPS

Mismo flujo que **autolinked-saas**: cada push a `main` dispara
`.github/workflows/deploy.yml`, que se conecta por SSH al VPS y ejecuta
`scripts/deploy.sh`. Nginx sirve los estáticos **directamente desde el
directorio del repo clonado** y hace proxy al contenedor del API de
contacto para `api.imationgroup.com`.

## Componentes en el VPS

| Servicio | Subdominio | Origen |
| --- | --- | --- |
| Web estática | `imationgroup.com` (+ `www`) | Nginx → `/home/deploy/apps/imationgroup-web` |
| API de contacto | `api.imationgroup.com` | Nginx → `127.0.0.1:8001` (contenedor `contact-api`) |

## Setup inicial (UNA sola vez)

### 1. Clave SSH para GitHub Actions → VPS

En el VPS, como `deploy`:

```bash
ssh-keygen -t ed25519 -C "github-actions-imationgroup-web" -f ~/.ssh/gha_imationgroup_web -N ""
cat ~/.ssh/gha_imationgroup_web.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
cat ~/.ssh/gha_imationgroup_web        # ← copia el bloque entero (BEGIN..END)
```

### 2. Secretos en GitHub

`Settings → Secrets and variables → Actions` del repo `imationgroup/web`:

| Secret | Valor |
| --- | --- |
| `VPS_HOST` | `76.13.56.232` |
| `VPS_USER` | `deploy` |
| `VPS_SSH_KEY` | el contenido de `~/.ssh/gha_imationgroup_web` (privada) |
| `VPS_PORT` | (opcional) `22` |

### 3. Clonar el repo en el VPS

```bash
ssh deploy@76.13.56.232
mkdir -p ~/apps && cd ~/apps
git clone https://github.com/imationgroup/web.git imationgroup-web
cd imationgroup-web
cp .env.example .env
nano .env   # rellena los SMTP_* (mismos valores que autolinked)
```

### 4. Nginx

#### Vhost del sitio estático

`/etc/nginx/sites-available/imationgroup.com`

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name imationgroup.com www.imationgroup.com;

    root /home/deploy/apps/imationgroup-web;
    index index.html;

    # Bloquea archivos del repo que NO deben servirse por HTTP
    location ~ /\.git/ { deny all; return 404; }
    location = /.gitignore { deny all; return 404; }
    location ~ ^/(backend|scripts|\.github)/ { deny all; return 404; }
    location ~ /\.env { deny all; return 404; }
    location ~ \.(md|sh|yml|yaml|Dockerfile)$ { deny all; return 404; }
    location = /CNAME { deny all; return 404; }

    location / {
        try_files $uri $uri/ =404;
    }

    # Long-cache para assets (si los hay)
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

> **Permisos**: Nginx (usuario `www-data`) tiene que poder leer
> `/home/deploy/apps/imationgroup-web`. Asegúralo con:
> ```bash
> sudo chmod o+x /home/deploy /home/deploy/apps
> chmod -R o+rX /home/deploy/apps/imationgroup-web
> ```

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

Si tenías GitHub Pages, **desactívalo** desde
`Settings → Pages → Source = None` cuando hayas comprobado que la versión
del VPS funciona.

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
docker compose up -d --build    # solo si afecta al backend
```
