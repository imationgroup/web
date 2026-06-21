"""Update the 'LinkedIn official developer' announcement post: remove any
phrasing that implies the previous state was not legitimate."""
import re
import requests

BASE = "https://imationgroup.com"
USER = "imationgroup"
PWD = "Putankamon,666"

POST_ID = 14

TITLE = "LinkedIn nos aprueba: somos desarrolladores oficiales con acceso a la Community Management API"
SLUG = "linkedin-desarrolladores-oficiales-community-management-api"
EXCERPT = (
    "LinkedIn ha aprobado a ImationGroup como desarrollador oficial con acceso Tier a la "
    "Community Management API. Una buena noticia para quien usa AutoLinked o construye con "
    "nosotros una integración con LinkedIn: operamos por la vía oficial, con todas las "
    "garantías que eso implica."
)

BODY = """\
<h2>Lo que ha pasado</h2>
<p>LinkedIn ha aprobado a <strong>ImationGroup</strong> como desarrollador oficial con
acceso <strong>Tier a la Community Management API</strong>. Es la vía oficial de LinkedIn para
automatizar la mayoría de acciones en su plataforma — y conseguirla no es trivial: requiere
superar un proceso de revisión en el que LinkedIn evalúa quién eres, qué construyes y cómo
manejas los datos de los usuarios.</p>

<h2>Por qué importa</h2>
<p>El mundo de la «automatización de LinkedIn» está plagado de herramientas que usan
scraping, extensiones de navegador no autorizadas o bots que simulan clics humanos. Funcionan…
hasta que LinkedIn las detecta, y entonces:</p>
<ul>
  <li>La cuenta del cliente se restringe o se cierra permanentemente.</li>
  <li>Los datos extraídos no se pueden usar legítimamente (problemas legales con RGPD y con los términos de LinkedIn).</li>
  <li>La herramienta deja de funcionar en cualquier momento, sin previo aviso.</li>
</ul>
<p>Con acceso oficial Tier nada de esto ocurre. Trabajamos contra los endpoints que LinkedIn
provee, con los rate-limits acordados, y los datos vienen con consentimiento explícito del
usuario. Sin riesgo de baneo, sin sustos.</p>

<h2>Qué podemos automatizar</h2>
<p>Entre otras cosas:</p>
<ul>
  <li>Publicar contenido en perfiles personales y páginas de empresa, con horario configurable.</li>
  <li>Leer y responder mensajes de la bandeja de entrada.</li>
  <li>Gestionar comentarios en publicaciones propias.</li>
  <li>Acceder a analíticas reales (impresiones, interacciones, reacciones) por publicación.</li>
  <li>Ejecutar campañas de invitaciones a página y de seguimiento a leads.</li>
</ul>
<p>Todo dentro del marco que LinkedIn permite y bajo el control del usuario que autoriza el
acceso a su cuenta vía OAuth.</p>

<h2>Qué significa para nuestros productos y clientes</h2>
<p><strong><a href="/es/projects#autolinked">AutoLinked</a></strong>, nuestro SaaS de
automatización de LinkedIn, opera al 100% sobre la API oficial. Para los clientes, esto se
traduce en algo crítico: <strong>durabilidad</strong>. Lo que automatizamos hoy seguirá
automatizándose mañana, sin sustos.</p>
<p>Para proyectos de consultoría también es relevante: si una empresa nos pide construirle
integraciones con LinkedIn — un CRM que sincronice mensajes, un dashboard de campañas, una
herramienta interna de social selling — podemos hacerlo con la garantía de que la solución es
legítima a largo plazo.</p>

<h2>El proceso de aprobación</h2>
<p>Para llegar aquí, LinkedIn ha auditado:</p>
<ul>
  <li>Quién es ImationGroup como empresa (estructura legal, equipo, trayectoria).</li>
  <li>Qué construimos con la API y cómo lo presentamos al usuario final.</li>
  <li>Cómo manejamos los datos: cifrado, retención, derechos del titular bajo RGPD.</li>
  <li>Nuestro flujo de OAuth y los permisos que solicitamos.</li>
  <li>El comportamiento esperado de cada endpoint que usamos (volumen, frecuencia, contexto).</li>
</ul>
<p>Es un filtro alto, y por eso hay tan pocas empresas con este tipo de acceso para
automatización en LinkedIn. Estamos orgullosos del trabajo del equipo para sacarlo adelante.</p>

<h2>Si quieres saber más</h2>
<p>Si necesitas automatizar acciones en LinkedIn de forma seria — para tu empresa o para un
proyecto de cliente — escríbenos a <a href="mailto:info@imationgroup.com">info@imationgroup.com</a>
y te contamos qué se puede hacer con el acceso oficial y qué no, sin promesas que no podamos
cumplir.</p>
"""


def main():
    s = requests.Session()
    r = s.post(f"{BASE}/admin/login",
               data={"username": USER, "password": PWD},
               allow_redirects=False, timeout=15)
    assert r.status_code in (302, 303), r.text[:500]
    print("login OK")

    payload = {
        "post_id": str(POST_ID),
        "title": TITLE,
        "slug": SLUG,
        "lang": "es",
        "excerpt": EXCERPT,
        "body_html": BODY,
        "is_published": "on",
        "category_id": "",
    }
    r = s.post(f"{BASE}/admin/posts", data=payload,
               allow_redirects=False, timeout=30)
    print(f"update es -> {r.status_code}  loc={r.headers.get('location','')}")
    assert r.status_code in (302, 303), r.text[:500]

    # Re-translate to all 6 non-es languages so the corrected wording propagates.
    r = s.post(f"{BASE}/admin/posts/{POST_ID}/translate", timeout=30,
               allow_redirects=False)
    print(f"translate-all -> {r.status_code}")


if __name__ == "__main__":
    main()
