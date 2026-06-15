"""Translate the new privacy_s9_* (International Transfers) to all 7 langs.
Targets i18n.js (the build picks it up at build time)."""
import re
from pathlib import Path

KEYS = {
    "en": {
        "privacy_s9_p1": "The website and its database run on a VPS hosted by Hostinger International Limited in Paris, France (European Union). Your contact-form messages, newsletter subscription record and visit logs stay within the European Economic Area (EEA).",
        "privacy_s9_p2": "The only third party that may transfer data outside the EEA is Google (Analytics 4 + Tag Manager), and only if you accept analytics cookies. Google's transfers are covered by Standard Contractual Clauses (SCCs) and the EU-US Data Privacy Framework adequacy decision (July 2023). IP anonymisation is enabled on our side to minimise the data shared.",
        "privacy_s9_p3": "No other personal data is shared with parties outside the EEA. If this ever changes we will update this policy before the new transfer starts.",
    },
    "es": {
        "privacy_s9_p1": "El sitio web y su base de datos se ejecutan en un VPS alojado por Hostinger International Limited en Paris, Francia (Union Europea). Tus mensajes del formulario, el registro de suscripcion al boletin y los logs de visita permanecen dentro del Espacio Economico Europeo (EEE).",
        "privacy_s9_p2": "El unico tercero que puede transferir datos fuera del EEE es Google (Analytics 4 + Tag Manager), y solo si aceptas las cookies de analitica. Las transferencias de Google estan cubiertas por las Clausulas Contractuales Tipo (SCCs) y la decision de adecuacion EU-US Data Privacy Framework (julio 2023). En nuestro lado tenemos la anonimizacion de IP activada para minimizar los datos compartidos.",
        "privacy_s9_p3": "Ningun otro dato personal se comparte con terceros fuera del EEE. Si esto cambia en el futuro, actualizaremos esta politica antes del inicio de la nueva transferencia.",
    },
    "gl": {
        "privacy_s9_p1": "O sitio web e a sua base de datos executanse nun VPS aloxado por Hostinger International Limited en Paris, Francia (Union Europea). As tuas mensaxes do formulario, o rexistro de subscricion ao boletin e os logs de visita permanecen dentro do Espazo Economico Europeo (EEE).",
        "privacy_s9_p2": "O unico terceiro que pode transferir datos fora do EEE e Google (Analytics 4 + Tag Manager), e so se aceptas as cookies de analitica. As transferencias de Google estan cubertas polas Clausulas Contractuais Tipo (SCCs) e a decision de adecuacion EU-US Data Privacy Framework (xullo 2023). No noso lado temos a anonimizacion de IP activada.",
        "privacy_s9_p3": "Ningun outro dato persoal se comparte con terceiros fora do EEE. Se isto cambia, actualizaremos esta politica antes do inicio da nova transferencia.",
    },
    "ca": {
        "privacy_s9_p1": "El lloc web i la seva base de dades s'executen en un VPS allotjat per Hostinger International Limited a Paris, Franca (Unio Europea). Els teus missatges del formulari, el registre de subscripcio al butlleti i els logs de visita romanen dins de l'Espai Economic Europeu (EEE).",
        "privacy_s9_p2": "L'unic tercer que pot transferir dades fora del EEE es Google (Analytics 4 + Tag Manager), i nomes si acceptes les cookies d'analitica. Les transferencies de Google estan cobertes per les Clausules Contractuals Tipus (SCCs) i la decisio d'adequacio EU-US Data Privacy Framework (juliol 2023). Al nostre costat tenim l'anonimitzacio d'IP activada.",
        "privacy_s9_p3": "Cap altre dada personal es comparteix amb tercers fora del EEE. Si aixo canvia, actualitzarem aquesta politica abans de l'inici de la nova transferencia.",
    },
    "pt": {
        "privacy_s9_p1": "O site e a sua base de dados sao executados num VPS alojado pela Hostinger International Limited em Paris, Franca (Uniao Europeia). As tuas mensagens do formulario, o registo de subscricao da newsletter e os logs de visita permanecem dentro do Espaco Economico Europeu (EEE).",
        "privacy_s9_p2": "O unico terceiro que pode transferir dados fora do EEE e a Google (Analytics 4 + Tag Manager), e apenas se aceitares as cookies de analise. As transferencias da Google estao cobertas pelas Clausulas Contratuais-Tipo (SCCs) e pela decisao de adequacao EU-US Data Privacy Framework (julho 2023). Do nosso lado, a anonimizacao de IP esta ativada.",
        "privacy_s9_p3": "Nenhum outro dado pessoal e partilhado com terceiros fora do EEE. Se isto mudar, atualizaremos esta politica antes do inicio da nova transferencia.",
    },
    "eu": {
        "privacy_s9_p1": "Webgunea eta bere datu-basea Hostinger International Limited-ek Parisen, Frantzian, ostatatzen duen VPS batean exekutatzen dira (Europako Batasuna). Formularioko zure mezuak, buletinaren harpidetza-erregistroa eta bisitaren logak Europako Esparru Ekonomikoaren (EEE) barruan geratzen dira.",
        "privacy_s9_p2": "EEE-tik kanpo datuak transferi ditzakeen hirugarren bakarra Google da (Analytics 4 + Tag Manager), eta soilik analitika cookieak onartzen badituzu. Googleren transferentziak Estandarrezko Kontratu-klausulek (SCCs) eta EU-US Data Privacy Framework (2023ko uztaila) egokitze-erabakiak estaltzen dituzte. Gure aldetik IP anonimizazioa aktibatuta dago.",
        "privacy_s9_p3": "EEE-tik kanpoko hirugarrenekin ez da beste datu pertsonalik partekatzen. Hori aldatzen bada, transferentzia berriaren aurretik politika hau eguneratuko dugu.",
    },
    "et": {
        "privacy_s9_p1": "Sait ja selle andmebaas tootavad VPS-il, mida hostib Hostinger International Limited Pariisis, Prantsusmaal (Euroopa Liit). Sinu kontaktivormi sonumid, uudiskirja tellimuse kirje ja kulastuste logid jaavad Euroopa Majanduspiirkonna (EMP) sisse.",
        "privacy_s9_p2": "Ainus kolmas isik, kes voib andmeid EMP-st valja edastada, on Google (Analytics 4 + Tag Manager), ja ainult juhul kui noustud analuutika kupsistega. Google'i edastusi katavad standardsed lepingulised punktid (SCC-d) ja EU-US Data Privacy Framework'i piisavusotsus (juuli 2023). Meie poolt on IP anonuumimine aktiveeritud.",
        "privacy_s9_p3": "Muid isikuandmeid EMP-valistele kolmandatele isikutele ei jagata. Kui see kunagi muutub, uuendame seda poliitikat enne uue edastuse algust.",
    },
}


def _js_string(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def patch_lang(s: str, lang: str, kv: dict) -> str:
    pat = re.compile(rf'(\b{lang}\s*:\s*\{{)(.*?)(\}})', re.S)
    m = pat.search(s)
    if not m:
        print(f"  {lang}: NO MATCH"); return s
    inside = m.group(2)
    rep = 0; add = 0
    for k, v in kv.items():
        repl = f"{k}:{_js_string(v)}"
        kpat = re.compile(rf'\b{k}\s*:\s*("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')')
        if kpat.search(inside):
            inside = kpat.sub(lambda _: repl, inside, count=1)
            rep += 1
        else:
            inside = inside.rstrip().rstrip(",") + ",\n    " + repl
            add += 1
    print(f"  {lang}: replaced={rep} added={add}")
    return s[: m.start()] + m.group(1) + inside + m.group(3) + s[m.end():]


p = Path(__file__).resolve().parent.parent / "i18n.js"
s = p.read_text(encoding="utf-8")
for lang, kv in KEYS.items():
    s = patch_lang(s, lang, kv)
p.write_text(s, encoding="utf-8")
print("Done.")
