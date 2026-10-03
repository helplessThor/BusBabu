#!/usr/bin/env python3
"""
Generate UEMCOS 2026 Conference Presentation for BusBabu Paper.
Creates:
  1. BusBabu_UEMCOS_2026_Presentation.pptx  – the slide deck
  2. BusBabu_UEMCOS_2026_Speaker_Notes.pptx  – same deck with detailed speaker notes per slide
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os, textwrap

BASE = r"c:\Users\Kuntal\Desktop\Projects\BusBabu"
PAPER_DIR = os.path.join(BASE, "Paper")
LOGO = os.path.join(BASE, "public", "img", "busbabu.png")

# ── colour palette (BusBabu brand: blue-yellow bus theme) ──
C_DARK     = RGBColor(0x0D, 0x1B, 0x2A)   # deep navy
C_BLUE     = RGBColor(0x1B, 0x4F, 0x72)   # medium blue
C_ACCENT   = RGBColor(0xF0, 0xC8, 0x08)   # bus-yellow
C_WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
C_LIGHT    = RGBColor(0xEC, 0xF0, 0xF1)
C_TEXT     = RGBColor(0x2C, 0x3E, 0x50)
C_RED      = RGBColor(0xE7, 0x4C, 0x3C)
C_GREEN    = RGBColor(0x27, 0xAE, 0x60)
C_GREY     = RGBColor(0x95, 0xA5, 0xA6)


def fill_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text, font_size=18,
                bold=False, color=C_WHITE, align=PP_ALIGN.LEFT, font_name="Calibri"):
    txBox = slide.shapes.add_textbox(Emu(left), Emu(top), Emu(width), Emu(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = align
    return txBox


def add_bullet_slide(slide, items, left, top, width, height,
                     font_size=16, color=C_WHITE, bullet="•", spacing=Pt(8)):
    txBox = slide.shapes.add_textbox(Emu(left), Emu(top), Emu(width), Emu(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"{bullet}  {item}"
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.space_after = spacing
    return txBox


def add_rect(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                   Emu(left), Emu(top), Emu(width), Emu(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


def add_rounded_rect(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   Emu(left), Emu(top), Emu(width), Emu(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


def make_section_title(slide, section_num, title, subtitle=""):
    fill_bg(slide, C_DARK)
    # accent bar
    add_rect(slide, 0, Inches(2.8).emu, Inches(10).emu, Inches(0.06).emu, C_ACCENT)
    add_textbox(slide, Inches(0.8).emu, Inches(1.8).emu, Inches(8.4).emu, Inches(0.6).emu,
                f"SECTION {section_num}", 14, True, C_ACCENT, PP_ALIGN.LEFT)
    add_textbox(slide, Inches(0.8).emu, Inches(2.2).emu, Inches(8.4).emu, Inches(0.8).emu,
                title, 36, True, C_WHITE, PP_ALIGN.LEFT)
    if subtitle:
        add_textbox(slide, Inches(0.8).emu, Inches(3.0).emu, Inches(8.4).emu, Inches(0.6).emu,
                    subtitle, 16, False, C_GREY, PP_ALIGN.LEFT)


def std_header(slide, title, subtitle=""):
    fill_bg(slide, C_DARK)
    # top accent line
    add_rect(slide, 0, 0, Inches(10).emu, Inches(0.06).emu, C_ACCENT)
    add_textbox(slide, Inches(0.6).emu, Inches(0.2).emu, Inches(8.8).emu, Inches(0.55).emu,
                title, 26, True, C_WHITE, PP_ALIGN.LEFT)
    if subtitle:
        add_textbox(slide, Inches(0.6).emu, Inches(0.7).emu, Inches(8.8).emu, Inches(0.35).emu,
                    subtitle, 13, False, C_ACCENT, PP_ALIGN.LEFT)
    # bottom line
    add_rect(slide, Inches(0.6).emu, Inches(0.95).emu, Inches(8.8).emu, Inches(0.02).emu, C_BLUE)


# ──────────────────────────────────────────────────────────────
#  SLIDES DATA – every slide is (builder_function, speaker_notes)
# ──────────────────────────────────────────────────────────────

def build_slides(prs):
    slides_data = []
    W = Inches(10).emu
    H = Inches(7.5).emu

    # ═══════════════════  SLIDE 1: TITLE  ═══════════════════
    def slide_title(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])  # blank
        fill_bg(sl, C_DARK)
        # yellow top bar
        add_rect(sl, 0, 0, W, Inches(0.08).emu, C_ACCENT)
        # logo
        if os.path.exists(LOGO):
            sl.shapes.add_picture(LOGO, Inches(3.6).emu, Inches(0.3).emu,
                                  Inches(2.8).emu, Inches(2.8).emu)
        # title
        add_textbox(sl, Inches(0.5).emu, Inches(3.2).emu, Inches(9).emu, Inches(0.8).emu,
                    "BusBabu", 44, True, C_ACCENT, PP_ALIGN.CENTER)
        add_textbox(sl, Inches(0.5).emu, Inches(3.9).emu, Inches(9).emu, Inches(0.7).emu,
                    "A Zero-Backend, Client-Side Graph Routing Solution\nfor Informally Operated Bus Networks in Kolkata",
                    18, False, C_WHITE, PP_ALIGN.CENTER)
        # conference
        add_textbox(sl, Inches(0.5).emu, Inches(5.0).emu, Inches(9).emu, Inches(0.35).emu,
                    "UEMCOS 2026  •  Paper Presentation Session", 14, True, C_GREY, PP_ALIGN.CENTER)
        # authors
        add_textbox(sl, Inches(0.5).emu, Inches(5.6).emu, Inches(9).emu, Inches(0.4).emu,
                    "Kuntal Paul", 16, True, C_WHITE, PP_ALIGN.CENTER)
        add_textbox(sl, Inches(0.5).emu, Inches(6.0).emu, Inches(9).emu, Inches(0.35).emu,
                    "Department of Information Technology\nRCC Institute of Information Technology, Kolkata",
                    12, False, C_GREY, PP_ALIGN.CENTER)
        # bottom bar
        add_rect(sl, 0, Inches(7.42).emu, W, Inches(0.08).emu, C_ACCENT)
        return sl

    notes_title = """[~30 seconds]
