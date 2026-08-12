# auditor_logic.py - ENHANCED VERSION WITH AITL CAPABILITIES

import psycopg2
import os
import smtplib
import ssl
import json
from fpdf import FPDF
from datetime import datetime, timedelta
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Load environment variables
load_dotenv()

class AuditReport(FPDF):
    """Enhanced PDF report with visualizations"""
    
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'CDLS PLATFORM: WEEKLY VARIANCE EXCEPTION REPORT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 8, f'California State Auditor Review', 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 6, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M PST")}', 0, 1, 'R')
        self.ln(8)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} | CONFIDENTIAL - For Institutional Review Only', 0, 0, 'C')
    
    def chapter_title(self, title, color=(0, 102, 153)):
        """Add styled chapter title"""
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(4)
    
    def add_metric_card(self, label, value, status='normal', x=None, y=None, w=90):
        """Add visual metric card"""
        if x and y:
            self.set_xy(x, y)
        
        # Status colors
        colors = {
            'good': (76, 175, 80),
            'warning': (255, 152, 0),
            'critical': (244, 67, 54),
            'normal': (97, 97, 97)
        }
        
        border_color = colors.get(status, colors['normal'])
        
        # Draw card
        self.set_draw_color(*border_color)
        self.set_line_width(0.8)
        self.rect(self.get_x(), self.get_y(), w, 20)
        
        # Label
        self.set_font('Arial', '', 9)
        self.set_text_color(97, 97, 97)
        self.cell(w, 8, label, 0, 1)
        
        # Value
        self.set_x(self.get_x())
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*border_color)
        self.cell(w, 10, str(value), 0, 1)
        
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)


