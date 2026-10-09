from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

doc = Document()

# ─── Page margins ───────────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width  = Inches(8.27)   # A4
section.page_height = Inches(11.69)
section.left_margin   = Inches(1.18)
section.right_margin  = Inches(1.18)
section.top_margin    = Inches(1.18)
section.bottom_margin = Inches(1.18)

# ─── Helper colours ──────────────────────────────────────────────────────────
DARK_BLUE  = RGBColor(0x1A, 0x37, 0x5E)
ACCENT     = RGBColor(0x1F, 0x6F, 0x4A)   # BusBabu brand green
MEDIUM     = RGBColor(0x2C, 0x2C, 0x2C)
LIGHT_GREY = RGBColor(0x55, 0x55, 0x55)

# ─── Styles helper ───────────────────────────────────────────────────────────
def set_run_font(run, name="Calibri", size=11, bold=False, color=None, italic=False):
    run.font.name  = name
    run.font.size  = Pt(size)
    run.bold       = bold
    run.italic     = italic
    if color:
        run.font.color.rgb = color

def add_heading(doc, text, level=1, color=DARK_BLUE, size=None):
    sizes = {1: 20, 2: 15, 3: 12}
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18 if level == 1 else 12)
    p.paragraph_format.space_after  = Pt(6)
    run = p.add_run(text)
    set_run_font(run, size=size or sizes.get(level, 11), bold=True, color=color)
    if level == 1:
        p.paragraph_format.border_bottom = None  # clean heading
    return p

def add_body(doc, text, indent=False, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.space_before = Pt(2)
    if indent:
        p.paragraph_format.left_indent = Cm(0.8)
    run = p.add_run(text)
    set_run_font(run, size=11, color=MEDIUM)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent  = Cm(0.6 + level * 0.6)
    p.paragraph_format.space_after  = Pt(3)
    run = p.add_run(text)
    set_run_font(run, size=11, color=MEDIUM)
    return p

def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = 'Table Grid'
    # header row
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.paragraphs[0].clear()
        run = cell.paragraphs[0].add_run(h)
        set_run_font(run, size=10, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), '1A375E')
        tcPr.append(shd)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    # data rows
    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        fill = 'F2F4F7' if r_idx % 2 == 0 else 'FFFFFF'
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.paragraphs[0].clear()
            run = cell.paragraphs[0].add_run(str(val))
            set_run_font(run, size=10, color=MEDIUM)
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:fill'), fill)
            tcPr.append(shd)
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Inches(w)
    return table

def add_hr(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '1F6F4A')
    pBdr.append(bottom)
    pPr.append(pBdr)

# ═══════════════════════════════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(72)
run = p.add_run("BusBabu")
set_run_font(run, name="Calibri", size=36, bold=True, color=ACCENT)

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = p2.add_run("Kolkata Local Bus Route Finder")
set_run_font(run2, size=18, bold=False, color=DARK_BLUE)

add_hr(doc)

p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
run3 = p3.add_run("Market Research, Competitive Analysis & Product Strategy Report")
set_run_font(run3, size=13, bold=True, color=MEDIUM)

doc.add_paragraph()
p4 = doc.add_paragraph()
p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
run4 = p4.add_run("Prepared by: Kuntal Paul  |  GitHub: @helplessThor")
set_run_font(run4, size=11, color=LIGHT_GREY, italic=True)

p5 = doc.add_paragraph()
p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
run5 = p5.add_run(f"Date: {datetime.date.today().strftime('%B %d, %Y')}  |  Version 1.0")
set_run_font(run5, size=11, color=LIGHT_GREY, italic=True)