Good morning/afternoon, respected jury members and fellow delegates. My name is Kuntal Paul from RCCIIT, Dept of IT.

Today I'm presenting our paper — "BusBabu: A Zero-Backend, Client-Side Graph Routing Solution for Informally Operated Bus Networks in the Kolkata Metropolitan Region."

This work addresses a very real, everyday problem that millions of Kolkata commuters face. Let me walk you through it."""
    slides_data.append((slide_title, notes_title))

    # ═══════════════════  SLIDE 2: AGENDA  ═══════════════════
    def slide_agenda(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        std_header(sl, "Presentation Outline")
        items = [
            "Problem Statement & Motivation",
            "Market Study & Existing Solutions",
            "Gap Analysis – What's Missing",
            "Our Solution: BusBabu",
            "System Architecture & Workflow",
            "Benchmark & Performance Results",
            "Feasibility Study",
            "Future Scope & Business Potential",
        ]
        for i, item in enumerate(items):
            y = Inches(1.2 + i * 0.65).emu
            # number circle
            add_rounded_rect(sl, Inches(0.8).emu, y, Inches(0.5).emu, Inches(0.5).emu, C_ACCENT)
            add_textbox(sl, Inches(0.8).emu, y, Inches(0.5).emu, Inches(0.5).emu,
                        str(i+1), 16, True, C_DARK, PP_ALIGN.CENTER)
            add_textbox(sl, Inches(1.5).emu, y, Inches(7).emu, Inches(0.5).emu,
                        item, 18, False, C_WHITE, PP_ALIGN.LEFT)
        return sl

    notes_agenda = """[~20 seconds]
Here's what we'll cover in the next 10 minutes. I'll start with the problem, move through market analysis, explain our solution and architecture, show real benchmark data, and finish with future scope.

Let me begin with the problem."""
    slides_data.append((slide_agenda, notes_agenda))

    # ═══════════════════  SLIDE 3: PROBLEM STATEMENT  ═══════════════════
    def slide_problem(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        make_section_title(sl, "01", "The Problem", "Why Kolkata's bus commuters are underserved")
        # stats boxes below
        stats = [
            ("10 Lakh+", "daily bus\npassengers"),
            ("48%", "commuters use\nbuses primarily"),
            ("60–70%", "routes run by\nprivate operators"),
            ("Zero", "standardised\ndigital feed"),
        ]
        for i, (big, small) in enumerate(stats):
            x = Inches(0.6 + i * 2.3).emu
            add_rounded_rect(sl, x, Inches(4.0).emu, Inches(2.0).emu, Inches(1.6).emu, C_BLUE)
            add_textbox(sl, x, Inches(4.15).emu, Inches(2.0).emu, Inches(0.6).emu,
                        big, 28, True, C_ACCENT, PP_ALIGN.CENTER)
            add_textbox(sl, x, Inches(4.75).emu, Inches(2.0).emu, Inches(0.6).emu,
                        small, 12, False, C_WHITE, PP_ALIGN.CENTER)
        # source
        add_textbox(sl, Inches(0.6).emu, Inches(5.85).emu, Inches(8.5).emu, Inches(0.3).emu,
                    "Sources: WBTC Annual Reports 2023–24; TOI Kolkata Bus Census 2024", 9, False, C_GREY, PP_ALIGN.LEFT)
        return sl

    notes_problem = """[~60 seconds]
Kolkata operates one of the largest and most fragmented urban bus networks in South Asia. Over 10 lakh passengers board buses daily. 48% of commuters use buses as their primary mode.

Here's the critical issue: 60 to 70 percent of daily bus services are run by private operators — hundreds of small, independent owners. And NONE of them publish their route data in any standard digital format like GTFS.

What this means is — Google Maps, Apple Maps, any mainstream navigation app — they have a structural blind spot. They simply cannot show you private bus routes because the data doesn't exist in their systems.

So how do people figure out which bus to take? Word of mouth. You stand at a stop, ask someone. This oral knowledge economy is fragile, non-searchable, and completely inaccessible to anyone new to the city.

