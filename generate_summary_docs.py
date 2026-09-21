"""
Executive Research & Knowledge Translation Summary Generator
Compiles the macro/micro cluster findings into DOCX and PDF formats.
"""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_DIR = Path(__file__).resolve().parent
DOCX_PATH = BASE_DIR / "EXECUTIVE_RESEARCH_KNOWLEDGE_SUMMARY.docx"
PDF_PATH = BASE_DIR / "EXECUTIVE_RESEARCH_KNOWLEDGE_SUMMARY.pdf"

def generate_docx():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    p_title = doc.add_paragraph()
    r_title = p_title.add_run("EXECUTIVE RESEARCH & KNOWLEDGE TRANSLATION SUMMARY")
    r_title.bold = True
    r_title.font.size = Pt(17)
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("CDLS Platform · Macro Strategic Overview vs. Micro Implementation Mechanics · 35 U.S.C. § 112 & IRC § 41")
    r_sub.font.size = Pt(10)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph(
        "This executive summary bridges the platform's backend technical experimentation with actionable product architecture and regulatory frameworks. "
        "It translates engineering findings across four patent clusters into clear macro-level system overviews and concrete micro-level implementation mechanics."
    )

    doc.add_heading("1. Strategic Architecture Overview", level=1)
    doc.add_paragraph(
        "• Cluster 1: Electro-Mechanical Fleet Systems — Quick-disconnect magnetic charging interfaces (USPTO #63/734829), 360 kWh mobile battery trailers, and IEEE 15118-20 V2G grid balancing.\n"
        "• Cluster 2: Cryptographic Integrity Engine (JUDAS AI) — Multi-angle optical transfer gantries, edge defect computer vision (YOLO/ResNet), dual-hash SHA-256 state commitments, and zk-SNARK non-repudiation ledgers.\n"
        "• Cluster 3: Adaptive Route & Fleet Intelligence (CARI / CESAR) — Three-layer stochastic route optimization stack combining LASSO historical denoising, 10,000-iteration MCMC Metropolis-Hastings sampling, and APLRE human stabilization.\n"
        "• Cluster 4: Regulatory Compliance & Data Security — Automated CARB Clean Truck Check (13 CCR §§ 2195–2199) API handshakes, AES-256-GCM AAD-bound tenant isolation, and Verra VCS carbon accounting."
    )

    doc.add_heading("2. Granular Cluster Breakdown: Macro Systems vs. Micro Mechanics", level=1)

    # Cluster 1
    doc.add_heading("Cluster 1: Electro-Mechanical & Grid-Tied Fleet Systems", level=2)
    doc.add_paragraph(
        "• Macro System Overview: Fleet operators face physical fatigue and terminal downtime from handling heavy high-amperage charging cables, while utilities struggle with peak distribution constraints. The platform pairs a quick-disconnect magnetic coupling array with a mobile 360 kWh battery storage pod to absorb local demand spikes and participate in utility demand-response markets.\n"
        "• Micro Implementation Mechanics:\n"
        "  - Coupler Retention vs. Separation: Calibrated N52 neodymium permanent magnets deliver continuous mechanical retention during vehicle vibration, paired with a mechanical cam/lever linkage enabling operator disconnect under 25 lb of manual pull force.\n"
        "  - High-Voltage Optical Interlock: An optical emitter/detector loop monitors the physical interface. If coupling tension drops or separation begins, the circuit triggers a contactor trip in under 10 ms to de-energize the DC conductors before physical separation occurs.\n"
        "  - Grid Protocol Stack: The mobile storage trailer communicates via ISO 15118-20 (AC/DC Distributed Energy Resource Services) and UL 9741, allowing the battery management system (BMS) to automate peak-shaving dispatch against utility signals."
    )

    t1 = doc.add_table(rows=1, cols=3)
    t1.style = 'Table Grid'
    hdr1 = t1.rows[0].cells
    hdr1[0].text, hdr1[1].text, hdr1[2].text = "Architectural Layer", "Target Specification", "Statutory & Industry Benchmark"
    for row_data in [
        ("Physical Coupling", "N52 NdFeB magnetic array; <25 lb manual release", "USPTO Provisional #63/734829"),
        ("Safety Interlock", "Optical circuit; <10 ms de-energization loop", "37 CFR § 1.84 Drawing Sheet / UL 9741"),
        ("Trailer Storage", "360 kWh LFP pack (120 parallel strings)", "DOT Motor Carrier Safety Standards"),
        ("Grid Communication", "Bidirectional PLC / 10BASE-T1S Ethernet", "ISO 15118-20 / IEEE 1547-2018")
    ]:
        row = t1.add_row().cells
        row[0].text, row[1].text, row[2].text = row_data

    # Cluster 2
    doc.add_heading("Cluster 2: Cryptographic Audit & Integrity Engine (JUDAS AI)", level=2)
    doc.add_paragraph(
        "• Macro System Overview: Vehicle condition transfers between carriers, repair shops, and fleet depots traditionally rely on manual paper manifests that are prone to fraud and disputes. JUDAS AI creates a tamper-evident audit portal that verifies surface defects and authenticates condition reports without exposing private corporate fleet imagery.\n"
        "• Micro Implementation Mechanics:\n"
        "  - Boundary Capture: Calibrated optical gantries record vehicle panels across standardized lighting angles during entry and exit.\n"
        "  - Edge Defect Detection: Computer vision models (YOLO v8 / ResNet-50) infer surface defects, classifying scrapes, dents, and frame damage into localized bounding boxes with associated confidence scores.\n"
        "  - Dual-Hash Cryptographic Ledger: Raw pixel arrays produce a root SHA-256 state hash stored in an append-only ledger. To maintain carrier confidentiality, a zk-SNARK prover generates a Pedersen vector commitment proving the inspection occurred within specified defect parameters without publishing raw photos to outside parties."
    )

    # Cluster 3
    doc.add_heading("Cluster 3: Adaptive Route & Fleet Intelligence (CARI / CESAR)", level=2)
    doc.add_paragraph(
        "• Macro System Overview: Standard commercial navigation software optimizes purely for distance or road congestion, failing to account for real-time electricity tariff volatility, ambient temperature battery derating, and mandatory driver rest schedules. The CARI three-layer stack optimizes Class 8 electric freight routes around dynamic operating costs rather than simple mileage.\n"
        "• Micro Implementation Mechanics:\n"
        "  - Layer 1 (Regression Denoising): A regularized LASSO/OLS regression model normalizes 10 years of historical freight, fuel, and tariff noise to establish baseline cost distributions.\n"
        "  - Layer 2 (Stochastic Sampling): A Markov Chain Monte Carlo (MCMC) sampler executes 10,000 Metropolis-Hastings iterations, evaluating route candidates against live CAISO Day-Ahead and spot marginal electricity tariffs.\n"
        "  - Layer 3 (Behavioral Stabilization): The Adaptive Predictive Lead-Route Engine (APLRE) filters candidate routes through deterministic hash assignments and hard Federal Hours-of-Service (49 CFR Part 395) rest rules, preventing route switching that causes dispatcher confusion."
    )

    t3 = doc.add_table(rows=1, cols=3)
    t3.style = 'Table Grid'
    hdr3 = t3.rows[0].cells
    hdr3[0].text, hdr3[1].text, hdr3[2].text = "Three-Layer Stack", "Computational Engine", "Key Constraints Evaluated"
    for row_data in [
        ("Layer 1: Denoising", "LASSO regularized regression", "10-year macroeconomic freight and fuel noise"),
        ("Layer 2: Stochastic", "MCMC Metropolis-Hastings (10,000 runs)", "Real-time CAISO Locational Marginal Pricing (LMP)"),
        ("Layer 3: Stabilization", "APLRE deterministic hash assignment", "FMCSA 49 CFR Part 395 Hours-of-Service (HOS)")
    ]:
        row = t3.add_row().cells
        row[0].text, row[1].text, row[2].text = row_data

    # Cluster 4
    doc.add_heading("Cluster 4: Regulatory Compliance, Carbon Accounting & Data Security", level=2)
    doc.add_paragraph(
        "• Macro System Overview: Fleet managers spend significant administrative overhead navigating evolving emissions programs and financial incentive workflows. This architecture automates statutory compliance filings, isolates dealer tenant data, and tokenizes verified carbon offsets.\n"
        "• Micro Implementation Mechanics:\n"
        "  - CARB Clean Truck Check (HD I/M): The engine links directly to state endpoints, querying Vehicle Identification Numbers (VINs) against 13 CCR §§ 2195–2199 to log and submit periodic OBD testing and opacity verification receipts.\n"
        "  - Tenant Isolation (AEAD): Multi-dealer database records are encrypted with AES-256-GCM using isolated Data Encryption Keys (DEKs) bound with Authenticated Additional Data (AAD), preventing cross-tenant leakage in multi-dealer setups.\n"
        "  - Automated Incentive Engines: Ingestion agents assemble California Hybrid and Zero-Emission Truck and Bus Voucher Incentive Project (HVIP) applications and apply Verra VCS methodology to calculate per-haul carbon offsets within 1.4% of manual accounting."
    )

    doc.add_heading("3. Contemporaneous R&D Substantiation (IRC § 41)", level=1)
    doc.add_paragraph(
        "To support statutory patent enablement (35 U.S.C. § 112) and R&D tax eligibility (26 U.S.C. § 41), every architectural design decision is mapped to contemporaneously recorded experimental activities:\n"
        "• Permitted Purpose (26 CFR § 1.41-4(a)(2)): Inventions improve operational performance, functional reliability, or cost efficiency of core fleet processes.\n"
        "• Technological in Nature (26 CFR § 1.41-4(a)(3)): Discoveries fundamentally rely on mechanical engineering, computer science, and applied cryptography.\n"
        "• Elimination of Technical Uncertainty (26 CFR § 1.41-4(a)(4)): Addressed acute uncertainties including magnetic coupling road-retention vs. manual breakaway limits, and MCMC convergence under live CAISO price volatility.\n"
        "• Process of Experimentation (26 CFR § 1.41-4(a)(5)): Alternatives evaluated through 10,000-run Monte Carlo simulations, CAD stress tests, and A/B controlled cohort pilots."
    )

    doc.save(str(DOCX_PATH))
    print(f"[OK] Generated DOCX: {DOCX_PATH}")

