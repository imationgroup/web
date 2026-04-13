// ImationGroup — translations
// Languages: en, es, gl (Galego), ca (Català), pt (Português), eu (Euskera), et (Eesti)

const TRANSLATIONS = {
  en: {
    page_title:"ImationGroup | Data Engineering and Software Solutions",
    nav_home:"Home",nav_about:"About",nav_services:"Services",nav_technologies:"Technologies",nav_projects:"Projects",nav_contact:"Contact",
    hero_tagline:"Data Engineering and Software Solutions",
    hero_description:"We transform data into actionable insights and build scalable software solutions that drive business growth. Our expertise spans data engineering, data science, and cloud-native development.",
    hero_btn_contact:"Contact Us",hero_btn_services:"Our Services",
    about_label:"About Us",about_title:"Pioneering Data-Driven Solutions",
    about_subtitle:"Building the future of enterprise technology through innovation and expertise",
    about_who_title:"Who We Are",
    about_who_p1:"ImationGroup is a forward-thinking technology company specialising in data engineering, data science, and scalable software solutions. We partner with organisations to unlock the full potential of their data and transform it into competitive advantage.",
    about_who_p2:"Our team of experienced engineers and data scientists brings together deep technical expertise with a passion for solving complex business challenges. We believe in building systems that are not only powerful but also maintainable, scalable, and future-proof.",
    value_innovation:"Innovation",value_innovation_desc:"Leveraging cutting-edge technologies to deliver breakthrough solutions",
    value_reliability:"Reliability",value_reliability_desc:"Building robust systems that perform consistently under any conditions",
    value_partnership:"Partnership",value_partnership_desc:"Working closely with clients to understand and exceed their expectations",
    value_excellence:"Excellence",value_excellence_desc:"Committed to delivering the highest quality in every project we undertake",
    stat_projects:"Projects Delivered",stat_satisfaction:"Client Satisfaction",stat_support:"Support Available",stat_experience:"Years Experience",
    services_label:"Services",services_title:"What We Offer",services_subtitle:"Comprehensive technology solutions tailored to your business needs",services_more:"See All Services",
    svc_data_eng:"Data Engineering",svc_data_eng_desc:"Design and build robust data pipelines, data warehouses, and ETL processes that handle massive volumes of data efficiently and reliably.",
    svc_data_sci:"Data Science",svc_data_sci_desc:"Transform raw data into actionable insights using advanced analytics, machine learning models, and predictive algorithms.",
    svc_soft_dev:"Software Development",svc_soft_dev_desc:"Build custom software solutions using modern architectures and best practices that scale with your business growth.",
    svc_cloud:"Cloud Solutions",svc_cloud_desc:"Migrate, optimise, and manage cloud infrastructure on AWS, Azure, or GCP with security and cost-efficiency in mind.",
    svc_consulting:"Consulting",svc_consulting_desc:"Strategic technology consulting to help you make informed decisions about your data strategy and digital transformation journey.",
    svc_bi:"Business Intelligence",svc_bi_desc:"We help teams create reporting layers and analytics environments that support faster decisions with trustworthy, well-structured data.",
    tech_label:"Technologies",tech_title:"Our Tech Stack",tech_subtitle:"Industry-leading technologies powering our solutions",
    projects_label:"Projects",projects_title:"Scalable Solutions in Action",projects_subtitle:"Delivering end-to-end systems that turn data into value and insight",
    proj_pipelines:"Data Pipelines",proj_pipelines_desc:"Automated, fault-tolerant data pipelines that connect sources, transform data, and ensure reliable delivery to analytics systems.",
    proj_etl:"ETL Systems",proj_etl_desc:"Designed and optimised high-performance ETL frameworks enabling seamless data integration across platforms and domains.",
    proj_bi:"Business Intelligence",proj_bi_desc:"Developed BI and analytics dashboards that empower strategic, data-informed decision-making in real time.",
    proj_custom:"Custom Software",proj_custom_desc:"End-to-end software tailored to your operational ecosystem — scalable, secure, and cloud-ready.",
    proj_cloud:"Cloud Infrastructure",proj_cloud_desc:"Cloud-native architectures on AWS designed for scalability, performance, and cost efficiency.",
    proj_scalable:"Scalable Architectures",proj_scalable_desc:"End-to-end architecture design for distributed systems, data platforms, and software ecosystems that grow with your business.",
    contact_label:"Contact",contact_title:"Get in Touch",contact_subtitle:"Let's discuss how ImationGroup can help transform your data and technology strategy",
    contact_desc:"We are ready to collaborate on your next data and software project. Reach out to discuss your challenges and goals.",
    contact_email_label:"Email",contact_phone_label:"Phone",contact_location_label:"Location",contact_location:"Global — Remote Projects Worldwide",
    form_name:"Name",form_name_placeholder:"Your name",form_email:"Email",form_email_placeholder:"you@example.com",
    form_message:"Message",form_message_placeholder:"How can we help you?",form_submit:"Send Message",
    footer_desc:"Data engineering, data science, and scalable software solutions designed to elevate your business performance.",
    footer_company:"Company",footer_support:"Support",footer_privacy:"Privacy Policy",footer_terms:"Terms of Service",footer_follow:"Follow",
    footer_copyright:"© 2025 ImationGroup. All rights reserved.",
    alert_success:"Thank you for reaching out! We'll be in touch soon.",alert_error:"Something went wrong. Please try again.",alert_network:"Network error. Please try again.",
    back_home:"Back to Home",
    cs_page_title:"Message Sent | ImationGroup",cs_label:"Message received",cs_title:"Thank you for reaching out!",
    cs_message:"We've received your message and will get back to you as soon as possible. Our team typically responds within 24–48 hours.",
    cs_detail1_title:"Confirmation email",cs_detail1_desc:"You'll receive a confirmation to the email address you provided.",
    cs_detail2_title:"Response time",cs_detail2_desc:"Our team will respond within 24–48 business hours.",
    cs_detail3_title:"Dedicated attention",cs_detail3_desc:"A specialist from our team will personally review your inquiry.",
    cs_back:"Back to Home",cs_rights:"All rights reserved.",cs_privacy:"Privacy Policy",cs_terms:"Terms of Service",
    svc_page_title:"Technology Services | ImationGroup",svc_label:"Services",
    svc_hero_title:"Technology Solutions That Drive Growth",
    svc_hero_desc:"From a stunning website to a complete digital strategy — we deliver the tools and expertise your business needs to thrive online.",
    svc_web_title:"Web Design",svc_web_subtitle:"Professional websites that convert visitors into customers — built for speed, SEO and mobile.",
    svc_web_f1:"Corporate websites — build trust and showcase your brand with a polished, high-performance site.",
    svc_web_f2:"Portfolio sites — elegant presentation of your work, optimised for creative professionals and agencies.",
    svc_web_f3:"E-commerce — full online stores with product management, secure checkout and payment integration.",
    svc_web_f4:"SEO-ready structure, fast loading times and responsive design included on every project.",
    svc_host_title:"Web Hosting",svc_host_subtitle:"Reliable, fast and secure hosting on our own VPS servers — full control, no hidden fees.",
    svc_host_f1:"Private VPS servers with dedicated resources — no shared slowdowns.",
    svc_host_f2:"99.9% uptime SLA with 24/7 monitoring and automatic backups.",
    svc_host_f3:"Free SSL certificate, CDN configuration and DDoS protection included.",
    svc_host_f4:"Scalable plans — upgrade resources instantly as your traffic grows.",
    svc_host_price:"From €10 / month",
    svc_app_title:"App Development",svc_app_subtitle:"Custom web and mobile applications built to automate, engage and scale your business.",
    svc_app_f1:"Progressive Web Apps (PWA) — app-like experience from any browser.",
    svc_app_f2:"Native and cross-platform mobile apps for iOS and Android.",
    svc_app_f3:"Internal business tools — dashboards, CRMs and workflow automation.",
    svc_app_f4:"API integrations — connect your app to payment gateways, ERPs and more.",
    svc_mkt_title:"Digital Marketing",svc_mkt_subtitle:"Data-driven strategies that increase visibility, attract leads and grow revenue.",
    svc_mkt_f1:"SEO — technical optimisation and content that ranks on Google.",
    svc_mkt_f2:"SEM & Google Ads — targeted campaigns that maximise ROI.",
    svc_mkt_f3:"Social media management — engaging content and community growth.",
    svc_mkt_f4:"Analytics & reporting — monthly performance reviews with clear dashboards.",
    svc_de_title:"Data Engineering",svc_de_subtitle:"Robust data pipelines and ETL processes that turn raw data into reliable, analytics-ready assets.",
    svc_de_f1:"End-to-end data pipeline design, development and maintenance.",
    svc_de_f2:"Data warehouse and data lake architecture on cloud platforms.",
    svc_de_f3:"Real-time streaming with Apache Kafka and Apache Spark.",
    svc_de_f4:"Data quality, governance and monitoring frameworks.",
    svc_ds_title:"Data Science & BI",svc_ds_subtitle:"From raw data to strategic insight — machine learning, predictive models and executive dashboards.",
    svc_ds_f1:"Predictive analytics and machine learning model development.",
    svc_ds_f2:"BI dashboards and self-service reporting for business teams.",
    svc_ds_f3:"A/B testing, experimentation frameworks and statistical analysis.",
    svc_ds_f4:"AI integration — LLMs, recommendation engines and anomaly detection.",
    svc_cta:"Request a Quote",
    cta_title:"Ready to grow your business?",cta_desc:"Tell us about your project and we'll get back to you within 24 hours with a tailored proposal.",cta_btn:"Contact Us Now",
    footer_rights:"All rights reserved."
  },
  es: {
    page_title:"ImationGroup | Ingeniería de Datos y Soluciones de Software",
    nav_home:"Inicio",nav_about:"Nosotros",nav_services:"Servicios",nav_technologies:"Tecnologías",nav_projects:"Proyectos",nav_contact:"Contacto",
    hero_tagline:"Ingeniería de Datos y Soluciones de Software",
    hero_description:"Transformamos datos en información accionable y construimos soluciones de software escalables que impulsan el crecimiento empresarial.",
    hero_btn_contact:"Contáctanos",hero_btn_services:"Nuestros Servicios",
    about_label:"Nosotros",about_title:"Soluciones Pioneras Basadas en Datos",
    about_subtitle:"Construyendo el futuro de la tecnología empresarial a través de la innovación y la experiencia",
    about_who_title:"Quiénes Somos",
    about_who_p1:"ImationGroup es una empresa tecnológica especializada en ingeniería de datos, ciencia de datos y soluciones de software escalables.",
    about_who_p2:"Nuestro equipo combina experiencia técnica profunda con pasión por resolver desafíos empresariales complejos.",
    value_innovation:"Innovación",value_innovation_desc:"Aprovechando tecnologías de vanguardia para ofrecer soluciones revolucionarias",
    value_reliability:"Fiabilidad",value_reliability_desc:"Construyendo sistemas robustos que funcionan consistentemente bajo cualquier condición",
    value_partnership:"Colaboración",value_partnership_desc:"Trabajando estrechamente con los clientes para comprender y superar sus expectativas",
    value_excellence:"Excelencia",value_excellence_desc:"Comprometidos con ofrecer la máxima calidad en cada proyecto",
    stat_projects:"Proyectos Entregados",stat_satisfaction:"Satisfacción del Cliente",stat_support:"Soporte Disponible",stat_experience:"Años de Experiencia",
    services_label:"Servicios",services_title:"Lo Que Ofrecemos",services_subtitle:"Soluciones tecnológicas integrales adaptadas a las necesidades de tu negocio",services_more:"Ver todos los servicios",
    svc_data_eng:"Ingeniería de Datos",svc_data_eng_desc:"Diseñamos y construimos pipelines de datos robustos, almacenes de datos y procesos ETL que manejan grandes volúmenes de datos.",
    svc_data_sci:"Ciencia de Datos",svc_data_sci_desc:"Transformamos datos en información accionable usando análisis avanzado, modelos de machine learning y algoritmos predictivos.",
    svc_soft_dev:"Desarrollo de Software",svc_soft_dev_desc:"Construimos soluciones de software personalizadas con arquitecturas modernas que escalan con el crecimiento de tu negocio.",
    svc_cloud:"Soluciones Cloud",svc_cloud_desc:"Migramos, optimizamos y gestionamos infraestructura en la nube en AWS, Azure o GCP.",
    svc_consulting:"Consultoría",svc_consulting_desc:"Consultoría tecnológica estratégica para ayudarte a tomar decisiones informadas sobre tu estrategia de datos.",
    svc_bi:"Business Intelligence",svc_bi_desc:"Ayudamos a los equipos a crear capas de reporting y entornos analíticos con datos fiables y bien estructurados.",
    tech_label:"Tecnologías",tech_title:"Nuestro Stack Tecnológico",tech_subtitle:"Tecnologías líderes en la industria que impulsan nuestras soluciones",
    projects_label:"Proyectos",projects_title:"Soluciones Escalables en Acción",projects_subtitle:"Entregando sistemas de extremo a extremo que convierten datos en valor",
    proj_pipelines:"Pipelines de Datos",proj_pipelines_desc:"Pipelines automatizados y tolerantes a fallos para entrega fiable a sistemas analíticos.",
    proj_etl:"Sistemas ETL",proj_etl_desc:"Frameworks ETL de alto rendimiento para integración de datos entre plataformas.",
    proj_bi:"Business Intelligence",proj_bi_desc:"Dashboards de BI para toma de decisiones estratégicas en tiempo real.",
    proj_custom:"Software Personalizado",proj_custom_desc:"Software de extremo a extremo adaptado a tu ecosistema — escalable, seguro y cloud-ready.",
    proj_cloud:"Infraestructura Cloud",proj_cloud_desc:"Arquitecturas cloud-native en AWS para escalabilidad, rendimiento y eficiencia de costes.",
    proj_scalable:"Arquitecturas Escalables",proj_scalable_desc:"Diseño de arquitectura para sistemas distribuidos y plataformas de datos que crecen con tu negocio.",
    contact_label:"Contacto",contact_title:"Ponte en Contacto",contact_subtitle:"Hablemos de cómo ImationGroup puede transformar tu estrategia de datos y tecnología",
    contact_desc:"Estamos listos para colaborar en tu próximo proyecto. Contáctanos para hablar de tus desafíos y objetivos.",
    contact_email_label:"Correo electrónico",contact_phone_label:"Teléfono",contact_location_label:"Ubicación",contact_location:"Global — Proyectos Remotos en Todo el Mundo",
    form_name:"Nombre",form_name_placeholder:"Tu nombre",form_email:"Correo electrónico",form_email_placeholder:"tu@ejemplo.com",
    form_message:"Mensaje",form_message_placeholder:"¿Cómo podemos ayudarte?",form_submit:"Enviar Mensaje",
    footer_desc:"Ingeniería de datos, ciencia de datos y soluciones de software diseñadas para elevar el rendimiento de tu negocio.",
    footer_company:"Empresa",footer_support:"Soporte",footer_privacy:"Política de Privacidad",footer_terms:"Términos de Servicio",footer_follow:"Síguenos",
    footer_copyright:"© 2025 ImationGroup. Todos los derechos reservados.",
    alert_success:"¡Gracias por contactarnos! Nos pondremos en contacto pronto.",alert_error:"Algo salió mal. Por favor, inténtalo de nuevo.",alert_network:"Error de red. Por favor, inténtalo de nuevo.",
    back_home:"Volver al Inicio",
    cs_page_title:"Mensaje Enviado | ImationGroup",cs_label:"Mensaje recibido",cs_title:"¡Gracias por contactarnos!",
    cs_message:"Hemos recibido tu mensaje y nos pondremos en contacto lo antes posible. Nuestro equipo responde habitualmente en 24–48 horas.",
    cs_detail1_title:"Email de confirmación",cs_detail1_desc:"Recibirás una confirmación en la dirección de correo que has proporcionado.",
    cs_detail2_title:"Tiempo de respuesta",cs_detail2_desc:"Nuestro equipo responderá en un plazo de 24–48 horas laborables.",
    cs_detail3_title:"Atención personalizada",cs_detail3_desc:"Un especialista de nuestro equipo revisará personalmente tu consulta.",
    cs_back:"Volver al Inicio",cs_rights:"Todos los derechos reservados.",cs_privacy:"Política de Privacidad",cs_terms:"Términos de Servicio",
    svc_page_title:"Servicios Tecnológicos | ImationGroup",svc_label:"Servicios",
    svc_hero_title:"Soluciones Tecnológicas que Impulsan tu Negocio",
    svc_hero_desc:"Desde una web profesional hasta una estrategia digital completa — te damos las herramientas que tu negocio necesita para crecer online.",
    svc_web_title:"Diseño Web",svc_web_subtitle:"Páginas web profesionales que convierten visitantes en clientes — rápidas, SEO y responsive.",
    svc_web_f1:"Páginas corporativas — transmite confianza con una web atractiva y de alto rendimiento.",
    svc_web_f2:"Portfolio — presentación elegante de tu trabajo para profesionales creativos.",
    svc_web_f3:"Comercio electrónico — tiendas online completas con pasarela de pago.",
    svc_web_f4:"Estructura SEO desde el primer día, carga rápida y diseño adaptable.",
    svc_host_title:"Alojamiento Web",svc_host_subtitle:"Hosting fiable y seguro en nuestros propios servidores VPS — sin costes ocultos.",
    svc_host_f1:"Servidores VPS privados con recursos dedicados.",
    svc_host_f2:"SLA de disponibilidad del 99,9% con monitorización 24/7 y copias de seguridad.",
    svc_host_f3:"Certificado SSL gratuito, CDN y protección DDoS incluidos.",
    svc_host_f4:"Planes escalables — amplía recursos según crece tu tráfico.",
    svc_host_price:"Desde 10€ / mes",
    svc_app_title:"Desarrollo de Aplicaciones",svc_app_subtitle:"Aplicaciones web y móviles a medida para automatizar y escalar tu negocio.",
    svc_app_f1:"Progressive Web Apps (PWA) — experiencia de app desde cualquier navegador.",
    svc_app_f2:"Apps nativas y multiplataforma para iOS y Android.",
    svc_app_f3:"Herramientas internas — dashboards, CRMs y automatización de flujos.",
    svc_app_f4:"Integraciones con APIs — pasarelas de pago, ERPs y servicios de terceros.",
    svc_mkt_title:"Marketing Digital",svc_mkt_subtitle:"Estrategias basadas en datos que aumentan visibilidad, atraen leads y hacen crecer ventas.",
    svc_mkt_f1:"SEO — optimización técnica y contenido que posiciona en Google.",
    svc_mkt_f2:"SEM y Google Ads — campañas de pago que maximizan el ROI.",
    svc_mkt_f3:"Gestión de redes sociales — contenido atractivo y crecimiento de comunidad.",
    svc_mkt_f4:"Análisis e informes — revisión de rendimiento mensual.",
    svc_de_title:"Ingeniería de Datos",svc_de_subtitle:"Pipelines robustos y procesos ETL que convierten datos en bruto en activos fiables para análisis.",
    svc_de_f1:"Diseño, desarrollo y mantenimiento de pipelines de datos de extremo a extremo.",
    svc_de_f2:"Arquitectura de data warehouse y data lake en plataformas cloud.",
    svc_de_f3:"Streaming en tiempo real con Apache Kafka y Apache Spark.",
    svc_de_f4:"Calidad del dato, gobernanza y frameworks de monitorización.",
    svc_ds_title:"Ciencia de Datos e BI",svc_ds_subtitle:"Del dato en bruto a la decisión estratégica — machine learning, modelos predictivos y dashboards ejecutivos.",
    svc_ds_f1:"Analítica predictiva y desarrollo de modelos de machine learning.",
    svc_ds_f2:"Dashboards de BI y reporting de autoservicio para equipos de negocio.",
    svc_ds_f3:"A/B testing, frameworks de experimentación y análisis estadístico.",
    svc_ds_f4:"Integración de IA — LLMs, motores de recomendación y detección de anomalías.",
    svc_cta:"Solicitar presupuesto",
    cta_title:"¿Listo para hacer crecer tu negocio?",cta_desc:"Cuéntanos tu proyecto y te responderemos en menos de 24 horas con una propuesta personalizada.",cta_btn:"Contáctanos ahora",
    footer_rights:"Todos los derechos reservados."
  },
  gl: {
    page_title:"ImationGroup | Enxeñaría de Datos e Solucións de Software",
    nav_home:"Inicio",nav_about:"Nós",nav_services:"Servizos",nav_technologies:"Tecnoloxías",nav_projects:"Proxectos",nav_contact:"Contacto",
    hero_tagline:"Enxeñaría de Datos e Solucións de Software",
    hero_description:"Transformamos datos en información accionable e construímos solucións de software escalables que impulsan o crecemento empresarial.",
    hero_btn_contact:"Contacta connosco",hero_btn_services:"Os nosos servizos",
    about_label:"Nós",about_title:"Solucións Pioneiras Baseadas en Datos",about_subtitle:"Construíndo o futuro da tecnoloxía empresarial a través da innovación",
    about_who_title:"Quen somos",about_who_p1:"ImationGroup é unha empresa tecnolóxica especializada en enxeñaría de datos, ciencia de datos e solucións de software escalables.",about_who_p2:"O noso equipo combina experiencia técnica profunda coa paixón por resolver retos empresariais complexos.",
    value_innovation:"Innovación",value_innovation_desc:"Aproveitando tecnoloxías punteiras para ofrecer solucións revolucionarias",value_reliability:"Fiabilidade",value_reliability_desc:"Construíndo sistemas robustos que funcionan de forma consistente",value_partnership:"Colaboración",value_partnership_desc:"Traballando estreitamente cos clientes para superar as súas expectativas",value_excellence:"Excelencia",value_excellence_desc:"Comprometidos coa máxima calidade en cada proxecto",
    stat_projects:"Proxectos Entregados",stat_satisfaction:"Satisfacción do Cliente",stat_support:"Soporte Dispoñible",stat_experience:"Anos de Experiencia",
    services_label:"Servizos",services_title:"O Que Ofrecemos",services_subtitle:"Solucións tecnolóxicas integrais adaptadas ás necesidades do teu negocio",services_more:"Ver todos os servizos",
    svc_data_eng:"Enxeñaría de Datos",svc_data_eng_desc:"Deseñamos e construímos pipelines de datos robustos e procesos ETL que xestionan grandes volumes de datos.",svc_data_sci:"Ciencia de Datos",svc_data_sci_desc:"Transformamos datos en información accionable usando análise avanzada e algoritmos preditivos.",svc_soft_dev:"Desenvolvemento de Software",svc_soft_dev_desc:"Construímos solucións de software personalizadas con arquitecturas modernas que escalan co teu negocio.",svc_cloud:"Solucións Cloud",svc_cloud_desc:"Migramos e xestionamos infraestrutura na nube en AWS, Azure ou GCP.",svc_consulting:"Consultoría",svc_consulting_desc:"Consultoría tecnolóxica estratéxica para axudarche a tomar decisións informadas.",svc_bi:"Business Intelligence",svc_bi_desc:"Axudamos aos equipos a crear capas de reporting e contornos analíticos con datos fiables.",
    tech_label:"Tecnoloxías",tech_title:"O Noso Stack Tecnolóxico",tech_subtitle:"Tecnoloxías líderes que impulsan as nosas solucións",
    projects_label:"Proxectos",projects_title:"Solucións Escalables en Acción",projects_subtitle:"Entregando sistemas de extremo a extremo que converten datos en valor",
    proj_pipelines:"Pipelines de Datos",proj_pipelines_desc:"Pipelines automatizados para entrega fiable a sistemas analíticos.",proj_etl:"Sistemas ETL",proj_etl_desc:"Frameworks ETL de alto rendemento para integración de datos.",proj_bi:"Business Intelligence",proj_bi_desc:"Dashboards de BI para toma de decisións estratéxicas en tempo real.",proj_custom:"Software Personalizado",proj_custom_desc:"Software adaptado ao teu ecosistema — escalable, seguro e cloud-ready.",proj_cloud:"Infraestrutura Cloud",proj_cloud_desc:"Arquitecturas cloud-native en AWS para escalabilidade e eficiencia.",proj_scalable:"Arquitecturas Escalables",proj_scalable_desc:"Deseño de arquitectura para sistemas distribuídos e plataformas de datos.",
    contact_label:"Contacto",contact_title:"Ponte en Contacto",contact_subtitle:"Falemos de como ImationGroup pode transformar a túa estratexia de datos",contact_desc:"Estamos listos para colaborar no teu próximo proxecto.",contact_email_label:"Correo electrónico",contact_phone_label:"Teléfono",contact_location_label:"Localización",contact_location:"Global — Proxectos Remotos en Todo o Mundo",
    form_name:"Nome",form_name_placeholder:"O teu nome",form_email:"Correo electrónico",form_email_placeholder:"ti@exemplo.com",form_message:"Mensaxe",form_message_placeholder:"Como podemos axudarche?",form_submit:"Enviar Mensaxe",
    footer_desc:"Enxeñaría de datos e solucións de software para elevar o rendemento do teu negocio.",footer_company:"Empresa",footer_support:"Soporte",footer_privacy:"Política de Privacidade",footer_terms:"Termos de Servizo",footer_follow:"Síguenos",footer_copyright:"© 2025 ImationGroup. Todos os dereitos reservados.",
    alert_success:"Grazas por contactar connosco! Poñerémonos en contacto en breve.",alert_error:"Algo saíu mal. Por favor, téntao de novo.",alert_network:"Erro de rede. Por favor, téntao de novo.",
    back_home:"Volver ao Inicio",cs_page_title:"Mensaxe Enviada | ImationGroup",cs_label:"Mensaxe recibida",cs_title:"Grazas por contactar connosco!",cs_message:"Recibimos a túa mensaxe e poñerémonos en contacto o antes posible. O noso equipo responde habitualmente en 24–48 horas.",cs_detail1_title:"Email de confirmación",cs_detail1_desc:"Recibirás unha confirmación no enderezo de correo que proporcionaches.",cs_detail2_title:"Tempo de resposta",cs_detail2_desc:"O noso equipo responderá nun prazo de 24–48 horas laborables.",cs_detail3_title:"Atención personalizada",cs_detail3_desc:"Un especialista do noso equipo revisará persoalmente a túa consulta.",cs_back:"Volver ao Inicio",cs_rights:"Todos os dereitos reservados.",cs_privacy:"Política de Privacidade",cs_terms:"Termos de Servizo",
    svc_page_title:"Servizos Tecnolóxicos | ImationGroup",svc_label:"Servizos",svc_hero_title:"Solucións Tecnolóxicas que Impulsan o teu Negocio",svc_hero_desc:"Desde unha web profesional ata unha estratexia dixital completa.",svc_web_title:"Deseño Web",svc_web_subtitle:"Páxinas web profesionais que converten visitantes en clientes.",svc_web_f1:"Páxinas corporativas de alto rendemento.",svc_web_f2:"Portfolio para profesionais creativos.",svc_web_f3:"Comercio electrónico con pasarela de pago.",svc_web_f4:"Estrutura SEO, carga rápida e deseño adaptable.",svc_host_title:"Aloxamento Web",svc_host_subtitle:"Hosting fiable en servidores VPS propios — sen custos ocultos.",svc_host_f1:"Servidores VPS privados con recursos dedicados.",svc_host_f2:"SLA do 99,9% con monitorización 24/7.",svc_host_f3:"SSL gratuíto, CDN e protección DDoS incluídos.",svc_host_f4:"Plans escalables segundo crece o teu tráfico.",svc_host_price:"Desde 10€ / mes",svc_app_title:"Desenvolvemento de Apps",svc_app_subtitle:"Aplicacións web e móbiles a medida.",svc_app_f1:"Progressive Web Apps desde calquera navegador.",svc_app_f2:"Apps nativas para iOS e Android.",svc_app_f3:"Ferramentas internas — dashboards e CRMs.",svc_app_f4:"Integracións con APIs e pasarelas de pago.",svc_mkt_title:"Marketing Dixital",svc_mkt_subtitle:"Estratexias baseadas en datos para aumentar visibilidade e vendas.",svc_mkt_f1:"SEO — optimización técnica e contido que posiciona en Google.",svc_mkt_f2:"SEM e Google Ads — campañas que maximizan o ROI.",svc_mkt_f3:"Xestión de redes sociais — contido atractivo.",svc_mkt_f4:"Análise e informes — revisión mensual do rendemento.",svc_de_title:"Enxeñaría de Datos",svc_de_subtitle:"Pipelines robustos e procesos ETL para activos de datos fiables.",svc_de_f1:"Deseño e desenvolvemento de pipelines de extremo a extremo.",svc_de_f2:"Arquitectura de data warehouse e data lake na nube.",svc_de_f3:"Streaming en tempo real con Kafka e Spark.",svc_de_f4:"Calidade do dato, gobernanza e monitorización.",svc_ds_title:"Ciencia de Datos e BI",svc_ds_subtitle:"Do dato en bruto á decisión estratéxica — ML e dashboards executivos.",svc_ds_f1:"Analítica preditiva e modelos de machine learning.",svc_ds_f2:"Dashboards de BI e reporting de autoservizo.",svc_ds_f3:"A/B testing e análise estatística.",svc_ds_f4:"Integración de IA — LLMs e motores de recomendación.",svc_cta:"Solicitar orzamento",cta_title:"Listo para facer crecer o teu negocio?",cta_desc:"Cóntanos o teu proxecto e responderémosche en menos de 24 horas.",cta_btn:"Contacta connosco agora",footer_rights:"Todos os dereitos reservados."
  },
  ca: {
    page_title:"ImationGroup | Enginyeria de Dades i Solucions de Software",
    nav_home:"Inici",nav_about:"Nosaltres",nav_services:"Serveis",nav_technologies:"Tecnologies",nav_projects:"Projectes",nav_contact:"Contacte",
    hero_tagline:"Enginyeria de Dades i Solucions de Software",hero_description:"Transformem dades en informació accionable i construïm solucions de software escalables que impulsen el creixement empresarial.",hero_btn_contact:"Contacta'ns",hero_btn_services:"Els nostres serveis",
    about_label:"Nosaltres",about_title:"Solucions Pioneres Basades en Dades",about_subtitle:"Construint el futur de la tecnologia empresarial a través de la innovació",about_who_title:"Qui som",about_who_p1:"ImationGroup és una empresa tecnològica especialitzada en enginyeria de dades, ciència de dades i solucions de software escalables.",about_who_p2:"El nostre equip combina experiència tècnica profunda amb passió per resoldre reptes empresarials complexos.",
    value_innovation:"Innovació",value_innovation_desc:"Aprofitant tecnologies d'avantguarda per oferir solucions revolucionàries",value_reliability:"Fiabilitat",value_reliability_desc:"Construint sistemes robustos que funcionen de manera consistent",value_partnership:"Col·laboració",value_partnership_desc:"Treballant estretament amb els clients per superar les seves expectatives",value_excellence:"Excel·lència",value_excellence_desc:"Compromesos amb la màxima qualitat en cada projecte",
    stat_projects:"Projectes Lliurats",stat_satisfaction:"Satisfacció del Client",stat_support:"Suport Disponible",stat_experience:"Anys d'Experiència",
    services_label:"Serveis",services_title:"El Que Oferim",services_subtitle:"Solucions tecnològiques integrals adaptades a les necessitats del teu negoci",services_more:"Veure tots els serveis",
    svc_data_eng:"Enginyeria de Dades",svc_data_eng_desc:"Dissenyem i construïm pipelines de dades robustos i processos ETL que gestionen grans volums de dades.",svc_data_sci:"Ciència de Dades",svc_data_sci_desc:"Transformem dades en informació accionable usant anàlisi avançada i algoritmes predictius.",svc_soft_dev:"Desenvolupament de Software",svc_soft_dev_desc:"Construïm solucions de software personalitzades amb arquitectures modernes.",svc_cloud:"Solucions Cloud",svc_cloud_desc:"Migrem i gestionem infraestructura al núvol en AWS, Azure o GCP.",svc_consulting:"Consultoria",svc_consulting_desc:"Consultoria tecnològica estratègica per prendre decisions informades.",svc_bi:"Business Intelligence",svc_bi_desc:"Ajudem els equips a crear capes de reporting i entorns analítics amb dades fiables.",
    tech_label:"Tecnologies",tech_title:"El Nostre Stack Tecnològic",tech_subtitle:"Tecnologies líders que impulsen les nostres solucions",
    projects_label:"Projectes",projects_title:"Solucions Escalables en Acció",projects_subtitle:"Lliurant sistemes d'extrem a extrem que converteixen dades en valor",
    proj_pipelines:"Pipelines de Dades",proj_pipelines_desc:"Pipelines automatitzats per al lliurament fiable a sistemes analítics.",proj_etl:"Sistemes ETL",proj_etl_desc:"Frameworks ETL d'alt rendiment per a integració de dades.",proj_bi:"Business Intelligence",proj_bi_desc:"Dashboards de BI per a la presa de decisions estratègiques en temps real.",proj_custom:"Software Personalitzat",proj_custom_desc:"Software adaptat al teu ecosistema — escalable, segur i cloud-ready.",proj_cloud:"Infraestructura Cloud",proj_cloud_desc:"Arquitectures cloud-native a AWS per a escalabilitat i eficiència.",proj_scalable:"Arquitectures Escalables",proj_scalable_desc:"Disseny d'arquitectura per a sistemes distribuïts i plataformes de dades.",
    contact_label:"Contacte",contact_title:"Posa't en Contacte",contact_subtitle:"Parlem de com ImationGroup pot transformar la teva estratègia de dades",contact_desc:"Estem preparats per col·laborar en el teu proper projecte.",contact_email_label:"Correu electrònic",contact_phone_label:"Telèfon",contact_location_label:"Ubicació",contact_location:"Global — Projectes Remots a Tot el Món",
    form_name:"Nom",form_name_placeholder:"El teu nom",form_email:"Correu electrònic",form_email_placeholder:"tu@exemple.com",form_message:"Missatge",form_message_placeholder:"Com podem ajudar-te?",form_submit:"Enviar Missatge",
    footer_desc:"Enginyeria de dades i solucions de software per elevar el rendiment del teu negoci.",footer_company:"Empresa",footer_support:"Suport",footer_privacy:"Política de Privacitat",footer_terms:"Termes de Servei",footer_follow:"Segueix-nos",footer_copyright:"© 2025 ImationGroup. Tots els drets reservats.",
    alert_success:"Gràcies per contactar-nos! Ens posarem en contacte aviat.",alert_error:"Alguna cosa ha anat malament. Si us plau, torna-ho a intentar.",alert_network:"Error de xarxa. Si us plau, torna-ho a intentar.",
    back_home:"Tornar a l'Inici",cs_page_title:"Missatge Enviat | ImationGroup",cs_label:"Missatge rebut",cs_title:"Gràcies per contactar-nos!",cs_message:"Hem rebut el teu missatge i ens posarem en contacte al més aviat possible. El nostre equip respon habitualment en 24–48 hores.",cs_detail1_title:"Correu de confirmació",cs_detail1_desc:"Rebràs una confirmació a l'adreça de correu que has proporcionat.",cs_detail2_title:"Temps de resposta",cs_detail2_desc:"El nostre equip respondrà en un termini de 24–48 hores laborables.",cs_detail3_title:"Atenció personalitzada",cs_detail3_desc:"Un especialista del nostre equip revisarà personalment la teva consulta.",cs_back:"Tornar a l'Inici",cs_rights:"Tots els drets reservats.",cs_privacy:"Política de Privacitat",cs_terms:"Termes de Servei",
    svc_page_title:"Serveis Tecnològics | ImationGroup",svc_label:"Serveis",svc_hero_title:"Solucions Tecnològiques que Impulsen el teu Negoci",svc_hero_desc:"Des d'una web professional fins a una estratègia digital completa.",svc_web_title:"Disseny Web",svc_web_subtitle:"Pàgines web professionals que converteixen visitants en clients.",svc_web_f1:"Pàgines corporatives d'alt rendiment.",svc_web_f2:"Portfolio per a professionals creatius.",svc_web_f3:"Comerç electrònic amb passarel·la de pagament.",svc_web_f4:"Estructura SEO, càrrega ràpida i disseny adaptable.",svc_host_title:"Allotjament Web",svc_host_subtitle:"Hosting fiable en servidors VPS propis — sense costos ocults.",svc_host_f1:"Servidors VPS privats amb recursos dedicats.",svc_host_f2:"SLA del 99,9% amb monitorització 24/7.",svc_host_f3:"SSL gratuït, CDN i protecció DDoS inclosos.",svc_host_f4:"Plans escalables segons creix el teu tràfic.",svc_host_price:"Des de 10€ / mes",svc_app_title:"Desenvolupament d'Apps",svc_app_subtitle:"Aplicacions web i mòbils a mida.",svc_app_f1:"Progressive Web Apps des de qualsevol navegador.",svc_app_f2:"Apps natives per a iOS i Android.",svc_app_f3:"Eines internes — dashboards i CRMs.",svc_app_f4:"Integracions amb APIs i passarel·les de pagament.",svc_mkt_title:"Màrqueting Digital",svc_mkt_subtitle:"Estratègies basades en dades per augmentar visibilitat i vendes.",svc_mkt_f1:"SEO — optimització tècnica i contingut que posiciona a Google.",svc_mkt_f2:"SEM i Google Ads — campanyes que maximitzen el ROI.",svc_mkt_f3:"Gestió de xarxes socials — contingut atractiu.",svc_mkt_f4:"Anàlisi i informes — revisió mensual del rendiment.",svc_de_title:"Enginyeria de Dades",svc_de_subtitle:"Pipelines robustos i processos ETL per a actius de dades fiables.",svc_de_f1:"Disseny i desenvolupament de pipelines d'extrem a extrem.",svc_de_f2:"Arquitectura de data warehouse i data lake al núvol.",svc_de_f3:"Streaming en temps real amb Kafka i Spark.",svc_de_f4:"Qualitat del dada, governança i monitorització.",svc_ds_title:"Ciència de Dades i BI",svc_ds_subtitle:"De la dada en brut a la decisió estratègica — ML i dashboards executius.",svc_ds_f1:"Analítica predictiva i models de machine learning.",svc_ds_f2:"Dashboards de BI i reporting d'autoservei.",svc_ds_f3:"A/B testing i anàlisi estadística.",svc_ds_f4:"Integració d'IA — LLMs i motors de recomanació.",svc_cta:"Sol·licitar pressupost",cta_title:"Preparat per fer créixer el teu negoci?",cta_desc:"Explica'ns el teu projecte i et respondrem en menys de 24 hores.",cta_btn:"Contacta'ns ara",footer_rights:"Tots els drets reservats."
  },
  pt: {
    page_title:"ImationGroup | Engenharia de Dados e Soluções de Software",
    nav_home:"Início",nav_about:"Sobre Nós",nav_services:"Serviços",nav_technologies:"Tecnologias",nav_projects:"Projetos",nav_contact:"Contato",
    hero_tagline:"Engenharia de Dados e Soluções de Software",hero_description:"Transformamos dados em insights acionáveis e construímos soluções de software escaláveis que impulsionam o crescimento empresarial.",hero_btn_contact:"Entre em Contacto",hero_btn_services:"Os Nossos Serviços",
    about_label:"Sobre Nós",about_title:"Soluções Pioneiras Baseadas em Dados",about_subtitle:"Construindo o futuro da tecnologia empresarial através da inovação e expertise",about_who_title:"Quem Somos",about_who_p1:"ImationGroup é uma empresa tecnológica especializada em engenharia de dados, ciência de dados e soluções de software escaláveis.",about_who_p2:"A nossa equipa combina profunda experiência técnica com paixão por resolver desafios empresariais complexos.",
    value_innovation:"Inovação",value_innovation_desc:"Aproveitando tecnologias de ponta para entregar soluções revolucionárias",value_reliability:"Fiabilidade",value_reliability_desc:"Construindo sistemas robustos que funcionam de forma consistente",value_partnership:"Parceria",value_partnership_desc:"Trabalhando em estreita colaboração com os clientes para superar as suas expectativas",value_excellence:"Excelência",value_excellence_desc:"Comprometidos com a máxima qualidade em cada projeto",
    stat_projects:"Projetos Entregues",stat_satisfaction:"Satisfação do Cliente",stat_support:"Suporte Disponível",stat_experience:"Anos de Experiência",
    services_label:"Serviços",services_title:"O Que Oferecemos",services_subtitle:"Soluções tecnológicas abrangentes adaptadas às necessidades do seu negócio",services_more:"Ver todos os serviços",
    svc_data_eng:"Engenharia de Dados",svc_data_eng_desc:"Desenhamos e construímos pipelines de dados robustos e processos ETL que gerem grandes volumes de dados.",svc_data_sci:"Ciência de Dados",svc_data_sci_desc:"Transformamos dados em insights acionáveis usando análise avançada e algoritmos preditivos.",svc_soft_dev:"Desenvolvimento de Software",svc_soft_dev_desc:"Construímos soluções de software personalizadas com arquiteturas modernas.",svc_cloud:"Soluções Cloud",svc_cloud_desc:"Migramos e gerimos infraestrutura na nuvem em AWS, Azure ou GCP.",svc_consulting:"Consultoria",svc_consulting_desc:"Consultoria tecnológica estratégica para tomar decisões informadas.",svc_bi:"Business Intelligence",svc_bi_desc:"Ajudamos equipas a criar camadas de reporting e ambientes analíticos com dados fiáveis.",
    tech_label:"Tecnologias",tech_title:"O Nosso Stack Tecnológico",tech_subtitle:"Tecnologias líderes que impulsionam as nossas soluções",
    projects_label:"Projetos",projects_title:"Soluções Escaláveis em Ação",projects_subtitle:"Entregando sistemas de ponta a ponta que convertem dados em valor",
    proj_pipelines:"Pipelines de Dados",proj_pipelines_desc:"Pipelines automatizados para entrega fiável a sistemas analíticos.",proj_etl:"Sistemas ETL",proj_etl_desc:"Frameworks ETL de alto desempenho para integração de dados.",proj_bi:"Business Intelligence",proj_bi_desc:"Dashboards de BI para tomada de decisões estratégicas em tempo real.",proj_custom:"Software Personalizado",proj_custom_desc:"Software adaptado ao seu ecossistema — escalável, seguro e cloud-ready.",proj_cloud:"Infraestrutura Cloud",proj_cloud_desc:"Arquiteturas cloud-native em AWS para escalabilidade e eficiência.",proj_scalable:"Arquiteturas Escaláveis",proj_scalable_desc:"Design de arquitetura para sistemas distribuídos e plataformas de dados.",
    contact_label:"Contato",contact_title:"Entre em Contacto",contact_subtitle:"Vamos discutir como o ImationGroup pode transformar a sua estratégia de dados",contact_desc:"Estamos prontos para colaborar no seu próximo projeto.",contact_email_label:"E-mail",contact_phone_label:"Telefone",contact_location_label:"Localização",contact_location:"Global — Projetos Remotos em Todo o Mundo",
    form_name:"Nome",form_name_placeholder:"O seu nome",form_email:"E-mail",form_email_placeholder:"voce@exemplo.com",form_message:"Mensagem",form_message_placeholder:"Como podemos ajudar?",form_submit:"Enviar Mensagem",
    footer_desc:"Engenharia de dados e soluções de software para elevar o desempenho do seu negócio.",footer_company:"Empresa",footer_support:"Suporte",footer_privacy:"Política de Privacidade",footer_terms:"Termos de Serviço",footer_follow:"Siga-nos",footer_copyright:"© 2025 ImationGroup. Todos os direitos reservados.",
    alert_success:"Obrigado por entrar em contacto! Responderemos em breve.",alert_error:"Algo correu mal. Por favor, tente novamente.",alert_network:"Erro de rede. Por favor, tente novamente.",
    back_home:"Voltar ao Início",cs_page_title:"Mensagem Enviada | ImationGroup",cs_label:"Mensagem recebida",cs_title:"Obrigado por entrar em contacto!",cs_message:"Recebemos a sua mensagem e responderemos o mais brevemente possível. A nossa equipa responde habitualmente em 24–48 horas.",cs_detail1_title:"E-mail de confirmação",cs_detail1_desc:"Receberá uma confirmação no endereço de e-mail que forneceu.",cs_detail2_title:"Tempo de resposta",cs_detail2_desc:"A nossa equipa responderá num prazo de 24–48 horas úteis.",cs_detail3_title:"Atenção personalizada",cs_detail3_desc:"Um especialista da nossa equipa analisará pessoalmente a sua consulta.",cs_back:"Voltar ao Início",cs_rights:"Todos os direitos reservados.",cs_privacy:"Política de Privacidade",cs_terms:"Termos de Serviço",
    svc_page_title:"Serviços Tecnológicos | ImationGroup",svc_label:"Serviços",svc_hero_title:"Soluções Tecnológicas que Impulsionam o seu Negócio",svc_hero_desc:"Desde um website profissional até uma estratégia digital completa.",svc_web_title:"Design Web",svc_web_subtitle:"Websites profissionais que convertem visitantes em clientes.",svc_web_f1:"Websites corporativos de alto desempenho.",svc_web_f2:"Portfolio para profissionais criativos.",svc_web_f3:"E-commerce com gateway de pagamento.",svc_web_f4:"Estrutura SEO, carregamento rápido e design responsivo.",svc_host_title:"Alojamento Web",svc_host_subtitle:"Hosting fiável em servidores VPS próprios — sem custos ocultos.",svc_host_f1:"Servidores VPS privados com recursos dedicados.",svc_host_f2:"SLA de 99,9% com monitorização 24/7.",svc_host_f3:"SSL gratuito, CDN e proteção DDoS incluídos.",svc_host_f4:"Planos escaláveis conforme o tráfego cresce.",svc_host_price:"A partir de 10€ / mês",svc_app_title:"Desenvolvimento de Apps",svc_app_subtitle:"Aplicações web e móveis personalizadas.",svc_app_f1:"Progressive Web Apps a partir de qualquer navegador.",svc_app_f2:"Apps nativas para iOS e Android.",svc_app_f3:"Ferramentas internas — dashboards e CRMs.",svc_app_f4:"Integrações com APIs e gateways de pagamento.",svc_mkt_title:"Marketing Digital",svc_mkt_subtitle:"Estratégias baseadas em dados para aumentar visibilidade e vendas.",svc_mkt_f1:"SEO — otimização técnica e conteúdo que rankeia no Google.",svc_mkt_f2:"SEM e Google Ads — campanhas que maximizam o ROI.",svc_mkt_f3:"Gestão de redes sociais — conteúdo envolvente.",svc_mkt_f4:"Análise e relatórios — revisão mensal do desempenho.",svc_de_title:"Engenharia de Dados",svc_de_subtitle:"Pipelines robustos e processos ETL para ativos de dados fiáveis.",svc_de_f1:"Design e desenvolvimento de pipelines de ponta a ponta.",svc_de_f2:"Arquitetura de data warehouse e data lake na nuvem.",svc_de_f3:"Streaming em tempo real com Kafka e Spark.",svc_de_f4:"Qualidade de dados, governança e monitorização.",svc_ds_title:"Ciência de Dados e BI",svc_ds_subtitle:"Do dado bruto à decisão estratégica — ML e dashboards executivos.",svc_ds_f1:"Análise preditiva e modelos de machine learning.",svc_ds_f2:"Dashboards de BI e reporting de self-service.",svc_ds_f3:"A/B testing e análise estatística.",svc_ds_f4:"Integração de IA — LLMs e motores de recomendação.",svc_cta:"Solicitar Orçamento",cta_title:"Pronto para fazer crescer o seu negócio?",cta_desc:"Conte-nos o seu projeto e responderemos em menos de 24 horas.",cta_btn:"Contacte-nos agora",footer_rights:"Todos os direitos reservados."
  },
  eu: {
    page_title:"ImationGroup | Datuen Ingeniaritza eta Software Soluzioak",
    nav_home:"Hasiera",nav_about:"Gu",nav_services:"Zerbitzuak",nav_technologies:"Teknologiak",nav_projects:"Proiektuak",nav_contact:"Kontaktua",
    hero_tagline:"Datuen Ingeniaritza eta Software Soluzioak",hero_description:"Datuak ekintza-prest informazio bihurtzen ditugu eta negozioen hazkundea bultzatzen duten software soluzio eskaladoreak eraikitzen ditugu.",hero_btn_contact:"Jarri Harremanetan",hero_btn_services:"Gure Zerbitzuak",
    about_label:"Gu",about_title:"Datuetan Oinarritutako Aitzindari Soluzioak",about_subtitle:"Etorkizuneko enpresa-teknologia eraikitzen, berrikuntza eta esperientziaren bidez",about_who_title:"Nor Gara",about_who_p1:"ImationGroup datuen ingeniaritzan, datu zientzian eta software soluzio eskaladoretan espezializatutako teknologia enpresa bat da.",about_who_p2:"Gure taldeak esperientzia tekniko sakona eta erronka konplexuak ebazteko grinak bat egiten ditu.",
    value_innovation:"Berrikuntza",value_innovation_desc:"Teknologia puntakoena baliatuz soluzio iraultzaileak emateko",value_reliability:"Fidagarritasuna",value_reliability_desc:"Sistema sendoak eraikiz edozein baldintzatan ondo funtzionatzen dutenak",value_partnership:"Lankidetza",value_partnership_desc:"Bezeroekin estuki lanean haien itxaropenak gainditzeko",value_excellence:"Bikaintasuna",value_excellence_desc:"Proiektu bakoitzean kalitate gorena emateari konprometituta",
    stat_projects:"Emandako Proiektuak",stat_satisfaction:"Bezero Asebetetzea",stat_support:"Laguntza Eskuragarri",stat_experience:"Esperientzia Urteak",
    services_label:"Zerbitzuak",services_title:"Eskaintzen Duguna",services_subtitle:"Zure negozioaren beharretara egokitutako soluzio teknologiko integralak",services_more:"Zerbitzu guztiak ikusi",
    svc_data_eng:"Datuen Ingeniaritza",svc_data_eng_desc:"Datu-pipeline sendoak eta ETL prozesuak diseinatu eta eraikitzen ditugu datu bolumen handiak kudeatzeko.",svc_data_sci:"Datu Zientzia",svc_data_sci_desc:"Datuak ekintza-prest informazio bihurtzen ditugu analisi aurreratua eta algoritmo prediktiboak erabiliz.",svc_soft_dev:"Software Garapena",svc_soft_dev_desc:"Arkitektura modernoekin software soluzio pertsonalizatuak eraikitzen ditugu.",svc_cloud:"Cloud Soluzioak",svc_cloud_desc:"AWS, Azure edo GCPn azpiegitura kudeatzen dugu segurtasunarekin.",svc_consulting:"Kontsultoretza",svc_consulting_desc:"Kontsultoretza teknologiko estrategikoa erabaki informatuak hartzeko.",svc_bi:"Business Intelligence",svc_bi_desc:"Taldeei reporting geruzak eta ingurune analitikoak sortzen laguntzen diegu.",
    tech_label:"Teknologiak",tech_title:"Gure Stack Teknologikoa",tech_subtitle:"Gure soluzioak bultzatzen dituzten teknologia liderrak",
    projects_label:"Proiektuak",projects_title:"Soluzio Eskaladoreak Ekintzan",projects_subtitle:"Datuak balioa bihurtzen dituzten mutur-muturko sistemak emanez",
    proj_pipelines:"Datu Pipeline-ak",proj_pipelines_desc:"Sistema analitikoetarako entrega fidagarria bermatzen duten pipeline automatizatuak.",proj_etl:"ETL Sistemak",proj_etl_desc:"Plataformen arteko datu-integrazioa ahalbidetzen duten ETL framework errendimendu altukoak.",proj_bi:"Business Intelligence",proj_bi_desc:"Denbora errealean erabaki estrategikoak hartzeko BI dashboard-ak.",proj_custom:"Software Pertsonalizatua",proj_custom_desc:"Zure ekosistemara egokitutako software-a — eskaladorea, segurua eta cloud-ready.",proj_cloud:"Cloud Azpiegitura",proj_cloud_desc:"AWSn cloud-native arkitekturak eskalagarritasun eta eraginkortasunerako.",proj_scalable:"Arkitektura Eskaladoreak",proj_scalable_desc:"Sistema banatuetarako eta datu plataformetarako arkitektura diseinua.",
    contact_label:"Kontaktua",contact_title:"Jarri Harremanetan",contact_subtitle:"Hitz egin dezagun ImationGroupek zure datu eta teknologia estrategia nola eraldatu dezakeen",contact_desc:"Prest gaude zure hurrengo proiektuan lankidetzan aritzeko.",contact_email_label:"Posta elektronikoa",contact_phone_label:"Telefonoa",contact_location_label:"Kokapena",contact_location:"Globala — Urruneko Proiektuak Mundu Osoan",
    form_name:"Izena",form_name_placeholder:"Zure izena",form_email:"Posta elektronikoa",form_email_placeholder:"zu@adibidea.com",form_message:"Mezua",form_message_placeholder:"Nola lagun diezazukegu?",form_submit:"Mezua Bidali",
    footer_desc:"Datuen ingeniaritza eta software soluzioak zure negozioaren errendimendua hobetzeko.",footer_company:"Enpresa",footer_support:"Laguntza",footer_privacy:"Pribatutasun Politika",footer_terms:"Zerbitzu Baldintzak",footer_follow:"Jarraitu",footer_copyright:"© 2025 ImationGroup. Eskubide guztiak erreserbatuak.",
    alert_success:"Eskerrik asko harremanetan jarri zarelako! Laster kontaktatuko dizugu.",alert_error:"Zerbait gaizki joan da. Mesedez, saiatu berriro.",alert_network:"Sareko errorea. Mesedez, saiatu berriro.",
    back_home:"Hasierara Itzuli",cs_page_title:"Mezua Bidalita | ImationGroup",cs_label:"Mezua jasota",cs_title:"Eskerrik asko harremanetan jarri zarelako!",cs_message:"Zure mezua jaso dugu eta ahal bezain laster harremanetan jarriko gara. Gure taldeak normalean 24–48 ordutan erantzuten du.",cs_detail1_title:"Baieztapen emaila",cs_detail1_desc:"Eman duzun helbide elektronikoan baieztatze bat jasoko duzu.",cs_detail2_title:"Erantzun denbora",cs_detail2_desc:"Gure taldeak 24–48 lan-ordutan erantzungo du.",cs_detail3_title:"Arreta pertsonalizatua",cs_detail3_desc:"Gure taldearen espezialista batek zure kontsulta pertsonalki aztertuko du.",cs_back:"Hasierara Itzuli",cs_rights:"Eskubide guztiak erreserbatuak.",cs_privacy:"Pribatutasun Politika",cs_terms:"Zerbitzu Baldintzak",
    svc_page_title:"Zerbitzu Teknologikoak | ImationGroup",svc_label:"Zerbitzuak",svc_hero_title:"Zure Negozioa Bultzatzen Duten Soluzio Teknologikoak",svc_hero_desc:"Web profesional batetik estrategia digital osora arte.",svc_web_title:"Web Diseinua",svc_web_subtitle:"Bisitariak bezero bihurtzen dituzten web profesionalak.",svc_web_f1:"Errendimendu altuko web korporatiboak.",svc_web_f2:"Portfolio profesional sortzaileentzat.",svc_web_f3:"Merkataritza elektronikoa ordainketa pasarelarekin.",svc_web_f4:"SEO egitura, karga azkarra eta diseinu moldagarria.",svc_host_title:"Web Ostatatzea",svc_host_subtitle:"Gure VPS zerbitzarietan fidagarri eta segurua — kostu ezkuturik gabe.",svc_host_f1:"Baliabide dedikatuekin VPS zerbitzari pribatuak.",svc_host_f2:"%99,9ko SLA 24/7 monitorizazioarekin.",svc_host_f3:"SSL doakoa, CDN eta DDoS babesa barne.",svc_host_f4:"Eskalagarri planak trafikoa hazi ahala.",svc_host_price:"10€tik / hilean",svc_app_title:"Aplikazioen Garapena",svc_app_subtitle:"Neurri egindako web eta mugikor aplikazioak.",svc_app_f1:"Progressive Web Apps edozein nabigatzailetik.",svc_app_f2:"iOS eta Android-erako aplikazio nativoak.",svc_app_f3:"Barne tresnak — dashboard-ak eta CRMak.",svc_app_f4:"API integrazio — ordainketa pasarela eta ERPak.",svc_mkt_title:"Marketing Digitala",svc_mkt_subtitle:"Ikusgaitasuna eta salmentak handitzen dituzten estrategiak.",svc_mkt_f1:"SEO — Google-n posizionatzen duen optimizazioa.",svc_mkt_f2:"SEM eta Google Ads — ROI maximizatzen duten kanpainak.",svc_mkt_f3:"Sare sozialen kudeaketa — eduki erakargarria.",svc_mkt_f4:"Analisi eta txostenak — hileko errendimendua.",svc_de_title:"Datuen Ingeniaritza",svc_de_subtitle:"Analisi-prest datu aktiboak egiteko pipeline sendoak.",svc_de_f1:"Mutur-muturko pipeline diseinu eta garapena.",svc_de_f2:"Data warehouse eta data lake arkitektura hodeiean.",svc_de_f3:"Denbora errealeko streaming Kafka eta Spark-ekin.",svc_de_f4:"Datu kalitatea, gobernantza eta monitorizazioa.",svc_ds_title:"Datu Zientzia eta BI",svc_ds_subtitle:"Datu gordinetatik erabaki estrategikoetara.",svc_ds_f1:"Analitika prediktiboa eta machine learning ereduak.",svc_ds_f2:"BI dashboard-ak eta self-service reporting-a.",svc_ds_f3:"A/B testing eta analisi estatistikoa.",svc_ds_f4:"AI integrazioa — LLMak eta gomendio motoreak.",svc_cta:"Aurrekontua Eskatu",cta_title:"Prest zure negozioa hazteko?",cta_desc:"Kontaiguzu zure proiektua eta 24 ordutan erantzungo dizugu.",cta_btn:"Jarri harremanetan orain",footer_rights:"Eskubide guztiak erreserbatuak."
  },
  et: {
    page_title:"ImationGroup | Andmete Inseneeria ja Tarkvaralahendused",
    nav_home:"Avaleht",nav_about:"Meist",nav_services:"Teenused",nav_technologies:"Tehnoloogiad",nav_projects:"Projektid",nav_contact:"Kontakt",
    hero_tagline:"Andmete Inseneeria ja Tarkvaralahendused",hero_description:"Me muudame andmed rakendatavateks teadmisteks ja ehitame skaleeritavaid tarkvaralahendusi, mis soodustavad ärikasvu.",hero_btn_contact:"Võta Ühendust",hero_btn_services:"Meie Teenused",
    about_label:"Meist",about_title:"Pioneersed Andmepõhised Lahendused",about_subtitle:"Ettevõtluse tuleviku ehitamine innovatsiooni ja ekspertiisi kaudu",about_who_title:"Kes Me Oleme",about_who_p1:"ImationGroup on edasivaatav tehnoloogiaettevõte, mis on spetsialiseerunud andmete inseneeriale, andmeteadusele ja skaleeritavatele tarkvaralahendustele.",about_who_p2:"Meie meeskond ühendab sügava tehnilise ekspertiisi kire lahendada keerulisi äriprobleeme.",
    value_innovation:"Innovatsioon",value_innovation_desc:"Tipptasemel tehnoloogiate kasutamine läbimurdelahenduste pakkumiseks",value_reliability:"Usaldusväärsus",value_reliability_desc:"Vastupidavate süsteemide ehitamine, mis töötavad järjepidevalt igas olukorras",value_partnership:"Partnerlus",value_partnership_desc:"Tihe koostöö klientidega nende ootuste mõistmiseks ja ületamiseks",value_excellence:"Tipptase",value_excellence_desc:"Pühendunud kõrgeima kvaliteedi saavutamisele igas projektis",
    stat_projects:"Teostatud Projekte",stat_satisfaction:"Klientide Rahulolu",stat_support:"Tugi Saadaval",stat_experience:"Kogemuse Aastat",
    services_label:"Teenused",services_title:"Mida Me Pakume",services_subtitle:"Teie ärile kohandatud terviklikud tehnoloogilahendused",services_more:"Vaata kõiki teenuseid",
    svc_data_eng:"Andmete Inseneeria",svc_data_eng_desc:"Disainime ja ehitame robustseid andmetorustikke ja ETL-protsesse, mis käsitlevad suuri andmemahtusid.",svc_data_sci:"Andmeteadus",svc_data_sci_desc:"Muudame toorandmed rakendatavateks teadmisteks täiustatud analüütika ja ennustavate algoritmide abil.",svc_soft_dev:"Tarkvaraarendus",svc_soft_dev_desc:"Ehitame kohandatud tarkvaralahendusi kaasaegsete arhitektuuridega, mis kasvavad koos teie äriga.",svc_cloud:"Pilvlahendused",svc_cloud_desc:"Migreerume, optimiseerime ja haldame pilveinfrastruktuuri AWS-is, Azure'is või GCP-s.",svc_consulting:"Konsultatsioon",svc_consulting_desc:"Strateegiline tehnoloogiakonsultatsioon teadlike otsuste tegemiseks.",svc_bi:"Business Intelligence",svc_bi_desc:"Aitame meeskondadel luua aruandluskihte ja analüütilisi keskkondi usaldusväärsete andmetega.",
    tech_label:"Tehnoloogiad",tech_title:"Meie Tehnoloogiavirn",tech_subtitle:"Juhtivad tehnoloogiad, mis toitavad meie lahendusi",
    projects_label:"Projektid",projects_title:"Skaleeritavad Lahendused Tegevuses",projects_subtitle:"Terviklike süsteemide tarnimmine, mis muudavad andmed väärtuseks",
    proj_pipelines:"Andmetorustikud",proj_pipelines_desc:"Automatiseeritud andmetorustikud analüütikasüsteemidele usaldusväärseks tarnimiseks.",proj_etl:"ETL Süsteemid",proj_etl_desc:"Suure jõudlusega ETL-raamistikud sujuvaks andmete integreerimiseks.",proj_bi:"Business Intelligence",proj_bi_desc:"BI ja analüütika armatuurlauad strateegiliseks otsuste tegemiseks reaalajas.",proj_custom:"Kohandatud Tarkvara",proj_custom_desc:"Teie ökosüsteemile kohandatud tarkvara — skaleeritav, turvaline ja pilvevalmis.",proj_cloud:"Pilveinfrastruktuur",proj_cloud_desc:"Cloud-native arhitektuurid AWS-is skaleeritavuse ja tõhususe jaoks.",proj_scalable:"Skaleeritavad Arhitektuurid",proj_scalable_desc:"Arhitektuuri disain hajutatud süsteemide ja andmeplatvormide jaoks.",
    contact_label:"Kontakt",contact_title:"Võta Ühendust",contact_subtitle:"Arutame, kuidas ImationGroup saab teie andme- ja tehnoloogiastrateegia muuta",contact_desc:"Oleme valmis koostööks teie järgmises projektis.",contact_email_label:"E-post",contact_phone_label:"Telefon",contact_location_label:"Asukoht",contact_location:"Globaalne — Kaugtöö Projektid Üle Maailma",
    form_name:"Nimi",form_name_placeholder:"Teie nimi",form_email:"E-post",form_email_placeholder:"teie@naite.ee",form_message:"Sõnum",form_message_placeholder:"Kuidas saame aidata?",form_submit:"Saada Sõnum",
    footer_desc:"Andmete inseneeria ja tarkvaralahendused teie äri tulemuslikkuse tõstmiseks.",footer_company:"Ettevõte",footer_support:"Tugi",footer_privacy:"Privaatsuspoliitika",footer_terms:"Teenusetingimused",footer_follow:"Jälgi",footer_copyright:"© 2025 ImationGroup. Kõik õigused kaitstud.",
    alert_success:"Täname, et võtsite ühendust! Võtame teiega peagi ühendust.",alert_error:"Midagi läks valesti. Palun proovige uuesti.",alert_network:"Võrgu viga. Palun proovige uuesti.",
    back_home:"Tagasi Avalehele",cs_page_title:"Sõnum Saadetud | ImationGroup",cs_label:"Sõnum vastu võetud",cs_title:"Täname, et võtsite ühendust!",cs_message:"Oleme teie sõnumi kätte saanud ja võtame teiega esimesel võimalusel ühendust. Meie meeskond vastab tavaliselt 24–48 tunni jooksul.",cs_detail1_title:"Kinnituse e-kiri",cs_detail1_desc:"Saate kinnituse teie esitatud e-posti aadressile.",cs_detail2_title:"Vastuse aeg",cs_detail2_desc:"Meie meeskond vastab 24–48 tööstunni jooksul.",cs_detail3_title:"Isiklik tähelepanu",cs_detail3_desc:"Meie meeskonna spetsialist vaatab teie päringu isiklikult läbi.",cs_back:"Tagasi Avalehele",cs_rights:"Kõik õigused kaitstud.",cs_privacy:"Privaatsuspoliitika",cs_terms:"Teenusetingimused",
    svc_page_title:"Tehnoloogiateenused | ImationGroup",svc_label:"Teenused",svc_hero_title:"Tehnoloogilahendused, mis Toetavad Teie Ärikasvu",svc_hero_desc:"Professionaalsest veebisaidist täieliku digitaalstrateegiania.",svc_web_title:"Veebidisain",svc_web_subtitle:"Professionaalsed veebisaidid, mis muudavad külastajad klientideks.",svc_web_f1:"Korporatiivsed veebisaidid kõrge jõudlusega.",svc_web_f2:"Portfolio loovprofessionaalidele.",svc_web_f3:"E-kaubandus makseväravaga.",svc_web_f4:"SEO struktuur, kiire laadimine ja reageeriv disain.",svc_host_title:"Veebimajutus",svc_host_subtitle:"Usaldusväärne majutus meie enda VPS-serverites — ilma varjatud tasudeta.",svc_host_f1:"Privaatsed VPS-serverid pühendatud ressurssidega.",svc_host_f2:"99,9% SLA 24/7 jälgimisega.",svc_host_f3:"Tasuta SSL, CDN ja DDoS kaitse kaasas.",svc_host_f4:"Skaleeritavad plaanid liikluse kasvades.",svc_host_price:"Alates 10€ / kuus",svc_app_title:"Rakenduste Arendus",svc_app_subtitle:"Kohandatud veebi- ja mobiilirakendused.",svc_app_f1:"Progressive Web Apps igast brauserist.",svc_app_f2:"Natiivsed rakendused iOS ja Androidile.",svc_app_f3:"Sisemised tööriistad — armatuurlauad ja CRM-id.",svc_app_f4:"API integratsioonid — makseväravad ja ERP-d.",svc_mkt_title:"Digiturunudus",svc_mkt_subtitle:"Andmepõhised strateegiad nähtavuse suurendamiseks ja müügi kasvatamiseks.",svc_mkt_f1:"SEO — tehniline optimeerimine ja Google'is eespool olev sisu.",svc_mkt_f2:"SEM ja Google Ads — ROI maksimeerivad kampaaniad.",svc_mkt_f3:"Sotsiaalmeedia haldus — kaasahaarav sisu.",svc_mkt_f4:"Analüütika ja aruanded — igakuine ülevaade.",svc_de_title:"Andmete Inseneeria",svc_de_subtitle:"Robustsed torustikud ja ETL protsessid usaldusväärsete andmevarade jaoks.",svc_de_f1:"Täielikud andmetorustiku disain ja arendus.",svc_de_f2:"Data warehouse ja data lake arhitektuur pilves.",svc_de_f3:"Reaalajas voogedastus Kafka ja Sparkiga.",svc_de_f4:"Andmekvaliteet, valitsemine ja jälgimine.",svc_ds_title:"Andmeteadus ja BI",svc_ds_subtitle:"Toorandmetest strateegiliste otsusteni — ML ja juhtimisarmatuurlauad.",svc_ds_f1:"Ennustav analüütika ja masinõppe mudelid.",svc_ds_f2:"BI armatuurlauad ja iseteeninduse aruandlus.",svc_ds_f3:"A/B testimine ja statistiline analüüs.",svc_ds_f4:"AI integratsioon — LLM-id ja soovitusmootorid.",svc_cta:"Küsi Pakkumist",cta_title:"Valmis oma äri kasvatama?",cta_desc:"Rääkige meile oma projektist ja vastame 24 tunni jooksul kohandatud ettepanekuga.",cta_btn:"Võta ühendust kohe",footer_rights:"Kõik õigused kaitstud."
  }
};

