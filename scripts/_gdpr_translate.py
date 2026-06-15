"""Translate GDPR additions (Newsletter section + Cookies section) into the
5 languages we previously left as English fallback (gl, ca, pt, eu, et).
Updates the inline language dicts at the bottom of templates/privacy.html."""
import re
from pathlib import Path

KEYS_EN_ES = {
    "en": {
        "privacy_s1_li1": "Contact Information: Name, email address and message you provide via the contact form. Your IP address is logged briefly for spam protection.",
        "privacy_sN_title": "7. Newsletter Subscriptions",
        "privacy_sN_p1": "When you subscribe to our newsletter from the website footer we collect and process:",
        "privacy_sN_li1": "Your email address — used only to send you new blog posts you opted in to receive.",
        "privacy_sN_li2": "Your language preference — so the newsletter and the confirmation email reach you in your language.",
        "privacy_sN_li3": "Subscription timestamps — proof of consent under GDPR.",
        "privacy_sN_p2": "Legal basis: your explicit consent (GDPR Art. 6(1)(a)). The subscription uses double opt-in.",
        "privacy_sN_p3": "Withdrawal: every newsletter email contains a one-click unsubscribe link. You can also email info@imationgroup.com.",
        "privacy_sN_p4": "Retention: we keep your subscription record while it is active. After you unsubscribe, the email hash is kept 12 months only to prevent accidental re-subscription.",
        "privacy_s7_title": "8. Cookies and Tracking",
        "privacy_s7_p1": "We use two categories of cookies. You can change your choice any time using the Cookie preferences link in the footer.",
        "privacy_s7_p2": "Essential cookies — always loaded. These store your language choice and your cookie-banner decision in your browser's localStorage. No personal data, no tracking, no third party.",
        "privacy_s7_p3": "Analytics cookies — loaded ONLY after you click Accept on our cookie banner. We use Google Analytics 4 and Google Tag Manager (provider: Google Ireland Ltd.) with IP-anonymisation enabled. If you click Reject, these scripts are never loaded.",
        "privacy_s7_p4": "A full list of Google's cookies and how to control them is available at policies.google.com/technologies/cookies.",
    },
    "es": {
        "privacy_s1_li1": "Informacion de contacto: nombre, email y mensaje que aportas a traves del formulario. Tu IP se registra brevemente para prevenir spam.",
        "privacy_sN_title": "7. Suscripciones al boletin",
        "privacy_sN_p1": "Cuando te suscribes al boletin desde el pie del sitio recogemos y tratamos:",
        "privacy_sN_li1": "Tu direccion de email — solo para enviarte los nuevos articulos del blog a los que has optado por suscribirte.",
        "privacy_sN_li2": "Tu preferencia de idioma — para que el boletin y el correo de confirmacion te lleguen en tu lengua.",
        "privacy_sN_li3": "Marcas de tiempo de la suscripcion — prueba del consentimiento segun el RGPD.",
        "privacy_sN_p2": "Base juridica: tu consentimiento explicito (Art. 6(1)(a) RGPD). La suscripcion usa doble opt-in.",
        "privacy_sN_p3": "Retirada del consentimiento: cada boletin incluye un enlace de baja con un solo click. Tambien puedes escribir a info@imationgroup.com.",
        "privacy_sN_p4": "Conservacion: guardamos tu registro de suscripcion mientras esta activa. Tras darte de baja, conservamos el hash de tu email durante 12 meses con el unico fin de evitar re-suscripciones accidentales.",
        "privacy_s7_title": "8. Cookies y seguimiento",
        "privacy_s7_p1": "Usamos dos categorias de cookies. Puedes cambiar tu eleccion en cualquier momento mediante el enlace Preferencias de cookies del pie.",
        "privacy_s7_p2": "Cookies esenciales — siempre cargadas. Guardan tu eleccion de idioma y tu decision sobre el banner en el localStorage. No contienen datos personales, no rastrean y no son de terceros.",
        "privacy_s7_p3": "Cookies de analitica — se cargan SOLO si pulsas Aceptar en el banner. Usamos Google Analytics 4 y Google Tag Manager (proveedor: Google Ireland Ltd.) con anonimizacion de IP activada. Si pulsas Rechazar, estos scripts nunca se cargan.",
        "privacy_s7_p4": "El listado completo de cookies de Google y como controlarlas esta en policies.google.com/technologies/cookies.",
    },
}

