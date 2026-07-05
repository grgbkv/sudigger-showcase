// Data for the showcase site. REAL_SAMPLE = 21 real 5-star targets
// (trimmed columns). SYNTH = synthetic rows showing the full schema.
const REAL_SAMPLE = [
 {
  "company_name": "Better Stack",
  "country": "CZ",
  "score_total": "5",
  "sector": "Internet, Software, Saas, Tech",
  "one_liner": "Better Stack provides observability and incident management tools for monitoring systems, logs, and uptime.",
  "funding_stage": "Series B",
  "website": "betterstack.com"
 },
 {
  "company_name": "Runecast",
  "country": "CZ",
  "score_total": "5",
  "sector": "Cybersecurity",
  "one_liner": "Software that helps enterprises detect and remediate configuration and security risks in IT environments.",
  "funding_stage": "Seed",
  "website": "runecast.com"
 },
 {
  "company_name": "Veriff",
  "country": "EE",
  "score_total": "5",
  "sector": "Other",
  "one_liner": "A global identity verification platform for remote onboarding and fraud prevention.",
  "funding_stage": "Series C+",
  "website": "https://veriff.com"
 },
 {
  "company_name": "BOTGUARD",
  "country": "EE",
  "score_total": "5",
  "sector": "Cybersecurity",
  "one_liner": "Botguard is a cybersecurity company that protects websites and online services from bot traffic and automated abuse.",
  "funding_stage": "Series C+",
  "website": "botguard.net"
 },
 {
  "company_name": "SEON",
  "country": "HU",
  "score_total": "5",
  "sector": "Cybersecurity",
  "one_liner": "SEON provides real-time fraud detection and risk intelligence software for fintechs, online merchants, and digital platforms.",
  "funding_stage": "Series C+",
  "website": "seon.io"
 },
 {
  "company_name": "Semeris",
  "country": "HU",
  "score_total": "5",
  "sector": "Legaltech",
  "one_liner": "Semeris uses AI to analyze legal and financial documents, helping financial institutions review contracts and extract structured legal insights.",
  "funding_stage": "Series A",
  "website": "https://www.semeris.com"
 },
 {
  "company_name": "Turing College",
  "country": "LT",
  "score_total": "5",
  "sector": "Edtech",
  "one_liner": "Online education platform providing AI, data science and digital-skills upskilling and reskilling programs.",
  "funding_stage": "Seed",
  "website": "https://www.turingcollege.com"
 },
 {
  "company_name": "Ligence",
  "country": "LT",
  "score_total": "5",
  "sector": "Healthtech",
  "one_liner": "Develops AI software for automated cardiac ultrasound and echocardiography analysis and reporting.",
  "funding_stage": "Series A",
  "website": "https://ligence.io"
 },
 {
  "company_name": "Corebook.io",
  "country": "LV",
  "score_total": "5",
  "sector": "SaaS",
  "one_liner": "Corebook.io provides a SaaS platform for building and managing brand guidelines and brand assets.",
  "funding_stage": "Seed",
  "website": "https://corebook.io"
 },
 {
  "company_name": "printful",
  "country": "LV",
  "score_total": "5",
  "sector": "Ecommerce",
  "one_liner": "Printful is a print-on-demand and fulfillment platform that helps businesses create, store, and ship custom merchandise.",
  "funding_stage": "Series C+",
  "website": "https://www.printful.com"
 },
 {
  "company_name": "Visely",
  "country": "MD",
  "score_total": "5",
  "sector": "Ecommerce",
  "one_liner": "Visely provides personalized product recommendations and visual search tools for ecommerce merchants.",
  "funding_stage": "Bootstrapped",
  "website": "visely.io"
 },
 {
  "company_name": "Personizely",
  "country": "MD",
  "score_total": "5",
  "sector": "SaaS",
  "one_liner": "Personizely offers on-site personalization, popups, forms and conversion-optimization tools for ecommerce websites.",
  "funding_stage": "Bootstrapped",
  "website": "https://www.personizely.net"
 },
 {
  "company_name": "Infermedica",
  "country": "PL",
  "score_total": "5",
  "sector": "Healthtech",
  "one_liner": "Infermedica builds AI-driven symptom checking and patient triage tools for healthcare providers, insurers, and digital health companies.",
  "funding_stage": "Series B",
  "website": "https://infermedica.com"
 },
 {
  "company_name": "ZEN.COM",
  "country": "PL",
  "score_total": "5",
  "sector": "Fintech",
  "one_liner": "ZEN.COM offers digital payments, multi-currency accounts, cards, and shopping protection services for consumers and merchants.",
  "funding_stage": "Series A",
  "website": "https://www.zen.com"
 },
 {
  "company_name": "Videowise",
  "country": "RO",
  "score_total": "5",
  "sector": "SaaS",
  "one_liner": "Provides a shoppable video platform that helps e-commerce brands add, manage and measure product videos on their online stores.",
  "funding_stage": "Series A",
  "website": "https://videowise.com"
 },
 {
  "company_name": "Sessions",
  "country": "RO",
  "score_total": "5",
  "sector": "SaaS",
  "one_liner": "Sessions is an all-in-one customer-meeting platform combining video meetings, scheduling, agendas, collaboration, and AI notes.",
  "funding_stage": "Series A",
  "website": "https://sessions.us"
 },
 {
  "company_name": "Solargis",
  "country": "SK",
  "score_total": "5",
  "sector": "SaaS",
  "one_liner": "Solargis provides solar-resource data, analytics, and software tools for assessing and operating photovoltaic projects.",
  "funding_stage": "Bootstrapped",
  "website": "https://solargis.com"
 },
 {
  "company_name": "Cloudtalk",
  "country": "SK",
  "score_total": "5",
  "sector": "Technologie",
  "one_liner": "A cloud-based call center and business phone software for sales and support teams.",
  "funding_stage": "Series B",
  "website": "https://www.cloudtalk.io/"
 },
 {
  "company_name": "Bookimed",
  "country": "UA",
  "score_total": "5",
  "sector": "Healthtech",
  "one_liner": "Bookimed is a medical-tourism marketplace that connects international patients with hospitals, clinics, and treatment programs abroad.",
  "funding_stage": "Seed",
  "website": "https://bookimed.com"
 },
 {
  "company_name": "Adwisely",
  "country": "UA",
  "score_total": "5",
  "sector": "SaaS",
  "one_liner": "Adwisely automates paid ad management for Shopify and WooCommerce merchants, helping ecommerce stores run and optimize campaigns.",
  "funding_stage": "Seed",
  "website": "https://www.adwisely.com"
 },
 {
  "company_name": "Musaffa Financial Solutions",
  "country": "UZ",
  "score_total": "5",
  "sector": "Fintech",
  "one_liner": "Builds Islamic finance technology, including halal investing and Shariah-compliant screening tools.",
  "funding_stage": "Seed",
  "website": "https://musaffa.com"
 }
];

