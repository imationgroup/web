# Registro de Actividades de Tratamiento (RAT)

**Documento interno** — Art. 30 Reglamento (UE) 2016/679 (RGPD).
No publicar. nginx ya bloquea `*.md` por defecto.

---

## 0. Identificación del Responsable

| Campo | Valor |
|---|---|
| Razón social | Imationgroup OÜ |
| Código de registro | 17473932 |
| Domicilio | Sepapaja tn 6, 15551 Tallinn, Harju Maakond, Estonia |
| Email contacto | info@imationgroup.com |
| Teléfono | +34 613 018 419 |
| Autoridad de control aplicable | AEPD (España) por establecimiento principal de actividad; subsidiariamente AKI (Estonia) |
| DPO designado | No (no obligatorio: < 250 empleados y sin tratamiento masivo de categorías especiales) |
| Última actualización | 2026-06-15 |

---

## 1. Formulario de contacto (`imationgroup.com/.../#contact`)

| Campo | Detalle |
|---|---|
| **Finalidad** | Responder a consultas comerciales y técnicas dirigidas por el visitante. |
| **Base jurídica** | Art. 6(1)(a) RGPD — Consentimiento explícito (checkbox obligatorio + texto enlazando a la política de privacidad). |
| **Categorías de interesados** | Visitantes del sitio que envían el formulario voluntariamente. |
| **Categorías de datos** | Nombre, email, mensaje, IP del remitente, idioma del navegador. |
| **Categorías de destinatarios** | Internos: equipo de ImationGroup. Externos: proveedor SMTP (ver §6). |
| **Transferencias internacionales** | No directamente. SMTP procesa dentro del EEE (ver §6). |
| **Plazo de conservación** | 24 meses desde el último contacto. Tras ese plazo, borrado del buzón. |
| **Medidas de seguridad** | TLS 1.3 en transporte (Let's Encrypt). Honeypot anti-bot. Rate-limit 5/h por IP. Servidor Linux con UFW + sudo controlado. Sin almacenamiento estructurado: el mensaje vive en el buzón de info@imationgroup.com. |
| **Origen de los datos** | Directamente del interesado. |
| **Derechos del interesado** | Acceso/rectificación/supresión/oposición/portabilidad: a través de info@imationgroup.com. |

---

## 2. Suscripciones al boletín (`/api/newsletter/subscribe`)

| Campo | Detalle |
|---|---|
| **Finalidad** | Envío de notificaciones automáticas cada vez que se publica un artículo del blog en el idioma del suscriptor. |
| **Base jurídica** | Art. 6(1)(a) RGPD — Consentimiento explícito vía doble opt-in. La suscripción no se considera válida hasta que el usuario pulsa el enlace de confirmación enviado a su buzón. |
| **Categorías de interesados** | Visitantes que rellenan el formulario del pie del sitio. |
| **Categorías de datos** | Email, idioma preferido, IP (solo para rate-limit transitorio), marca temporal de alta y confirmación, token aleatorio de gestión (sustituye al envío de contraseña). |
| **Categorías de destinatarios** | Internos: backend FastAPI. Externos: proveedor SMTP de envío (ver §6). Los datos no se ceden ni se comparten con terceros con fines comerciales. |
| **Transferencias internacionales** | No directamente. SMTP en EEE. |
| **Plazo de conservación** | Mientras la suscripción esté activa. Tras baja: hash del email durante 12 meses (anti re-suscripción accidental); pasado ese plazo, borrado total. |
| **Medidas de seguridad** | TLS 1.3. Token aleatorio (32 bytes urlsafe) por suscriptor. Honeypot. Rate-limit 5/h por IP. Cada email lleva enlace de baja de un click. Almacenamiento en SQLite con backups del volumen Docker. |
| **Origen** | Directamente del interesado. |
| **Derechos** | Baja un-click + email a info@imationgroup.com. |

---

## 3. Analítica web (Google Analytics 4 + Google Tag Manager)

| Campo | Detalle |
|---|---|
| **Finalidad** | Métricas agregadas de uso para mejorar el sitio (páginas vistas, idioma, dispositivo, fuente de tráfico). |
| **Base jurídica** | Art. 6(1)(a) RGPD — Consentimiento. NO se carga si el usuario no pulsa "Aceptar" en el banner de cookies. |
| **Categorías de interesados** | Visitantes que aceptan analítica en el banner. |
| **Categorías de datos** | IP **anonimizada** (`anonymize_ip: true`), URL visitada, referrer, user-agent, eventos automáticos GA4. |
| **Categorías de destinatarios** | Google Ireland Limited (corresponsable / encargado según la configuración GA4). |
| **Transferencias internacionales** | Google puede subprocesar datos en USA. Cobertura legal: Cláusulas Contractuales Tipo (SCCs) de la Comisión Europea publicadas por Google + Decisión de Adecuación EU-US Data Privacy Framework (julio 2023). |
| **Plazo de conservación** | Configurado en GA4 al mínimo posible (2 meses para datos a nivel de usuario). |
| **Medidas de seguridad** | Carga condicionada al consentimiento. IP anonymizado. Sin remarketing. |
| **Origen** | Recogida automática vía script Google al aceptar cookies. |
| **Derechos** | El usuario puede revocar el consentimiento en cualquier momento mediante "Preferencias de cookies" del footer. |

---

## 4. Visitas a posts del blog (`Post.view_count`)

| Campo | Detalle |
|---|---|
| **Finalidad** | Contador anónimo de lectores por artículo. Solo visible para el administrador. |
| **Base jurídica** | Art. 6(1)(f) — Interés legítimo (medir audiencia del propio contenido). Sin identificación. |
| **Datos** | Solo un entero por (artículo, idioma). Sin asociación a usuario, sin cookies. |
| **Filtro de bots** | UA contiene `bot`, `crawl`, `spider`, `curl/`, etc. → no se incrementa. |
| **Conservación** | Indefinida (es un contador agregado, no PII). |

---

## 5. Logs del servidor (nginx)

| Campo | Detalle |
|---|---|
| **Finalidad** | Diagnóstico operativo, detección de abuso/seguridad. |
| **Base jurídica** | Art. 6(1)(f) — Interés legítimo. |
| **Datos** | IP, timestamp, ruta, código de respuesta, user-agent, bytes, tiempo de respuesta. |
| **Destinatarios** | Internos. |
| **Transferencias** | Ninguna (logs en disco del VPS). |
| **Plazo de conservación** | logrotate semanal, 4 ficheros = ~28 días máximo. |
| **Medidas** | Servidor con sudo restringido. Acceso por SSH key. UFW activo. |

---

## 6. Proveedores / Encargados del tratamiento

| Proveedor | Servicio | Ubicación | Marco legal |
|---|---|---|---|
| **Hostinger International Limited** | VPS (`srv1615339.hstgr.cloud`, datacentre París, Francia) | EEE (Lituania + Francia) | DPA estándar de Hostinger. **Sin transferencia internacional.** |
| **Google Ireland Limited** | Google Analytics 4 + Google Tag Manager (solo si el usuario consiente) | Irlanda; subprocessing en US | DPA + SCCs publicados por Google + EU-US DPF |
| **Anthropic PBC** | API Claude usada para traducción automática de borradores del admin (no procesa datos de visitantes) | USA | Acuerdo de API estándar. **Tratamiento de B2B, datos de la empresa admin solamente**. |
| **SMTP del VPS / proveedor de envío** | Envío de emails (contacto, confirmación, newsletter) | EEE | Sin acuerdo formal escrito por el momento — pendiente verificar y firmar DPA con el proveedor concreto. |

> ⚠ Pendiente: identificar el proveedor SMTP exacto en `.env` (`SMTP_HOST`) y, si es externo, archivar DPA firmado.

---

## 7. Derechos de los interesados — procedimiento interno

Cualquier solicitud (acceso, rectificación, supresión, oposición, portabilidad, limitación, retirada del consentimiento) que llegue a `info@imationgroup.com` o vía formulario:

1. **Acuse de recibo** en 24h hábiles desde recepción.
2. **Verificación de identidad** del solicitante (responder al email desde el que se contactó).
3. **Localización del dato**:
   - Contacto → buzón info@.
   - Suscripción → tabla `subscriber` en `/var/imationgroup-blog/db.sqlite3`.
   - Logs/visitas → no son PII identificable; informar al solicitante.
4. **Ejecución**:
   - Acceso: exportar lo que tengamos.
   - Supresión: borrar del buzón y de SQLite.
   - Oposición: marcar `status=unsubscribed`.
5. **Respuesta** al solicitante en máximo **1 mes** (Art. 12.3 RGPD), prorrogable a 2 si solicitud compleja.
6. **Anotación** del caso en el registro interno (este documento, sección 9 abajo).

---

## 8. Evaluación de impacto (PIA)

A día de hoy NO se realizan tratamientos que requieran PIA obligatoria (Art. 35 RGPD):
- No hay scoring/perfilado automático con efectos jurídicos.
- No hay tratamiento masivo de categorías especiales.
- No hay observación sistemática de zonas públicas.

Reevaluar si se añade: scoring de leads, perfilado de marketing, datos de salud, etc.

---

## 9. Registro de incidencias y solicitudes

| Fecha | Tipo | Resumen | Resolución |
|---|---|---|---|
| _(vacío al iniciar)_ | | | |

Añadir aquí: solicitudes RGPD recibidas, brechas, decisiones de retención excepcional.