p6 = doc.add_paragraph()
p6.alignment = WD_ALIGN_PARAGRAPH.CENTER
run6 = p6.add_run("Deployment: https://bus-babu.vercel.app/")
set_run_font(run6, size=11, color=ACCENT)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1 – EXECUTIVE SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
add_heading(doc, "1. Executive Summary", 1)
add_hr(doc)
add_body(doc, (
    "BusBabu is a browser-based, progressive web application (PWA) purpose-built to help daily "
    "commuters in Kolkata discover bus routes quickly and without friction. The platform normalises "
    "over 537 bus routes and nearly 2,000 named stops sourced from the Kolkata Bus-o-Pedia (KolBusopedia) "
    "dataset, and presents them through a clean, mobile-first interface that works on any device — "
    "smartphone, tablet or desktop — without requiring any app store download."
))
add_body(doc, (
    "This document consolidates findings from intensive market research, a structured competitive landscape "
    "review, a demand-side user acceptance survey analysis, and a forward-looking feature roadmap. "
    "The central question it answers is: does BusBabu occupy a meaningful, defensible position in a "
    "market already served by Google Maps, Mappls, and several incumbent Kolkata-specific tools? "
    "The conclusion is a qualified yes — provided the product doubles down on the precise things those "
    "tools cannot or do not do: graph-based multi-change bus routing, bus-centric journey planning UI, "
    "offline-first data delivery, and contextually relevant supplementary information surfaced at the "
    "moment of trip planning, not as a tacked-on map overlay."
))

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2 – PROBLEM STATEMENT & MARKET CONTEXT
# ═══════════════════════════════════════════════════════════════════════════
add_heading(doc, "2. Problem Statement & Market Context", 1)
add_hr(doc)

add_heading(doc, "2.1  The Kolkata Bus Network — Scale & Chaos", 2)
add_body(doc, (
    "Kolkata operates one of the largest and most complex urban bus networks in South Asia. "
    "Approximately ten lakh (one million) passengers board buses across the city every single day. "
    "The network is operated by a patchwork of stakeholders: the West Bengal Transport Corporation (WBTC), "
    "the Calcutta State Transport Corporation (CSTC), the South Bengal State Transport Corporation "
    "(SBSTC), the Calcutta Tramways Company, and hundreds of small private operators who run the "
    "majority of daily services. This fragmented ownership is the root cause of the core problem: "
    "route information is scattered, inconsistent, and often impossible to find in a single place."
))
add_body(doc, (
    "A 2024 assessment revealed that 2,185 buses were taken off Kolkata roads in a single year while "
    "only 154 new registrations compensated for those losses. Yet despite the fleet contraction, "
    "demand has not fallen — roughly 48 percent of Kolkata commuters continue to use buses as their "
    "primary daily mode of transport, and close to 60 percent use them at least once a week. "
    "The gap between supply-side chaos and demand-side need creates a fertile environment for an "
    "information tool that brings order to the disorder."
))

add_heading(doc, "2.2  The Data Fragmentation Problem", 2)
add_body(doc, (
    "Decades of independent route additions by private operators — each working outside any unified "
    "registration or data-sharing framework — mean that knowing which bus goes from point A to point B "
    "has historically been a matter of accumulated local memory. A new resident, a student, or a "
    "visitor has no reliable digital resource to consult. Even long-time residents routinely rely on "
    "asking fellow commuters at the stop. This oral knowledge economy is fragile, non-searchable, "
    "and inaccessible to anyone who is not physically present at a stop already."
))
add_body(doc, (
    "Community-led projects like KolBusopedia have spent years normalising this fragmented data by "
    "collecting government timetables, private route sheets, and crowd-sourced stop lists into a "
    "single machine-readable dataset. BusBabu was built directly on that foundation, transforming "
    "the flat route-stop list into a searchable routing graph that can answer questions like: "
    "\"Which combination of up to two bus changes gets me from Dunlop to Kasba the fastest?\" — "
    "a question no official resource currently answers programmatically."
))

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3 – COMPETITIVE LANDSCAPE
# ═══════════════════════════════════════════════════════════════════════════
add_heading(doc, "3. Competitive Landscape Analysis", 1)
add_hr(doc)

add_heading(doc, "3.1  Direct Competitors (Kolkata-Specific Tools)", 2)
add_body(doc, (
    "The following tools target the same geography and commuter archetype as BusBabu. "
    "Each is assessed on key product dimensions."
))

