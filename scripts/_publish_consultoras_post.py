"""Update the 'consultoras' blog post: new content, only es/gl/ca/eu."""
import re
import sys
import requests

BASE = "https://imationgroup.com"
USER = "imationgroup"
PWD = "Putankamon,666"

TITLE = "Consultoras y agentes digitalizadores: somos tu equipo técnico"
SLUG = "consultoras-equipo-tecnico-digitalizacion"
EXCERPT = (
    "Si tu cliente te pide una web a medida, una app móvil, un ERP o una solución con IA "
    "y tú no eres una empresa de desarrollo, podemos ser tu equipo técnico. "
    "Tres formas de colaborar, sin exclusividad."
)
BODY = """\
<h2>El problema que vemos cada semana</h2>
<p>Cada vez más consultoras de negocio, asesorías y agentes digitalizadores se encuentran con
clientes que les piden cosas que no saben hacer: una tienda online a medida, una app móvil para
sus operarios, una integración con su ERP, o una automatización con inteligencia artificial. Lo
que pasa después suele ser una de tres cosas:</p>
<ul>
  <li>Rechazan el proyecto y pierden la oportunidad (y a menudo también al cliente, que se va a buscarlo a otra parte).</li>
  <li>Subcontratan a freelances sueltos sin coordinación y el proyecto se desboca.</li>
  <li>Empiezan ellos con una plantilla genérica y a los seis meses todo se reescribe desde cero.</li>
</ul>
<p>Ninguna de las tres es buena ni para ti ni para tu cliente.</p>

<h2>Lo que ofrecemos a consultoras</h2>
<p>En <strong>ImationGroup</strong> somos una red de empresas y profesionales senior con más de
10 años de experiencia construyendo software a medida para pequeñas, medianas y grandes
empresas. Trabajamos con perfiles que vienen de grandes tecnológicas y de proyectos punteros
de IA. No solo programamos: entendemos el negocio y adaptamos cada desarrollo a cómo trabaja
realmente el cliente.</p>
<p>Cubrimos:</p>
<ul>
  <li><strong>Webs corporativas y comercio electrónico</strong> a medida.</li>
  <li><strong>Aplicaciones a medida</strong> para móvil, tablet, escritorio y web.</li>
  <li><strong>Implantación de ERPs</strong> en medianas y grandes empresas.</li>
  <li><strong>Soluciones con IA</strong> que generan ahorro real, no demos bonitas.</li>
  <li><strong>Consultoría de negocio</strong> para alinear la tecnología con los procesos del cliente.</li>
</ul>

<h2>Tres formas de colaborar</h2>

<h3>1. Tu equipo técnico subcontratado (Kit Digital y proyectos subvencionados)</h3>
<p>Si tu consultora es <em>agente digitalizador</em> o gestiona ayudas como Kit Digital, NextGen
o líneas autonómicas, podemos ser tu equipo de desarrollo: ejecutamos la parte técnica, la
dejamos documentada como pide la justificación de la ayuda, y tú mantienes la relación con el
cliente, la facturación de la subvención y la responsabilidad ante la administración. Para el
cliente final, somos invisibles.</p>

<h3>2. Recomendación con comisión</h3>
<p>Si tienes un cliente que necesita desarrollo y no quieres meterte de lleno, nos lo presentas
formalmente (un correo basta) y trabajamos su proyecto. Por cada cliente recomendado que
contrate, te abonamos una comisión sobre el importe facturado. Las condiciones concretas las
recogemos en un <strong>Acuerdo de Colaboración y Recomendación Comercial</strong> sencillo,
sin exclusividad, que adaptamos a cada caso.</p>

<h3>3. Co-venta</h3>
<p>Vamos juntos al cliente. Tú aportas la gestión, la consultoría de negocio y el conocimiento
del sector; nosotros aportamos el desarrollo. Cada uno factura su parte. Útil cuando el cliente
quiere un único interlocutor de cabecera y tú quieres mantener esa posición.</p>

<h2>Por qué te interesa hablar con nosotros</h2>
<ul>
  <li><strong>Senior contrastado:</strong> colaboradores procedentes de grandes tecnológicas y proyectos de IA de primer nivel.</li>
  <li><strong>Entregables documentados:</strong> si el proyecto va con subvención, te dejamos la parte técnica lista para que tu justificación sea sólida.</li>
  <li><strong>Resultados medibles:</strong> no vendemos «soluciones que funcionan», vendemos ahorros de tiempo y dinero cuantificables.</li>
  <li><strong>Flexibilidad:</strong> trabajamos como tu equipo cuando te conviene, o como proveedor recomendado cuando no quieres asumir el desarrollo.</li>
</ul>

<h2>Siguiente paso</h2>
<p>Si esto te encaja, escríbenos a
<a href="mailto:info@imationgroup.com">info@imationgroup.com</a> contándonos brevemente:</p>
<ul>
  <li>Qué tipo de cliente te suele llegar (sector, tamaño).</li>
  <li>Qué desarrollos te están pidiendo y no estás cubriendo.</li>
  <li>Si trabajas con ayudas/subvenciones o solo con proyectos privados.</li>
</ul>
<p>Te respondemos en menos de <strong>24 horas</strong> con una primera propuesta de colaboración
adaptada a tu caso y, si encaja, te pasamos el acuerdo para firmar.</p>
"""

POST_ID_ES = 10
KEEP_LANGS = {"es", "gl", "ca", "eu"}
DROP_LANGS = {"en", "pt", "et"}


def main():
    s = requests.Session()
    r = s.post(f"{BASE}/admin/login",
               data={"username": USER, "password": PWD},
               allow_redirects=False, timeout=15)
    assert r.status_code in (302, 303), f"login failed: {r.status_code}"
    print("login OK")

    # 1) Update the ES post with new body.
    payload = {
        "post_id": str(POST_ID_ES),
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

    # 2) Trigger re-translation to gl/ca/eu (the translate endpoint replaces
    #    the existing sibling). After it runs, the new sibling lands as a
    #    draft -- we publish it via the DB out-of-band (see shell command).
    for target in ("gl", "ca", "eu"):
        r = s.post(f"{BASE}/admin/posts/{POST_ID_ES}/translate/{target}",
                   allow_redirects=False, timeout=30)
        print(f"translate to {target} -> {r.status_code}")


def _get_group_of_master(s):
    rp = s.get(f"{BASE}/admin/posts/{POST_ID_ES}/edit", timeout=15)
    gid = re.search(r'name="group_id"\s+value="([^"]*)"', rp.text)
    return gid.group(1) if gid else None


if __name__ == "__main__":
    main()