A 2024 assessment found 2,185 buses withdrawn from Kolkata roads in a single year against only 154 new registrations. The network is shrinking, and the information problem is getting worse."""
    slides_data.append((slide_problem, notes_problem))

    # ═══════════════════  SLIDE 4: THE DATA GAP  ═══════════════════
    def slide_data_gap(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        std_header(sl, "The Structural Data Gap", "Why Google Maps fails for Kolkata buses")
        # visual comparison
        # left box - Google Maps
        add_rounded_rect(sl, Inches(0.6).emu, Inches(1.3).emu, Inches(4.1).emu, Inches(3.0).emu, RGBColor(0x17, 0x17, 0x20))
        add_textbox(sl, Inches(0.8).emu, Inches(1.4).emu, Inches(3.7).emu, Inches(0.4).emu,
                    "Google Maps / Mainstream Apps", 14, True, C_RED, PP_ALIGN.CENTER)
        items_left = [
            "Only shows Metro + some WBTC routes",
            "Suggests walking / auto for bus-served trips",
            "No private-operator data at all",
            "Requires GTFS feed — not available",
        ]
        for i, item in enumerate(items_left):
            add_textbox(sl, Inches(0.9).emu, Inches(1.9 + i * 0.55).emu, Inches(3.6).emu, Inches(0.5).emu,
                        f"✗  {item}", 12, False, C_LIGHT, PP_ALIGN.LEFT)
        # right box - BusBabu
        add_rounded_rect(sl, Inches(5.3).emu, Inches(1.3).emu, Inches(4.1).emu, Inches(3.0).emu, RGBColor(0x17, 0x17, 0x20))
        add_textbox(sl, Inches(5.5).emu, Inches(1.4).emu, Inches(3.7).emu, Inches(0.4).emu,
                    "BusBabu", 14, True, C_GREEN, PP_ALIGN.CENTER)
        items_right = [
            "2,406 routes including private operators",
            "Direct + 1-change + 2-change journeys",
            "Works fully offline after first load",
            "Community-normalised dataset",
        ]
        for i, item in enumerate(items_right):
            add_textbox(sl, Inches(5.5).emu, Inches(1.9 + i * 0.55).emu, Inches(3.6).emu, Inches(0.5).emu,
                        f"✓  {item}", 12, False, C_LIGHT, PP_ALIGN.LEFT)
        # key insight
        add_rounded_rect(sl, Inches(0.6).emu, Inches(4.6).emu, Inches(8.8).emu, Inches(1.2).emu, C_BLUE)
        add_textbox(sl, Inches(0.8).emu, Inches(4.7).emu, Inches(8.4).emu, Inches(1.0).emu,
                    "Key Insight: The problem is not absence of bus services.\nIt is absence of machine-readable data for those services.\nThis is a data gap, not a supply gap.",
                    14, True, C_WHITE, PP_ALIGN.CENTER)
        # source
        add_textbox(sl, Inches(0.6).emu, Inches(6.0).emu, Inches(8.8).emu, Inches(0.3).emu,
                    "Reference: Eros et al., Transp. Res. Rec. 2014; Klopp et al., Digital Matatu 2015 — documented same gap in Mexico City & Nairobi",
                    9, False, C_GREY, PP_ALIGN.LEFT)
        return sl

    notes_data_gap = """[~45 seconds]
Let me make this concrete. When you search Howrah to Gariahat on Google Maps, it may suggest Metro plus walking. But any Kolkata commuter knows there are direct buses — route 12C/1B, or route 3B with a change at Rashbehari.

Google can't show these because private operators don't publish GTFS feeds. This is not unique to Kolkata — the same gap has been documented in Nairobi's matatu network and Mexico City's pesero system.

The key insight in our paper: the problem is not an absence of bus services. It is an absence of machine-readable data for those services. A data gap, not a supply gap.

BusBabu closes this gap by compiling community-normalised route data into a searchable, offline-capable routing engine."""
    slides_data.append((slide_data_gap, notes_data_gap))

    # ═══════════════════  SLIDE 5: MARKET STUDY  ═══════════════════
    def slide_market(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        std_header(sl, "Market Study & Existing Solutions", "Six incumbent tools assessed (Table I in Paper)")
        # Table header
        cols = ["Tool", "Route\nSearch", "Offline", "Map", "Multi-\nChange", "Zero\nBackend", "Platform"]
        col_widths = [1.8, 0.85, 0.85, 0.75, 0.85, 0.85, 1.1]
        y_start = Inches(1.2).emu
        row_h = Inches(0.42).emu
        x_start = Inches(0.5).emu

        # header row
        x = x_start
        for j, col in enumerate(cols):
            w = Inches(col_widths[j]).emu
            add_rounded_rect(sl, x, y_start, w, row_h, C_ACCENT)
            add_textbox(sl, x, y_start, w, row_h, col, 9, True, C_DARK, PP_ALIGN.CENTER)
            x += w

        # data rows
        rows = [
            ["KolBusopedia Web", "✓", "✗", "✗", "✗", "✗", "Browser"],
            ["KolBusopedia App", "✓", "Partial", "✗", "✗", "✗", "Android"],
            ["Kolkata Bus Route", "✓", "✗", "✗", "✗", "✗", "Android"],
            ["Bus RouteFinder", "✓", "✗", "✓", "✗", "✗", "Android"],
            ["Pathadisha (Govt)", "✓", "✗", "✓", "Partial", "✗", "Android"],
            ["Yatri Sathi (Govt)", "✓", "✗", "✓", "✗", "✗", "Android"],
            ["BusBabu (Ours)", "✓", "✓", "✓", "✓", "✓", "PWA/Any"],
        ]
        for i, row in enumerate(rows):
            y = y_start + (i + 1) * row_h
            bg = RGBColor(0x16, 0x3A, 0x5F) if i < 6 else C_GREEN
            x = x_start
            for j, cell in enumerate(row):
                w = Inches(col_widths[j]).emu
                add_rounded_rect(sl, x, y, w, row_h, bg)
                c = C_WHITE
                if cell == "✗": c = C_RED
                elif cell == "✓" and i < 6: c = RGBColor(0x80, 0xCC, 0x80)
                elif cell == "Partial": c = C_ACCENT
                add_textbox(sl, x, y, w, row_h, cell, 9, (i == 6), c, PP_ALIGN.CENTER)
                x += w

        add_textbox(sl, Inches(0.5).emu, Inches(5.2).emu, Inches(9).emu, Inches(0.4).emu,
                    "→  BusBabu is the ONLY tool combining: browser delivery + full offline + multi-change routing + zero backend",
                    13, True, C_ACCENT, PP_ALIGN.LEFT)
        add_textbox(sl, Inches(0.5).emu, Inches(5.7).emu, Inches(9).emu, Inches(0.3).emu,
                    "Source: Table I, BusBabu IEEE Paper (2026); assessment conducted Jan–Aug 2026", 9, False, C_GREY, PP_ALIGN.LEFT)
        return sl

    notes_market = """[~60 seconds]
We conducted a systematic comparison of six existing Kolkata-specific bus tools across six product dimensions. This is Table I from our paper.

Let me highlight the key findings:

KolBusopedia — excellent data source, but no offline, no map, no multi-change routing. It's a search tool, not a routing engine.

Pathadisha — the strongest government competitor. It has live GPS tracking, partial multi-change support, but requires Android installation, a maintained backend, and does not work offline.

Yatri Sathi — government-operated, live tracking, but again Android-only, backend-dependent, no multi-change routing.

All the community apps — Bus RouteFinder, Kolkata Bus Route — they offer route search but none implement multi-change routing, offline caching, and zero-backend simultaneously.

BusBabu is the only tool that combines ALL five: browser-native delivery, full offline, map view, multi-change routing, and a zero-backend architecture. This is our central competitive finding."""
    slides_data.append((slide_market, notes_market))

    # ═══════════════════  SLIDE 6: OUR SOLUTION  ═══════════════════
    def slide_solution(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        make_section_title(sl, "02", "Our Solution: BusBabu", "A zero-infrastructure, offline-first transit routing engine")
        # 3 key pillars
        pillars = [
            ("Community Data\n→ Routing Graph", "2,406 routes, 2,964 stops\nnormalised from KolBusopedia\n+ Bus Repository corpus"),
            ("Client-Side\nBFS Engine", "Direct, 1-change, 2-change\njourneys computed entirely\nin the browser — no server"),
            ("Installable\nOffline PWA", "Service Worker caches all\nassets + data on first visit\n— works without internet"),
        ]
        for i, (title, desc) in enumerate(pillars):
            x = Inches(0.5 + i * 3.15).emu
            add_rounded_rect(sl, x, Inches(4.0).emu, Inches(2.9).emu, Inches(2.4).emu, C_BLUE)
            add_textbox(sl, x, Inches(4.15).emu, Inches(2.9).emu, Inches(0.7).emu,
                        title, 14, True, C_ACCENT, PP_ALIGN.CENTER)
            add_textbox(sl, x, Inches(4.9).emu, Inches(2.9).emu, Inches(1.2).emu,
                        desc, 11, False, C_WHITE, PP_ALIGN.CENTER)
        return sl

    notes_solution = """[~40 seconds]
BusBabu rests on three pillars:

FIRST — Data. We take community-normalised route data from KolBusopedia and a wider bus repository, and compile it through a Python pipeline that canonicalises thousands of inconsistent stop names into a single graph. Currently: 2,406 routes, 2,964 unique stops.

SECOND — Engine. A bounded-hop BFS engine runs entirely in your browser. Given origin and destination, it explores the adjacency graph and returns direct, one-change, and two-change itineraries. No server call needed.