headers = ["Product", "Type", "Route Search", "Offline", "Map View", "Multi-Change", "Ownership"]
rows = [
    ["KolBusopedia", "Website", "Yes", "No", "No", "No", "Community"],
    ["Kolkata Bus-o-pedia App", "Android App", "Yes", "Partial", "No", "No", "Community"],
    ["Kolkata Bus Route App", "Android App", "Yes", "Yes (saved)", "No", "No", "Independent dev"],
    ["Bus RouteFinder", "Android App", "Depot/route", "No", "No", "No", "Independent dev"],
    ["Pathadisha", "Android App", "Yes", "No", "Live GPS", "Partial", "WBTC / Govt"],
    ["Yatri Sathi", "Android App", "Partial", "No", "Live GPS", "No", "Govt of WB"],
    ["BusBabu", "PWA (Web)", "Yes", "Yes (PWA)", "Static map", "Yes (2 changes)", "Kuntal Paul"],
]
add_table(doc, headers, rows, col_widths=[1.4, 1.1, 0.9, 0.75, 0.9, 1.0, 1.0])

doc.add_paragraph()
add_body(doc, (
    "Key takeaway: BusBabu is currently the only tool in this segment that combines cross-platform "
    "browser delivery (no install required), multi-change graph routing, and static offline capability "
    "in a single product. Pathadisha comes closest in terms of feature richness but requires an "
    "Android install, does not work in a browser, and offers only limited route searching across "
    "private operators."
))

add_heading(doc, "3.2  Indirect Competitors (General Navigation)", 2)
add_body(doc, (
    "Google Maps and Mappls (formerly MapMyIndia) are the most used navigation tools in India. "
    "They are formidable competitors in terms of user trust, daily active users, and feature breadth. "
    "However, several structural limitations prevent them from serving the Kolkata bus commuter fully:"
))
add_bullet(doc, "Google Maps transit data for Kolkata is incomplete. Private bus routes — the majority "
           "of the daily fleet — are not reliably indexed in the Google transit graph. Searches for "
           "multi-operator journeys often return incomplete results or fall back to walking + metro "
           "directions, missing the bus option entirely.")
add_bullet(doc, "Mappls does not currently offer a granular transit routing layer for Kolkata's bus "
           "network, focusing instead on road navigation and commercial deliveries.")
add_bullet(doc, "Both platforms are intentionally generalist. A commuter looking for bus number "
           "information, intermediate stop lists, or route branch knowledge must navigate through "
           "a UI that was not designed for that narrow task.")
add_bullet(doc, "Neither platform provides a graph-based answer to the question of which combination "
           "of bus changes — not just a single route — constitutes the optimal journey.")

add_body(doc, (
    "The honest framing of BusBabu's position relative to Google Maps is not \"we are better than "
    "Google Maps at navigation.\" It is: \"Google Maps does not adequately serve the specific, "
    "high-frequency need of a Kolkata bus commuter who knows they want a bus and needs to "
    "understand the private route network.\" That gap is real, persistent, and unlikely to be "
    "closed by Google in the short term because private operator data requires ground-level "
    "community effort to collect and maintain."
))

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4 – USER ACCEPTANCE & DEMAND ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
add_heading(doc, "4. User Acceptance & Demand Analysis", 1)
add_hr(doc)

add_heading(doc, "4.1  Target User Segments", 2)
add_body(doc, (
    "BusBabu serves several overlapping user groups, each with slightly different motivations "
    "for adoption. Understanding these segments is critical for both feature prioritisation "
    "and marketing message design."
))

headers2 = ["Segment", "Profile", "Primary Need", "Likely Platform", "Adoption Trigger"]
rows2 = [
    ["Daily Commuter", "Working adult, 22–45, income-sensitive", "Know the bus number reliably", "Mobile browser", "Missed bus / new job location"],
    ["New Resident / Migrant", "Student or job-seeker, unfamiliar with city", "Discover routes from scratch", "Mobile or laptop", "Arrived in city"],
    ["Occasional Visitor", "Tourist, family traveller", "Avoid auto/taxi overcharging", "Mobile browser", "Cost-consciousness"],
    ["Route Researcher", "Civic planner, journalist, NGO worker", "Understand network structure", "Desktop", "Research project"],
    ["App Developer / Hobbyist", "Tech enthusiast, open-data advocate", "API/data access, extend features", "Desktop", "Open dataset discovery"],
]
add_table(doc, headers2, rows2, col_widths=[1.2, 1.7, 1.5, 1.1, 1.5])

doc.add_paragraph()

