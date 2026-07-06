"""Publish the 'LinkedIn + top 5 CRMs' blog post on imationgroup.com."""
import re
import requests

BASE = "https://imationgroup.com"
USER = "imationgroup"
PWD = "Putankamon,666"

TITLE = "Integramos LinkedIn en los 5 mejores CRM del mercado"
SLUG = "linkedin-crm-integraciones"
EXCERPT = (
    "Tus leads de LinkedIn dejan de vivir en una hoja de cálculo y aterrizan "
    "directamente en el CRM donde tu equipo comercial trabaja: Salesforce, "
    "HubSpot, Pipedrive, Zoho y Microsoft Dynamics. Te contamos qué hace cada "
    "uno y qué cambia cuando tu LinkedIn habla con ellos."
)

BODY = """\
<p>La mayoría de equipos comerciales pierden leads simplemente porque <strong>el
contacto que entra por LinkedIn no llega al CRM</strong> donde se trabaja la
pipeline. Quien hace la captación (marketing o el propio fundador) acumula
notas, mensajes y formularios de Lead Gen en un sitio; comercial trabaja en
otro. Y entre uno y otro se cuela el 30-40 % de las oportunidades.</p>

<p>En <strong>ImationGroup</strong> integramos LinkedIn de forma nativa con
los cinco CRM más usados del mercado, vía sus APIs oficiales (sin scraping, sin
Zapier de andar por casa, sin riesgo de baneo). Estos son los cinco, qué hace
cada uno, y qué desbloquea conectarlos con LinkedIn.</p>

<h2>1. Salesforce</h2>
<p><strong>Qué es:</strong> el CRM líder mundial. Funcionalidades para
gestionar cuentas, oportunidades, casos de soporte, automatizaciones (Flow),
analítica avanzada (Tableau), atención multicanal (Service Cloud) y todo el
stack Marketing Cloud. Es el estándar en empresas medianas y grandes.</p>
<p><strong>Qué integramos:</strong> sincronización en tiempo real de leads
desde LinkedIn Lead Gen Forms a objetos Lead/Contact, conversión automática a
Opportunity con scoring, registro de interacciones (mensajes, conexiones,
comentarios) en el activity timeline, y atribución de pipeline a campañas
LinkedIn Ads para que veas el ROI real por campaña, no solo el coste por lead.</p>

<h2>2. HubSpot</h2>
<p><strong>Qué es:</strong> el CRM más popular en pymes y empresas en
crecimiento, con un tier gratuito potente. Incluye CRM, Marketing Hub (email,
landings, automation), Sales Hub (pipeline, secuencias, calling), Service Hub
(tickets, chatbot, base de conocimiento) y CMS para la web.</p>
<p><strong>Qué integramos:</strong> Lead Gen Forms de LinkedIn entran como
Contact + Deal en HubSpot con propiedades enriquecidas, los workflows de
HubSpot disparan secuencias de seguimiento por email, y los mensajes
intercambiados en LinkedIn aparecen como Engagements en la ficha del contacto.
Además sincronizamos las propiedades de la empresa (sector, tamaño, web)
desde el perfil de LinkedIn para que el segmentador de HubSpot tenga datos
limpios.</p>

<h2>3. Pipedrive</h2>
<p><strong>Qué es:</strong> CRM diseñado para equipos de ventas que viven en
la pipeline visual (kanban de oportunidades). Funcionalidades fuertes en
gestión de actividades, automatizaciones simples, email tracking, llamadas
integradas, generación de presupuestos y reporting orientado a actividad
comercial. Curva de aprendizaje muy baja.</p>
<p><strong>Qué integramos:</strong> cada lead de LinkedIn se convierte
automáticamente en un Deal en la fase inicial de tu pipeline, con la fuente
"LinkedIn" y los datos del formulario rellenados. Si el lead responde a un
DM o acepta una conexión, se registra como Activity y se mueve de fase según
tus reglas. Pipedrive Insights pasa a medir conversión por canal, con
LinkedIn como uno más al lado de email y referidos.</p>

<h2>4. Zoho CRM</h2>
<p><strong>Qué es:</strong> CRM completo dentro del ecosistema Zoho (45+
aplicaciones de negocio: contabilidad, RRHH, helpdesk, BI…). Cubre desde
gestión de leads y cuentas hasta automatización con su asistente Zia, blueprint
para procesos de venta, atención omnicanal y un nivel de personalización
altísimo a precio asequible. Muy fuerte en pymes españolas y latinoamericanas.</p>
<p><strong>Qué integramos:</strong> sync bidireccional con LinkedIn — leads
nuevos entran como Lead/Contact, los datos enriquecidos del perfil
(empresa, cargo, sector) actualizan los registros existentes para evitar
duplicados, y los blueprints de Zoho pueden disparar tareas y emails cuando
un lead cumple cierto criterio en LinkedIn (por ejemplo, cambia de empresa o
interactúa con un post tuyo).</p>

<h2>5. Microsoft Dynamics 365</h2>
<p><strong>Qué es:</strong> la apuesta de Microsoft, integrada con todo el
stack 365 (Outlook, Teams, Power BI, Power Automate, SharePoint). Sales,
Customer Service, Field Service, Marketing y Finance + Operations conviven en
una misma plataforma. Estándar de facto en grandes corporaciones que ya viven
en el entorno Microsoft.</p>
<p><strong>Qué integramos:</strong> los leads de LinkedIn fluyen a Dynamics
365 Sales, las interacciones se registran en el Timeline del contacto, Power
Automate dispara flujos cross-system (notificaciones en Teams, tareas en
Planner, registros en SharePoint), y Power BI cruza los datos de LinkedIn Ads
con la pipeline para dashboards en tiempo real. Si ya tienes el stack
Microsoft, esta integración cierra el círculo.</p>

<h2>¿Qué utilidad real tiene esto para ti?</h2>
<ul>
  <li><strong>Cero leads perdidos en hojas de Excel.</strong> Cada formulario relleno en LinkedIn entra en tu CRM en cuestión de minutos, con el responsable comercial asignado por reglas.</li>
  <li><strong>Tiempo de respuesta &lt; 5 minutos.</strong> El primer comercial que responde se queda con el lead. La integración elimina la fricción del "exportar CSV → importar al CRM" que mata la conversión.</li>
  <li><strong>Atribución real de pipeline a LinkedIn.</strong> Sabrás cuánto te cuesta NO solo el lead, sino el cliente cerrado. Cambias la conversación con marketing/dirección.</li>
  <li><strong>Ficha de contacto unificada.</strong> Los mensajes de LinkedIn, los emails, las llamadas y las reuniones aparecen todos en el mismo timeline del CRM. El comercial no tiene que abrir 5 pestañas.</li>
  <li><strong>Automatización end-to-end.</strong> Lead entra → se cualifica → se asigna → se le manda mensaje personalizado por DM y email → se crea oportunidad → se notifica al equipo. Todo sin tocar nada.</li>
  <li><strong>Sin riesgo de baneo.</strong> Usamos las APIs oficiales de LinkedIn (somos partner aprobado para Sign In, Share, Community Management, Verified). Ni scraping ni bots: cero riesgo para la cuenta del cliente.</li>
</ul>

<h2>¿Cómo lo hacemos?</h2>
<p>Cada integración es un proyecto a medida — no hay dos pipelines comerciales
iguales y meter LinkedIn en un CRM que ya tiene tres años de configuración
requiere entender cómo trabaja tu equipo. El flujo típico:</p>
<ol>
  <li><strong>Discovery</strong> (1 sesión, gratis): vemos tu CRM actual, tu volumen de leads LinkedIn y qué quieres conseguir.</li>
  <li><strong>Diseño</strong>: te entregamos el mapeo de campos, las reglas de asignación y los flujos de automatización en un documento que apruebas antes de tocar nada.</li>
  <li><strong>Implementación</strong>: conectamos vía OAuth + API oficial de LinkedIn (Sign In, Share, Community Management, Verified — tenemos los cuatro productos aprobados), configuramos los webhooks o jobs de sync, y dejamos logging para auditoría.</li>
  <li><strong>Formación + soporte</strong>: una sesión de 1 hora con tu equipo + 30 días de soporte incluido para iterar lo que haga falta.</li>
</ol>

<h2>Siguiente paso</h2>
<p>Escríbenos a <a href="mailto:info@imationgroup.com">info@imationgroup.com</a>
diciéndonos qué CRM usas y aproximadamente cuántos leads de LinkedIn manejas
al mes. En menos de <strong>24 horas</strong> te respondemos con una propuesta
inicial y, si encaja, agendamos la sesión de discovery.</p>
"""


def main():
    s = requests.Session()
    r = s.post(f"{BASE}/admin/login",
               data={"username": USER, "password": PWD},
               allow_redirects=False, timeout=15)
    assert r.status_code in (302, 303), r.text[:500]
    print("login OK")

    payload = {
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
    print(f"create -> {r.status_code}  loc={r.headers.get('location','')}")
    assert r.status_code in (302, 303), r.text[:500]
    m = re.search(r"/admin/posts/(\d+)", r.headers.get("location", ""))
    post_id = m.group(1)
    print(f"post_id={post_id}")

    # Translate to all 7 languages.
    r = s.post(f"{BASE}/admin/posts/{post_id}/translate", timeout=30,
               allow_redirects=False)
    print(f"translate-all -> {r.status_code}")


if __name__ == "__main__":
    main()
