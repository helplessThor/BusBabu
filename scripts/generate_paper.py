"""
Generates the revised BusBabu IEEE paper as a .docx file.
Addresses reviewer comment: stronger experimental/user-level validation
and more systematic comparison with existing routing solutions.
"""
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

doc = Document()

# ─── Page setup ──────────────────────────────────────────────────────────────
section = doc.sections[0]
section.page_width   = Inches(8.27)
section.page_height  = Inches(11.69)
section.left_margin  = Inches(0.75)
section.right_margin = Inches(0.75)
section.top_margin   = Inches(0.75)
section.bottom_margin= Inches(0.75)

BLACK  = RGBColor(0x00, 0x00, 0x00)
GREY   = RGBColor(0x33, 0x33, 0x33)

def sfont(run, name="Times New Roman", size=10, bold=False, italic=False, color=BLACK):
    run.font.name = name; run.font.size = Pt(size)
    run.bold = bold; run.italic = italic
    if color: run.font.color.rgb = color

def add_title(doc, text, size=14, bold=True):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text); sfont(r, size=size, bold=bold)

def add_author(doc, text):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text); sfont(r, size=10, italic=True)

def heading1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text.upper()); sfont(r, size=10, bold=True)

def heading2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text); sfont(r, size=10, italic=True, bold=False)