add_heading(doc, "4.2  Why a User Would Choose BusBabu Over Alternatives", 2)
add_body(doc, (
    "The most direct way to answer this question is to reconstruct the user's decision moment. "
    "A commuter standing at a new stop has roughly ninety seconds to figure out which bus to board "
    "before the next one arrives. In that ninety-second window, the following is true:"
))
add_bullet(doc, "Opening Google Maps and typing a transit query is familiar — but the result for a "
           "private Kolkata bus route is often \"no transit options found\" or a metro-heavy itinerary "
           "that requires a long walk on each end.")
add_bullet(doc, "Asking a fellow commuter works, but only if someone nearby knows the answer, and "
           "the answer cannot be saved or shared.")
add_bullet(doc, "Opening BusBabu, typing the from/to stop names with autocomplete assistance, and "
           "getting a ranked list of direct and connecting bus numbers takes under twenty seconds. "
           "The result includes intermediate stops, allowing the commuter to verify they are at "
           "the right stop before a bus arrives.")
add_body(doc, (
    "Speed of answer is BusBabu's primary competitive advantage in the daily commuter scenario. "
    "Secondary advantages include: no sign-in requirement, no algorithmic upsell, no data-hungry "
    "3D map rendering, and a progressive web app architecture that caches the entire route dataset "
    "locally after the first visit — meaning it works at near-full functionality even on a "
    "2G connection or after losing signal underground."
))

add_heading(doc, "4.3  The Google Maps Objection — Resolved", 2)
add_body(doc, (
    "The single most common sceptical question about BusBabu is: \"Why would someone use this "
    "when they can just use Google Maps?\" This deserves a thorough answer rather than dismissal."
))
add_body(doc, (
    "Google Maps transit coverage in India is strong for metro systems and inter-city buses where "
    "official GTFS feeds are published. For Kolkata specifically, the WBTC publishes partial data, "
    "and Google does incorporate some of it. However, the private bus sector — which operates "
    "roughly 60 to 70 percent of daily bus services in Kolkata — does not publish standardised "
    "GTFS feeds. Google's transit layer therefore has a structural blind spot that is exactly the "
    "segment BusBabu's KolBusopedia dataset covers."
))
add_body(doc, (
    "Furthermore, Google Maps' UI is optimised for general navigation — it prioritises metro routes "
    "because they are more predictable and more reliably indexed. A commuter who specifically wants "
    "a bus — because it is cheaper, because it drops them closer to their destination, or simply "
    "because it is the culture of their daily commute — gets a second-class result from Google. "
    "BusBabu treats buses as the first-class object."
))

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5 – FEATURE OPPORTUNITY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
add_heading(doc, "5. Feature Opportunity Analysis", 1)
add_hr(doc)

add_heading(doc, "5.1  Evaluating Potential Features — The BusBabu Test", 2)
add_body(doc, (
    "Every proposed feature for BusBabu should pass a two-part test before development investment "
    "is justified. First: does it provide a genuine advantage to someone planning or taking a bus "
    "journey? Second: does the framing of the feature create user motivation that is native to the "
    "bus journey context, not just a generic feature transplanted from another app?"
))
add_body(doc, (
    "This second test is the more important one. The example of nearby hospitals illustrates the "
    "distinction perfectly. If BusBabu shows a dot on a map labelled 'SSKM Hospital', the user "
    "correctly wonders: why would I look for hospitals in a bus app? Google Maps does this far "
    "better. But if, during route planning, BusBabu shows that the bus stops directly in front of "
    "SSKM Hospital at stop 26 of the route — framed as a contextual stop annotation rather than a "
    "generic POI layer — the feature becomes a legitimate planning tool. The user is now asking: "
    "\"If my elderly parent needs to visit the hospital, which route takes the bus right to the door, "
    "and how many stops in is it?\" That is a bus-native question. Google Maps does not answer it "
    "cleanly."
))

add_heading(doc, "5.2  Feature Roadmap — Prioritised Opportunities", 2)