def generate_pdf():
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=15, leading=19, textColor=colors.HexColor("#0f172a"), spaceAfter=5)
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=8.5, leading=11, textColor=colors.HexColor("#64748b"), spaceAfter=12)
    h1_style = ParagraphStyle('H1', parent=styles['Heading2'], fontSize=11, leading=15, textColor=colors.HexColor("#1e3a8a"), spaceBefore=10, spaceAfter=5)
    h2_style = ParagraphStyle('H2', parent=styles['Heading3'], fontSize=9.5, leading=13, textColor=colors.HexColor("#0f172a"), spaceBefore=7, spaceAfter=3)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8, leading=11, textColor=colors.HexColor("#334155"), spaceAfter=5)
    bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontSize=8, leading=11, textColor=colors.HexColor("#334155"), leftIndent=10, spaceAfter=3)
    tbl_hdr_style = ParagraphStyle('TH', parent=styles['Normal'], fontSize=7.5, leading=9.5, fontName="Helvetica-Bold", textColor=colors.white)
    tbl_cell_style = ParagraphStyle('TC', parent=styles['Normal'], fontSize=7, leading=9, textColor=colors.HexColor("#1e293b"))

    story = []

    story.append(Paragraph("EXECUTIVE RESEARCH & KNOWLEDGE TRANSLATION SUMMARY", title_style))
    story.append(Paragraph("CDLS Platform · Macro Strategic Overview vs. Micro Implementation Mechanics · 35 U.S.C. § 112 & IRC § 41", sub_style))
    story.append(Paragraph("This executive summary bridges backend technical experimentation with actionable product architecture and regulatory frameworks. It translates engineering findings across four patent clusters into macro-level system overviews and concrete micro-level implementation mechanics.", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Strategic Architecture Overview", h1_style))
    story.append(Paragraph("<b>Cluster 1: Electro-Mechanical Fleet Systems</b> — Quick-disconnect magnetic charging interfaces (USPTO #63/734829), 360 kWh mobile battery trailers, and IEEE 15118-20 V2G grid balancing.", bullet_style))
    story.append(Paragraph("<b>Cluster 2: Cryptographic Integrity Engine (JUDAS AI)</b> — Multi-angle optical transfer gantries, edge defect computer vision (YOLO/ResNet), dual-hash SHA-256 state commitments, and zk-SNARK non-repudiation ledgers.", bullet_style))
    story.append(Paragraph("<b>Cluster 3: Adaptive Route & Fleet Intelligence (CARI / CESAR)</b> — Three-layer stochastic route optimization stack combining LASSO historical denoising, 10,000-iteration MCMC Metropolis-Hastings sampling, and APLRE human stabilization.", bullet_style))
    story.append(Paragraph("<b>Cluster 4: Regulatory Compliance & Data Security</b> — Automated CARB Clean Truck Check (13 CCR §§ 2195–2199) API handshakes, AES-256-GCM AAD-bound tenant isolation, and Verra VCS carbon accounting.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Granular Cluster Breakdown: Macro Systems vs. Micro Mechanics", h1_style))
    
    # Cluster 1
    story.append(Paragraph("Cluster 1: Electro-Mechanical & Grid-Tied Fleet Systems", h2_style))
    story.append(Paragraph("<b>Macro System Overview:</b> Fleet operators face physical fatigue and terminal downtime from handling heavy charging cables, while utilities struggle with peak distribution constraints. The platform pairs a magnetic quick-disconnect array with a mobile 360 kWh battery storage pod to absorb local demand spikes and participate in utility demand-response markets.", body_style))
    story.append(Paragraph("<b>Micro Implementation Mechanics:</b> N52 NdFeB magnetic array calibrated for vehicle vibration retention vs. &lt;25 lb manual breakaway release; sub-10ms optical safety loop interlock; ISO 15118-20 / UL 9741 bidirectional power inverter automation.", body_style))

    data_t1 = [
        [Paragraph("Architectural Layer", tbl_hdr_style), Paragraph("Target Specification", tbl_hdr_style), Paragraph("Statutory / Industry Benchmark", tbl_hdr_style)],
        [Paragraph("Physical Coupling", tbl_cell_style), Paragraph("N52 NdFeB array; &lt;25 lb release", tbl_cell_style), Paragraph("USPTO Provisional #63/734829", tbl_cell_style)],
        [Paragraph("Safety Interlock", tbl_cell_style), Paragraph("Optical loop; &lt;10 ms de-energization", tbl_cell_style), Paragraph("37 CFR § 1.84 / UL 9741", tbl_cell_style)],
        [Paragraph("Trailer Storage", tbl_cell_style), Paragraph("360 kWh LFP pack (120 strings)", tbl_cell_style), Paragraph("DOT Motor Carrier Standards", tbl_cell_style)],
        [Paragraph("Grid Communication", tbl_cell_style), Paragraph("Bidirectional PLC / 10BASE-T1S", tbl_cell_style), Paragraph("ISO 15118-20 / IEEE 1547-2018", tbl_cell_style)]
    ]
    t1 = Table(data_t1, colWidths=[125, 185, 194])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t1)
    story.append(Spacer(1, 6))

    # Cluster 2
    story.append(Paragraph("Cluster 2: Cryptographic Audit & Integrity Engine (JUDAS AI)", h2_style))
    story.append(Paragraph("<b>Macro System Overview:</b> Eliminates disputed paper manifests during vehicle transfers by capturing tamper-evident optical records that prove surface defect status without exposing confidential fleet imagery.", body_style))
    story.append(Paragraph("<b>Micro Implementation Mechanics:</b> YOLO v8 / ResNet-50 defect inference; root SHA-256 raw image hash commit; zk-SNARK Pedersen vector commitment verification; append-only GAGAS audit ledger.", body_style))
    story.append(Spacer(1, 4))

    # Cluster 3
    story.append(Paragraph("Cluster 3: Adaptive Route & Fleet Intelligence (CARI / CESAR)", h2_style))
    story.append(Paragraph("<b>Macro System Overview:</b> Replaces static navigation with a dynamic cost-optimizing dispatcher accounting for live grid pricing, temperature derating, and mandatory driver rest breaks.", body_style))
    story.append(Paragraph("<b>Micro Implementation Mechanics:</b> Layer 1 LASSO 10-year denoising; Layer 2 MCMC Metropolis-Hastings (10,000 iterations against CAISO OASIS LMP feeds); Layer 3 APLRE behavioral stabilization enforcing FMCSA 49 CFR Part 395 HOS rules.", body_style))
    story.append(Spacer(1, 6))

    # Cluster 4
    story.append(Paragraph("Cluster 4: Regulatory Compliance, Carbon Accounting & Data Security", h2_style))
    story.append(Paragraph("<b>Macro System Overview:</b> Automates state zero-emission compliance, multi-tenant dealer credential protection, and tokenized carbon credit accounting.", body_style))
    story.append(Paragraph("<b>Micro Implementation Mechanics:</b> Automated VIN parsing against CARB Clean Truck Check (13 CCR §§ 2195–2199); AES-256-GCM envelope encryption with per-dealer isolated DEKs bound with AAD; automated HVIP voucher filing and Verra VCS carbon offset calculation within 1.4% of manual audit.", body_style))
    story.append(Spacer(1, 6))

    # Section 3
    story.append(Paragraph("3. Contemporaneous R&D Substantiation (IRC § 41)", h1_style))
    story.append(Paragraph("<b>• Permitted Purpose:</b> Enhances function, reliability, and cost-efficiency across fleet operations.", bullet_style))
    story.append(Paragraph("<b>• Technological in Nature:</b> Relies on computer science, mechanical engineering, and applied cryptography.", bullet_style))
    story.append(Paragraph("<b>• Elimination of Technical Uncertainty:</b> Resolves structural retention, MCMC convergence, and regulatory schema latency.", bullet_style))
    story.append(Paragraph("<b>• Process of Experimentation:</b> Systematically proven via 10,000-iteration simulations, CAD stress tests, and cohort trials.", bullet_style))

    doc.build(story)
    print(f"[OK] Generated PDF: {PDF_PATH}")

if __name__ == "__main__":
    generate_docx()
    generate_pdf()