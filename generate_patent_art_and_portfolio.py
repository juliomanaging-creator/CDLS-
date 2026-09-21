"""
Complete USPTO Patent Art & Portfolio Disclosure Generator
Produces 37 CFR § 1.84 vector drawing sheets (FIG. 1 - FIG. 4)
and compiles the complete patent specification Word document (.docx).
"""

import os
from pathlib import Path
from typing import Optional
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# ----------------------------------------------------------------------
# 1. 37 CFR § 1.84 VECTOR PATENT DRAWINGS (FIG. 1 - FIG. 4)
# ----------------------------------------------------------------------

FIG1_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 816 1056" width="816" height="1056">
  <style>
    .patent-line { stroke: #000000; stroke-width: 2.2; fill: none; stroke-linecap: round; stroke-linejoin: round; }
    .patent-thin { stroke: #000000; stroke-width: 1.2; fill: none; }
    .patent-dash { stroke: #000000; stroke-width: 1.5; stroke-dasharray: 6,4; fill: none; }
    .patent-num  { font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold; fill: #000000; }
    .fig-label   { font-family: 'Arial', sans-serif; font-size: 18px; font-weight: bold; fill: #000000; text-anchor: middle; }
  </style>

  <!-- Sight Boundary: 1.0 inch margins per 37 CFR 1.84 -->
  <rect x="96" y="96" width="624" height="864" class="patent-thin" stroke-dasharray="2,8" opacity="0.15"/>

  <g transform="translate(140, 160)">
    <!-- Vehicle Receptacle 104 -->
    <rect x="360" y="80" width="160" height="240" class="patent-line"/>
    <line x1="360" y1="120" x2="480" y2="120" class="patent-line"/>
    <line x1="360" y1="280" x2="480" y2="280" class="patent-line"/>

    <!-- Male Coupler Body 102 -->
    <path d="M 60,110 L 280,110 L 280,70 L 350,70 L 350,330 L 280,330 L 280,290 L 60,290 Z" class="patent-line"/>

    <!-- High-Current DC Terminals 108 -->
    <rect x="290" y="140" width="110" height="30" class="patent-line"/>
    <rect x="290" y="230" width="110" height="30" class="patent-line"/>
    <line x1="300" y1="140" x2="300" y2="170" class="patent-dash"/>
    <line x1="300" y1="230" x2="300" y2="260" class="patent-dash"/>

    <!-- Permanent N52 Magnet Array 106 -->
    <rect x="330" y="85" width="20" height="45" class="patent-line" fill="#000000" fill-opacity="0.12"/>
    <rect x="330" y="270" width="20" height="45" class="patent-line" fill="#000000" fill-opacity="0.12"/>
    <rect x="360" y="85" width="20" height="45" class="patent-line" fill="#000000" fill-opacity="0.12"/>
    <rect x="360" y="270" width="20" height="45" class="patent-line" fill="#000000" fill-opacity="0.12"/>

    <!-- Optical Interlock Auxiliary Loop 110 -->
    <circle cx="345" cy="200" r="14" class="patent-line"/>
    <path d="M 335,200 L 355,200 M 345,190 L 345,210" class="patent-line"/>

    <!-- Mechanical Release Cam & Lever 112 -->
    <path d="M 280,330 L 240,430 L 160,470" class="patent-line"/>
    <circle cx="280" cy="330" r="6" class="patent-line"/>
    <circle cx="160" cy="470" r="10" class="patent-line"/>

    <!-- Strain Relief Boot 114 -->
    <path d="M 60,110 C 20,110 0,160 0,200 C 0,240 20,290 60,290" class="patent-line"/>

    <!-- Lead Lines & Reference Numerals -->
    <text x="210" y="40" class="patent-num">100</text>
    <line x1="225" y1="45" x2="260" y2="90" class="patent-thin"/>

    <text x="140" y="90" class="patent-num">102</text>
    <line x1="155" y1="95" x2="180" y2="120" class="patent-thin"/>

    <text x="440" y="50" class="patent-num">104</text>
    <line x1="445" y1="55" x2="430" y2="90" class="patent-thin"/>

    <text x="380" y="70" class="patent-num">106</text>
    <line x1="380" y1="75" x2="350" y2="95" class="patent-thin"/>

    <text x="430" y="160" class="patent-num">108</text>
    <line x1="425" y1="160" x2="395" y2="160" class="patent-thin"/>

    <text x="270" y="195" class="patent-num">110</text>
    <line x1="295" y1="195" x2="330" y2="200" class="patent-thin"/>

    <text x="100" y="465" class="patent-num">112</text>
    <line x1="125" y1="465" x2="150" y2="470" class="patent-thin"/>

    <text x="10" y="170" class="patent-num">114</text>
    <line x1="25" y1="175" x2="40" y2="190" class="patent-thin"/>
  </g>

  <text x="408" y="930" class="fig-label">FIG. 1</text>
</svg>"""

FIG2_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 816 1056" width="816" height="1056">
  <style>
    .patent-line { stroke: #000000; stroke-width: 2.2; fill: none; stroke-linecap: round; stroke-linejoin: round; }
    .patent-thin { stroke: #000000; stroke-width: 1.2; fill: none; }
    .patent-box  { stroke: #000000; stroke-width: 2.0; fill: #FFFFFF; }
    .patent-num  { font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold; fill: #000000; }
    .patent-text { font-family: 'Arial', sans-serif; font-size: 13px; fill: #000000; text-anchor: middle; }
    .fig-label   { font-family: 'Arial', sans-serif; font-size: 18px; font-weight: bold; fill: #000000; text-anchor: middle; }
  </style>

  <rect x="96" y="96" width="624" height="864" class="patent-thin" stroke-dasharray="2,8" opacity="0.15"/>

  <g transform="translate(140, 160)">
    <!-- Trailer Chassis 200 -->
    <rect x="20" y="60" width="480" height="380" rx="15" class="patent-line"/>
    <circle cx="120" cy="470" r="35" class="patent-line"/>
    <circle cx="120" cy="470" r="15" class="patent-line"/>
    <circle cx="400" cy="470" r="35" class="patent-line"/>
    <circle cx="400" cy="470" r="15" class="patent-line"/>
    <text x="510" y="80" class="patent-num">200</text>

    <!-- 360 kWh LFP Storage 202 -->
    <rect x="50" y="90" width="200" height="160" class="patent-box"/>
    <text x="150" y="160" class="patent-text">360 kWh LFP PACK</text>
    <text x="150" y="185" class="patent-text">(120 PARALLEL STRINGS)</text>
    <text x="60" y="115" class="patent-num">202</text>

    <!-- Bidirectional Inverter 204 -->
    <rect x="280" y="90" width="190" height="160" class="patent-box"/>
    <text x="375" y="160" class="patent-text">BIDIRECTIONAL INVERTER</text>
    <text x="375" y="185" class="patent-text">(38.4 kW / 400V DC)</text>
    <text x="290" y="115" class="patent-num">204</text>

    <!-- IEEE 15118-20 Controller 206 -->
    <rect x="50" y="280" width="200" height="120" class="patent-box"/>
    <text x="150" y="335" class="patent-text">V2G CONTROLLER</text>
    <text x="150" y="360" class="patent-text">(IEEE 15118-20 PLC)</text>
    <text x="60" y="305" class="patent-num">206</text>

    <!-- MagSafe Cable Reel 208 -->
    <circle cx="375" cy="340" r="50" class="patent-line"/>
    <circle cx="375" cy="340" r="20" class="patent-line"/>
    <text x="375" y="345" class="patent-text">REEL 208</text>

    <!-- Grid Interconnect Feed 210 -->
    <path d="M 425,340 L 520,340" class="patent-line"/>
    <text x="530" y="345" class="patent-num">210</text>
  </g>

  <text x="408" y="930" class="fig-label">FIG. 2</text>
</svg>"""

FIG3_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 816 1056" width="816" height="1056">
  <style>
    .patent-line { stroke: #000000; stroke-width: 2.2; fill: none; stroke-linecap: round; stroke-linejoin: round; }
    .patent-thin { stroke: #000000; stroke-width: 1.2; fill: none; }
    .patent-box  { stroke: #000000; stroke-width: 2.0; fill: #FFFFFF; }
    .patent-num  { font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold; fill: #000000; }
    .patent-text { font-family: 'Arial', sans-serif; font-size: 13px; fill: #000000; text-anchor: middle; }
    .fig-label   { font-family: 'Arial', sans-serif; font-size: 18px; font-weight: bold; fill: #000000; text-anchor: middle; }
  </style>

  <rect x="96" y="96" width="624" height="864" class="patent-thin" stroke-dasharray="2,8" opacity="0.15"/>

  <g transform="translate(160, 140)">
    <!-- 302 Imaging Sensor -->
    <rect x="110" y="40" width="260" height="60" class="patent-box"/>
    <text x="240" y="75" class="patent-text">OPTICAL IMAGING SENSOR</text>
    <text x="70" y="55" class="patent-num">302</text>
    <line x1="95" y1="55" x2="110" y2="65" class="patent-thin"/>

    <!-- Arrow Down -->
    <path d="M 240,100 L 240,150 M 235,140 L 240,150 L 245,140" class="patent-line"/>

    <!-- 304 Edge CV Model -->
    <rect x="110" y="150" width="260" height="70" class="patent-box"/>
    <text x="240" y="180" class="patent-text">EDGE CV DAMAGE DETECTOR</text>
    <text x="240" y="200" class="patent-text">(YOLO v8 / RESNET)</text>
    <text x="70" y="170" class="patent-num">304</text>
    <line x1="95" y1="170" x2="110" y2="180" class="patent-thin"/>

    <!-- Dual Fork Arrow -->
    <path d="M 240,220 L 240,260 M 240,260 L 140,260 L 140,300 M 135,290 L 140,300 L 145,290 M 240,260 L 340,260 L 340,300 M 335,290 L 340,300 L 345,290" class="patent-line"/>

    <!-- 306 Primary Hash Engine -->
    <rect x="40" y="300" width="200" height="70" class="patent-box"/>
    <text x="140" y="335" class="patent-text">PRIMARY HASH ENGINE</text>
    <text x="140" y="355" class="patent-text">(SHA-256)</text>
    <text x="10" y="315" class="patent-num">306</text>
    <line x1="30" y1="320" x2="40" y2="330" class="patent-thin"/>

    <!-- 308 ZKP Commitment Engine -->
    <rect x="250" y="300" width="210" height="70" class="patent-box"/>
    <text x="355" y="335" class="patent-text">ZKP COMMITMENT ENGINE</text>
    <text x="355" y="355" class="patent-text">(zk-SNARK / PEDERSEN)</text>
    <text x="475" y="315" class="patent-num">308</text>
    <line x1="470" y1="320" x2="455" y2="330" class="patent-thin"/>

    <!-- Rejoin Flow -->
    <path d="M 140,370 L 140,420 L 240,420 M 355,370 L 355,420 L 240,420 M 240,420 L 240,460 M 235,450 L 240,460 L 245,450" class="patent-line"/>

    <!-- 310 Immutable Ledger -->
    <rect x="100" y="460" width="280" height="80" class="patent-box"/>
    <text x="240" y="495" class="patent-text">IMMUTABLE APPEND-ONLY</text>
    <text x="240" y="515" class="patent-text">AUDIT LEDGER</text>
    <text x="60" y="480" class="patent-num">310</text>
    <line x1="85" y1="480" x2="105" y2="495" class="patent-thin"/>

    <!-- 300 Transfer Boundary Envelope -->
    <rect x="10" y="10" width="465" height="560" class="patent-thin" stroke-dasharray="8,6"/>
    <text x="20" y="30" class="patent-num">300</text>
  </g>

  <text x="408" y="930" class="fig-label">FIG. 3</text>
</svg>"""

FIG4_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 816 1056" width="816" height="1056">
  <style>
    .patent-line { stroke: #000000; stroke-width: 2.2; fill: none; stroke-linecap: round; stroke-linejoin: round; }
    .patent-thin { stroke: #000000; stroke-width: 1.2; fill: none; }
    .patent-box  { stroke: #000000; stroke-width: 2.0; fill: #FFFFFF; }
    .patent-num  { font-family: 'Arial', sans-serif; font-size: 15px; font-weight: bold; fill: #000000; }
    .patent-text { font-family: 'Arial', sans-serif; font-size: 13px; fill: #000000; text-anchor: middle; }
    .fig-label   { font-family: 'Arial', sans-serif; font-size: 18px; font-weight: bold; fill: #000000; text-anchor: middle; }
  </style>

  <rect x="96" y="96" width="624" height="864" class="patent-thin" stroke-dasharray="2,8" opacity="0.15"/>

  <g transform="translate(160, 140)">
    <!-- 402 Layer 1 Foundation -->
    <rect x="60" y="40" width="360" height="80" class="patent-box"/>
    <text x="240" y="75" class="patent-text">LAYER 1: REGULARIZED REGRESSION</text>
    <text x="240" y="95" class="patent-text">(10-YEAR HISTORICAL NOISE FILTER)</text>
    <text x="20" y="65" class="patent-num">402</text>

    <!-- Arrow Down -->
    <path d="M 240,120 L 240,180 M 235,170 L 240,180 L 245,170" class="patent-line"/>

    <!-- 404 Layer 2 Stochastic MCMC -->
    <rect x="60" y="180" width="360" height="90" class="patent-box"/>
    <text x="240" y="215" class="patent-text">LAYER 2: STOCHASTIC MCMC SAMPLER</text>
    <text x="240" y="235" class="patent-text">(METROPOLIS-HASTINGS 10,000 RUNS)</text>
    <text x="20" y="205" class="patent-num">404</text>

    <!-- 406 Real-Time CAISO Grid Pricing -->
    <path d="M 480,225 L 420,225 M 430,220 L 420,225 L 430,230" class="patent-line"/>
    <text x="500" y="230" class="patent-num">406</text>

    <!-- Arrow Down -->
    <path d="M 240,270 L 240,330 M 235,320 L 240,330 L 245,320" class="patent-line"/>

    <!-- 408 Layer 3 APLRE Stabilization -->
    <rect x="60" y="330" width="360" height="90" class="patent-box"/>
    <text x="240" y="365" class="patent-text">LAYER 3: BEHAVIORAL STABILIZATION</text>
    <text x="240" y="385" class="patent-text">(DETERMINISTIC HASH A/B &amp; HOS LIMITS)</text>
    <text x="20" y="355" class="patent-num">408</text>

    <!-- Stack Boundary 400 -->
    <rect x="10" y="10" width="460" height="450" class="patent-thin" stroke-dasharray="8,6"/>
    <text x="20" y="30" class="patent-num">400</text>
  </g>

  <text x="408" y="930" class="fig-label">FIG. 4</text>
</svg>"""

# ----------------------------------------------------------------------
# 2. COMPLETE SPECIFICATION BUILDER (.DOCX)
# ----------------------------------------------------------------------

def generate_patent_word_doc(output_path: str = "CDLS_IP_Patent_Portfolio_Submission.docx"):
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    NAVY = RGBColor(16, 44, 87)
    CHARCOAL = RGBColor(33, 37, 41)
    SLATE = RGBColor(100, 116, 139)

    def add_h(text: str, level: int = 1):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.bold = True
        if level == 1:
            r.font.size = Pt(15)
            r.font.color.rgb = NAVY
        elif level == 2:
            r.font.size = Pt(12)
            r.font.color.rgb = NAVY
        else:
            r.font.size = Pt(10.5)
            r.font.color.rgb = CHARCOAL

    def add_p(text: str = "", bold_prefix: Optional[str] = None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(10)
            rb.bold = True
            rb.font.color.rgb = CHARCOAL
        if text:
            rt = p.add_run(text)
            rt.font.name = "Calibri"
            rt.font.size = Pt(10)
            rt.font.color.rgb = CHARCOAL

    def add_claim(claim_num: str, preamble: str, elements: list[str]):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        p.paragraph_format.space_after = Pt(3)
        r_num = p.add_run(claim_num + " ")
        r_num.font.name = "Consolas"
        r_num.font.size = Pt(9.5)
        r_num.bold = True
        r_pre = p.add_run(preamble)
        r_pre.font.name = "Consolas"
        r_pre.font.size = Pt(9.5)
        
        for elem in elements:
            pe = doc.add_paragraph(style="List Bullet 2")
            pe.paragraph_format.left_indent = Inches(0.5)
            pe.paragraph_format.space_after = Pt(2)
            re = pe.add_run(elem)
            re.font.name = "Consolas"
            re.font.size = Pt(9.5)

    # Title & Subtitle
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("INTELLECTUAL PROPERTY DISCLOSURE & PATENT SPECIFICATION PORTFOLIO")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(17)
    r_title.bold = True
    r_title.font.color.rgb = NAVY

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Consolidated Technical Disclosures, Independent Claims, and R&D Verification for USPTO Filing")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.italic = True
    r_sub.font.color.rgb = SLATE

    # Metadata Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_rows = [
        ("Applicant / Assignee:", "California Investment Auto LP (CDLS Platform)"),
        ("Primary Inventor:", "Julio Cesar Umanzor"),
        ("Filing Status / Target:", "USPTO Non-Provisional & Provisional Patent Portfolio"),
        ("Related Filings:", "USPTO Provisional Patent Application #63/734829 (MagSafe Quick-Disconnect)"),
        ("Statutory Basis:", "35 U.S.C. § 101, § 102, § 103, § 112 | IRC § 41 Contemporaneous Support"),
    ]
    for i, (k, v) in enumerate(meta_rows):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.2), Inches(4.3)
        c0.paragraphs[0].add_run(k).bold = True
        c1.paragraphs[0].add_run(v)
        c0._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w'))))

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 1. Executive Summary
    add_h("1. Executive Summary of Patentable Inventions", level=1)
    add_p("This specification documents the novel technological solutions, statutory claim structures, and formal drawing disclosures derived directly from 675+ qualified engineering hours across the CDLS platform:")
    clusters = [
        ("Cluster 1: Electro-Mechanical Fleet Systems (FIGS. 1–2) — ", "High-amperage magnetic quick-disconnect charging couplers (USPTO #63/734829), mobile battery pod trailers (360 kWh), and IEEE 15118-20 bidirectional V2G grid interconnection architectures."),
        ("Cluster 2: Cryptographic Audit & Integrity Engine (JUDAS AI / FIG. 3) — ", "Zero-knowledge proof verification pipeline utilizing dual-hash commitments, automated computer vision damage inspection, and GAGAS-compliant non-repudiation ledgers."),
        ("Cluster 3: Adaptive Route & Fleet Intelligence (CARI / CESAR / FIG. 4) — ", "Three-layer stochastic route optimization engine combining regularized OLS noise elimination, Markov Chain Monte Carlo (MCMC) simulations, and A/B human-centric stabilization (APLRE)."),
        ("Cluster 4: Multi-Tenant Credential & Compliance Architecture — ", "AES-256-GCM authenticated envelope encryption (AAD-Bound AEAD) with hardware-isolated data encryption keys (DEKs) and real-time CARB CTC / TRUCRS API automation engines.")
    ]
    for pfx, txt in clusters:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(pfx)
        r.bold = True
        p.add_run(txt)

    # 2. Brief Description of the Drawings
    add_h("2. Brief Description of the Drawings", level=1)
    add_p("The accompanying patent drawings, adhering to 37 CFR § 1.84 line art and margin standards, illustrate exemplary embodiments of the present invention:")
    drawings_desc = [
        ("FIG. 1 ", "is a cross-sectional elevation view of the high-amperage magnetic breakaway coupling assembly (100) in an engaged operational state, illustrating the magnetic retention array (106), DC terminals (108), optical interlock (110), and foot-pedal release cam (112)."),
        ("FIG. 2 ", "is a schematic system diagram of the mobile battery pod trailer (200) housing the 360 kWh LFP cell pack (202), bidirectional inverter (204), IEEE 15118-20 PLC controller (206), and MagSafe reel interface (208)."),
        ("FIG. 3 ", "is an architectural data flow diagram of the JUDAS AI cryptographic audit engine (300), showing the optical sensor boundary (302), edge CV damage detector (304), primary hash engine (306), zero-knowledge commitment module (308), and immutable ledger (310)."),
        ("FIG. 4 ", "is a layer architecture diagram of the CARI adaptive three-layer route intelligence engine (400), illustrating the regularized regression baseline (402), stochastic MCMC sampler (404), real-time CAISO feed (406), and APLRE behavioral stabilization layer (408).")
    ]
    for fig_num, desc in drawings_desc:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(fig_num)
        r.bold = True
        p.add_run(desc)

    # 3. Detailed Description & Claims - Cluster 1
    add_h("3. Detailed Description: Magnetic Quick-Disconnect & V2G System (FIGS. 1–2)", level=1)
    add_p("USPTO Provisional Patent Application #63/734829 | IPC Classes: H01R, B60L, H02J", bold_prefix="Reference: ")
    add_p("Prior Art Deficiencies: Conventional commercial high-power DC fast-charging couplings (such as CCS Type 1/2 or MCS) utilize rigid mechanical pin-and-sleeve latch assemblies requiring manual insertion forces exceeding 35 pounds. When vehicles roll away unexpectedly or operate under persistent mechanical vibration during mobile trailer transport, these rigid assemblies shear contact pins, crack connector housings, and create severe arc-flash risks during unlatched separation.")
    add_p("Technical Uncertainties Resolved: CAD force simulations proved that an N52 neodymium-iron-boron (NdFeB) magnetic array (106) provides clamping retention resisting highway vibration up to 1.5G RMS while releasing under less than 25 pounds of applied mechanical pedal force (112). An auxiliary optical sensing loop (110) de-energizes the 400V DC contactors within 15 milliseconds, eliminating electrical arcs prior to complete air-gap separation.")
    
    add_h("Exemplary Claims — Cluster 1:", level=3)
    add_claim(
        "Claim 1.",
        "An automated breakaway bidirectional electrical coupling assembly (100), comprising:",
        [
            "a connector interface (102) configured to conduct direct currents exceeding 200 amperes at voltages exceeding 350 volts DC;",
            "a magnetic retention array (106) disposed about said connector interface comprising rare-earth permanent magnets configured to provide a retention clamping force resisting mechanical vibration up to 1.5G RMS;",
            "a mechanical release linkage (112) operatively coupled to a release lever configured to overcome said magnetic retention clamping force with an applied operator actuation force of less than 25 pounds; and",
            "an auxiliary sensing loop (110) configured to detect initial physical displacement and generate an interlock signal de-energizing high-voltage contactors within 15 milliseconds."
        ]
    )
    add_claim(
        "Claim 2.",
        "The electrical coupling assembly of claim 1, further comprising:",
        [
            "a mobile transport trailer (200) housing a plurality of lithium iron phosphate (LFP) energy storage modules (202) providing at least 360 kilowatt-hours of capacity configured to deliver bidirectional vehicle-to-grid power via an IEEE 15118-20 protocol stack (206)."
        ]
    )

    # 4. Detailed Description & Claims - Cluster 2
    add_h("4. Detailed Description: Cryptographic Zero-Knowledge Audit Kernel (JUDAS AI / FIG. 3)", level=1)
    add_p("Project Code: COMPLIANCE-001 | IPC Classes: G06F 21/64, H04L 9/32, G06T 7/00", bold_prefix="Reference: ")
    add_p("Prior Art Deficiencies: Transport carriers and dealerships face billions in disputed freight damage claims. Existing digital inspection systems store full-resolution imagery in centralized servers, leaking proprietary freight metadata, carrier telematics, and customer PII while remaining vulnerable to post-hoc digital manipulation.")
    add_p("Technical Uncertainties Resolved: Validated a two-tier dual-hash commitment architecture (306, 308) combining SHA-256 and zero-knowledge proofs (zk-SNARKs / Pedersen commitments) to guarantee court-admissible non-repudiation under GAGAS standards without disclosing unredacted imagery. Fine-tuned YOLO v8 models (304) achieved <5% false negatives across dawn, dusk, and overcast yard lighting conditions.")

    add_h("Exemplary Claims — Cluster 2:", level=3)
    add_claim(
        "Claim 3.",
        "A computer-implemented method for verified cargo condition auditing, comprising:",
        [
            "capturing raw freight imagery via an optical imaging sensor (302) at an automotive transfer boundary (300);",
            "executing an edge inference pipeline (304) to detect physical damage classifications with precision exceeding 90%;",
            "generating a dual-hash cryptographic commitment comprising a primary cryptographic hash (306) and an auxiliary zero-knowledge proof commitment (308);",
            "publishing said cryptographic commitment to an append-only verification ledger (310); and",
            "verifying non-repudiation of vehicle condition during dispute resolution by matching a challenged image against said published commitment without disclosing unredacted customer metadata."
        ]
    )

    # 5. Detailed Description & Claims - Cluster 3
    add_h("5. Detailed Description: Adaptive Route Intelligence Engine (CARI / FIG. 4)", level=1)
    add_p("Project Code: AI-001 | IPC Classes: G06Q 10/04, G06N 3/00", bold_prefix="Reference: ")
    add_p("Prior Art Deficiencies: Existing logistics route solvers optimize purely for static shortest-path distance, failing to integrate non-stationary electrical wholesale energy prices (CAISO), battery thermal derating, and driver compliance constraints, causing route rejection rates exceeding 30%.")
    add_p("Technical Uncertainties Resolved: Applied LASSO-regularized OLS regression (402) to isolate structural route-cost signals from 10 years of noisy freight data. A 10,000-run Metropolis-Hastings MCMC sampler (404) achieved stable P10/P90 confidence boundaries. APLRE deterministic hash A/B assignment (408) eliminated driver selection bias in field trials.")

    add_h("Exemplary Claims — Cluster 3:", level=3)
    add_claim(
        "Claim 4.",
        "A computer-implemented system for commercial freight route optimization (400), comprising:",
        [
            "one or more hardware processors configured to execute an adaptive three-layer route intelligence engine comprising:",
            "(a) a foundation regression layer (402) configured to establish baseline haul costs by regularizing historical logistics records;",
            "(b) a stochastic simulation layer (404) configured to evaluate candidate routes using a Metropolis-Hastings Markov Chain Monte Carlo sampler coupled to real-time electrical grid pricing feeds (406); and",
            "(c) an adaptive behavioral stabilization layer (408) configured to assign route variants via deterministic hashing and adjust dispatch recommendations based on driver Hours-of-Service constraints."
        ]
    )

    # 6. Detailed Description - Cluster 4
    add_h("6. Detailed Description: AAD-Bound Multi-Tenant Boundary & Automated CARB Engine", level=1)
    add_p("Project Codes: DEALER-001 & COMPLIANCE-001 | IPC Classes: H04L 9/00, G06F 21/60", bold_prefix="Reference: ")
    add_p("Prior Art Deficiencies: Shared multi-tenant databases expose credentials to memory-scraping vulnerabilities. Environmental reporting under California Advanced Clean Fleets (ACF) requires extensive manual paperwork across disparate dealer DMS platforms.")
    add_p("Technical Uncertainties Resolved: AES-256-GCM envelope encryption cryptographically binds tenant identifiers into Additional Authenticated Data (AAD), mathematically prohibiting ciphertext decryption in mismatched tenant contexts. High-volume API handshakes with CARB CTC and TRUCRS endpoints automate reporting compliance under 13 CCR §§ 2195–2199.")

    # 7. Contemporaneous Evidence Ledger Table
    add_h("7. Contemporaneous R&D Experimental Evidence Ledger", level=1)
    add_p("The following contemporaneous engineering records substantiate statutory patent enablement under 35 U.S.C. § 112:")

    table_data = [
        ("Date", "Project Code / Area", "Technical Uncertainty", "Experimental Validation"),
        ("R&D Phase", "Four-Part Test Guide - 4. BUSINESS", "Whether core algorithms improve performance or create new business components.", "Improved function: Faster route optimization; Improved performance: Real-time vs batch processing; Improved reliability: Mathematical proof."),
        ("R&D Phase", "Four-Part Test Guide - 2. ELIMINATE", "Uncertainty regarding model error rates and legacy regulatory API compatibility.", "Unknown: Will ML model achieve <10% error rate? Unknown: Can CARB API support real-time blockchain integration?"),
        ("2026-03-05", "AI Route Optimization — Phase 8: KB", "Does artifact sandbox environment support parallel outbound API calls on mobile client?", "Debugging / Experimentation: Mobile blocks outbound fetch; sequential mode + desktop workaround identified."),
        ("2026-03-01", "AI Route Optimization — Phase 8: 6-Agent", "Can parallel AI subagents process domain-specific CDLS knowledge faster than sequential processing?", "System Architecture: Parallel 6-agent architecture designed; 5x speed improvement over sequential projected."),
        ("2026-02-01", "Fleet Management Dashboard — Phase 7", "What technical interconnection standard does SMUD require and what is the critical path?", "Regulatory Research: SMUD determination gates launch date; cannot be compressed with capital."),
        ("2026-01-12", "Carbon Credit Automation — Phase 7", "Can automated per-haul carbon accounting match manual Verra VCS calculation within 2%?", "Algorithm Development: Automated calc within 1.4% of manual; 347 credits/haul average (pilot sample n=40)."),
        ("2025-11-05", "Dealer Dashboard — Phase 6: 48-Hour", "Does 48-hr onboarding pipeline achieve >=95% accuracy across dealer tiers A/B/C?", "User Acceptance Testing: 95.4% accuracy across all 3 dealer tiers; 2 edge cases flagged for Tier C (small dealers)."),
        ("2025-10-10", "Dealer Dashboard — Phase 6: Dealer", "Can AI agent automate HVIP application filing with <5% error rate vs manual process?", "Feature Development: HVIP auto-filing: 96.8% accuracy, average 2.3 hrs vs 6 hrs manual."),
        ("2025-09-01", "Fleet Management Dashboard — Phase 5", "Does the full V2G pipeline function without manual intervention from CAISO signal to token issuance?", "Integration Testing: Pipeline functional; average 4.2 min from CAISO signal to $CARBON mint."),
        ("2025-08-15", "CARB Automation — Phase 5: LCFS Credit", "Which methodology maximizes defensible LCFS credit value per haul for Tesla Semi profile?", "Regulatory Research: Verra VCS selected; $8,000-$22,000/truck/yr range confirmed via methodology."),
        ("2025-07-08", "Fleet Management Dashboard — Phase 5", "Can forex arbitrage methodology (MCMC + regression) predict CAISO peak pricing with >80% accuracy?", "Algorithm Development: 82.3% price prediction accuracy; V2G dispatch optimization improves revenue estimate by $6,200/truck/yr."),
        ("2025-06-01", "Carbon Credit Automation — Phase 4", "Do contracts meet security standards for production deployment with real LP capital?", "Security Testing: 2 medium-severity issues resolved; gas reduced 34% via struct packing.")
    ]

    t = doc.add_table(rows=len(table_data), cols=4)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = t.rows[r_idx].cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Calibri"
            if r_idx == 0:
                run.bold = True
                run.font.size = Pt(9)
                cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="E2E8F0"/>'.format(nsdecls('w'))))
            else:
                run.font.size = Pt(8.5)
                if c_idx in [0, 1]:
                    run.bold = True

    doc.save(output_path)
    print(f"[OK] Patent specification Word document generated: {output_path}")

# ----------------------------------------------------------------------
# 3. MAIN RUNNER
# ----------------------------------------------------------------------

if __name__ == "__main__":
    out_dir = Path("patent_drawings")
    out_dir.mkdir(exist_ok=True)
    
    (out_dir / "FIG_1.svg").write_text(FIG1_SVG, encoding="utf-8")
    (out_dir / "FIG_2.svg").write_text(FIG2_SVG, encoding="utf-8")
    (out_dir / "FIG_3.svg").write_text(FIG3_SVG, encoding="utf-8")
    (out_dir / "FIG_4.svg").write_text(FIG4_SVG, encoding="utf-8")
    print(f"[OK] 4 USPTO-compliant vector drawing sheets saved to: {out_dir.resolve()}")

    generate_patent_word_doc("CDLS_IP_Patent_Portfolio_Submission.docx")