KEYS = {
    "gl": {
        "privacy_s1_li1": "Información de contacto: nome, email e mensaxe que aportas mediante o formulario. O teu IP rexístrase brevemente para previr spam.",
        "privacy_sN_title": "7. Subscricións ao boletín",
        "privacy_sN_p1": "Cando te subscribes ao boletín dende o pé do sitio recollemos e tratamos:",
        "privacy_sN_li1": "O teu enderezo de email — só para enviarte os novos artigos do blog aos que te subscribiches.",
        "privacy_sN_li2": "A túa preferencia de idioma — para que o boletín e o correo de confirmación cheguen na túa lingua.",
        "privacy_sN_li3": "Marcas temporais da subscrición — proba do consentimento segundo o RXPD.",
        "privacy_sN_p2": "Base xurídica: o teu consentimento explícito (Art. 6(1)(a) RXPD). A subscrición usa doble opt-in: tes que premer no enlace de confirmación enviado á túa caixa antes de que se envíe ningún correo.",
        "privacy_sN_p3": "Retirada do consentimento: cada boletín inclúe un enlace de baixa cunha só pulsación. Tamén podes escribir a info@imationgroup.com para que te eliminemos.",
        "privacy_sN_p4": "Conservación: gardamos o teu rexistro de subscrición mentres está activa. Tras darte de baixa, conservamos o hash do teu email durante 12 meses co único fin de evitar re-subscricións accidentais.",
        "privacy_s7_title": "8. Cookies e seguimento",
        "privacy_s7_p1": "Usamos dúas categorías de cookies. Podes cambiar a túa elección en calquera momento mediante o enlace de Preferencias de cookies do pé.",
        "privacy_s7_p2": "Cookies esenciais — sempre cargadas. Gardan a túa elección de idioma e a túa decisión sobre o banner no localStorage. Non conteñen datos persoais, non rastrexan e non son de terceiros.",
        "privacy_s7_p3": "Cookies de analítica — cárganse SÓ se premes Aceptar no banner. Usamos Google Analytics 4 e Google Tag Manager (provedor: Google Ireland Ltd.) con anonimización de IP activada. Se premes Rexeitar, estes scripts nunca se cargan.",
        "privacy_s7_p4": "O listado completo de cookies de Google e como controlalas está en policies.google.com/technologies/cookies.",
    },
    "ca": {
        "privacy_s1_li1": "Informacio de contacte: nom, correu i missatge que aportes a traves del formulari. La teva IP es registra breument per prevenir spam.",
        "privacy_sN_title": "7. Subscripcions al butlleti",
        "privacy_sN_p1": "Quan et subscrius al butlleti des del peu del lloc recollim i tractem:",
        "privacy_sN_li1": "La teva adreca de correu — nomes per enviar-te els nous articles del blog als quals t'has subscrit.",
        "privacy_sN_li2": "La teva preferencia d'idioma — perque el butlleti i el correu de confirmacio t'arribin en la teva llengua.",
        "privacy_sN_li3": "Marques de temps de la subscripcio — prova del consentiment segons el RGPD.",
        "privacy_sN_p2": "Base juridica: el teu consentiment explicit (Art. 6(1)(a) RGPD). La subscripcio utilitza doble opt-in: has de fer click en un enllac de confirmacio enviat a la teva safata abans que s'enviï cap correu.",
        "privacy_sN_p3": "Retirada del consentiment: cada butlleti inclou un enllac de baixa amb un sol click. Tambe pots escriure a info@imationgroup.com perque t'eliminem.",
        "privacy_sN_p4": "Conservacio: guardem el teu registre de subscripcio mentre esta activa. Despres de donar-te de baixa, conservem el hash del teu correu durant 12 mesos amb l'unica finalitat d'evitar re-subscripcions accidentals.",
        "privacy_s7_title": "8. Cookies i seguiment",
        "privacy_s7_p1": "Utilitzem dues categories de cookies. Pots canviar la teva eleccio en qualsevol moment mitjancant l'enllac Preferencies de cookies del peu.",
        "privacy_s7_p2": "Cookies essencials — sempre carregades. Guarden la teva eleccio d'idioma i la teva decisio sobre el banner al localStorage. No contenen dades personals, no rastregen i no son de tercers.",
        "privacy_s7_p3": "Cookies d'analitica — es carreguen NOMES si fas click a Acceptar al banner. Utilitzem Google Analytics 4 i Google Tag Manager (proveidor: Google Ireland Ltd.) amb anonimitzacio d'IP activada. Si fas click a Rebutjar, aquests scripts mai no es carreguen.",
        "privacy_s7_p4": "El llistat complet de cookies de Google i com controlar-les es a policies.google.com/technologies/cookies.",
    },
    "pt": {
        "privacy_s1_li1": "Informacao de contacto: nome, email e mensagem que forneces atraves do formulario. O teu IP e registado brevemente para prevenir spam.",
        "privacy_sN_title": "7. Subscricoes da newsletter",
        "privacy_sN_p1": "Quando te subscreves na newsletter a partir do rodape do site recolhemos e tratamos:",
        "privacy_sN_li1": "O teu endereco de email — apenas para te enviar os novos artigos do blog para os quais te subscreveste.",
        "privacy_sN_li2": "A tua preferencia de idioma — para que a newsletter e o email de confirmacao cheguem na tua lingua.",
        "privacy_sN_li3": "Carimbos temporais da subscricao — prova do consentimento ao abrigo do RGPD.",
        "privacy_sN_p2": "Base juridica: o teu consentimento explicito (Art. 6.o, n.o 1, al. a) do RGPD). A subscricao usa double opt-in: tens de clicar no link de confirmacao enviado para a tua caixa antes de receberes qualquer correio.",
        "privacy_sN_p3": "Retirada do consentimento: cada newsletter inclui um link de cancelamento de um clique. Tambem podes escrever para info@imationgroup.com para seres removido.",
        "privacy_sN_p4": "Conservacao: guardamos o teu registo de subscricao enquanto estiver ativa. Apos cancelares, conservamos o hash do teu email durante 12 meses apenas para evitar re-subscricoes acidentais.",
        "privacy_s7_title": "8. Cookies e rastreio",
        "privacy_s7_p1": "Utilizamos duas categorias de cookies. Podes alterar a tua escolha a qualquer momento atraves do link Preferencias de cookies no rodape.",
        "privacy_s7_p2": "Cookies essenciais — sempre carregadas. Guardam a tua escolha de idioma e a tua decisao sobre o banner no localStorage. Nao contem dados pessoais, nao rastreiam e nao sao de terceiros.",
        "privacy_s7_p3": "Cookies de analise — so sao carregadas se clicares em Aceitar no banner. Utilizamos Google Analytics 4 e Google Tag Manager (fornecedor: Google Ireland Ltd.) com anonimizacao de IP ativada. Se clicares em Rejeitar, estes scripts nunca sao carregados.",
        "privacy_s7_p4": "A lista completa de cookies da Google e como controla-las esta em policies.google.com/technologies/cookies.",
    },
    "eu": {
        "privacy_s1_li1": "Kontaktu informazioa: izena, emaila eta mezua, kontaktu inprimakitik bidalitakoak. Zure IP helbidea spam-aren aurka epe laburrean erregistratzen da.",
        "privacy_sN_title": "7. Buletinaren harpidetzak",
        "privacy_sN_p1": "Webgunearen oinean buletinera harpidetzen zarenean, datu hauek biltzen eta tratatzen ditugu:",
        "privacy_sN_li1": "Zure email helbidea — soilik harpidetu zaren blogeko artikulu berriak bidaltzeko.",
        "privacy_sN_li2": "Zure hizkuntza-hobespena — buletina eta berrespen-mezua zure hizkuntzan jaso ditzazun.",
        "privacy_sN_li3": "Harpidetzaren denbora-zigiluak — DBOAren araberako baimenaren proba.",
        "privacy_sN_p2": "Oinarri juridikoa: zure berariazko adostasuna (6(1)(a) artikulua, DBOA). Harpidetzak doble opt-in erabiltzen du: zure bandejara bidalitako berrespen-estekan klik egin behar duzu posta bat ere bidali aurretik.",
        "privacy_sN_p3": "Adostasunaren erretiratzea: buletin bakoitzak baja-esteka klik bakarrekoa du. Halaber, info@imationgroup.com helbidera idatzi dezakezu ezabatua izateko.",
        "privacy_sN_p4": "Atxikitzea: zure harpidetza-erregistroa aktibo dagoen bitartean gordetzen dugu. Baja eman ondoren, zure emailaren hash-a 12 hilabetez gordetzen dugu nahi gabeko berriz harpidetzeak ekiditeko helburuarekin.",
        "privacy_s7_title": "8. Cookieak eta jarraipena",
        "privacy_s7_p1": "Bi kategoriako cookieak erabiltzen ditugu. Zure aukera edozein unetan alda dezakezu oinean dagoen Cookie hobespenak estekaren bidez.",
        "privacy_s7_p2": "Funtsezko cookieak — beti kargatzen dira. Zure hizkuntza-aukera eta cookie banner-aren erabakia nabigatzailearen localStorage-an gordetzen dituzte. Ez dute datu pertsonalik biltzen, ez dute jarraipenik egiten eta ez dira hirugarrenenak.",
        "privacy_s7_p3": "Analitika cookieak — SOILIK kargatzen dira cookie banner-ean Onartu klik egiten baduzu. Google Analytics 4 eta Google Tag Manager erabiltzen ditugu (hornitzailea: Google Ireland Ltd.) IP anonimizazioa aktibatuta. Ezetz klik egiten baduzu, script hauek inoiz ez dira kargatzen.",
        "privacy_s7_p4": "Google-en cookien zerrenda osoa eta nola kontrolatu policies.google.com/technologies/cookies helbidean dago.",
    },
    "et": {
        "privacy_s1_li1": "Kontaktandmed: nimi, e-post ja sonum, mille esitad kontaktivormi kaudu. Sinu IP-aadress logitakse luhidalt spammi tokestamiseks.",
        "privacy_sN_title": "7. Uudiskirja tellimused",
        "privacy_sN_p1": "Kui tellid uudiskirja saidi jaluse kaudu, kogume ja tootleme:",
        "privacy_sN_li1": "Sinu e-posti aadressi — kasutame seda ainult uute blogipostituste saatmiseks, mille saamiseks oled tellinud.",
        "privacy_sN_li2": "Sinu keele-eelistust — et uudiskiri ja kinnituskiri jouaks sinuni Sinu keeles.",
        "privacy_sN_li3": "Tellimuse ajatempleid — nousoleku toend GDPR-i alusel.",
        "privacy_sN_p2": "Oiguslik alus: Sinu selgesonaline nousolek (GDPR Art. 6(1)(a)). Tellimine kasutab kahekordset opt-in'i: enne uhegi uudiskirja saatmist pead klopsama oma postkasti saadetud kinnituslinki.",
        "privacy_sN_p3": "Nousoleku tagasivotmine: iga uudiskiri sisaldab uhe klopsuga tellimuse lopetamise linki. Voib ka kirjutada aadressile info@imationgroup.com, et Sinu andmed eemaldataks.",
        "privacy_sN_p4": "Sailitamine: hoiame Sinu tellimuse aktiivsena, kuni see kehtib. Parast tellimuse lopetamist sailitame Sinu e-posti aadressi rasi 12 kuud, et valtida juhuslikku uuesti tellimist.",
        "privacy_s7_title": "8. Kupsised ja jalgimine",
        "privacy_s7_p1": "Kasutame kahte kategooriat kupsiseid. Saad oma valikut igal ajal muuta jaluse Kupsiste eelistused lingi kaudu.",
        "privacy_s7_p2": "Olulised kupsised — alati laaditud. Need salvestavad Sinu keelevaliku ja kupsisebanneri otsuse brauseri localStorage'i. Need ei sisalda isikuandmeid, ei jalgi ega ole kolmanda osapoole omad.",
        "privacy_s7_p3": "Analuutika kupsised — laaditakse AINULT siis, kui klopsad kupsisebanneril Noustun. Kasutame Google Analytics 4 ja Google Tag Manager'it (pakkuja: Google Ireland Ltd.) IP-anonuumseks muutmisega. Kui klopsad Keeldun, neid skripte ei laadita kunagi.",
        "privacy_s7_p4": "Google'i kupsiste taielik loetelu ja kuidas neid juhtida on aadressil policies.google.com/technologies/cookies.",
    },
}