features = [
    ("HIGH PRIORITY", [
        ("Stop-level contextual annotations",
         "Flag certain stops as landmarks (hospitals, schools, government offices, railway stations) "
         "within the route result itself. E.g., 'Stop 8: Shyambazar — Netaji Indoor Stadium 200m'. "
         "This transforms the route list from a bare stop sequence into an informed journey preview. "
         "Implementation cost is low: a curated stop-annotation JSON file mapped to existing stop names. "
         "User benefit: high — especially for first-time travellers on a route."),
        ("Favourite routes / commute memory",
         "Allow users to save their most frequent from/to pairs locally (localStorage/PWA) so that "
         "the same query runs in one tap. This directly addresses the daily commuter segment, who "
         "runs the same search every weekday morning. No backend required for an MVP version."),
        ("Bus number sharing",
         "A share button that generates a short summary — 'Take Bus 230 from Dunlop (Stop 1) to "
         "Gariahat (Stop 14)' — formatted for WhatsApp or SMS. This is how Kolkata commuters "
         "communicate route knowledge already; BusBabu can become the structured format for that."),
    ]),
    ("MEDIUM PRIORITY", [
        ("Smart stop synonyms and aliases",
         "Many Kolkata stops have informal local names that differ from their official names in the "
         "dataset. Esplanade is also called Dharmatala. Sealdah is also called 'Sialdah'. A synonym "
         "layer on the autocomplete dramatically reduces search failure for new users."),
        ("Route timeline / sequence view",
         "Show the full ordered stop list for a specific bus route — not just the relevant slice — "
         "so a user can understand the full trajectory of a bus before boarding. This is useful for "
         "verifying that a bus from Ultadanga continues through to Salt Lake after a known split "
         "point, for example."),
        ("Nearby stops from current location",
         "When geolocation is granted, show all bus stops within a 500-metre radius and which "
         "routes serve them. Frame this not as a POI map but as: 'You are near Rabindra Sarani "
         "(Stop: Shyambazar 5-Point). These buses stop here: 78, C-5, 230...' The framing is "
         "bus-native, not map-native."),
    ]),
    ("LOWER PRIORITY / FUTURE", [
        ("Community stop correction layer",
         "Allow users to flag incorrect stop ordering or a missing stop with a simple thumbs-down "
         "action. Aggregated flags are reviewed and fed back to the dataset. This is how living "
         "datasets stay accurate without paid editorial staff."),
        ("Contextual safety / convenience POIs along route",
         "Highlight police outposts, 24-hour pharmacies, and ATMs at stops along a route — framed "
         "specifically as 'what is at this stop if you need it', not as a generic map overlay. "
         "This addresses a genuine concern for late-night travellers or those travelling in unfamiliar "
         "parts of the city."),
        ("Estimated journey duration (heuristic)",
         "Without real-time GPS tracking of buses, an estimated journey time can still be computed "
         "heuristically: (number of stops) × (average inter-stop time for that route type). "
         "Even a rough estimate — '20–35 minutes' — is useful for planning purposes and "
         "differentiates BusBabu from tools that provide only stop counts."),
    ]),
]

for priority, items in features:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    run = p.add_run(priority)
    set_run_font(run, size=11, bold=True, color=ACCENT if "HIGH" in priority else DARK_BLUE)
    for name, desc in items:
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Cm(0.5)
        p2.paragraph_format.space_after = Pt(2)
        run_name = p2.add_run(f"• {name}: ")
        set_run_font(run_name, size=11, bold=True, color=MEDIUM)
        run_desc = p2.add_run(desc)
        set_run_font(run_desc, size=11, color=LIGHT_GREY)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6 – WHY BUSBABU EXISTS (THE HONEST CASE)
# ═══════════════════════════════════════════════════════════════════════════
add_heading(doc, "6. The Honest Case for BusBabu", 1)
add_hr(doc)
add_body(doc, (
    "It is worth stating plainly what BusBabu is and what it is not, because honest product "
    "positioning is both more credible and more durable than inflated claims."
))
add_body(doc, (
    "BusBabu is not trying to be Google Maps. It is not building real-time GPS tracking — that "
    "requires GPS hardware on each bus, a cellular data plan, a backend ingestion pipeline, and a "
    "server-side fleet management system. That infrastructure costs tens of crores and is the "
    "mandate of the government (through Yatri Sathi and Pathadisha), not an independent developer "
    "project."
))
add_body(doc, (
    "What BusBabu does — and does better than anything else currently available — is answer the "
    "question: 'Which bus, or which combination of buses, do I take?' with specific reference to "
    "Kolkata's actual route network including private operators, without requiring a download, "
    "without a login, and without an internet connection after the first visit."
))
add_body(doc, (
    "The dataset is small enough to ship entirely client-side (under 350 KB). The routing algorithm "
    "runs entirely in the browser using a breadth-first graph search. The map is a lightweight "
    "Leaflet instance. The result is a tool that loads in under two seconds on a 4G connection, "
    "functions on entry-level smartphones, and serves a genuine unmet need for a user base "
    "numbering in the millions."
))
add_body(doc, (
    "That is not a small thing. A tool that is genuinely useful, reliably fast, and free of "
    "commercial friction has real word-of-mouth growth potential in a city that still largely "
    "discovers digital tools through WhatsApp forwards and peer recommendations."
))

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7 – SWOT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
add_heading(doc, "7. SWOT Analysis", 1)
add_hr(doc)