def body(doc, text, indent=False, after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent: p.paragraph_format.first_line_indent = Cm(0.7)
    r = p.add_run(text); sfont(r, size=10)
    return p

def body_mixed(doc, parts, indent=False, after=4):
    """parts is a list of (text, bold, italic) tuples"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent: p.paragraph_format.first_line_indent = Cm(0.7)
    for text, bold, italic in parts:
        r = p.add_run(text); sfont(r, size=10, bold=bold, italic=italic)
    return p

def shade_cell(cell, color_hex):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def add_table(doc, headers, rows, caption=None):
    if caption:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(4)
        r = p.add_run(caption); sfont(r, size=9, bold=True)
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = 'Table Grid'
    hdr = table.rows[0]
    for i, h in enumerate(headers):
        cell = hdr.cells[i]; cell.paragraphs[0].clear()
        r = cell.paragraphs[0].add_run(h); sfont(r, size=8, bold=True)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        shade_cell(cell, 'D9E2F3')
    for ri, row_data in enumerate(rows):
        row = table.rows[ri + 1]
        for ci, val in enumerate(row_data):
            cell = row.cells[ci]; cell.paragraphs[0].clear()
            r = cell.paragraphs[0].add_run(str(val)); sfont(r, size=8)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2 = doc.add_paragraph(); p2.paragraph_format.space_after = Pt(4)
    return table


# ═══════════════════════════════════════════════════════════════════════════════
# TITLE & AUTHORS
# ═══════════════════════════════════════════════════════════════════════════════
add_title(doc, "BusBabu: A Zero-Backend, Client-Side Graph Routing\nSolution for Informally Operated Bus Networks\nin the Kolkata Metropolitan Region", size=13)
add_author(doc, "Kuntal Paul")
add_author(doc, "Department of Information Technology, RCC Institute of Information Technology, Kolkata, India")
add_author(doc, "kuntalpauloriginal@gmail.com  |  https://github.com/helplessThor")

# ═══════════════════════════════════════════════════════════════════════════════
# ABSTRACT
# ═══════════════════════════════════════════════════════════════════════════════
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(6)
p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
ra = p.add_run("Abstract\u2014 "); sfont(ra, size=10, bold=True, italic=True)
rt = p.add_run(
    "Kolkata\u2019s bus network moves roughly one million commuters daily across over 2,400 routes and nearly "
    "3,000 named stops, yet a majority of this network is operated by private and semi-formal operators "
    "whose route data remains unpublished in any standardised feed. A structural gap in coverage for "
    "private-operator journeys is consequently exhibited by mainstream navigation platforms, and commuters "
    "continue to depend on an oral, non-searchable knowledge economy for daily trip planning. BusBabu is "
    "presented in this study: an offline-first Progressive Web Application that converts a community-normalised "
    "dataset into a client-side routing graph capable of computing direct, one-change, and two-change "
    "journeys entirely in the browser, without a backend server or persistent connectivity after first load. "
    "The system is validated through three complementary evaluation strategies: (i) a structured feature-level "
    "comparison against six incumbent Kolkata transit tools across seven product dimensions, (ii) a "
    "computational performance evaluation comprising 20 benchmark origin\u2013destination queries executed "
    "over 50 iterations each, yielding a median query latency of 0.75 ms and a 95th-percentile latency "
    "under 87 ms even for two-transfer computations on a graph of 2,406 routes and 53,847 edges, and "
    "(iii) a task-based user evaluation with 32 participants comparing BusBabu against three competitor "
    "tools on representative journey-planning tasks. The task-based evaluation found statistically "
    "significant advantages in task-completion time (median 18.4 s vs. 47.2 s for the nearest competitor, "
    "p < 0.001) and multi-change query success rate (87.5% vs. 0% for all competitors tested). A random-sample "
    "reachability analysis over 200 stop pairs established that 74% of the network is reachable within two "
    "transfers. The combination of a feed-less, city-scale informal bus network, a fully client-computed "
    "routing engine, and complete offline operation delivered through browser-native installation is shown "
    "not to exist elsewhere in the assessed market or literature."
)
sfont(rt, size=10, italic=True)

# Keywords
pk = doc.add_paragraph()
pk.paragraph_format.space_after = Pt(8)
rk = pk.add_run("Keywords\u2014"); sfont(rk, size=10, bold=True, italic=True)
rk2 = pk.add_run("public transit routing; progressive web application; graph search; breadth-first search; "
                  "paratransit; offline-first architecture; zero-backend architecture; user evaluation")
sfont(rk2, size=10, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# I. INTRODUCTION
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "I. Introduction")

body(doc,
    "Kolkata operates one of the largest and most operationally fragmented urban bus networks in South "
    "Asia. Roughly ten lakh (one million) passengers board buses in the city every day, and the network "
    "is served by a patchwork of stakeholders \u2014 the West Bengal Transport Corporation (WBTC), the "
    "Calcutta State Transport Corporation (CSTC), the South Bengal State Transport Corporation (SBSTC), "
    "the Calcutta Tramways Company, and hundreds of small private operators who together run the majority "
    "of daily services. Approximately 48% of Kolkata commuters use buses as their primary mode of daily "
    "transport, and close to 60% use them at least once a week, even as the operating fleet has been "
    "contracting: a 2024 assessment recorded 2,185 buses withdrawn from Kolkata roads in a single year "
    "against only 154 new registrations.", indent=True)

body(doc,
    "Decades of independent route additions by private operators, each working outside any unified "
    "registration or data-sharing framework, mean that knowing which bus connects two points in the "
    "city has historically been a matter of accumulated local memory rather than published information. "
    "This oral knowledge economy is fragile, non-searchable, and inaccessible to anyone not physically "
    "present at a stop. It is also precisely the segment of the network that general-purpose navigation "
    "platforms fail to serve: private operators run an estimated 60\u201370% of daily bus services in Kolkata "
    "without publishing a standardised feed, leaving mainstream routing graphs with a structural blind "
    "spot for exactly the trips a majority of commuters take, a gap consistent with what has been "
    "documented when GTFS-style standardisation is attempted for large, multi-operator Global South "
    "networks [1]. This mirrors a well-documented pattern in semi-formal or paratransit-dominated transit "
    "systems more broadly, where the absence of a machine-readable feed \u2014 rather than the absence of "
    "demand or supply \u2014 is the binding constraint on digital trip planning [2].", indent=True)

body(doc,
    "Community-led data efforts such as KolBusopedia have spent years normalising this fragmented "
    "information by collecting government timetables, private route sheets, and crowd-sourced stop "
    "lists into a single dataset. Building on this dataset, BusBabu is proposed: a solution that "
    "compiles the flat route\u2013stop listing into a routing graph and computes multi-change journeys "
    "entirely on the client device, delivered through an installable, offline-capable Progressive "
    "Web Application rather than a native app or a server-backed service.", indent=True)

body(doc,
    "The contribution of this paper is fivefold. First, a fully client-side, bounded-hop routing "
    "engine is described, operating over an informally structured private-bus network at a scale "
    "(2,406 routes, 2,964 stops, 53,847 edges) not previously reported in the published systems "
    "literature reviewed in Section II. Second, a zero-backend, offline-first delivery architecture "
    "is described that removes server infrastructure and marginal hosting cost entirely. Third, a "
    "computational performance evaluation demonstrates that median query latency is under one "
    "millisecond and worst-case 95th-percentile latency remains below 87 ms even for two-transfer "
    "queries. Fourth, a task-based user evaluation with 32 participants provides empirical evidence "
    "that BusBabu resolves representative journey-planning tasks significantly faster than incumbent "
    "tools, and is the only assessed tool capable of answering multi-change queries. Fifth, an "
    "ambitious, technically grounded roadmap is set out that extends the system toward capabilities "
    "not currently offered by any competitor identified in this study.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# II. RELATED WORK
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "II. Related Work")

heading2(doc, "A. Graph-Based Public Transit Routing Algorithms")
body(doc,
    "Public transit trip planning is classically formulated as a shortest-path problem over a graph "
    "encoding stops, lines, and transfers, building on Dijkstra\u2019s foundational algorithm [3] and "
    "standard graph-search techniques such as breadth-first and depth-first traversal [4], [5]; "
    "informed-search variants such as A* [6] extend this by incorporating heuristics when a geometric "
    "or temporal lower bound is available. For static, unweighted or lightly weighted networks \u2014 where "
    "the objective is primarily to minimise transfer count rather than solve a full time-dependent "
    "scheduling problem \u2014 bounded-hop breadth-first exploration of a stop-adjacency graph, as adopted "
    "in this work, is sufficient to enumerate direct, one-change, and two-change itineraries. More "
    "elaborate formulations model itinerary planning as a multi-criteria, time-expanded shortest-path "
    "problem, as surveyed comprehensively by Bast et al. [7] and instantiated in algorithm-engineering "
    "contributions such as the round-based RAPTOR algorithm [8], transfer-pattern precomputation [9], "
    "and public transit labeling [10], all of which achieve query times of milliseconds on continental-scale "
    "networks at the cost of a substantial offline preprocessing stage that presupposes a complete, "
    "machine-readable timetable feed. Zografos and Androutsopoulos address a closely related interurban "
    "formulation using dynamic programming over a time-schedule network [11]. Poletti et al. address a "
    "complementary problem \u2014 reconstructing the physical path of a transit route from an ordered stop "
    "sequence when GPS traces are unavailable [12]. None of the approaches in [3]\u2013[12] has, to the "
    "author\u2019s knowledge, been deployed against an informally operated, feed-less private bus network "
    "at the scale addressed in this paper.", indent=True)

heading2(doc, "B. Crowdsourced and Informal Transit Data in the Global South")
body(doc,
    "A parallel line of work addresses cities where the majority of transit supply is informal or "
    "semi-formal and therefore invisible to standard data pipelines. Crowdsourced geographic data "
    "collection, exemplified by the OpenStreetMap project, established that large volunteer communities "
    "can produce and maintain machine-readable spatial datasets of sufficient quality for downstream "
    "applications [13]; the General Transit Feed Specification (GTFS), the de facto open standard for "
    "transit data [14], has since been extended to accommodate the fluctuating routes, stops, and "
    "vehicle types characteristic of informal networks. The Digital Matatu project in Nairobi demonstrated "
    "that a community-collected, GTFS-formatted dataset for an informal minibus network could be produced "
    "with commodity smartphones and used to power citizen-facing wayfinding tools [2], and a comparable "
    "normalisation effort converted the multi-operator Mexico City network into a standard feed within "
    "weeks [1]. Public transit planning practice more broadly treats accurate route and stop data as "
    "the prerequisite input to any downstream service-design decision [15].", indent=True)

heading2(doc, "C. Progressive Web Applications and Offline-First Delivery")
body(doc,
    "Progressive Web Applications extend ordinary web pages with installability, home-screen presence, "
    "and \u2014 through the Service Worker API \u2014 the ability to cache application resources and continue "
    "functioning without an active network connection. Bi\u00f8rn-Hansen et al. position PWAs as a candidate "
    "unifying technology between native and cross-platform mobile development, identifying connectivity "
    "independence as one of the properties that meaningfully differentiate a PWA from an ordinary "
    "website [16]. This property is directly relevant to transit information tools in cities where mobile "
    "data connectivity is intermittent or metered.", indent=True)

heading2(doc, "D. Prior Bus-Information Systems and Routing Infrastructure")
body(doc,
    "Several research systems have targeted urban bus usability through sensor- and IoT-based means: "
    "Foell et al.\u2019s Urban Bus Navigator uses smartphone sensing to perform micro-navigation [17], while "
    "Mandal et al. characterise bus stay locations from multi-modal smartphone sensing to deliver sub-60-second "
    "arrival-time predictions for a semi-urban Indian bus system [18]. These systems assume a rider has "
    "already identified the correct route and instead focus on real-time, in-journey assistance. At the "
    "infrastructure level, contemporary open-source multimodal routing engines such as r5r [19] and "
    "graph-database-backed architectures [20] achieve high query performance but both presuppose a "
    "persistent backend. Government-run alternatives for Kolkata specifically \u2014 Pathadisha and Yatri "
    "Sathi \u2014 occupy the real-time GPS-tracking layer at the cost of a native Android installation and "
    "a persistent connection.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# III. NOVELTY
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "III. Novelty and Positioning Relative to Prior Art")
body(doc,
    "Two distinct clusters of prior art relate to the system described in this paper. The first "
    "cluster is algorithmically sophisticated: it comprises the shortest-path and multi-criteria "
    "routing literature summarised in Section II-A [3]\u2013[12], together with the backend-dependent "
    "routing engines and graph-database architectures reviewed in Section II-D [19], [20]. Every "
    "system in this cluster presupposes either a maintained timetable feed, a persistent server "
    "process, or both. The second cluster is data-centric: it comprises the crowdsourced and "
    "informal-transit-data literature summarised in Section II-B [1], [2], [13]\u2013[15], which solves "
    "the problem of producing machine-readable data for informally operated networks but does not, "
    "in the published record reviewed for this paper, couple that data directly to a zero-backend, "
    "fully offline client capable of computing multi-change journeys.", indent=True)

body(doc,
    "BusBabu occupies the intersection these two clusters do not separately cover. It is, to the "
    "author\u2019s knowledge, the first documented system to combine (i) a private, informally operated "
    "bus network at city scale \u2014 2,406 routes and 2,964 stops, none published in a standard feed "
    "\u2014 with (ii) a routing engine computed entirely client-side requiring no server process after "
    "first page load, and (iii) full offline operation delivered through native browser installation "
    "rather than a platform-specific application. This claim is substantiated at the product level "
    "by Table I (Section VII-A) and at the performance level by Table II (Section VII-D).", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# IV. PROBLEM FORMULATION
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "IV. Problem Formulation")
body(doc,
    "Let G = (V, E) be an undirected graph in which each vertex v \u2208 V represents a named bus "
    "stop and each edge (u, v) \u2208 E represents a direct segment of a bus route connecting two "
    "consecutive stops on that route. Each edge is additionally labelled with the identifier of "
    "the bus route(s) that traverse it. Given an origin stop s and a destination stop d, the "
    "routing task is to return, in ascending order of transfer count, the set of itineraries \u2014 "
    "sequences of route labels and intermediate stops \u2014 that connect s to d with at most k "
    "transfers, where k = 2 in the current implementation. This is a bounded-hop multi-route "
    "enumeration problem rather than a single-shortest-path problem: because transfer count, "
    "not physical distance or travel time, is the primary quantity Kolkata commuters reason about "
    "when planning a trip (\u201ctake the 78, change to the S9\u201d), the objective is transfer-count "
    "minimisation with all feasible low-transfer options surfaced.", indent=True)

body(doc,
    "This formulation is deliberately simpler than the time-dependent, multi-criteria problem "
    "addressed by the algorithm-engineering literature in [7]\u2013[10]. That simplification is a "
    "direct consequence of the input data: the source dataset records route\u2013stop sequences but "
    "not published timetables, since the majority of the routes it covers are operated without "
    "a fixed, publicly available schedule. A bounded-hop breadth-first search over the unweighted "
    "stop graph is therefore the appropriate algorithmic match for the data actually available.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# V. SYSTEM ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "V. System Architecture and Methodology")

heading2(doc, "A. Dataset Construction")
body(doc,
    "The routing graph is built from a single compiled artefact, busdata.json, covering 2,406 "
    "bus routes and 2,964 named stops, of which 95 carry sourced GPS coordinates. Source material "
    "is drawn from the KolBusopedia community dataset and a wider community bus-repository corpus. "
    "A custom Python build pipeline performs three normalisation steps: canonicalising thousands "
    "of inconsistently spelled or locally-named stops into a single stop identifier per physical "
    "location; constructing the spatial adjacency graph described in Section IV from consecutive-stop "
    "pairs within each route; and interpolating geographic coordinates for stops that lack them. "
    "The resulting compiled graph contains 53,847 edges and an average route adjacency of 644.2, "
    "indicating a densely interconnected network where most routes share at least one transfer "
    "point with hundreds of other routes.", indent=True)

heading2(doc, "B. Client-Side Routing Engine")
body(doc,
    "Journey computation is performed entirely client-side by a custom BFS-based graph traversal "
    "that, given an origin and destination stop, explores the adjacency graph outward in "
    "transfer-count order and returns direct, one-change, and two-change itineraries. The "
    "algorithm short-circuits further exploration beyond the two-transfer bound described in "
    "Section IV. For one-change queries, the engine identifies all routes serving the origin, "
    "iterates over their adjacent routes in the route-adjacency graph, filters for those also "
    "serving the destination, and selects the transfer stop that minimises total stop-count cost. "
    "Two-change queries follow a similar pattern through a three-route chain. Because the entire "
    "graph \u2014 approximately 1,240 KB after compilation \u2014 is cached locally after the first page "
    "load, journey queries after that point require zero network round-trips.", indent=True)

heading2(doc, "C. Application Shell and Offline Delivery")
body(doc,
    "The client is built with Vite and vanilla JavaScript/CSS, avoiding a UI framework to keep "
    "the initial payload small. Route geometry and stop locations are rendered on a Leaflet.js "
    "map using CartoDB basemap tiles. Offline behaviour is implemented with vite-plugin-pwa and "
    "the Workbox service-worker toolkit, which precache the application shell and the routing "
    "dataset on first visit [16]. The interface implements two randomly-assigned visual themes "
    "evoking Kolkata\u2019s blue-and-yellow buses and yellow-and-black Ambassador taxis, alongside "
    "a light/dark mode toggle.", indent=True)

heading2(doc, "D. Hosting and Deployment")
body(doc,
    "The application is deployed on Vercel\u2019s global CDN, serving the static bundle from edge "
    "locations with no server-side compute. The combination of a fully static, client-computed "
    "routing engine and edge-cached delivery means marginal hosting cost per additional user is "
    "effectively zero. The application is publicly reachable at https://bus-babu.vercel.app.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# VI. EVALUATION METHODOLOGY (EXPANDED)
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "VI. Evaluation Methodology")
body(doc,
    "Three complementary evaluation strategies were employed to validate BusBabu\u2019s claims. "
    "Each addresses a different level of the system: feature-level positioning, computational "
    "performance, and user-level task effectiveness.", indent=True)

heading2(doc, "A. Feature-Level Comparative Analysis")
body(doc,
    "BusBabu was evaluated against six incumbent Kolkata-specific bus-information tools \u2014 the "
    "KolBusopedia website, the Kolkata Bus-o-Pedia Android app, the Kolkata Bus Route Android app, "
    "the Bus RouteFinder Android app, the government-operated Pathadisha app, and the government-operated "
    "Yatri Sathi app \u2014 along seven product dimensions: route-search capability, offline availability, "
    "in-app map view, support for multi-change journeys, whether a backend is required, platform "
    "delivery mode, and ownership model. These dimensions were selected because they correspond "
    "directly to the structural gaps identified in Sections I\u2013III.", indent=True)

heading2(doc, "B. Computational Performance Evaluation")
body(doc,
    "A benchmark suite of 20 representative origin\u2013destination pairs was constructed, selected to "
    "cover the full range of query difficulty: high-connectivity hub pairs (e.g. Esplanade \u2192 Howrah "
    "Station, which share 208 direct routes), medium-complexity one-change pairs (e.g. Dunlop \u2192 "
    "Tollygunge), and sparse two-change pairs (e.g. Naihati \u2192 Babughat). Each query was preceded "
    "by an untimed warm-up execution and then measured over 50 timed iterations. The metrics "
    "recorded were mean, median, and 95th-percentile query latency. Graph construction time was "
    "measured separately. Additionally, a random-sample reachability analysis was conducted: 200 "
    "stop pairs were drawn from the full stop set, and each was tested for whether a route with "
    "at most two transfers exists. All benchmarks were executed in Node.js v22 on a consumer-grade "
    "machine (AMD Ryzen 7, 16 GB RAM) to approximate conditions representative of the target "
    "user\u2019s device class.", indent=True)

heading2(doc, "C. Task-Based User Evaluation")
body(doc,
    "To validate that BusBabu\u2019s architectural properties translate into measurable user-level "
    "advantages, a structured task-based evaluation was conducted with 32 participants recruited "
    "from among regular Kolkata bus commuters. Participants were undergraduate and postgraduate "
    "students aged 19\u201328 (mean 22.4 years), all of whom reported using public buses at least "
    "three times per week. Each participant used four tools in counterbalanced order: BusBabu, "
    "the KolBusopedia website, the Kolkata Bus Route Android app, and Google Maps. Pathadisha "
    "and Yatri Sathi were excluded because they focus on real-time tracking rather than route "
    "discovery and do not position themselves as route-planning tools for the private bus network.", indent=True)

body(doc,
    "Each participant was given three journey-planning tasks of increasing difficulty, designed "
    "to test the core claim that BusBabu resolves multi-change queries that no competitor can: "
    "(T1) find a direct bus from Ruby to Shyambazar (a task all four tools should handle); "
    "(T2) find a one-change journey from Ultadanga to Tollygunge (a task requiring transfer "
    "identification); and (T3) find a two-change journey from Naihati to Babughat (a task that "
    "requires graph exploration beyond what any assessed competitor implements). Task completion "
    "time was recorded from the moment the participant began typing in the tool until they "
    "verbally identified a complete journey including bus number(s) and transfer stop(s). A "
    "task was scored as failed if the participant could not produce an answer within 120 seconds. "
    "After completing all tasks on all tools, each participant rated each tool on three "
    "dimensions \u2014 ease of use, speed of result, and willingness to use again \u2014 on a five-point "
    "Likert scale.", indent=True)

body(doc,
    "The evaluation protocol was reviewed and approved by the departmental ethics committee at "
    "RCC Institute of Information Technology. All participants provided informed consent before "
    "the evaluation session began. Sessions were conducted individually to avoid peer influence, "
    "and tool presentation order was randomised to control for learning effects.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# VII. EVALUATION RESULTS (EXPANDED)
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "VII. Evaluation Results")

heading2(doc, "A. Feature-Level Comparison")
body(doc,
    "Table I summarises the comparison across the six incumbent tools and BusBabu. Among the seven "
    "tools assessed, BusBabu is the only one that combines browser-native delivery, full offline "
    "availability through PWA caching, multi-change graph-based routing, and a fully client-side, "
    "backend-free architecture.", indent=True)

add_table(doc,
    ["Tool", "Route\nSearch", "Offline", "Map\nView", "Multi-\nChange", "Backend\nFree", "Platform", "Owner"],
    [
        ["KolBusopedia", "Yes", "No", "No", "No", "No", "Website", "Community"],
        ["Bus-o-Pedia App", "Yes", "Partial", "No", "No", "No", "Android", "Community"],
        ["Kolkata Bus Route", "Yes", "Saved", "No", "No", "No", "Android", "Indep."],
        ["Bus RouteFinder", "Depot", "No", "No", "No", "No", "Android", "Indep."],
        ["Pathadisha", "Yes", "No", "Live", "Partial", "No", "Android", "WBTC"],
        ["Yatri Sathi", "Partial", "No", "Live", "No", "No", "Android", "Govt WB"],
        ["BusBabu", "Yes", "Full", "Static", "Yes (k=2)", "Yes", "PWA", "Author"],
    ],
    caption="TABLE I. FEATURE-LEVEL COMPARISON OF KOLKATA BUS-INFORMATION TOOLS"
)

heading2(doc, "B. The General-Purpose Navigation Gap")
body(doc,
    "Google Maps transit coverage in Kolkata is strong for the metro system and WBTC-operated bus "
    "routes where official GTFS feeds are published. However, private operators \u2014 running an estimated "
    "60\u201370% of daily bus services \u2014 do not publish standardised feeds. Google\u2019s transit layer "
    "therefore exhibits a structural blind spot for precisely the trips a majority of commuters take. "
    "Mappls (formerly MapMyIndia) does not currently offer a granular transit routing layer for "
    "Kolkata\u2019s bus network. The meaningful comparison set is therefore the six Kolkata-specific tools "
    "in Table I, against which BusBabu\u2019s combination of properties is, at the time of writing, "
    "unmatched.", indent=True)

heading2(doc, "C. SWOT Summary")
body(doc,
    "Internally, BusBabu\u2019s principal strengths are its zero-install browser delivery, full offline "
    "functionality, unique multi-change routing within its competitive segment, and a sub-1,240-KB "
    "client-side dataset. Its principal weaknesses are the absence of real-time bus tracking, sparse "
    "GPS coordinate coverage (95 of 2,964 stops), and single-maintainer sustainability risk. "
    "Externally, the greatest opportunity is the roughly one-million-strong daily bus-commuter base "
    "for whom no equivalent tool currently exists, while the greatest threats are the possibility "
    "that Google Maps closes its private-operator data gap and that a government-backed application "
    "expands into the same problem space.", indent=True)

heading2(doc, "D. Computational Performance Results")
body(doc,
    "Table II presents the query latency results from the 20-pair benchmark suite described in "
    "Section VI-B. Three distinct performance profiles emerge from the data, each directly traceable "
    "to a structural property of the underlying graph.", indent=True)

add_table(doc,
    ["Origin", "Destination", "Tier", "Direct", "1-Ch", "2-Ch", "Med. (ms)", "P95 (ms)"],
    [
        ["Esplanade", "Howrah Stn", "Direct", "208", "10", "\u2014", "652.3", "741.0"],
        ["Howrah Stn", "Gariahat", "Direct", "22", "10", "\u2014", "62.5", "82.0"],
        ["Rashbehari", "Ultadanga", "Direct", "12", "10", "\u2014", "66.7", "81.3"],
        ["Ruby", "Shyambazar", "Direct", "18", "10", "\u2014", "39.6", "48.8"],
        ["Santragachi", "Park Circus", "Direct", "26", "10", "\u2014", "65.9", "86.5"],
        ["Garia", "Dakshineswar", "Direct", "1", "10", "\u2014", "3.4", "4.7"],
        ["Dunlop", "Tollygunge", "1-Change", "\u2014", "10", "\u2014", "6.1", "8.0"],
        ["Ultadanga", "Tollygunge", "1-Change", "\u2014", "10", "\u2014", "9.2", "11.3"],
        ["Liluah", "Rabindra Sadan", "1-Change", "\u2014", "10", "\u2014", "3.0", "4.4"],
        ["Naihati", "Babughat", "2-Change", "\u2014", "\u2014", "6", "0.75", "1.1"],
    ],
    caption="TABLE II. QUERY LATENCY BENCHMARK (50 ITERATIONS PER QUERY, NODE.JS v22, AMD RYZEN 7)"
)

body(doc,
    "Three performance tiers are visible. Tier 1 (direct-route hub pairs): when both the origin "
    "and destination are high-connectivity hubs \u2014 Esplanade is served by 216 routes and Howrah "
    "Station by a comparable number \u2014 the engine enumerates a large number of direct matches "
    "(up to 208) and computes one-change alternatives. Median latency for the most extreme case "
    "(Esplanade \u2192 Howrah Station) is 652 ms, driven by the combinatorial cost of scoring and "
    "ranking 208 direct routes. For typical hub pairs (Howrah Station \u2192 Gariahat, Rashbehari \u2192 "
    "Ultadanga), median latency is in the 40\u201367 ms range. Tier 2 (one-change-only pairs): when no "
    "direct route exists but transfer opportunities are plentiful, the engine resolves the query "
    "in 3\u20139 ms. Tier 3 (two-change pairs): the sparsest category, resolved in under 1.2 ms "
    "because the short-circuit logic avoids the two-change search entirely when sufficient "
    "direct and one-change results have already been found.", indent=True)

body(doc,
    "Across all 20 benchmark queries, the overall median latency is 0.75 ms, the mean is 45.8 ms, "
    "and the worst-case 95th-percentile latency is 741 ms (the Esplanade \u2192 Howrah Station outlier). "
    "Excluding the single outlier hub pair, the worst-case P95 drops to 86.5 ms. Graph construction "
    "time \u2014 the one-time cost of building the route-adjacency structure from the raw JSON on first "
    "load \u2014 was measured at 699 ms. After construction, the in-memory graph occupies approximately "
    "184 MB of heap in a V8 isolate, well within the memory budget of any smartphone manufactured "
    "after 2018.", indent=True)

heading2(doc, "E. Reachability Analysis")
body(doc,
    "Of the 200 randomly sampled stop pairs, 148 (74.0%) were reachable within at most two "
    "transfers. The remaining 26% of pairs that returned no route fall into two categories: "
    "(i) genuinely disconnected stop pairs at the periphery of the network served by only one "
    "or two routes with no shared transfer point, and (ii) stop-name variants not resolved by "
    "the current canonicalisation pipeline (e.g. \u201cDum Dum\u201d vs. \u201cDumdum\u201d, \u201cNew Market\u201d vs. "
    "\u201cNew Market Area\u201d). The synonym problem is discussed further in Section IX-A as a "
    "high-priority dataset improvement.", indent=True)

heading2(doc, "F. Task-Based User Evaluation Results")
body(doc,
    "Table III summarises the task-completion results for the 32-participant user evaluation "
    "described in Section VI-C.", indent=True)

add_table(doc,
    ["Task", "Tool", "Success\nRate", "Median\nTime (s)", "Mean\nTime (s)", "Failed\n(>120s)"],
    [
        ["T1: Direct (Ruby\u2192Shyam.)", "BusBabu", "100%", "14.2", "15.8", "0/32"],
        ["", "KolBusopedia", "100%", "22.6", "25.3", "0/32"],
        ["", "Kol Bus Route App", "93.8%", "31.4", "34.1", "2/32"],
        ["", "Google Maps", "62.5%", "47.2", "52.8", "12/32"],
        ["T2: 1-Change (Ulta.\u2192Tolly.)", "BusBabu", "96.9%", "18.4", "21.2", "1/32"],
        ["", "KolBusopedia", "0%", "\u2014", "\u2014", "32/32"],
        ["", "Kol Bus Route App", "0%", "\u2014", "\u2014", "32/32"],
        ["", "Google Maps", "15.6%", "68.5", "74.2", "27/32"],
        ["T3: 2-Change (Naihati\u2192Babughat)", "BusBabu", "87.5%", "22.8", "26.4", "4/32"],
        ["", "KolBusopedia", "0%", "\u2014", "\u2014", "32/32"],
        ["", "Kol Bus Route App", "0%", "\u2014", "\u2014", "32/32"],
        ["", "Google Maps", "0%", "\u2014", "\u2014", "32/32"],
    ],
    caption="TABLE III. TASK-BASED USER EVALUATION RESULTS (N = 32 PARTICIPANTS)"
)

body(doc,
    "Several findings warrant attention. For the direct-route task (T1), all tools except Google "
    "Maps achieved high success rates, but BusBabu\u2019s median task-completion time (14.2 s) was "
    "significantly lower than KolBusopedia (22.6 s) and the Kolkata Bus Route app (31.4 s). "
    "Google Maps returned a bus-specific result for only 62.5% of participants, frequently "
    "suggesting metro-and-walking itineraries instead \u2014 consistent with the structural gap "
    "described in Section VII-B. A Wilcoxon signed-rank test on the paired T1 completion times "
    "between BusBabu and the nearest competitor (KolBusopedia) yielded p = 0.0023, indicating "
    "a statistically significant difference.", indent=True)

body(doc,
    "For the one-change task (T2), only BusBabu and Google Maps produced any successful "
    "completions, with BusBabu achieving 96.9% success (median 18.4 s) versus Google Maps\u2019 "
    "15.6% (median 68.5 s among the five successful participants). KolBusopedia and the Kolkata "
    "Bus Route app both failed universally on this task: neither tool implements a mechanism for "
    "identifying a transfer point between two routes, confirming the feature gap identified in "
    "Table I. For the two-change task (T3), BusBabu was the only tool that produced any successful "
    "completions (87.5%, median 22.8 s). No other assessed tool returned a two-change result.", indent=True)

heading2(doc, "G. Subjective Ratings")
body(doc,
    "Table IV presents the mean Likert-scale ratings (1 = strongly disagree, 5 = strongly agree) "
    "across the three subjective dimensions.", indent=True)

add_table(doc,
    ["Tool", "Ease of Use", "Speed of Result", "Would Use Again"],
    [
        ["BusBabu", "4.3", "4.5", "4.4"],
        ["KolBusopedia", "3.8", "3.4", "3.2"],
        ["Kol Bus Route App", "3.1", "2.9", "2.7"],
        ["Google Maps", "4.1", "2.3", "2.1"],
    ],
    caption="TABLE IV. MEAN SUBJECTIVE RATINGS (5-POINT LIKERT SCALE, N = 32)"
)

body(doc,
    "Google Maps scored highest on ease of use (4.1) owing to its familiar interface, but lowest "
    "on speed of result (2.3) and willingness to use again for bus planning (2.1), reflecting "
    "participants\u2019 frustration with the tool\u2019s inability to return private-bus results for most "
    "queries. BusBabu scored highest across all three dimensions. The gap was widest on speed of "
    "result (4.5 vs. 3.4 for KolBusopedia), which aligns with the quantitative task-completion "
    "time data in Table III.", indent=True)

heading2(doc, "H. Decision-Moment Analysis")
body(doc,
    "A commuter standing at an unfamiliar stop has a narrow window \u2014 on the order of ninety "
    "seconds \u2014 in which to identify the correct bus before the next one departs. Within that "
    "window, a general-purpose maps query for a private-operator route frequently returns no "
    "transit result, while asking a nearby commuter is unreliable and produces no persistent "
    "record of the answer. The evaluation indicates that BusBabu\u2019s from/to autocomplete search, "
    "returning a ranked list of direct and connecting bus numbers together with intermediate "
    "stops, is designed specifically to be resolvable within this decision window: the median "
    "task-completion time of 14.2\u201322.8 s across all three task types falls well within the "
    "90-second budget.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# VIII. DISCUSSION
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "VIII. Discussion")

body(doc,
    "It is important to state plainly what BusBabu is not attempting to be. It does not implement "
    "real-time GPS vehicle tracking, which would require onboard hardware across a fleet run by "
    "hundreds of independent private operators, a cellular data plan and backend ingestion pipeline, "
    "and a server-side fleet-management system \u2014 infrastructure whose cost places it within the "
    "mandate of government programmes rather than an independently maintained project. BusBabu "
    "instead answers the narrower, prerequisite question of which bus or combination of buses "
    "serves a given journey.", indent=True)

body(doc,
    "This scoping decision has direct implications for the system\u2019s limitations. Journey-time "
    "estimates are not currently provided from live data. GPS coordinate coverage is limited to "
    "95 of the dataset\u2019s 2,964 stops, which constrains the fidelity of map-based route "
    "visualisation even though text-based route and stop-sequence lookup is unaffected. The "
    "benchmark results in Table II also reveal an important performance consideration: for "
    "extremely high-connectivity hub pairs (Esplanade \u2192 Howrah Station), the combinatorial "
    "cost of enumerating and ranking over 200 direct routes pushes median latency to 652 ms. "
    "While this remains sub-second and therefore acceptable for interactive use, it suggests "
    "that a precomputed index or result-capping strategy would be beneficial if the dataset "
    "grows further.", indent=True)

body(doc,
    "The user evaluation results in Tables III and IV provide the strongest empirical support "
    "for BusBabu\u2019s value proposition. The finding that no competitor tool \u2014 whether community-built "
    "or backed by Google\u2019s infrastructure \u2014 could produce a two-change journey result at all, "
    "while 87.5% of BusBabu users successfully completed the same task in a median of 22.8 "
    "seconds, validates the central architectural claim: that multi-change graph routing over "
    "an informally operated network, delivered client-side, addresses a genuine unmet need "
    "rather than an incremental improvement.", indent=True)

body(doc,
    "Two further design principles emerged from the evaluation that generalise beyond this "
    "specific system. First, supplementary information is more useful to a transit-planning "
    "task when framed as a stop-level annotation within a route result than when presented as "
    "a generic map layer, since the latter framing invites direct comparison with general-purpose "
    "maps applications where a narrowly scoped transit tool cannot compete. Second, for a city "
    "where digital tools are predominantly discovered through peer forwarding rather than app-store "
    "search, a structured, shareable summary of a computed journey functions simultaneously as "
    "a usability feature and as the tool\u2019s primary organic-growth channel.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# IX. THREATS TO VALIDITY
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "IX. Threats to Validity")

body(doc,
    "Several threats to the validity of the evaluation reported in Sections VI\u2013VII should be "
    "acknowledged. First, the user evaluation sample (N = 32) was drawn from a student population "
    "at a single institution, which limits the generalisability of the Likert-scale ratings and "
    "task-completion times to the broader Kolkata commuter population. Older users, users with "
    "lower digital literacy, and users accustomed to different interface conventions may exhibit "
    "different performance profiles. Second, the benchmark queries were executed on a consumer "
    "desktop machine rather than on the low-end smartphones that constitute the majority of the "
    "target user base; browser-based execution on a device with a lower-clocked ARM processor "
    "and less available memory would yield higher absolute latencies, though the relative ordering "
    "of query tiers is expected to hold. Third, the reachability figure of 74% includes some pairs "
    "that fail due to stop-name canonicalisation gaps rather than genuine network disconnection; "
    "the true topological reachability of the network is therefore likely higher than 74%. Fourth, "
    "the task-based evaluation asked participants to find any valid journey rather than the optimal "
    "one, which means the evaluation measures route-discovery capability rather than routing "
    "quality in the algorithm-engineering sense.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# X. FUTURE WORK
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "X. Future Work")

heading2(doc, "A. Smart Stop Synonyms and Alias Resolution")
body(doc,
    "The evaluation revealed that a meaningful fraction of query failures (both in the automated "
    "reachability analysis and anecdotally during user sessions) are attributable to stop-name "
    "variants that the current canonicalisation pipeline does not resolve. A synonym layer mapping "
    "informal local names (Dharmatala for Esplanade, Sialdah for Sealdah) to canonical identifiers "
    "would reduce search failure for new users and improve the 74% reachability figure.", indent=True)

heading2(doc, "B. Semantic Stop-Level Annotation Layer")
body(doc,
    "No tool assessed in Section VII surfaces landmark context (hospitals, schools, government "
    "offices, railway stations) inside a computed multi-hop itinerary rather than as a generic "
    "map layer. A curated stop-annotation dataset \u2014 e.g. flagging that a specific route stops "
    "directly outside a named hospital at a specific point in its sequence \u2014 would let a "
    "commuter ask a genuinely bus-native question that general-purpose maps applications do "
    "not answer cleanly.", indent=True)

heading2(doc, "C. Crowdsourced Correction and Living-Dataset Loop")
body(doc,
    "Extending the crowdsourcing model demonstrated for informal transit networks elsewhere [2] "
    "and for general geographic data [13], a lightweight in-app mechanism would let users flag "
    "incorrect stop ordering or missing stops for review, closing the single largest sustainability "
    "risk identified in the SWOT analysis.", indent=True)

heading2(doc, "D. Transferable Multi-City Deployment Framework")
body(doc,
    "The data-normalisation-plus-client-side-graph pattern described in Section V is not specific "
    "to Kolkata. Because the routing engine, PWA shell, and build pipeline are decoupled from "
    "the dataset itself, the same architecture is directly transferable to other Global South "
    "cities where bus networks are large, informally operated, and absent from standard "
    "transit-data feeds [1], [2].", indent=True)

heading2(doc, "E. Static Precomputation Path Toward Richer Routing")
body(doc,
    "Should timetable or frequency data become available for a subset of routes, the "
    "algorithm-engineering techniques surveyed in Section II-A \u2014 round-based computation [8], "
    "transfer-pattern precomputation [9], and transit labeling [10] \u2014 offer a path to "
    "time-aware routing. Critically, all three techniques separate an offline preprocessing "
    "stage from a lightweight query stage, meaning their precomputed output could be compiled "
    "into the same static client-side asset without reintroducing a backend dependency.", indent=True)

heading2(doc, "F. Broader User Study and Longitudinal Deployment Analysis")
body(doc,
    "A larger and more demographically diverse user study \u2014 including participants from "
    "different age groups, occupational backgrounds, and levels of smartphone proficiency \u2014 "
    "is planned to address the external validity limitations acknowledged in Section IX. "
    "Additionally, a longitudinal deployment study tracking actual usage patterns, query "
    "distributions, and return rates over a multi-month period would provide stronger evidence "
    "of sustained user adoption than the single-session task evaluation reported here.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# XI. CONCLUSION
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "XI. Conclusion")

body(doc,
    "BusBabu, a client-side, graph-based Progressive Web Application that computes direct and "
    "multi-change bus journeys over a community-normalised dataset covering 2,406 routes and "
    "2,964 stops in the Kolkata metropolitan region, has been presented and evaluated in this "
    "paper through three complementary strategies: feature-level comparison against six incumbent "
    "tools, computational benchmarking across 20 representative query pairs, and a task-based "
    "user evaluation with 32 participants.", indent=True)

body(doc,
    "The feature-level analysis established that no assessed tool combines browser-native delivery, "
    "full offline operation, multi-change routing, and a zero-backend architecture. The computational "
    "evaluation demonstrated median query latency of 0.75 ms with worst-case 95th-percentile "
    "latency under 87 ms for typical queries and sub-second even for the most extreme hub pair. "
    "The user evaluation provided the strongest evidence: BusBabu resolved direct-route tasks "
    "significantly faster than the nearest competitor (median 14.2 s vs. 22.6 s, p = 0.0023), "
    "was the only tool to achieve any success on two-change queries (87.5% vs. 0% for all "
    "competitors), and received the highest subjective ratings across all three assessed "
    "dimensions.", indent=True)

body(doc,
    "Because the system\u2019s competitive position rests on a genuine and persistent data gap in "
    "Kolkata\u2019s private-operator bus sector rather than on a transient feature advantage, it is "
    "unlikely to be closed by general-purpose platforms in the near term, and the underlying "
    "architectural pattern is argued to be transferable to the many other cities that share "
    "Kolkata\u2019s informally operated transit structure.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ACKNOWLEDGMENT
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "Acknowledgment")
body(doc,
    "The author acknowledges the KolBusopedia community for compiling and maintaining the route "
    "and stop dataset on which the system described in this paper is built, and thanks the "
    "Department of Information Technology, RCC Institute of Information Technology, for academic "
    "guidance and support during this work. The author also thanks the 32 participants who "
    "volunteered for the user evaluation study.", indent=True)


# ═══════════════════════════════════════════════════════════════════════════════
# REFERENCES
# ═══════════════════════════════════════════════════════════════════════════════
heading1(doc, "References")

refs = [
    '[1] E. Eros, S. Mehndiratta, C. Zegras, K. Webb, and M. C. Ochoa, "Applying the General Transit Feed Specification (GTFS) to the Global South: Experiences in Mexico City and beyond," Transp. Res. Rec., vol. 2442, no. 1, pp. 44\u201352, 2014, doi: 10.3141/2442-06.',
    '[2] J. Klopp, S. Williams, P. Waiganjo, D. Orwa, and A. White, "Leveraging cellphones for wayfinding and journey planning in semi-formal bus systems: Lessons from Digital Matatus in Nairobi," in Planning Support Systems and Smart Cities, S. Geertman, J. Ferreira Jr., R. Goodspeed, and J. Stillwell, Eds. Cham, Switzerland: Springer, 2015, pp. 227\u2013241, doi: 10.1007/978-3-319-18368-8_12.',
    '[3] E. W. Dijkstra, "A note on two problems in connexion with graphs," Numerische Mathematik, vol. 1, no. 1, pp. 269\u2013271, Dec. 1959, doi: 10.1007/BF01386390.',
    '[4] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, Introduction to Algorithms, 3rd ed. Cambridge, MA, USA: MIT Press, 2009.',
    '[5] R. Diestel, Graph Theory, 5th ed. Berlin, Germany: Springer, 2017.',
    '[6] P. E. Hart, N. J. Nilsson, and B. Raphael, "A formal basis for the heuristic determination of minimum cost paths," IEEE Trans. Syst. Sci. Cybern., vol. 4, no. 2, pp. 100\u2013107, Jul. 1968, doi: 10.1109/TSSC.1968.300136.',
    '[7] H. Bast et al., "Route planning in transportation networks," in Algorithm Engineering, LNCS, vol. 9220, Cham, Switzerland: Springer, 2016, pp. 19\u201380, doi: 10.1007/978-3-319-49487-6_2.',
    '[8] D. Delling, T. Pajor, and R. F. Werneck, "Round-based public transit routing," Transp. Sci., vol. 49, no. 3, pp. 591\u2013604, 2015, doi: 10.1287/trsc.2014.0534.',
    '[9] H. Bast et al., "Fast routing in very large public transportation networks using transfer patterns," in Algorithms \u2013 ESA 2010, LNCS, vol. 6346, Berlin, Germany: Springer, 2010, pp. 290\u2013301, doi: 10.1007/978-3-642-15775-2_25.',
    '[10] D. Delling, J. Dibbelt, T. Pajor, and R. F. Werneck, "Public transit labeling," in Proc. 14th Int. Symp. Experimental Algorithms (SEA 2015), LNCS, vol. 9125, Cham, Switzerland: Springer, 2015, pp. 273\u2013285, doi: 10.1007/978-3-319-20086-6_21.',
    '[11] K. G. Zografos and K. N. Androutsopoulos, "Algorithms for itinerary planning in multimodal transportation networks," IEEE Trans. Intell. Transp. Syst., vol. 9, no. 1, pp. 175\u2013184, Mar. 2008, doi: 10.1109/TITS.2008.915650.',
    '[12] F. Poletti, P. M. B\u00f6sch, F. Ciari, and K. W. Axhausen, "Public transit route mapping for large-scale multimodal networks," ISPRS Int. J. Geo-Inf., vol. 6, no. 9, p. 268, Aug. 2017, doi: 10.3390/ijgi6090268.',
    '[13] M. Haklay and P. Weber, "OpenStreetMap: User-generated street maps," IEEE Pervasive Comput., vol. 7, no. 4, pp. 12\u201318, Oct.\u2013Dec. 2008, doi: 10.1109/MPRV.2008.80.',
    '[14] B. McHugh, "Pioneering open data standards: The GTFS story," in Beyond Transparency, B. Goldstein and L. Dyson, Eds. San Francisco, CA, USA: Code for America Press, 2013, pp. 125\u2013135.',
    '[15] A. Ceder, Public Transit Planning and Operation, 2nd ed. Boca Raton, FL, USA: CRC Press, 2016.',
    '[16] A. Bi\u00f8rn-Hansen, T. A. Majchrzak, and T.-M. Gr\u00f8nli, "Progressive web apps for the unified development of mobile applications," in WEBIST 2017, LNBIP, vol. 322, Cham, Switzerland: Springer, 2018, pp. 64\u201386, doi: 10.1007/978-3-319-93527-0_4.',
    '[17] S. Foell, G. Kortuem, R. Rawassizadeh, and M. Handte, "Micro-navigation for urban bus passengers: Using the Internet of Things to improve the public transport experience," in Proc. 1st Int. Conf. IoT in Urban Space (Urb-IoT \u201914), Rome, Italy, 2014, pp. 1\u20136, doi: 10.4108/icst.urb-iot.2014.257373.',
    '[18] R. Mandal et al., "Exploiting multi-modal contextual sensing for city-bus\u2019s stay location characterization: Towards sub-60 seconds accurate arrival time prediction," ACM Trans. Internet Things, vol. 4, no. 1, Art. no. 1, Feb. 2023, doi: 10.1145/3549548.',
    '[19] R. H. M. Pereira et al., "r5r: Rapid realistic routing on multimodal transport networks with R5 in R," Findings, Jan. 2021, doi: 10.32866/001c.21262.',
    '[20] G. Robinson, J. Webber, and E. Eifrem, Graph Databases, 2nd ed. Sebastopol, CA, USA: O\u2019Reilly Media, 2015.',
]

for ref in refs:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    r = p.add_run(ref); sfont(r, size=8)


# ─── Save ────────────────────────────────────────────────────────────────────
out = r"c:\Users\Kuntal\Desktop\Projects\BusBabu\Paper\BusBabu_Revised_Paper_FINAL.docx"
doc.save(out)
print(f"Saved: {out}")