p = Path(__file__).resolve().parent.parent / "i18n.js"
s = p.read_text(encoding="utf-8")


def _js_string(s: str) -> str:
    """Encode a python str as a JS double-quoted string. Backslash + inner
    double quotes are escaped; everything else passes through (the values
    here are restricted to safe characters)."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def patch_lang(s: str, lang: str, kv: dict) -> str:
    """Insert / update keys inside the `<lang>: { ... }` dict block. Replaces
    existing keys conservatively (matches `key:` followed by EITHER a single-
    or double-quoted JS string up to the matching closing quote) and appends
    new ones."""
    pat = re.compile(rf'(\b{lang}\s*:\s*\{{)(.*?)(\}})', re.S)
    m = pat.search(s)
    if not m:
        print(f"  {lang}: NO MATCH"); return s
    inside = m.group(2)
    replaced = 0; added = 0
    for k, v in kv.items():
        repl = f"{k}:{_js_string(v)}"
        # Match key followed by a JS string in either quote style,
        # using non-greedy capture between the matched quote pair.
        kpat = re.compile(rf'\b{k}\s*:\s*("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')')
        if kpat.search(inside):
            inside = kpat.sub(lambda _: repl, inside, count=1)
            replaced += 1
        else:
            inside = inside.rstrip().rstrip(",") + ",\n    " + repl
            added += 1
    print(f"  {lang}: replaced={replaced} added={added}")
    return s[: m.start()] + m.group(1) + inside + m.group(3) + s[m.end():]


for lang, kv in {**KEYS_EN_ES, **KEYS}.items():
    s = patch_lang(s, lang, kv)

p.write_text(s, encoding="utf-8")
print("Translations applied.")