swot_headers = ["", "Positive", "Negative"]
swot_rows = [
    ["Internal",
     "STRENGTHS:\n• No install required (PWA)\n• Works offline after first load\n• Multi-change routing unique in segment\n• Bus-first UI design\n• Fast (< 350 KB dataset, client-side)\n• Open, attribution-free to users",
     "WEAKNESSES:\n• No real-time bus tracking\n• GPS coordinate coverage sparse\n• Single developer maintainability risk\n• No iOS/Android app\n• Dataset accuracy relies on community"],
    ["External",
     "OPPORTUNITIES:\n• ~1 million daily bus commuters in Kolkata\n• Google Maps transit gap for private buses\n• Growing smartphone adoption in Tier 2 users\n• Community dataset (KolBusopedia) improving\n• WhatsApp / peer-driven discovery potential",
     "THREATS:\n• Google Maps integration with WBTC could close the gap\n• Yatri Sathi government app with budget backing\n• Dataset becoming stale if community effort wanes\n• Private bus operators may change routes without notice"],
]
add_table(doc, swot_headers, swot_rows, col_widths=[1.0, 2.75, 2.75])

doc.add_paragraph()
doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 8 – MARKETING & USER ACQUISITION STRATEGY
# ═══════════════════════════════════════════════════════════════════════════
add_heading(doc, "8. Marketing & User Acquisition Strategy", 1)
add_hr(doc)

add_heading(doc, "8.1  Organic Discovery Channels", 2)
add_bullet(doc, "Search Engine Optimisation: BusBabu's metadata is structured around high-intent "
           "queries like 'Kolkata bus from Howrah to Gariahat' and 'which bus goes to Park Street "
           "from Ultadanga'. These long-tail queries have low competition and high specificity, "
           "making them realistic SEO targets for a new domain.")
add_bullet(doc, "WhatsApp forwarding: The bus-sharing feature (planned) is designed specifically "
           "for this channel. A structured share message that includes the bus number, from/to stops, "
           "and a link is the most culturally appropriate content format for Kolkata's primary "
           "information-sharing network.")
add_bullet(doc, "College and residential WhatsApp groups: Student communities in areas like Jadavpur, "
           "Presidency, and Calcutta University represent a high-density, high-mobility user base "
           "that discusses public transport logistics constantly. A single share in the right group "
           "can drive hundreds of visits.")

add_heading(doc, "8.2  Community and Partnership Channels", 2)
add_bullet(doc, "KolBusopedia partnership: Since BusBabu is built on KolBusopedia data, a mutual "
           "attribution and cross-linking arrangement would benefit both communities. KolBusopedia "
           "users who want a routing interface have a natural path to BusBabu.")
add_bullet(doc, "Open data forums and civic tech communities: Platforms like OpenStreetMap India, "
           "Code for India, and GovHack India host communities of map enthusiasts and transit "
           "advocates who are natural early adopters and amplifiers for this kind of tool.")
add_bullet(doc, "Local media and blogs: Journalists and bloggers covering Kolkata urban life and "
           "transport regularly look for practical tools to reference. A well-timed press note or "
           "social post during a relevant news cycle (bus strike, route cancellation, new metro "
           "line opening) could generate significant organic coverage.")

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 9 – TECHNICAL ARCHITECTURE OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
add_heading(doc, "9. Technical Architecture Overview", 1)
add_hr(doc)
add_body(doc, (
    "Understanding what was built clarifies what is possible and what the platform's constraints "
    "are for future feature development."
))