const SYNTH_SAMPLE = [
 {
  "company_name": "Aurora Robotics",
  "country": "CZ",
  "score_total": "5",
  "score_b2b": "Yes",
  "score_saas": "Yes",
  "score_global": "Yes",
  "score_ecosystem_fit": "Yes",
  "score_performance": "Yes",
  "sector": "Robotics / AI",
  "one_liner": "Autonomous warehouse robots with vision-based picking",
  "funding_stage": "Series A",
  "funding_info": "Series A - $8.5M (synthetic)",
  "employee_count": "51-200",
  "founder_ceo_name": "Jan Novak",
  "website": "https://example.com/aurora",
  "linkedin_company": "https://linkedin.com/company/example-aurora",
  "last_90d_signals": "hiring surge (12 eng roles); partnership with logistics provider",
  "discovered_date": "2026-02-14",
  "geo_verified": "True"
 },
 {
  "company_name": "Baltic Ledger",
  "country": "EE",
  "score_total": "4",
  "score_b2b": "Yes",
  "score_saas": "Yes",
  "score_global": "Yes",
  "score_ecosystem_fit": "Unclear",
  "score_performance": "Yes",
  "sector": "Fintech",
  "one_liner": "Cross-border payment reconciliation for SMEs",
  "funding_stage": "Seed",
  "funding_info": "Seed - €2.1M (synthetic)",
  "employee_count": "11-50",
  "founder_ceo_name": "Kati Tamm",
  "website": "https://example.com/balticledger",
  "linkedin_company": "https://linkedin.com/company/example-balticledger",
  "last_90d_signals": "funding round detected via hiring signal 18 days pre-announcement",
  "discovered_date": "2026-03-02",
  "geo_verified": "True"
 },
 {
  "company_name": "SteppeML",
  "country": "KZ",
  "score_total": "4",
  "score_b2b": "Yes",
  "score_saas": "Yes",
  "score_global": "Unclear",
  "score_ecosystem_fit": "Yes",
  "score_performance": "Yes",
  "sector": "AI / NLP",
  "one_liner": "Kazakh-Russian speech recognition APIs for call centers",
  "funding_stage": "Seed",
  "funding_info": "Seed - $1.4M (synthetic)",
  "employee_count": "11-50",
  "founder_ceo_name": "Aigerim Bekova",
  "website": "https://example.com/steppeml",
  "linkedin_company": "https://linkedin.com/company/example-steppeml",
  "last_90d_signals": "new enterprise client announced; 2 news mentions",
  "discovered_date": "2026-04-21",
  "geo_verified": "True"
 },
 {
  "company_name": "Vilnius Quantum",
  "country": "LT",
  "score_total": "5",
  "score_b2b": "Yes",
  "score_saas": "No",
  "score_global": "Yes",
  "score_ecosystem_fit": "Yes",
  "score_performance": "Yes",
  "sector": "Deep tech",
  "one_liner": "Photonic components for quantum communication",
  "funding_stage": "Series B",
  "funding_info": "Series B - €15M (synthetic)",
  "employee_count": "51-200",
  "founder_ceo_name": "Tomas Petrauskas",
  "website": "https://example.com/vilniusquantum",
  "linkedin_company": "https://linkedin.com/company/example-vq",
  "last_90d_signals": "EU research grant; CTO keynote at industry conference",
  "discovered_date": "2026-01-30",
  "geo_verified": "True"
 },
 {
  "company_name": "Tashkent Pay",
  "country": "UZ",
  "score_total": "4",
  "score_b2b": "Yes",
  "score_saas": "Yes",
  "score_global": "Unclear",
  "score_ecosystem_fit": "Yes",
  "score_performance": "Yes",
  "sector": "Fintech",
  "one_liner": "Mobile-first payment infrastructure for Central Asian merchants",
  "funding_stage": "Series A",
  "funding_info": "Series A - $5M (synthetic)",
  "employee_count": "201-500",
  "founder_ceo_name": "Aziz Karimov",
  "website": "https://example.com/tashkentpay",
  "linkedin_company": "https://linkedin.com/company/example-tpay",
  "last_90d_signals": "registry update; product launch covered by regional press",
  "discovered_date": "2026-05-12",
  "geo_verified": "True"
 }
];

