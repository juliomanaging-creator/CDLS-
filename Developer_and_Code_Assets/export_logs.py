from fpdf import FPDF
import os

def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=12)
    pdf.cell(200, 10, txt="IRON HALO - SYSTEM AUDIT REPORT", ln=True, align='C')
    
    log_path = "mesh_audit_log.txt"
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            for line in f:
                pdf.cell(200, 8, txt=line.strip(), ln=True)
    
    pdf.output("Halo_Audit_Report.pdf")
    print("PDF Generated.")

if __name__ == "__main__":
    create_pdf()