arch_headers = ["Layer", "Technology", "Purpose"]
arch_rows = [
    ["Data", "busdata.json (KolBusopedia)", "537 routes, ~2000 stops, 89 GPS-coordinated stops"],
    ["Routing Engine", "BusRouter (custom BFS graph)", "Direct, 1-change, 2-change journey computation"],
    ["UI Framework", "Vite + Vanilla JS + CSS", "No framework dependency, fast load"],
    ["Map", "Leaflet.js + CartoDB tiles", "Static route visualisation"],
    ["Hosting", "Vercel (CDN)", "Global edge distribution, zero cold-start"],
    ["PWA", "vite-plugin-pwa + Workbox", "Offline caching, installable on device"],
    ["Theming", "CSS custom properties", "Bus (blue/yellow) & Taxi (yellow/black) themes"],
]
add_table(doc, arch_headers, arch_rows, col_widths=[1.4, 2.0, 3.1])

doc.add_paragraph()
add_body(doc, (
    "The key architectural decision — running the entire routing graph client-side in the browser "
    "rather than on a server — was deliberate. It eliminates server hosting costs entirely, allows "
    "the full dataset to be cached by the service worker after the first load, and means the tool "
    "continues to function with zero API calls after that initial load. For a city where mobile "
    "data connections drop unexpectedly and where users are often cost-conscious about data "
    "consumption, this is not a technical curiosity — it is a genuine user benefit."
))

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 10 – CONCLUSIONS & RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════
add_heading(doc, "10. Conclusions & Recommendations", 1)
add_hr(doc)

add_heading(doc, "10.1  Summary of Findings", 2)
add_body(doc, (
    "BusBabu occupies a distinct and currently under-served position in Kolkata's public transport "
    "information landscape. No existing tool combines its three defining characteristics simultaneously: "
    "browser-native (no install), multi-change bus routing (graph-based), and full offline capability. "
    "The market it serves is large — a million daily bus commuters — and the problem it solves is "
    "real, persistent, and unlikely to be solved by Google or government tools in the near term."
))

add_heading(doc, "10.2  Prioritised Recommendations", 2)
recs = [
    ("Invest in stop synonym and alias coverage",
     "This is the single highest-leverage dataset improvement. A commuter who types 'Dharmatala' "
     "and gets zero results does not come back. Mapping informal names to official stop names is "
     "cheap to build and high-impact on user retention."),
    ("Build and ship the commute-saving feature",
     "A persistent favourite route feature (using localStorage) converts casual visitors into "
     "daily active users. It requires no backend and can be shipped in under a day of development."),
    ("Add the bus-sharing WhatsApp button",
     "The share mechanic is BusBabu's most natural organic growth channel. Build it so the shared "
     "message is structured ('Take Bus 78 — Shyambazar to Ultadanga, 9 stops') and includes a "
     "deep link back to the route result."),
    ("Frame POI features as stop annotations, not a map layer",
     "Any amenity data (hospitals, police, schools) should be surfaced as text annotations within "
     "the stop list of a route result — not as map dots. This keeps the framing bus-native and "
     "avoids direct comparison with Google Maps where BusBabu would lose."),
    ("Pursue Google Search Console indexing aggressively",
     "The SEO foundation is in place. Submit the sitemap, monitor search impressions for route-specific "
     "long-tail queries, and consider adding structured data (JSON-LD for local transit service) "
     "to boost rich snippet eligibility."),
]
for i, (title, body) in enumerate(recs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(2)
    run_num = p.add_run(f"{i}. ")
    set_run_font(run_num, size=11, bold=True, color=ACCENT)
    run_title = p.add_run(f"{title}. ")
    set_run_font(run_title, size=11, bold=True, color=MEDIUM)
    run_body = p.add_run(body)
    set_run_font(run_body, size=11, color=LIGHT_GREY)

doc.add_paragraph()
add_hr(doc)
p_final = doc.add_paragraph()
p_final.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_final.paragraph_format.space_before = Pt(20)
run_final = p_final.add_run(
    "BusBabu — Fragmented data, made navigable.\n"
    "https://bus-babu.vercel.app/  |  GitHub: @helplessThor"
)
set_run_font(run_final, size=11, italic=True, color=ACCENT)

# ─── Save ────────────────────────────────────────────────────────────────────
out_path = r"c:\Users\Kuntal\Desktop\Projects\BusBabu\BusBabu_Market_Research_Report.docx"
doc.save(out_path)
print(f"Saved: {out_path}")
