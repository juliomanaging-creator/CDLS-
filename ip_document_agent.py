"""
IP Document Generation Agent
Compiles verified R&D logs from SQLite into a formatted Word (.docx) patent specification.
"""

import logging
import os
import sqlite3
from datetime import datetime
from typing import Any, Optional

try:
    from logger import setup_logger  # type: ignore
    logger = setup_logger("ip_document_agent")
except ImportError:
    try:
        from utils.logger import setup_logger  # type: ignore
        logger = setup_logger("ip_document_agent")
    except ImportError:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("ip_document_agent")


class IPDocumentAgent:
    """Generates an IP disclosure document from R&D logs."""

    def __init__(self, config: dict, db_manager: Any):
        self.config = config
        self.db = db_manager

    def generate_ip_word_doc(self, output_path: str = "CDLS_IP_Patent_Portfolio_Submission.docx") -> str:
        try:
            from docx import Document
            from docx.shared import Inches, Pt, RGBColor
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            from docx.enum.table import WD_TABLE_ALIGNMENT
            from docx.oxml import parse_xml
            from docx.oxml.ns import nsdecls
        except ImportError:
            logger.error("python-docx is not installed. Please run: pip install python-docx")
            return ""

        if not self.db.sqlite_conn:
            logger.warning("Database connection unavailable for IP doc generation.")
            return ""

        cursor = self.db.sqlite_conn.cursor()
        cursor.execute("""
            SELECT title, content, domain, importance_score, url 
            FROM documents 
            WHERE source_category = 'rd_time_tracker' OR url LIKE '%.xlsx%'
            ORDER BY importance_score DESC
        """)
        records = cursor.fetchall()

        logger.info(f"Generating patent disclosure document from {len(records)} verified records...")

        doc = Document()
        for section in doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)

        NAVY = RGBColor(16, 44, 87)
        CHARCOAL = RGBColor(33, 37, 41)
        SLATE = RGBColor(100, 116, 139)

        def add_heading(text: str, level: int = 1):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(text)
            run.font.name = 'Calibri'
            run.font.bold = True
            if level == 1:
                run.font.size = Pt(15)
                run.font.color.rgb = NAVY
            elif level == 2:
                run.font.size = Pt(12.5)
                run.font.color.rgb = NAVY
            else:
                run.font.size = Pt(11)
                run.font.color.rgb = CHARCOAL

        def add_p(text: str = "", bold_prefix: Optional[str] = None):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            if bold_prefix:
                r_bold = p.add_run(bold_prefix)
                r_bold.font.name = 'Calibri'
                r_bold.font.size = Pt(10.5)
                r_bold.font.bold = True
                r_bold.font.color.rgb = CHARCOAL
            if text:
                r_text = p.add_run(text)
                r_text.font.name = 'Calibri'
                r_text.font.size = Pt(10.5)
                r_text.font.color.rgb = CHARCOAL
            return p

        # Title
        p_title = doc.add_paragraph()
        r_title = p_title.add_run("INTELLECTUAL PROPERTY DISCLOSURE & PATENT SPECIFICATION PORTFOLIO")
        r_title.font.name = 'Calibri'
        r_title.font.size = Pt(18)
        r_title.font.bold = True
        r_title.font.color.rgb = NAVY

        p_sub = doc.add_paragraph()
        r_sub = p_sub.add_run("Consolidated Technical Disclosures, Independent Claims, and R&D Verification for USPTO Filing")
        r_sub.font.name = 'Calibri'
        r_sub.font.size = Pt(11)
        r_sub.font.italic = True
        r_sub.font.color.rgb = SLATE

        # Metadata Table
        meta_table = doc.add_table(rows=5, cols=2)
        meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        meta_data = [
            ("Applicant / Assignee:", "California Investment Auto LP (CDLS Platform)"),
            ("Primary Inventor:", "Julio Cesar Umanzor"),
            ("Filing Status / Target:", "USPTO Non-Provisional & Provisional Patent Portfolio"),
            ("Related Filings:", "USPTO Provisional Patent Application #63/734829 (MagSafe Quick-Disconnect)"),
            ("Statutory Basis:", "35 U.S.C. § 101, § 102, § 103, § 112 | IRC § 41 Contemporaneous Support"),
        ]
        for i, (label, val) in enumerate(meta_data):
            row = meta_table.rows[i]
            cell_lbl, cell_val = row.cells[0], row.cells[1]
            cell_lbl.width, cell_val.width = Inches(2.2), Inches(4.3)
            cell_lbl.paragraphs[0].add_run(label).bold = True
            cell_val.paragraphs[0].add_run(val)
            shd = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
            cell_lbl._tc.get_or_add_tcPr().append(shd)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

        # 1. Executive Summary
        add_heading("1. Executive Summary of Patentable Inventions", level=1)
        add_p("This specification documents the novel technological solutions and statutory claim structures derived directly from qualified R&D activities across the CDLS platform:")
        clusters = [
            ("Cluster 1: Electro-Mechanical Fleet Systems — ", "High-amperage magnetic quick-disconnect charging couplers (USPTO #63/734829), mobile battery pod trailers (360 kWh), and IEEE 15118-20 bidirectional V2G grid interconnection architectures."),
            ("Cluster 2: Cryptographic Audit & Integrity Engine (JUDAS AI) — ", "Zero-knowledge proof verification pipeline utilizing dual-hash commitments, automated computer vision damage inspection, and GAGAS-compliant non-repudiation ledgers."),
            ("Cluster 3: Adaptive Route & Fleet Intelligence (CARI / CESAR) — ", "Three-layer stochastic route optimization engine combining regularized OLS noise elimination, Markov Chain Monte Carlo (MCMC) simulations, and A/B human-centric stabilization (APLRE)."),
            ("Cluster 4: Multi-Tenant Credential & Compliance Architecture — ", "AES-256-GCM authenticated envelope encryption (AAD-Bound AEAD) with hardware-isolated data encryption keys (DEKs) and real-time CARB CTC / TRUCRS API automation engines.")
        ]
        for c_title, c_desc in clusters:
            p_item = doc.add_paragraph(style='List Bullet')
            p_item.paragraph_format.space_after = Pt(2)
            r1 = p_item.add_run(c_title)
            r1.bold = True
            p_item.add_run(c_desc)

        # 2. Cluster 1: Electro-Mechanical Fleet Systems
        add_heading("2. Invention Disclosure: Magnetic Quick-Disconnect & V2G Storage", level=1)
        add_p("USPTO Provisional Patent Application #63/734829", bold_prefix="Reference: ")
        add_p("Technical Field: Heavy-duty electric vehicle (EV) charging interfaces, bidirectional vehicle-to-grid (V2G) power transmission, and automated breakaway coupling mechanisms.")
        add_p("Technical Uncertainties Resolved:")
        p1 = doc.add_paragraph(style='List Bullet')
        p1.add_run("Magnetic Retention vs. Release Limits: ").bold = True
        p1.add_run("Achieved N52 NdFeB magnetic coupling force sufficient for 1.5G RMS road vibration retention without exceeding <25 lb foot-pedal release ergonomic limits.")
        p2 = doc.add_paragraph(style='List Bullet')
        p2.add_run("Arc-Fault Detection Interlock: ").bold = True
        p2.add_run("Developed zero-latency auxiliary interlock de-energizing high-voltage contactors in <15 ms prior to complete mechanical separation.")

        add_heading("Exemplary Claim 1 (Breakaway Bidirectional Coupling):", level=3)
        add_p("1. An automated breakaway bidirectional electrical coupling assembly, comprising: a connector interface configured to conduct DC currents exceeding 200 amperes; a magnetic retention array comprising rare-earth permanent magnets providing clamping force resisting vibration up to 1.5G RMS; a mechanical release linkage configured to overcome retention clamping force with an actuation force under 25 pounds; and an auxiliary sensing loop configured to de-energize high-voltage power contactors within 15 milliseconds of physical displacement.")

        # 3. Cluster 2: Cryptographic Audit Engine
        add_heading("3. Invention Disclosure: Cryptographic Zero-Knowledge Audit Kernel (JUDAS AI)", level=1)
        add_p("Project Code: COMPLIANCE-001 | Zero-Knowledge Proofs & Computer Vision", bold_prefix="Reference: ")
        add_p("Technical Uncertainties Resolved:")
        p3 = doc.add_paragraph(style='List Bullet')
        p3.add_run("Non-Repudiation Without Image Disclosure: ").bold = True
        p3.add_run("Benchmarked two-tier dual-hash commitment scheme (SHA-256 + Pedersen/zk-SNARKs) satisfying GAGAS audit standards for court-admissible condition verification.")
        p4 = doc.add_paragraph(style='List Bullet')
        p4.add_run("Variable Lighting CV Model: ").bold = True
        p4.add_run("Benchmarked YOLO v8 against ResNet-50 on damage images across dawn/dusk/overcast conditions, achieving <5% false-negative rates at 0.5 IoU.")

        add_heading("Exemplary Claim 1 (Condition Auditing Method):", level=3)
        add_p("1. A computer-implemented method for verified condition auditing, comprising: capturing raw freight imagery via an optical sensor at an automotive transfer boundary; executing an inference pipeline to detect physical damage classifications with precision exceeding 90%; generating a dual-hash cryptographic commitment comprising a primary hash of raw imagery and an auxiliary zero-knowledge proof commitment; publishing said commitment to an append-only ledger; and verifying non-repudiation of vehicle condition during dispute resolution without disclosing unredacted customer metadata.")

        # 4. Verified R&D Evidence Index Table
        add_heading("4. Contemporaneous R&D Experimental Evidence Ledger", level=1)
        add_p("The following entries from the verified R&D tracker substantiate patent enablement under 35 U.S.C. § 112:")

        ev_table = doc.add_table(rows=1, cols=4)
        ev_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers = ["Date", "Project Code / Area", "Technical Uncertainty", "Experimental Validation"]
        for idx, h in enumerate(headers):
            cell = ev_table.rows[0].cells[idx]
            cell.paragraphs[0].add_run(h).bold = True
            shd = parse_xml(r'<w:shd {} w:fill="E2E8F0"/>'.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(shd)

        added_count = 0
        for title, content, domain, score, url in records:
            text = str(content)
            if any(k in text.lower() for k in ["uncertainty", "magsafe", "zkp", "mcmc", "carb", "patent"]):
                date_val, uncert, exper = "", "", ""
                for line in text.splitlines():
                    if line.startswith("Date:"):
                        date_val = line.replace("Date:", "").strip()
                    elif line.startswith("Technical Uncertainty:"):
                        uncert = line.replace("Technical Uncertainty:", "").strip()
                    elif line.startswith("Experimentation & Testing:"):
                        exper = line.replace("Experimentation & Testing:", "").strip()

                if uncert or exper:
                    row = ev_table.add_row()
                    row.cells[0].paragraphs[0].add_run(date_val[:10] if date_val else "R&D Phase")
                    row.cells[1].paragraphs[0].add_run(str(title)[:35]).bold = True
                    row.cells[2].paragraphs[0].add_run(uncert[:120] + ("..." if len(uncert) > 120 else ""))
                    row.cells[3].paragraphs[0].add_run(exper[:120] + ("..." if len(exper) > 120 else ""))
                    added_count += 1
                    if added_count >= 12:
                        break

        doc.save(output_path)
        logger.info(f"Patent specification document saved to {output_path}")
        return output_path