class AuditorEngine:
    """Main audit processing engine with AITL capabilities"""
    
    def __init__(self):
        self.conn = None
        self.email_config = {
            'user': os.getenv('EMAIL_USER'),
            'password': os.getenv('EMAIL_PASS'),
            'receiver': os.getenv('EMAIL_RECEIVER'),
            'cc': os.getenv('EMAIL_CC', '').split(',') if os.getenv('EMAIL_CC') else []
        }
        
    def connect_db(self):
        """Establish database connection with retry logic"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                self.conn = psycopg2.connect(
                    host=os.getenv('DB_HOST'),
                    dbname=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASS'),
                    connect_timeout=10
                )
                return True
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise Exception(f"Database connection failed after {max_retries} attempts: {e}")
                time.sleep(2)
    
    def fetch_exception_data(self):
        """Fetch variance exceptions from institutional audit view"""
        cur = self.conn.cursor()
        
        # Main exceptions query
        cur.execute("""
            SELECT 
                transaction_id,
                haul_timestamp,
                integrity_score,
                reconciliation_status,
                gps_variance_pct,
                energy_variance_pct,
                financial_variance_pct,
                haul_token_tx_hash,
                carbon_mint_tx_hash,
                cesar_controller_id,
                exception_notes
            FROM institutional_audit_view
            ORDER BY integrity_score ASC, haul_timestamp DESC
            LIMIT 100
        """)
        
        exceptions = cur.fetchall()
        
        # Summary statistics
        cur.execute("""
            SELECT 
                COUNT(*) as total_transactions,
                COUNT(*) FILTER (WHERE integrity_score < 0.95) as flagged_count,
                AVG(integrity_score) as avg_integrity,
                COUNT(*) FILTER (WHERE reconciliation_status = 'exception') as critical_count,
                SUM(financial_variance_pct) FILTER (WHERE ABS(financial_variance_pct) > 5) as total_financial_variance
            FROM transaction_reconciliation
            WHERE created_at >= NOW() - INTERVAL '7 days'
        """)
        
        summary = cur.fetchone()
        
        # Regulatory compliance check
        cur.execute("""
            SELECT 
                alert_type,
                severity,
                message,
                created_at
            FROM regulatory_alerts
            WHERE created_at >= NOW() - INTERVAL '7 days'
                AND severity IN ('critical', 'high')
            ORDER BY created_at DESC
        """)
        
        alerts = cur.fetchall()
        
        cur.close()
        
        return {
            'exceptions': exceptions,
            'summary': summary,
            'alerts': alerts
        }
    
    def generate_visualizations(self, data):
        """Generate charts for the report"""
        
        # Integrity Score Distribution
        fig, axes = plt.subplots(2, 2, figsize=(11, 8))
        fig.suptitle('CDLS Platform Health Metrics (7-Day Window)', fontsize=14, fontweight='bold')
        
        # Chart 1: Integrity Score Distribution
        if data['exceptions']:
            integrity_scores = [float(row[2]) for row in data['exceptions']]
            axes[0, 0].hist(integrity_scores, bins=20, color='#4CAF50', edgecolor='black', alpha=0.7)
            axes[0, 0].axvline(x=0.95, color='red', linestyle='--', label='Threshold (95%)')
            axes[0, 0].set_xlabel('Integrity Score')
            axes[0, 0].set_ylabel('Frequency')
            axes[0, 0].set_title('Integrity Score Distribution')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
        
        # Chart 2: Variance Types
        gps_var = [abs(float(row[4])) for row in data['exceptions']]
        energy_var = [abs(float(row[5])) for row in data['exceptions']]
        financial_var = [abs(float(row[6])) for row in data['exceptions']]
        
        variance_types = ['GPS', 'Energy', 'Financial']
        variance_means = [
            np.mean(gps_var) if gps_var else 0,
            np.mean(energy_var) if energy_var else 0,
            np.mean(financial_var) if financial_var else 0
        ]
        
        colors = ['#2196F3', '#FF9800', '#9C27B0']
        axes[0, 1].bar(variance_types, variance_means, color=colors, edgecolor='black', alpha=0.7)
        axes[0, 1].set_ylabel('Average Variance (%)')
        axes[0, 1].set_title('Mean Variance by Type')
        axes[0, 1].axhline(y=5.0, color='red', linestyle='--', label='5% Threshold')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Chart 3: Daily Transaction Volume
        cur = self.conn.cursor()
        cur.execute("""
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as count
            FROM transaction_reconciliation
            WHERE created_at >= NOW() - INTERVAL '7 days'
            GROUP BY DATE(created_at)
            ORDER BY date
        """)
        daily_data = cur.fetchall()
        cur.close()
        
        if daily_data:
            dates = [row[0].strftime('%m/%d') for row in daily_data]
            counts = [row[1] for row in daily_data]
            axes[1, 0].plot(dates, counts, marker='o', color='#4CAF50', linewidth=2)
            axes[1, 0].fill_between(range(len(dates)), counts, alpha=0.3, color='#4CAF50')
            axes[1, 0].set_xlabel('Date')
            axes[1, 0].set_ylabel('Transactions')
            axes[1, 0].set_title('Daily Transaction Volume')
            axes[1, 0].grid(True, alpha=0.3)
        
        # Chart 4: Status Breakdown
        status_counts = {}
        for row in data['exceptions']:
            status = row[3]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            statuses = list(status_counts.keys())
            counts = list(status_counts.values())
            colors_map = {
                'verified': '#4CAF50',
                'review': '#FF9800',
                'exception': '#F44336'
            }
            pie_colors = [colors_map.get(s, '#9E9E9E') for s in statuses]
            
            axes[1, 1].pie(counts, labels=statuses, autopct='%1.1f%%', 
                          colors=pie_colors, startangle=90)
            axes[1, 1].set_title('Reconciliation Status Distribution')
        
        plt.tight_layout()
        chart_path = '/tmp/audit_charts.png'
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def generate_pdf_report(self, data):
        """Generate comprehensive PDF report"""
        pdf = AuditReport()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # Executive Summary Section
        pdf.chapter_title('EXECUTIVE SUMMARY', (0, 102, 153))
        
        summary = data['summary']
        total_txn = summary[0]
        flagged = summary[1]
        avg_integrity = summary[2]
        critical = summary[3]
        
        # Metric cards
        y_pos = pdf.get_y()
        pdf.add_metric_card(
            'Total Transactions (7d)',
            f'{total_txn:,}',
            'good',
            x=10, y=y_pos, w=45
        )
        
        pdf.add_metric_card(
            'Flagged for Review',
            f'{flagged}',
            'warning' if flagged > 0 else 'good',
            x=60, y=y_pos, w=45
        )
        
        pdf.add_metric_card(
            'Critical Exceptions',
            f'{critical}',
            'critical' if critical > 0 else 'good',
            x=110, y=y_pos, w=45
        )
        
        pdf.add_metric_card(
            'Avg Integrity Score',
            f'{float(avg_integrity)*100:.1f}%',
            'good' if float(avg_integrity) >= 0.95 else 'warning',
            x=160, y=y_pos, w=45
        )
        
        pdf.ln(28)
        
        # Risk Assessment
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 8, 'Risk Assessment:', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        risk_level = 'LOW'
        risk_color = (76, 175, 80)
        
        if critical > 5 or float(avg_integrity) < 0.90:
            risk_level = 'HIGH'
            risk_color = (244, 67, 54)
        elif critical > 0 or flagged > 10:
            risk_level = 'MEDIUM'
            risk_color = (255, 152, 0)
        
        pdf.set_fill_color(*risk_color)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(50, 8, f'Overall Risk: {risk_level}', 0, 1, 'C', True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        
        # Regulatory Alerts
        if data['alerts']:
            pdf.chapter_title('REGULATORY COMPLIANCE ALERTS', (211, 47, 47))
            
            for alert in data['alerts'][:5]:  # Top 5 alerts
                pdf.set_font('Arial', 'B', 10)
                pdf.set_text_color(244, 67, 54)
                pdf.cell(0, 6, f"• {alert[1].upper()}: {alert[0]}", 0, 1)
                pdf.set_text_color(0, 0, 0)
                pdf.set_font('Arial', '', 9)
                pdf.multi_cell(0, 5, f"  {alert[2]}")
                pdf.set_font('Arial', 'I', 8)
                pdf.cell(0, 5, f"  Timestamp: {alert[3].strftime('%Y-%m-%d %H:%M')}", 0, 1)
                pdf.ln(2)
        
        # Exception Details Table
        pdf.add_page()
        pdf.chapter_title('VARIANCE EXCEPTION DETAILS', (0, 102, 153))
        
        # Table Header
        pdf.set_fill_color(200, 220, 255)
        pdf.set_font('Arial', 'B', 9)
        
        col_widths = [35, 25, 25, 25, 25, 25, 30]
        headers = ['Transaction ID', 'Integrity', 'GPS Var%', 'Energy Var%', 
                  'Finance Var%', 'Status', 'Timestamp']
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 8, header, 1, 0, 'C', True)
        pdf.ln()
        
        # Table Data
        pdf.set_font('Arial', '', 8)
        
        for row in data['exceptions'][:25]:  # Top 25 exceptions
            # Color code by integrity score
            integrity = float(row[2])
            if integrity < 0.85:
                pdf.set_text_color(244, 67, 54)  # Red
            elif integrity < 0.95:
                pdf.set_text_color(255, 152, 0)  # Orange
            else:
                pdf.set_text_color(0, 0, 0)  # Black
            
            pdf.cell(col_widths[0], 7, str(row[0])[:10] + '...', 1, 0, 'C')
            pdf.cell(col_widths[1], 7, f'{integrity*100:.1f}%', 1, 0, 'C')
            pdf.cell(col_widths[2], 7, f'{abs(float(row[4])):.1f}%', 1, 0, 'C')
            pdf.cell(col_widths[3], 7, f'{abs(float(row[5])):.1f}%', 1, 0, 'C')
            pdf.cell(col_widths[4], 7, f'{abs(float(row[6])):.1f}%', 1, 0, 'C')
            pdf.cell(col_widths[5], 7, row[3].upper(), 1, 0, 'C')
            pdf.cell(col_widths[6], 7, row[1].strftime('%m/%d %H:%M'), 1, 1, 'C')
        
        pdf.set_text_color(0, 0, 0)
        
        # Add visualizations
        pdf.add_page()
        pdf.chapter_title('STATISTICAL ANALYSIS', (0, 102, 153))
        
        chart_path = self.generate_visualizations(data)
        pdf.image(chart_path, x=10, y=pdf.get_y(), w=190)
        
        # Recommendations
        pdf.add_page()
        pdf.chapter_title('AUDITOR RECOMMENDATIONS', (76, 175, 80))
        
        pdf.set_font('Arial', '', 10)
        recommendations = []
        
        if critical > 0:
            recommendations.append(
                f"CRITICAL: {critical} transactions require immediate manual review. "
                f"Investigate root causes of integrity scores below 85%."
            )
        
        if flagged > 20:
            recommendations.append(
                f"HIGH: {flagged} transactions flagged for review. "
                f"Consider implementing additional automated validation rules."
            )
        
        if float(avg_integrity) < 0.95:
            recommendations.append(
                f"MEDIUM: Average integrity score ({float(avg_integrity)*100:.1f}%) "
                f"below 95% threshold. Review data collection processes."
            )
        
        if not recommendations:
            recommendations.append(
                "All systems operating within acceptable parameters. "
                "Continue standard monitoring procedures."
            )
        
        for i, rec in enumerate(recommendations, 1):
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, f'{i}. ', 0, 0)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 6, rec)
            pdf.ln(3)
        
        # Sign-off section
        pdf.ln(10)
        pdf.set_font('Arial', 'I', 9)
        pdf.cell(0, 6, 'This report is automatically generated by the CDLS Audit Agent.', 0, 1)
        pdf.cell(0, 6, 'For questions, contact: engineering@californiadealerlogistics.com', 0, 1)
        
        # Save PDF
        file_path = f'/tmp/CDLS_Audit_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf'
        pdf.output(file_path, 'F')
        
        return file_path
    
    def send_email_report(self, pdf_path, data):
        """Send report via secure email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['user']
            msg['To'] = self.email_config['receiver']
            
            if self.email_config['cc']:
                msg['Cc'] = ', '.join(self.email_config['cc'])
            
            # Subject with risk indicator
            summary = data['summary']
            critical = summary[3]
            
            subject_prefix = '🔴 CRITICAL' if critical > 5 else '🟡 ALERT' if critical > 0 else '🟢 NORMAL'
            msg['Subject'] = f'{subject_prefix} CDLS Weekly Audit Report - {datetime.now().strftime("%Y-%m-%d")}'
            
            # Email body
            body = f"""
CALIFORNIA DEALER LOGISTICS SOLUTIONS
Weekly Variance Exception Report

SUMMARY:
• Total Transactions (7d): {summary[0]:,}
• Flagged for Review: {summary[1]}
• Critical Exceptions: {critical}
• Average Integrity Score: {float(summary[2])*100:.1f}%

{"⚠️ IMMEDIATE ACTION REQUIRED: " + str(critical) + " critical exceptions detected." if critical > 0 else "✓ All systems within acceptable parameters."}

Full analysis attached as PDF.

---
This is an automated report from the CDLS Audit Agent.
For technical support: engineering@californiadealerlogistics.com
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach PDF
            with open(pdf_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
                msg.attach(part)
            
            # Send via secure SMTP
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(self.email_config['user'], self.email_config['password'])
                
                recipients = [self.email_config['receiver']] + self.email_config['cc']
                server.sendmail(self.email_config['user'], recipients, msg.as_string())
            
            return True
            
        except Exception as e:
            print(f'Email transmission failed: {str(e)}')
            return False
    
    def log_audit_execution(self, success, data):
        """Log audit execution to database"""
        cur = self.conn.cursor()
        
        try:
            cur.execute("""
                INSERT INTO audit_execution_log 
                (execution_timestamp, success, total_exceptions, critical_count, metadata)
                VALUES (NOW(), %s, %s, %s, %s)
            """, (
                success,
                data['summary'][1],
                data['summary'][3],
                json.dumps({
                    'total_transactions': data['summary'][0],
                    'avg_integrity': float(data['summary'][2]),
                    'alert_count': len(data['alerts'])
                })
            ))
            
            self.conn.commit()
        except Exception as e:
            print(f'Failed to log audit execution: {str(e)}')
        finally:
            cur.close()
    
    def run(self):
        """Main execution flow"""
        try:
            print('Starting CDLS Audit Agent...')
            
            # Connect to database
            self.connect_db()
            print('Database connected.')
            
            # Fetch data
            print('Fetching exception data...')
            data = self.fetch_exception_data()
            print(f'Found {len(data["exceptions"])} exceptions to review.')
            
            # Generate PDF report
            print('Generating PDF report...')
            pdf_path = self.generate_pdf_report(data)
            print(f'Report generated: {pdf_path}')
            
            # Send email
            print('Sending email...')
            success = self.send_email_report(pdf_path, data)
            
            if success:
                print('✓ Email sent successfully.')
            else:
                print('✗ Email transmission failed.')
            
            # Log execution
            self.log_audit_execution(success, data)
            
            # Cleanup
            self.conn.close()
            
            print('Audit cycle complete.')
            return True
            
        except Exception as e:
            print(f'Audit execution failed: {str(e)}')
            import traceback
            traceback.print_exc()
            return False


def main():
    """Entry point"""
    engine = AuditorEngine()
    engine.run()


if __name__ == '__main__':
    main()