// Language metadata with flag emojis (from Unicode — works in all modern browsers)
const LANG_META = {
  en: { label: "English",  flag: "🇬🇧" },
  es: { label: "Español",  flag: "🇪🇸" },
  gl: { label: "Galego",   flag: "🏴" },
  ca: { label: "Català",   flag: "🏴" },
  pt: { label: "Português",flag: "🇵🇹" },
  eu: { label: "Euskera",  flag: "🏴" },
  et: { label: "Eesti",    flag: "🇪🇪" }
};

// Language detection — respects browser locale
function detectLanguage() {
  const saved = localStorage.getItem('ig_lang');
  if (saved && TRANSLATIONS[saved]) return saved;
  const langs = navigator.languages || [navigator.language || 'en'];
  for (const l of langs) {
    const code = l.toLowerCase().split('-')[0];
    if (TRANSLATIONS[code]) return code;
    // region-based fallback
    if (l.toLowerCase().startsWith('gl')) return 'gl';
    if (l.toLowerCase().startsWith('ca')) return 'ca';
    if (l.toLowerCase().startsWith('eu')) return 'eu';
    if (l.toLowerCase().startsWith('pt')) return 'pt';
    if (l.toLowerCase().startsWith('et')) return 'et';
  }
  return 'en';
}

function setLanguage(lang) {
  if (!TRANSLATIONS[lang]) return;
  localStorage.setItem('ig_lang', lang);
  document.documentElement.lang = lang;
  const t = TRANSLATIONS[lang];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (!t[key]) return;
    if (el.tagName === 'TITLE') document.title = t[key];
    else el.textContent = t[key];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (t[key]) el.placeholder = t[key];
  });
  // Update switcher UI
  document.querySelectorAll('.lang-option[data-lang]').forEach(opt => {
    opt.classList.toggle('active', opt.getAttribute('data-lang') === lang);
  });
  document.querySelectorAll('#currentLangLabel').forEach(el => {
    el.textContent = lang.toUpperCase();
  });
}

function getCurrentLang() {
  return localStorage.getItem('ig_lang') || detectLanguage();
}

if (typeof module !== 'undefined') module.exports = { TRANSLATIONS, LANG_META, detectLanguage, setLanguage, getCurrentLang };
