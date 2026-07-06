"""Update the COSMIC TOP SECRET post: reframe around NATO as primary
client, EU/national as secondary. Retranslate to all 7 languages."""
import re
import requests

BASE = "https://imationgroup.com"
USER = "imationgroup"
PWD = "Putankamon,666"

POST_ID = 27

TITLE = "Obtenemos la acreditación COSMIC TOP SECRET para trabajar con la OTAN en datos clasificados"
SLUG = "cosmic-top-secret-clearance-union-europea"
EXCERPT = (
    "ImationGroup ha obtenido la acreditación COSMIC TOP SECRET, el nivel "
    "máximo de clasificación de la OTAN. A partir de hoy podemos trabajar "
    "en el corazón de la Alianza — planes militares, inteligencia aliada, "
    "sistemas de armas y comunicaciones — junto con los aliados europeos y "
    "sus servicios de defensa e inteligencia."
)

COVER_IMG = (
    "https://image.pollinations.ai/prompt/"
    "NATO%20intelligence%20operations%20room%2C%20classified%20briefing%2C%20"
    "NATO%20flag%2C%20military%20officers%2C%20blue%20cinematic%20lighting%2C%20"
    "secure%20command%20center%2C%20high%20detail%2C%20professional%20editorial%20photo?"
    "width=1200&height=630&nologo=true"
)

BODY = f"""\
<p><img src="{COVER_IMG}" alt="Centro de operaciones de la OTAN — información clasificada" style="width:100%;height:auto;border-radius:12px;margin-bottom:24px;" /></p>

<h2>Qué es COSMIC TOP SECRET</h2>
<p><strong>COSMIC TOP SECRET (CTS)</strong> es el nivel máximo de
clasificación de seguridad de la <strong>OTAN</strong>. El prefijo
«COSMIC» identifica precisamente la información propia de la Alianza
Atlántica: es el rótulo que la OTAN aplica a los documentos y sistemas
cuyo compromiso causaría, en sus propios términos, <em>«daño
excepcionalmente grave»</em> a la seguridad de la Alianza y de sus
Estados miembros.</p>
<p>Por encima de <em>Secret</em>, <em>Confidential</em> y
<em>Restricted</em>, es el escalón al que se somete la información sobre
planes militares en curso de la Alianza, capacidades reales de
inteligencia estratégica y sistemas de armas de última generación
integrados en la estructura de la OTAN. Sólo un número muy reducido de
organizaciones del sector privado en cada país aliado está autorizado a
tratar información a este nivel.</p>

<h2>Un año de investigación sobre nuestro personal</h2>
<p>Obtener la habilitación CTS no es un trámite: durante <strong>más de
un año</strong>, todo el personal susceptible de acceder a información
clasificada de nivel COSMIC TOP SECRET ha estado siendo investigado en
paralelo por múltiples autoridades de inteligencia y seguridad, tanto
aliadas como nacionales.</p>
<p>El proceso lo lidera en España el <strong>CNI (Centro Nacional de
Inteligencia)</strong>, como Autoridad Nacional de Seguridad (ONS), y se
apoya en el intercambio de información con servicios homólogos: la
<strong>CIA</strong> y otras agencias aliadas de la comunidad de
inteligencia occidental, el <strong>NATO Office of Security (NOS)</strong>,
las <strong>NSA/DSA</strong> (National / Designated Security Authorities)
de cada Estado aliado donde nuestro personal haya residido o trabajado, y
el <strong>EU INTCEN</strong> del Servicio Europeo de Acción Exterior en
los ámbitos de cooperación UE-OTAN.</p>
<p>Cada persona ha sido sometida a un escrutinio exhaustivo que cubre,
entre otras piezas:</p>
<ul>
  <li><strong>Historial delictivo</strong> — antecedentes penales, policiales y de investigaciones abiertas en todos los países donde el candidato ha residido, no sólo en España.</li>
  <li><strong>Background personal y familiar</strong> — datos completos de padres, hermanos, pareja y descendientes; verificación de vínculos con actores hostiles a la Alianza.</li>
  <li><strong>Situación financiera</strong> — deudas, patrones de gasto anómalos, movimientos bancarios, participaciones societarias, indicios de vulnerabilidad económica.</li>
  <li><strong>Historial de viajes</strong> — desplazamientos a países considerados de riesgo por la OTAN, contactos internacionales, alojamiento y motivos.</li>
  <li><strong>Actividad digital</strong> — huella online, redes sociales, foros, publicaciones, comunicaciones cifradas conocidas.</li>
  <li><strong>Círculo relacional</strong> — parejas actuales y pasadas, amistades cercanas, referencias personales y profesionales entrevistadas una a una.</li>
  <li><strong>Entrevistas presenciales</strong> con agentes de investigación en varias sesiones, cruces de declaraciones y verificación de coherencia.</li>
</ul>
<p>Tras superar cada uno de esos filtros y ser evaluados de forma
independiente por varias autoridades — con la OTAN como referente
último —, el equipo ha obtenido finalmente la habilitación personal en
firme al nivel CTS.</p>

<h2>Por qué esto importa</h2>
<p>Hasta hoy, el desarrollo de software y la analítica sobre información
clasificada de nivel COSMIC TOP SECRET dentro de la OTAN ha sido
territorio de un pequeño grupo de grandes integradores tradicionales. La
acreditación permite que un partner ágil como ImationGroup entre en ese
terreno y trabaje directamente con la <strong>estructura militar
aliada</strong>, con las <strong>agencias OTAN</strong> (NCIA, NATO STO,
NATO CI Agency) y con los <strong>ministerios de Defensa e
Inteligencia</strong> de Estados aliados.</p>
<p>Para nuestros clientes actuales en <strong>banca, industria y
sanidad</strong>, significa además que el mismo proveedor que les entrega
su plataforma de datos, su ERP, su integración con la API oficial de
LinkedIn o su motor de validación en tiempo real cumple ya los
estándares de seguridad más exigentes que existen en el mundo
occidental.</p>

<h2>Siguiente paso</h2>
<p>Si perteneces a un <strong>ministerio o agencia aliada de la
OTAN</strong> (Defensa, Interior, Exteriores, servicios de
inteligencia), a la <strong>estructura militar de la Alianza</strong>, a
una <strong>agencia OTAN</strong>, o eres un integrador que participa en
licitaciones clasificadas al nivel CTS, escríbenos a
<a href="mailto:info@imationgroup.com">info@imationgroup.com</a>.</p>
<p>Toda comunicación inicial se tramita por <strong>canal cifrado</strong>
y bajo <strong>acuerdo de confidencialidad reforzado</strong> desde el
primer correo. Respondemos en menos de <strong>24 horas</strong>.</p>
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
               allow_redirects=False, timeout=45)
    print(f"update es -> {r.status_code}  loc={r.headers.get('location','')}")
    assert r.status_code in (302, 303), r.text[:500]

    r = s.post(f"{BASE}/admin/posts/{POST_ID}/translate", timeout=45,
               allow_redirects=False)
    print(f"translate-all -> {r.status_code}")


if __name__ == "__main__":
    main()
