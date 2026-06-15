# Procedimiento de respuesta a brechas de seguridad

**Documento interno** — Arts. 33 y 34 RGPD.
No publicar.

---

## 0. Definición

> Una "brecha" es cualquier incidente que provoque la **destrucción, pérdida, alteración, divulgación o acceso no autorizado** a datos personales tratados por ImationGroup.

Ejemplos concretos:
- Acceso no autorizado a `/var/imationgroup-blog/db.sqlite3` (suscriptores).
- Robo de credenciales SSH del VPS o de la cuenta admin del blog.
- Exposición pública accidental de logs con IPs.
- Bug que envía un email del newsletter a la lista equivocada.
- Compromiso del proveedor SMTP que guarda copia del correo enviado.

---

## 1. Detección

**Señales** que disparan el protocolo:
- Login fallido masivo en `/admin/login` (revisar `docker logs` y `nginx access.log`).
- IP desconocida en `last -i` en el VPS.
- Aviso de Hostinger u otro proveedor.
- Correo / aviso de un usuario reportando uso indebido de sus datos.
- Cambio inesperado en la base de datos (suscriptores nuevos no provocados por subscribe, posts modificados sin pasar por admin).

**Cómo detectar proactivamente** (rutina semanal):
```bash
ssh deploy@imationgroup.com 'sudo last -n 30; sudo journalctl -u nginx --since "7 days ago" | grep -i denied | tail'
```

---

## 2. Las primeras 4 horas

Cuando se detecta una posible brecha:

1. **Aislamiento**:
   - Si el incidente está en curso: `sudo ufw deny from <ip>` o desactivar el servicio comprometido (`docker compose down contact-api`).
   - Rotar password: cambiar `ADMIN_PASSWORD_HASH` en `.env` y `docker compose up -d --force-recreate`.
   - Si SSH comprometido: revocar la SSH key del atacante en `~/.ssh/authorized_keys` y rotar el resto.

2. **Snapshot forense**:
   ```bash
   ssh deploy@imationgroup.com 'sudo tar czf /tmp/forensic-$(date +%s).tar.gz \
     /var/log/nginx /var/log/auth.log /var/imationgroup-blog/db.sqlite3 \
     ~/apps/imationgroup-web/.env'
   ```
   Descargar inmediatamente con `scp` a almacenamiento seguro local.

3. **Análisis preliminar** (responder con honestidad):
   - ¿Qué datos pueden haber sido expuestos? (emails, IPs, mensajes, hashes)
   - ¿Cuántos sujetos afectados?
   - ¿La brecha "es probable que entrañe un riesgo para los derechos y libertades" del interesado? (Art. 33.1)

---

## 3. Las primeras 72 horas — notificación a AEPD

Si la brecha **entraña un riesgo** para los interesados (la mayoría sí, salvo trivialidades), notificación **OBLIGATORIA** a la AEPD en **72 horas** desde la detección.

**Vía**: Sede electrónica AEPD → "Notificación de brechas de seguridad" → formulario online.
URL: `https://sedeagpd.gob.es/sede-electronica-web/vistas/formBrechaSeguridad/procedimientoBrechaSeguridad.jsf`

**Contenido mínimo** (Art. 33.3):
- Naturaleza de la brecha (qué pasó técnicamente).
- Categorías y número aproximado de interesados afectados.
- Categorías y número aproximado de registros afectados.
- Posibles consecuencias.
- Medidas adoptadas y propuestas.

**Si no se llega en 72h**: notificar lo antes posible explicando el retraso (Art. 33.1).

---

## 4. Notificación a los afectados

Si la brecha es **de alto riesgo** (emails + contraseñas en claro, datos de salud, etc.), notificación adicional **DIRECTA a los interesados** (Art. 34) en plazo razonable (~días-semanas) describiendo:
- Naturaleza de la brecha (en lenguaje claro, no jurídico).
- Datos del DPO o punto de contacto (= info@imationgroup.com).
- Posibles consecuencias.
- Medidas tomadas o que pueden tomar ellos (cambiar contraseñas en otros sitios si la reutilizan, vigilar fraude, etc.).

**Cómo enviar**:
- Para suscriptores del newsletter: query directa sobre `subscriber.email` filtrando por `status=confirmed`, broadcast vía SMTP del backend.
- Para contactos puntuales: extraer del buzón info@.
- **NO** notificar por el formulario público.

> Excepciones a la notificación a interesados (Art. 34.3):
> - Los datos ya estaban cifrados de forma robusta.
> - Se han adoptado medidas que eliminan el riesgo posterior.
> - Implicaría un esfuerzo desproporcionado (entonces: comunicación pública en el sitio).

---

## 5. Registro interno

Anotar la brecha en `docs/RAT.md` §9 con:
- Fecha y hora de detección.
- Fecha y hora de notificación a AEPD (si procede).
- Resumen técnico.
- Sujetos y registros afectados.
- Medidas correctivas.
- Estado: en curso / cerrada.

Este registro debe estar disponible para inspección si la AEPD lo pide (Art. 33.5).

---

## 6. Post-mortem

Pasada la urgencia, antes de cerrar:
1. **Cambios técnicos preventivos** documentados en commit (ej. añadir 2FA al admin, mejor rate-limit, etc.).
2. **Lecciones aprendidas** en `docs/RAT.md` §9.
3. **Revisión del propio procedimiento** si el incidente reveló agujeros en este documento.

---

## 7. Plantilla de notificación a AEPD (borrador inicial)

```
NOTIFICACIÓN DE BRECHA DE SEGURIDAD

Responsable: Imationgroup OÜ (Reg. 17473932)
Contacto: info@imationgroup.com

Fecha y hora de detección: <YYYY-MM-DD HH:MM CEST>
Fecha y hora estimada de inicio: <…>
Detectada por: <miembro del equipo / sistema automático / aviso externo>

Naturaleza de la brecha:
<descripción técnica del incidente>

Datos afectados:
- Categorías: <ej. emails de suscriptores>
- Volumen estimado: <ej. ~120 registros>
- Sensibilidad: <ej. media — emails sin contraseñas>

Posibles consecuencias para los interesados:
<ej. spam, phishing dirigido>

Medidas adoptadas hasta la fecha:
- <…>

Medidas previstas:
- <…>

Notificación a los interesados:
- Realizada / no realizada / pendiente, motivo: <…>
```

---

## 8. Plantilla de email a interesados

```
Asunto: Aviso importante de seguridad — ImationGroup

Hola <Nombre>,

Te escribimos para informarte de un incidente de seguridad ocurrido el <fecha> que ha
podido afectar a tus datos personales en nuestro sistema.

Qué ha pasado:
<descripción honesta y clara, sin jerga>

Qué datos tuyos están implicados:
<ej. tu dirección de email>

Qué NO está implicado:
<ej. no había contraseñas en nuestros sistemas porque usamos enlaces sin clave>

Qué hemos hecho:
<resumen acciones>

Qué te recomendamos:
<acciones concretas para el usuario>

Si tienes preguntas, responde a este correo o escríbenos a info@imationgroup.com.
Hemos notificado el incidente a la Agencia Española de Protección de Datos según
exige el RGPD.

Disculpa las molestias.

— Equipo ImationGroup
```
