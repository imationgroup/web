# ImationGroup contact API

Mini backend FastAPI para el formulario de contacto de imationgroup.com.
Mismo patrón que el SaaS de autolinked: recibe `POST /api/contact`, valida,
aplica rate-limit por IP, manda un correo vía SMTP con `Reply-To` del
remitente.

## Despliegue local

```bash
cp .env.example .env
docker compose up --build
curl http://localhost:8001/api/health
```

## Despliegue en el VPS (Hostinger)

1. **Sube el repo al VPS** (si no está ya):
   ```bash
   ssh deploy@76.13.56.232
   git clone https://github.com/imationgroup/web.git /home/deploy/imationgroup-web
   cd /home/deploy/imationgroup-web
   cp .env.example .env
   nano .env   # rellena los SMTP_* con los mismos valores que usas en autolinked
   docker compose up -d --build
   ```

2. **Nginx**: añade un vhost para `api.imationgroup.com` que haga proxy
   a `127.0.0.1:8001`. Ejemplo:

   ```nginx
   server {
       server_name api.imationgroup.com;

       location / {
           proxy_pass http://127.0.0.1:8001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   Después:
   ```bash
   sudo certbot --nginx -d api.imationgroup.com
   sudo systemctl reload nginx
   ```

3. **DNS**: en Hostinger / Cloudflare, añade un registro A
   `api.imationgroup.com` apuntando a `76.13.56.232`.

4. **Comprueba**:
   ```bash
   curl https://api.imationgroup.com/api/health
   ```

## Endpoints

- `GET  /api/health` — devuelve `{"status":"ok","smtp_configured":true|false}`.
- `POST /api/contact` — body JSON `{name,email,message,website?}`.
  - `website` es honeypot (debe estar vacío).
  - Devuelve `429` si la IP excede 5 envíos/hora.
  - Devuelve siempre `{"sent":true}` salvo en caso de validación o rate-limit.