const CATCHES = [
 {
  "company": "BirdyChat",
  "country": "LV",
  "flag": "🇱🇻",
  "inPipeline": "2026-04-15",
  "public": "2026-05-07",
  "lead": 22,
  "round": "€1.7M round",
  "how": "hiring + news signals, rescored before announcement",
  "links": [
   [
    "Arctic Startup",
    "https://arcticstartup.com"
   ],
   [
    "Mam Startup",
    "https://mamstartup.pl"
   ]
  ],
  "unattended": false
 },
 {
  "company": "Kodesage",
  "country": "HU",
  "flag": "🇭🇺",
  "inPipeline": "2026-05-14",
  "public": "2026-06-04",
  "lead": 21,
  "round": "$6.6M seed led by VentureFriends",
  "how": "curated-report ingestion flagged it as a top target at entry",
  "links": [
   [
    "Tech.eu",
    "https://tech.eu/2026/06/04/kodesage-raises-66m-for-ai-powered-legacy-software-modernisation/"
   ],
   [
    "BBJ",
    "https://bbj.hu/business/tech/innovation/hungarian-founded-kodesage-raises-usd-6-6-mln-to-modernize-legacy-enterprise-software/"
   ]
  ],
  "unattended": true
 },
 {
  "company": "TAPAYA",
  "country": "CZ",
  "flag": "🇨🇿",
  "inPipeline": "2026-04-13",
  "public": "2026-04-29",
  "lead": 16,
  "round": "funding event",
  "how": "discovery + momentum signals pre-announcement",
  "links": [],
  "unattended": false
 },
 {
  "company": "DesignVerse",
  "country": "RO",
  "flag": "🇷🇴",
  "inPipeline": "2026-05-04",
  "public": "2026-05-13",
  "lead": 9,
  "round": "$5.5M seed — the tracked investor joined the round",
  "how": "investor-portfolio watcher saw the interest before the press did",
  "links": [
   [
    "Tech.eu",
    "https://tech.eu/2026/05/13/romanian-designverse-raises-55m-to-modernise-legacy-enterprise-software/"
   ],
   [
    "Romania Insider",
    "https://www.romania-insider.com/design-verse-seed-round-may-2026"
   ]
  ],
  "unattended": true
 },
 {
  "company": "Webout",
  "country": "CZ",
  "flag": "🇨🇿",
  "inPipeline": "2026-05-26",
  "public": "2026-06-03",
  "lead": 8,
  "round": "€1.65M round",
  "how": "round detected in local-language press before details went wide; rescored 2★→5★",
  "links": [
   [
    "Startitup.sk",
    "https://startitup.sk"
   ]
  ],
  "unattended": true
 },
 {
  "company": "Edmund",
  "country": "CZ",
  "flag": "🇨🇿",
  "inPipeline": "2026-04-09",
  "public": "2026-04-13",
  "lead": 4,
  "round": "funding event",
  "how": "discovery signal days before announcement",
  "links": [],
  "unattended": false
 }
];