THIRD — Delivery. It's a Progressive Web App. Service Worker caches everything on first visit. After that — full offline. No install from Play Store needed. Works on any device with a browser."""
    slides_data.append((slide_solution, notes_solution))

    # ═══════════════════  SLIDE 7: ARCHITECTURE  ═══════════════════
    def slide_architecture(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        std_header(sl, "System Architecture", "Section V of Paper")
        # Pipeline flow: boxes with arrows
        stages = [
            ("Raw Route\nDumps", "JSON + TXT\nKolBusopedia\nBus Repository", C_BLUE),
            ("Python Build\nPipeline", "Stop canonicalisation\nGraph construction\nCoord interpolation", RGBColor(0x8E, 0x44, 0xAD)),
            ("busdata.json\n(Static Asset)", "2,406 routes\n2,964 stops\n< 350 KB", C_GREEN),
            ("Browser\nRouting Engine", "BFS traversal\n0-/1-/2-transfer\nFull client-side", C_ACCENT),
        ]
        for i, (title, desc, color) in enumerate(stages):
            x = Inches(0.35 + i * 2.45).emu
            add_rounded_rect(sl, x, Inches(1.3).emu, Inches(2.15).emu, Inches(2.2).emu, color)
            add_textbox(sl, x, Inches(1.4).emu, Inches(2.15).emu, Inches(0.7).emu,
                        title, 13, True, C_WHITE if color != C_ACCENT else C_DARK, PP_ALIGN.CENTER)
            add_textbox(sl, x, Inches(2.1).emu, Inches(2.15).emu, Inches(1.2).emu,
                        desc, 10, False, C_WHITE if color != C_ACCENT else C_DARK, PP_ALIGN.CENTER)
            # arrow
            if i < 3:
                ax = Inches(0.35 + (i+1) * 2.45 - 0.2).emu
                add_textbox(sl, ax, Inches(2.1).emu, Inches(0.3).emu, Inches(0.5).emu,
                            "→", 24, True, C_ACCENT, PP_ALIGN.CENTER)
        # PWA layer below
        add_rounded_rect(sl, Inches(0.35).emu, Inches(3.9).emu, Inches(9.3).emu, Inches(1.3).emu, RGBColor(0x17, 0x17, 0x20))
        add_textbox(sl, Inches(0.5).emu, Inches(4.0).emu, Inches(9.0).emu, Inches(0.4).emu,
                    "PWA Shell: Vite + Vanilla JS/CSS  |  Leaflet.js Map  |  Workbox Service Worker  |  Vercel CDN (edge-cached)",
                    12, True, C_ACCENT, PP_ALIGN.CENTER)
        add_textbox(sl, Inches(0.5).emu, Inches(4.5).emu, Inches(9.0).emu, Inches(0.5).emu,
                    "• Zero server-side compute  • Zero cold-start latency  • Zero marginal hosting cost per user\n• Precached on first visit — every subsequent query is local, offline-capable",
                    11, False, C_WHITE, PP_ALIGN.CENTER)
        # Key metrics
        add_textbox(sl, Inches(0.5).emu, Inches(5.5).emu, Inches(9).emu, Inches(0.35).emu,
                    "Graph: 2,964 vertices  |  53,847 edges  |  Avg adjacency: 644.2  |  Build time: 699 ms  |  Dataset: < 350 KB",
                    11, True, C_ACCENT, PP_ALIGN.LEFT)
        return sl

    notes_arch = """[~60 seconds]
Here's the full architecture, corresponding to Section V of the paper.

Stage 1: Raw route dumps. JSON arrays and text files from KolBusopedia and community repositories. Messy, inconsistent spellings — Rashbehari vs Rashbihari vs Rasbehari — hundreds of such variants.

Stage 2: Our Python build pipeline. It does three things — canonicalises stop names using a spelling dictionary of 130+ entries, constructs the adjacency graph from consecutive stop pairs, and interpolates GPS coordinates.

Stage 3: Output is a single static JSON file — busdata.json — under 350 KB. This is the entire routing graph. 2,964 vertices, 53,847 edges.

Stage 4: This JSON is loaded once in the browser, and our BFS engine searches it. Direct routes, one-change, two-change — all computed locally.

The bottom layer is the PWA shell — Vite build, vanilla JS, Leaflet maps, Workbox service worker for offline caching, deployed on Vercel's CDN.

The result: zero server compute, zero cold-start, zero marginal cost per user. A genuinely zero-infrastructure transit tool."""
    slides_data.append((slide_architecture, notes_arch))

    # ═══════════════════  SLIDE 8: LIVE APP DEMO  ═══════════════════
    def slide_demo(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        std_header(sl, "Live Application", "https://bus-babu.vercel.app/")
        # screenshots
        screenshots = [
            ("screenshot_landing.png", "Landing Page"),
            ("screenshot_results.png", "Search Results"),
            ("screenshot_route_detail.png", "Route Details + Map"),
        ]
        for i, (fname, label) in enumerate(screenshots):
            path = os.path.join(PAPER_DIR, fname)
            x = Inches(0.3 + i * 3.2).emu
            if os.path.exists(path):
                sl.shapes.add_picture(path, Emu(x), Inches(1.2).emu,
                                      Inches(3.0).emu, Inches(4.8).emu)
            add_textbox(sl, x, Inches(6.1).emu, Inches(3.0).emu, Inches(0.35).emu,
                        label, 11, True, C_ACCENT, PP_ALIGN.CENTER)
        add_textbox(sl, Inches(0.5).emu, Inches(6.6).emu, Inches(9).emu, Inches(0.3).emu,
                    "Live at: bus-babu.vercel.app  •  Screenshots captured September 2026", 9, False, C_GREY, PP_ALIGN.LEFT)
        return sl

    notes_demo = """[~30 seconds]
Here are screenshots from the live application, deployed and accessible right now at bus-babu.vercel.app.

Left — the landing page with autocomplete search. Users type source and destination.

Center — search results showing direct routes, one-change options, sorted by transfer count.

Right — route details with map view showing the path, intermediate stops, and transfer points.

The app implements two random visual themes — blue-yellow bus theme and yellow-black taxi theme — with dark mode toggle. It's installable on any device as a PWA."""
    slides_data.append((slide_demo, notes_demo))

    # ═══════════════════  SLIDE 9: BENCHMARKS  ═══════════════════
    def slide_benchmarks(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        std_header(sl, "Performance Benchmarks", "Table II in Paper — 20 O-D pairs × 50 iterations each")
        # benchmark table
        cols = ["Metric", "Value"]
        data = [
            ("Graph Build Time", "699 ms (one-time, on page load)"),
            ("Median Query Latency", "0.75 ms"),
            ("Mean Query Latency", "45.8 ms (skewed by hub outliers)"),
            ("P95 Latency (excl. outliers)", "86.5 ms"),
            ("Worst-Case (Esplanade hub)", "208 ms (explores 644 adjacencies)"),
            ("Network Reachability (2 transfers)", "74% of random O-D pairs"),
            ("Dataset Size (compressed)", "< 350 KB"),
            ("Memory Footprint", "~4 MB in-browser"),
        ]
        y = Inches(1.3).emu
        for i, (metric, value) in enumerate(data):
            row_y = y + i * Inches(0.55).emu
            bg = C_BLUE if i % 2 == 0 else RGBColor(0x16, 0x3A, 0x5F)
            add_rounded_rect(sl, Inches(0.5).emu, row_y, Inches(4.0).emu, Inches(0.48).emu, bg)
            add_textbox(sl, Inches(0.6).emu, row_y, Inches(3.8).emu, Inches(0.48).emu,
                        metric, 12, True, C_WHITE, PP_ALIGN.LEFT)
            add_rounded_rect(sl, Inches(4.5).emu, row_y, Inches(5.0).emu, Inches(0.48).emu, bg)
            add_textbox(sl, Inches(4.6).emu, row_y, Inches(4.8).emu, Inches(0.48).emu,
                        value, 12, False, C_ACCENT, PP_ALIGN.LEFT)
        add_textbox(sl, Inches(0.5).emu, Inches(5.9).emu, Inches(9).emu, Inches(0.3).emu,
                    "Source: BusBabu Benchmark Suite (benchmark.mjs), Node.js v22, August 2026. Warm-up run excluded.",
                    9, False, C_GREY, PP_ALIGN.LEFT)
        # takeaway
        add_rounded_rect(sl, Inches(0.5).emu, Inches(6.3).emu, Inches(9.0).emu, Inches(0.6).emu, C_GREEN)
        add_textbox(sl, Inches(0.7).emu, Inches(6.35).emu, Inches(8.6).emu, Inches(0.5).emu,
                    "Takeaway: Sub-millisecond median latency. 90-second commuter decision window is comfortably met.",
                    13, True, C_WHITE, PP_ALIGN.CENTER)
        return sl

    notes_benchmarks = """[~50 seconds]
These are real benchmark numbers from our automated test suite — not theoretical estimates.

We ran 20 origin-destination pairs, 50 iterations each, with a warm-up run excluded.

Graph builds in 699 milliseconds on page load — that's a one-time cost.

After that, median query latency is 0.75 milliseconds. Less than one millisecond to compute a multi-change journey.

Mean is higher — 45.8 ms — because hub stops like Esplanade with 208 direct routes create outlier queries. But even worst-case is 208 ms.

Network reachability: 74% of random origin-destination pairs can be connected within 2 transfers. The 26% failures are primarily due to stop-name synonym mismatches — we identify that as a known limitation.

The key takeaway: a commuter's decision window at a bus stop is roughly 90 seconds. Our engine responds in under 1 millisecond. That's several orders of magnitude of headroom."""
    slides_data.append((slide_benchmarks, notes_benchmarks))

    # ═══════════════════  SLIDE 10: FEASIBILITY  ═══════════════════
    def slide_feasibility(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        std_header(sl, "Feasibility Study", "Technical, Economic, and Operational viability")
        # 3 columns
        categories = [
            ("Technical\nFeasibility", [
                "Runs on ANY browser (Chrome, Safari, Firefox)",
                "No native app install needed",
                "Entire stack: HTML + JS + CSS",
                "Dataset < 350 KB — loads on 2G",
                "Offline-first via Service Worker",
            ], C_BLUE),
            ("Economic\nFeasibility", [
                "Zero hosting cost (Vercel free tier)",
                "Zero server infrastructure",
                "Zero per-user marginal cost",
                "No cloud compute needed",
                "Sustainable without funding",
            ], C_GREEN),
            ("Operational\nFeasibility", [
                "Single-maintainer viable",
                "Dataset updated via build script",
                "Community data source (KolBusopedia)",
                "Incremental route additions",
                "No fleet coordination required",
            ], RGBColor(0x8E, 0x44, 0xAD)),
        ]
        for i, (title, items, color) in enumerate(categories):
            x = Inches(0.35 + i * 3.15).emu
            add_rounded_rect(sl, x, Inches(1.2).emu, Inches(2.95).emu, Inches(4.3).emu, color)
            add_textbox(sl, x, Inches(1.3).emu, Inches(2.95).emu, Inches(0.65).emu,
                        title, 14, True, C_WHITE, PP_ALIGN.CENTER)
            for j, item in enumerate(items):
                add_textbox(sl, Emu(x + Inches(0.15).emu), Inches(2.0 + j * 0.6).emu,
                            Inches(2.65).emu, Inches(0.55).emu,
                            f"✓  {item}", 10, False, C_WHITE, PP_ALIGN.LEFT)
        return sl

    notes_feasibility = """[~40 seconds]
Three dimensions of feasibility:

TECHNICAL — it's a web app. Runs on any browser on any device. The entire dataset is under 350 KB, small enough to load even on 2G networks. After first load, everything is cached locally by the Service Worker. No native install, no Play Store dependency.

ECONOMIC — this is perhaps BusBabu's strongest argument. Zero hosting cost — we're on Vercel's free tier. Zero server infrastructure. Zero per-user marginal cost. Because everything runs client-side, adding a million users doesn't cost us a single rupee more. This makes the project sustainable without institutional funding.

OPERATIONAL — a single maintainer can run this. When routes change, we update the raw data files and run the build script. The Python pipeline normalises everything and outputs a fresh busdata.json. No fleet coordination, no GPS hardware, no backend to maintain."""
    slides_data.append((slide_feasibility, notes_feasibility))

    # ═══════════════════  SLIDE 11: SWOT  ═══════════════════
    def slide_swot(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        std_header(sl, "SWOT Analysis", "Section VII-C of Paper")
        quadrants = [
            ("Strengths", [
                "Zero-install browser delivery",
                "Full offline functionality",
                "Unique multi-change routing",
                "Zero backend architecture",
                "Sub-350 KB lightweight dataset",
            ], C_GREEN, 0.4, 1.15),
            ("Weaknesses", [
                "No real-time GPS tracking",
                "Limited geocoding (95 of 2,964 stops)",
                "Single-maintainer risk",
                "No timetable / frequency data",
            ], C_RED, 5.1, 1.15),
            ("Opportunities", [
                "10 lakh daily commuters underserved",
                "WB Govt digitisation push (2026)",
                "Multi-city transferability",
                "Peer-forwarding discovery pattern",
            ], C_BLUE, 0.4, 4.0),
            ("Threats", [
                "Google Maps closing GTFS gap",
                "Yatri Sathi / Pathadisha expansion",
                "Data staleness without correction loop",
                "Competing apps with funding",
            ], C_ACCENT, 5.1, 4.0),
        ]
        for title, items, color, x, y in quadrants:
            add_rounded_rect(sl, Inches(x).emu, Inches(y).emu, Inches(4.5).emu, Inches(2.6).emu, RGBColor(0x17, 0x17, 0x20))
            add_rounded_rect(sl, Inches(x).emu, Inches(y).emu, Inches(4.5).emu, Inches(0.45).emu, color)
            tc = C_WHITE if color != C_ACCENT else C_DARK
            add_textbox(sl, Inches(x).emu, Inches(y).emu, Inches(4.5).emu, Inches(0.45).emu,
                        title, 14, True, tc, PP_ALIGN.CENTER)
            for j, item in enumerate(items):
                add_textbox(sl, Inches(x + 0.15).emu, Inches(y + 0.55 + j * 0.45).emu,
                            Inches(4.2).emu, Inches(0.4).emu,
                            f"•  {item}", 10, False, C_WHITE, PP_ALIGN.LEFT)
        add_textbox(sl, Inches(0.4).emu, Inches(6.8).emu, Inches(9).emu, Inches(0.3).emu,
                    "Source: SWOT analysis from Section VII-C of Paper; assessment period Jan–Aug 2026", 9, False, C_GREY, PP_ALIGN.LEFT)
        return sl

    notes_swot = """[~30 seconds]
Quick SWOT summary from the paper:

STRENGTHS — zero install, full offline, unique multi-change routing in the competitive segment.

WEAKNESSES — no real-time tracking (by design — that needs fleet hardware), limited GPS coverage, single-maintainer risk.

OPPORTUNITIES — 10 lakh daily commuters with no equivalent tool. The West Bengal government's 2026 digitisation push creates policy alignment. The architecture is transferable to other cities.

THREATS — Google closing the data gap through a WBTC integration, government apps expanding, and data staleness if we don't build a correction mechanism.

This directly motivates our future roadmap."""
    slides_data.append((slide_swot, notes_swot))

    # ═══════════════════  SLIDE 12: FUTURE SCOPE  ═══════════════════
    def slide_future(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        make_section_title(sl, "03", "Future Scope", "Section IX of Paper — Extending the lead, not just maintaining it")
        items = [
            ("Semantic Stop Annotations", "Flag hospitals, schools, stations at stop level inside route results\n— a genuinely bus-native query no competitor answers"),
            ("Crowdsourced Correction Loop", "In-app flagging for wrong stop order / missing stop\n— closes the #1 sustainability risk in our SWOT"),
            ("Multi-City Transferable Framework", "Architecture is city-agnostic — same pipeline works for\nNairobi matatus, Dhaka buses, or any informal network"),
            ("Static Precomputation → Richer Routing", "When timetable data becomes available, RAPTOR / transfer-pattern\nalgorithms can be compiled as static client assets — no backend needed"),
            ("Heuristic Journey-Time Estimation", "Stop-count × avg inter-stop time → estimated duration\n+ opt-in user reports for refinement over time"),
            ("WB Govt Late-Night Services (Aug 2026)", "New 10 PM corridors to hospitals — prime dataset expansion.\nRoute S-71 (Khardaha–Nabanna) already integrated"),
        ]
        for i, (title, desc) in enumerate(items):
            y = Inches(3.65 + i * 0.62).emu
            add_rounded_rect(sl, Inches(0.5).emu, y, Inches(0.4).emu, Inches(0.4).emu, C_ACCENT)
            add_textbox(sl, Inches(0.5).emu, y, Inches(0.4).emu, Inches(0.4).emu,
                        str(i+1), 11, True, C_DARK, PP_ALIGN.CENTER)
            add_textbox(sl, Inches(1.0).emu, y, Inches(2.8).emu, Inches(0.55).emu,
                        title, 11, True, C_ACCENT, PP_ALIGN.LEFT)
            add_textbox(sl, Inches(4.0).emu, y, Inches(5.5).emu, Inches(0.55).emu,
                        desc, 9, False, C_WHITE, PP_ALIGN.LEFT)
        return sl

    notes_future = """[~60 seconds]
Section IX of our paper outlines six future directions. Let me highlight the most impactful:

FIRST — Semantic stop annotations. Imagine asking "which bus passes a hospital near stop 14?" — no existing tool answers this. We plan to attach landmark metadata directly to stop sequences.

SECOND — Crowdsourced correction loop. The biggest sustainability risk is data staleness. A lightweight in-app flagging mechanism — "this stop doesn't exist anymore" or "you're missing a stop here" — feeds corrections back into the build pipeline.

THIRD — Multi-city framework. Our architecture is not Kolkata-specific. The same normalisation + client-graph pattern works for any city with informal transit — Nairobi, Dhaka, Lagos. We've designed for transferability.

FOURTH — Static precomputation. This is a key technical insight: algorithms like RAPTOR and transfer patterns have an offline preprocessing stage. We can compile their output into a static JSON, just like we do now. This gives us time-aware routing without reintroducing a backend — preserving our zero-infrastructure property.

FIFTH — Recent WB Government developments. The August 2026 late-night bus corridors to hospitals, the new S-71 Khardaha–Nabanna route — these are already being integrated into our dataset. Policy alignment is creating new scope for us."""
    slides_data.append((slide_future, notes_future))

    # ═══════════════════  SLIDE 13: BUSINESS MODEL  ═══════════════════
    def slide_business(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        std_header(sl, "Business Model Potential", "From open-source tool to sustainable platform")
        items = [
            ("Hyperlocal Advertising", "Stop-level ads for shops, restaurants near\nbus stops — contextually relevant, non-intrusive"),
            ("API Licensing (B2B)", "Normalised route graph as API for real-estate,\nlogistics, and e-commerce delivery platforms"),
            ("White-Label Transit Kit", "Multi-city framework licensed to municipalities\nor NGOs in other Global South cities"),
            ("Government Partnership", "Data layer for WB Transport Dept's\ndigitisation initiatives (Pathadisha/Yatri Sathi)"),
        ]
        for i, (title, desc) in enumerate(items):
            x = Inches(0.4 + (i % 2) * 4.8).emu
            y = Inches(1.2 + (i // 2) * 2.5).emu
            add_rounded_rect(sl, x, y, Inches(4.5).emu, Inches(2.1).emu, C_BLUE)
            add_textbox(sl, x, Emu(y + Inches(0.1).emu), Inches(4.5).emu, Inches(0.45).emu,
                        title, 16, True, C_ACCENT, PP_ALIGN.CENTER)
            add_textbox(sl, Emu(x + Inches(0.2).emu), Emu(y + Inches(0.65).emu),
                        Inches(4.1).emu, Inches(1.2).emu,
                        desc, 12, False, C_WHITE, PP_ALIGN.CENTER)
        add_textbox(sl, Inches(0.4).emu, Inches(6.4).emu, Inches(9).emu, Inches(0.5).emu,
                    "Current status: Open-source, zero-cost. Revenue paths exist when user base scales.",
                    12, True, C_GREY, PP_ALIGN.CENTER)
        return sl

    notes_business = """[~30 seconds]
While BusBabu is currently open-source and free, there are clear revenue paths at scale:

Hyperlocal advertising — contextual, stop-level ads. Not generic banner ads, but "there's a pharmacy 50 metres from your transfer stop."

API licensing — our normalised route graph is valuable to real-estate platforms, logistics companies, and delivery services who need Kolkata transit coverage.

White-label framework — the multi-city architecture can be licensed to municipalities or NGOs.

Government partnership — we can serve as the data normalisation layer for the WB Transport Department's own digitisation efforts."""
    slides_data.append((slide_business, notes_business))

    # ═══════════════════  SLIDE 14: REFERENCES  ═══════════════════
    def slide_references(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        std_header(sl, "Key References", "Selected from paper bibliography")
        refs = [
            '[1] Eros et al., "Applying GTFS to the Global South," Transp. Res. Rec., 2014',
            '[2] Klopp et al., "Digital Matatus in Nairobi," Springer, 2015',
            '[7] Bast et al., "Route Planning in Transportation Networks," Springer, 2016',
            '[8] Delling et al., "Round-Based Public Transit Routing (RAPTOR)," Transp. Sci., 2015',
            '[13] Haklay & Weber, "OpenStreetMap: User-Generated Street Maps," IEEE, 2008',
            '[14] McHugh, "Pioneering Open Data Standards: The GTFS Story," Code for America, 2013',
            '[16] Biorn-Hansen et al., "Progressive Web Apps," WEBIST/Springer, 2018',
            '[17] Foell et al., "Urban Bus Navigator -- Micro-navigation," Urb-IoT, 2014',
        ]
        for i, ref in enumerate(refs):
            y = Inches(1.2 + i * 0.62).emu
            add_textbox(sl, Inches(0.6).emu, y, Inches(8.8).emu, Inches(0.55).emu,
                        ref, 11, False, C_LIGHT, PP_ALIGN.LEFT)
        add_textbox(sl, Inches(0.6).emu, Inches(6.3).emu, Inches(8.8).emu, Inches(0.4).emu,
                    "Full bibliography: 20 references in paper -- available with the submission.", 10, False, C_GREY, PP_ALIGN.LEFT)
        return sl

    notes_refs = """[~10 seconds]
These are selected references from our full bibliography of 20 papers. The complete list is in the submitted paper. I'd like to highlight Eros et al. and the Digital Matatu project — they document the same structural data gap in Mexico City and Nairobi that we address for Kolkata."""
    slides_data.append((slide_references, notes_refs))

    # ═══════════════════  SLIDE 15: THANK YOU  ═══════════════════
    def slide_thankyou(prs):
        sl = prs.slides.add_slide(prs.slide_layouts[6])
        fill_bg(sl, C_DARK)
        add_rect(sl, 0, 0, W, Inches(0.08).emu, C_ACCENT)
        if os.path.exists(LOGO):
            sl.shapes.add_picture(LOGO, Inches(3.8).emu, Inches(0.5).emu,
                                  Inches(2.4).emu, Inches(2.4).emu)
        add_textbox(sl, Inches(0.5).emu, Inches(3.1).emu, Inches(9).emu, Inches(0.7).emu,
                    "Thank You", 40, True, C_ACCENT, PP_ALIGN.CENTER)
        add_textbox(sl, Inches(0.5).emu, Inches(3.9).emu, Inches(9).emu, Inches(0.5).emu,
                    "Questions are welcome", 18, False, C_WHITE, PP_ALIGN.CENTER)
        # contact info
        add_rounded_rect(sl, Inches(2.0).emu, Inches(4.8).emu, Inches(6.0).emu, Inches(1.8).emu, C_BLUE)
        info = (
            "Live App:  bus-babu.vercel.app\n"
            "GitHub:  github.com/helplessThor/BusBabu\n"
            "Data Source:  kolbusopedia.com\n"
            "Author:  Kuntal Paul  |  RCCIIT, Dept of IT"
        )
        add_textbox(sl, Inches(2.2).emu, Inches(4.9).emu, Inches(5.6).emu, Inches(1.6).emu,
                    info, 13, False, C_WHITE, PP_ALIGN.CENTER)
        add_rect(sl, 0, Inches(7.42).emu, W, Inches(0.08).emu, C_ACCENT)
        return sl

    notes_thankyou = """[~10 seconds]
Thank you for your time and attention. The application is live — you can try it right now at bus-babu.vercel.app. The source code is open on GitHub.

I'm happy to take any questions."""
    slides_data.append((slide_thankyou, notes_thankyou))

    return slides_data


# ══════════════════════════════════════════════════════════════════
#  GENERATE BOTH FILES
# ══════════════════════════════════════════════════════════════════

def create_presentation(with_notes=False):
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    slides_data = build_slides(prs)
    for builder, notes in slides_data:
        sl = builder(prs)
        if with_notes:
            notes_slide = sl.notes_slide
            notes_slide.notes_text_frame.text = notes.strip()
    return prs


# Main presentation (no notes in the file — clean for projection)
print("Generating main presentation...")
prs_main = create_presentation(with_notes=False)
main_path = os.path.join(PAPER_DIR, "BusBabu_UEMCOS_2026_Presentation.pptx")
prs_main.save(main_path)
print(f"Saved: {main_path}")

# Speaker notes version (same slides + detailed notes per slide)
print("Generating speaker notes version...")
prs_notes = create_presentation(with_notes=True)
notes_path = os.path.join(PAPER_DIR, "BusBabu_UEMCOS_2026_Speaker_Notes.pptx")
prs_notes.save(notes_path)
print(f"Saved: {notes_path}")

print("\nDone! Both files are in the Paper folder.")
print(f"  Presentation:   {os.path.basename(main_path)}")
print(f"  Speaker Notes:  {os.path.basename(notes_path)}")
print(f"\nTotal slides: 15")
print("Estimated time: ~8-9 minutes (leaves buffer for Q&A within 10 min)")
