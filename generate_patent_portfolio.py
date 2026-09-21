"""
Patent Portfolio & Engineering Disclosure Generator
Compiles technical disclosures, claims, prior art citations, and R&D logs
into a USPTO-ready Word specification (.docx).
"""

import os
from typing import Optional
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_full_patent_portfolio(output_path: str = "CDLS_IP_Patent_Portfolio_Submission.docx") -> str:
    doc = Document()

    # Set standard 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

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
        return p

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
        return p

    def add_claim_block(claim_text: str):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(claim_text)
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

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

    # Bibliographic Metadata Table
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
    add_p("This specification documents the novel technological solutions, enablement criteria, and statutory claim structures derived directly from qualified R&D activities across the CDLS platform:")
    clusters = [
        ("Cluster 1: Electro-Mechanical Fleet Systems — ", "High-amperage magnetic quick-disconnect charging couplers (USPTO #63/734829), mobile battery pod trailers (360 kWh), and IEEE 15118-20 bidirectional V2G grid interconnection architectures."),
        ("Cluster 2: Cryptographic Audit & Integrity Engine (JUDAS AI) — ", "Zero-knowledge proof verification pipeline utilizing dual-hash commitments, automated computer vision damage inspection, and GAGAS-compliant non-repudiation ledgers."),
        ("Cluster 3: Adaptive Route & Fleet Intelligence (CARI / CESAR) — ", "Three-layer stochastic route optimization engine combining regularized OLS noise elimination, Markov Chain Monte Carlo (MCMC) simulations, and A/B human-centric stabilization (APLRE)."),
        ("Cluster 4: Multi-Tenant Credential & Compliance Architecture — ", "AES-256-GCM authenticated envelope encryption (AAD-Bound AEAD) with hardware-isolated data encryption keys (DEKs) and real-time CARB CTC / TRUCRS API automation engines.")
    ]
    for prefix, body in clusters:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(prefix)
        r.bold = True
        p.add_run(body)

    # 2. Invention 1: MagSafe Coupler & V2G
    add_h("2. Invention Disclosure: Magnetic Quick-Disconnect & V2G Storage", level=1)
    add_p("USPTO Provisional Patent Application #63/734829 | IPC Classes: H01R, B60L, H02J", bold_prefix="Reference: ")
    add_h("2.1 Technical Field & Background Art", level=2)
    add_p("Technical Field: Heavy-duty electric vehicle (EV) charging interfaces, bidirectional vehicle-to-grid (V2G) power transmission, and automated breakaway coupling mechanisms.")
    add_p("Prior Art Deficiencies: Standard commercial high-power DC charging couplings (such as CCS Type 1/2 and MCS) use mechanical latch pins requiring >35 lb manual force. Under unexpected vehicle rollaway or severe trailer vibration, these rigid couplings cause mechanical shearing, contact pin deformation, and catastrophic arc-fault flashover.")
    
    add_h("2.2 Technical Uncertainties Resolved Through Experimentation", level=2)
    add_p("Magnetic Retention vs. Release Limits: Achieved N52 NdFeB magnetic coupling force sufficient for 1.5G RMS road vibration retention without exceeding <25 lb foot-pedal release ergonomic limits.")
    add_p("Arc-Fault Detection Interlock: Developed zero-latency auxiliary interlock de-energizing high-voltage contactors in <15 ms prior to complete mechanical separation.")
    add_p("Cell String Balancing During V2G ELRP Discharge: Validated that a 120-unit parallel LFP cell configuration (360 kWh mobile trailer) maintains balanced state-of-charge under high-rate discharge (38.4 kW over 5.8 hours) while preserving 3,000+ cycle lifespan under 80% depth-of-discharge (DoD).")

    add_h("2.3 Representative Claims", level=2)
    add_claim_block("1. An automated breakaway bidirectional electrical coupling assembly, comprising:\n"
                    "  a connector interface configured to conduct DC currents exceeding 200 amperes at voltages exceeding 350 volts DC;\n"
                    "  a magnetic retention array comprising rare-earth permanent magnets providing clamping force resisting vibration up to 1.5G RMS;\n"
                    "  a mechanical release linkage configured to overcome retention clamping force with an actuation force under 25 pounds; and\n"
                    "  an auxiliary sensing loop configured to de-energize high-voltage power contactors within 15 milliseconds of initial physical displacement.")
    add_claim_block("2. The electrical coupling assembly of claim 1, further comprising a mobile transport trailer housing a plurality of lithium iron phosphate (LFP) energy storage modules providing at least 360 kilowatt-hours of aggregate capacity configured to deliver bidirectional V2G power to an electrical grid in compliance with IEEE 15118-20 protocol standards.")

    # 3. Invention 2: JUDAS AI Cryptographic Audit
    add_h("3. Invention Disclosure: Cryptographic Zero-Knowledge Audit Kernel (JUDAS AI)", level=1)
    add_p("Project Code: COMPLIANCE-001 | IPC Classes: G06F 21/64, H04L 9/32, G06T 7/00", bold_prefix="Reference: ")
    add_h("3.1 Technical Field & Background Art", level=2)
    add_p("Technical Field: Cryptographic non-repudiation, computer vision inspection, Zero-Knowledge Proofs (ZKP), and regulatory audit integrity.")
    add_p("Prior Art Deficiencies: Transport carriers and dealerships experience billions in disputed cargo damage. Conventional digital inspection regimes upload full images to centralized databases, exposing commercial trade secrets, carrier location metadata, and customer PII, while remaining susceptible to post-hoc digital image manipulation.")

    add_h("3.2 Technical Uncertainties Resolved Through Experimentation", level=2)
    add_p("Non-Repudiation Without Image Disclosure: Benchmarked two-tier dual-hash commitment scheme (SHA-256 + Pedersen/zk-SNARKs) satisfying GAGAS audit standards for court-admissible condition verification without full imagery disclosure.")
    add_p("Variable Lighting CV Model: Benchmarked YOLO v8 against ResNet-50 on damage images across dawn/dusk/overcast conditions, achieving <5% false-negative rates at 0.5 IoU.")

    add_h("3.3 Representative Claims", level=2)
    add_claim_block("1. A computer-implemented method for verified condition auditing, comprising:\n"
                    "  capturing raw freight imagery via an optical sensor at an automotive transfer boundary;\n"
                    "  executing an inference pipeline over said raw freight imagery using a convolutional neural network fine-tuned to detect physical damage classifications with precision exceeding 90%;\n"
                    "  generating a dual-hash cryptographic commitment comprising a primary cryptographic hash of said raw freight imagery and an auxiliary zero-knowledge proof commitment;\n"
                    "  publishing said cryptographic commitment to an append-only verification ledger; and\n"
                    "  verifying non-repudiation of vehicle condition during a dispute by matching a challenged image against said published commitment without disclosing unredacted customer metadata.")

    # 4. Invention 3: Three-Layer Stochastic Route Optimization
    add_h("4. Invention Disclosure: Adaptive Three-Layer Route Intelligence Engine (CARI / CESAR)", level=1)
    add_p("Project Code: AI-001 | IPC Classes: G06Q 10/04, G06N 3/00", bold_prefix="Reference: ")
    add_h("4.1 Technical Field & Background Art", level=2)
    add_p("Technical Field: Real-time logistics dispatch, Markov Chain Monte Carlo (MCMC) routing, and behavioral stabilization.")
    add_p("Prior Art Deficiencies: Existing route solvers optimize purely for static distance, failing to integrate non-stationary wholesale energy market rates (CAISO day-ahead/real-time), dynamic battery derating, and driver compliance constraints, leading to route rejection rates >30%.")

    add_h("4.2 Technical Uncertainties Resolved Through Experimentation", level=2)
    add_p("10-Year Denoising: Applied LASSO-regularized OLS regression to separate true freight demand signals from historical macro anomalies (pandemics, port congestion).")
    add_p("Convergence Stability: Proved 10,000 Metropolis-Hastings iterations achieve stable P10/P90 confidence boundaries across 4 correlated variables.")
    add_p("Driver Variance Mitigation: Benchmarked hash-based deterministic A/B assignment (APLRE) across 6 pilot dealerships, reducing route variance to <10%.")

    add_h("4.3 Representative Claims", level=2)
    add_claim_block("1. A computer-implemented system for commercial freight route optimization, comprising:\n"
                    "  one or more hardware processors configured to execute an adaptive three-layer route intelligence engine comprising:\n"
                    "  (a) a foundation regression layer configured to establish baseline haul costs by regularizing multi-year logistics records;\n"
                    "  (b) a stochastic simulation layer configured to sample candidate routes using a Metropolis-Hastings Markov Chain Monte Carlo engine coupled to real-time electrical grid pricing feeds; and\n"
                    "  (c) an adaptive behavioral stabilization layer configured to assign route variants via deterministic hashing and adjust dispatch recommendations based on driver Hours-of-Service constraints.")

    # 5. Invention 4: Multi-Tenant Credential Boundary & CARB Automation
    add_h("5. Invention Disclosure: AAD-Bound AEAD Credential Boundary & Automated CARB Engine", level=1)
    add_p("Project Codes: DEALER-001 & COMPLIANCE-001 | IPC Classes: H04L 9/00, G06F 21/60", bold_prefix="Reference: ")
    add_h("5.1 Technical Field & Background Art", level=2)
    add_p("Technical Field: Multi-tenant cloud cryptographic isolation and automated environmental compliance filing (CARB CTC / TRUCRS).")
    add_p("Prior Art Deficiencies: Shared-database multi-tenant applications remain vulnerable to cross-tenant memory leakage. Environmental reporting under California Advanced Clean Fleets (ACF) requires extensive manual data consolidation across DMS providers.")

    add_h("5.2 Technical Uncertainties Resolved Through Experimentation", level=2)
    add_p("Cryptographic Boundary: Formulated AES-256-GCM envelope encryption binding tenant identifiers into Additional Authenticated Data (AAD), mathematically prohibiting ciphertext decryption in mismatched contexts.")
    add_p("Automated Regulatory API Handshake: Built a real-time VIN cross-query engine connecting to CARB Clean Truck Check (HD I/M) endpoints, eliminating manual paperwork under 13 CCR §§ 2195–2199.")

    # 6. Contemporaneous Evidence Ledger Table
    add_h("6. Contemporaneous R&D Experimental Evidence Ledger", level=1)
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
    print(f"[OK] Document generated at: {output_path}")
    return output_path

if __name__ == "__main__":
    create_full_patent_portfolio()