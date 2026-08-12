#!/usr/bin/env python3
"""
CALIFORNIA STATE AUDITOR - MASTER AUDIT AGENT
Enterprise-grade automated audit system for all 132 California state departments

Version: 1.0
Classification: Official State Government Use
"""

import psycopg2
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import numpy as np
import pandas as pd
from fpdf import FPDF
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Load environment
load_dotenv()

# Department Registry (132 California State Departments)
DEPARTMENT_REGISTRY = {
    # EXECUTIVE BRANCH - Major Departments
    'CALTRANS': {
        'name': 'Department of Transportation',
        'agency': 'Transportation Agency',
        'annual_budget': 15700000000,
        'risk_level': 'HIGH',
        'audit_frequency': 'weekly'
    },
    'CDCR': {
        'name': 'Department of Corrections and Rehabilitation',
        'agency': 'Executive',
        'annual_budget': 15500000000,
        'risk_level': 'HIGH',
        'audit_frequency': 'weekly'
    },
    'DOF': {
        'name': 'Department of Finance',
        'agency': 'Executive',
        'annual_budget': 500000000,
        'risk_level': 'CRITICAL',
        'audit_frequency': 'daily'
    },
    'EDD': {
        'name': 'Employment Development Department',
        'agency': 'Labor and Workforce Development',
        'annual_budget': 17000000000,
        'risk_level': 'HIGH',
        'audit_frequency': 'weekly'
    },
    'DHCS': {
        'name': 'Department of Health Care Services',
        'agency': 'Health and Human Services',
        'annual_budget': 124000000000,
        'risk_level': 'CRITICAL',
        'audit_frequency': 'daily'
    },
    'DSS': {
        'name': 'Department of Social Services',
        'agency': 'Health and Human Services',
        'annual_budget': 32000000000,
        'risk_level': 'HIGH',
        'audit_frequency': 'weekly'
    },
    'DMV': {
        'name': 'Department of Motor Vehicles',
        'agency': 'Government Operations',
        'annual_budget': 1200000000,
        'risk_level': 'MEDIUM',
        'audit_frequency': 'bi-weekly'
    },
    'CALFIRE': {
        'name': 'Department of Forestry and Fire Protection',
        'agency': 'Natural Resources',
        'annual_budget': 3600000000,
        'risk_level': 'HIGH',
        'audit_frequency': 'weekly'
    },
    
    # CONSTITUTIONAL OFFICES
    'CONTROLLER': {
        'name': 'State Controller',
        'agency': 'Constitutional Office',
        'annual_budget': 250000000,
        'risk_level': 'CRITICAL',
        'audit_frequency': 'daily'
    },
    'TREASURER': {
        'name': 'State Treasurer',
        'agency': 'Constitutional Office',
        'annual_budget': 150000000,
        'risk_level': 'CRITICAL',
        'audit_frequency': 'daily'
    },
    'SOS': {
        'name': 'Secretary of State',
        'agency': 'Constitutional Office',
        'annual_budget': 100000000,
        'risk_level': 'MEDIUM',
        'audit_frequency': 'monthly'
    },
    
    # INDEPENDENT AGENCIES
    'CPUC': {
        'name': 'Public Utilities Commission',
        'agency': 'Independent',
        'annual_budget': 350000000,
        'risk_level': 'HIGH',
        'audit_frequency': 'weekly'
    },
    'CEC': {
        'name': 'Energy Commission',
        'agency': 'Independent',
        'annual_budget': 800000000,
        'risk_level': 'HIGH',
        'audit_frequency': 'weekly'
    },
    'CALPERS': {
        'name': 'Public Employees Retirement System',
        'agency': 'Independent',
        'annual_budget': 500000000,  # Admin budget
        'assets_under_management': 469000000000,
        'risk_level': 'CRITICAL',
        'audit_frequency': 'daily'
    },
    'CALSTRS': {
        'name': 'State Teachers Retirement System',
        'agency': 'Independent',
        'annual_budget': 400000000,
        'assets_under_management': 315000000000,
        'risk_level': 'CRITICAL',
        'audit_frequency': 'daily'
    },
    'UC': {
        'name': 'University of California',
        'agency': 'Higher Education',
        'annual_budget': 44000000000,
        'risk_level': 'HIGH',
        'audit_frequency': 'weekly'
    },
    'CSU': {
        'name': 'California State University',
        'agency': 'Higher Education',
        'annual_budget': 12000000000,
        'risk_level': 'HIGH',
        'audit_frequency': 'weekly'
    },
    
    # Add remaining 116 departments...
    # (Shortened for brevity - production system would include all 132)
}


class StateAuditorMasterAgent:
    """
    Master audit agent for California State Auditor
    Coordinates audits across all 132 state departments
    """
    
    def __init__(self):
        self.conn = None
        self.departments = DEPARTMENT_REGISTRY
        self.audit_date = datetime.now()
        
    def connect_database(self):
        """Connect to master audit database"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASS')
            )
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    def audit_department(self, dept_id):
        """
        Perform comprehensive audit of a single department
        """
        dept_info = self.departments.get(dept_id)
        if not dept_info:
            return None
        
        cur = self.conn.cursor()
        
        # 1. Financial Integrity Check
        financial_score = self.check_financial_integrity(dept_id, cur)
        
        # 2. Operational Compliance
        compliance_score = self.check_operational_compliance(dept_id, cur)
        
        # 3. Data Quality
        data_quality_score = self.check_data_quality(dept_id, cur)
        
        # 4. Fraud Detection
        fraud_alerts = self.detect_fraud(dept_id, cur)
        
        # 5. Performance Metrics
        performance = self.assess_performance(dept_id, cur)
        
        # Composite risk score
        risk_score = self.calculate_risk_score(
            financial_score,
            compliance_score,
            data_quality_score,
            len(fraud_alerts),
            performance
        )
        
        cur.close()
        
        return {
            'dept_id': dept_id,
            'dept_name': dept_info['name'],
            'audit_date': self.audit_date,
            'financial_integrity_score': financial_score,
            'operational_compliance_score': compliance_score,
            'data_quality_score': data_quality_score,
            'fraud_alerts': fraud_alerts,
            'performance_metrics': performance,
            'composite_risk_score': risk_score,
            'risk_level': self.categorize_risk(risk_score)
        }
    
    def check_financial_integrity(self, dept_id, cursor):
        """
        Validates financial transactions and reconciliation
        """
        # Query last 30 days of transactions
        cursor.execute("""
            SELECT 
                COUNT(*) as total_txns,
                SUM(amount) as total_amount,
                AVG(integrity_score) as avg_integrity,
                COUNT(*) FILTER (WHERE integrity_score < 0.95) as flagged_count,
                COUNT(*) FILTER (WHERE audit_status = 'exception') as exception_count
            FROM department_transactions
            WHERE dept_id = %s
                AND transaction_date >= NOW() - INTERVAL '30 days'
        """, (dept_id,))
        
        result = cursor.fetchone()
        
        if not result or result[0] == 0:
            return 1.0  # No transactions = perfect score (or N/A)
        
        total_txns = result[0]
        avg_integrity = result[2] or 1.0
        flagged_count = result[3] or 0
        exception_count = result[4] or 0
        
        # Calculate score (0-1 scale)
        flagged_rate = flagged_count / total_txns
        exception_rate = exception_count / total_txns
        
        # Weighted scoring
        score = (
            avg_integrity * 0.5 +
            (1 - flagged_rate) * 0.3 +
            (1 - exception_rate) * 0.2
        )
        
        return min(max(score, 0), 1)
    
    def check_operational_compliance(self, dept_id, cursor):
        """
        Checks policy adherence and regulatory compliance
        """
        cursor.execute("""
            SELECT 
                COUNT(*) as total_checks,
                COUNT(*) FILTER (WHERE compliance_status = 'Compliant') as compliant_count,
                COUNT(*) FILTER (WHERE violation_severity = 'Critical') as critical_violations
            FROM compliance_events
            WHERE dept_id = %s
                AND compliance_date >= NOW() - INTERVAL '30 days'
        """, (dept_id,))
        
        result = cursor.fetchone()
        
        if not result or result[0] == 0:
            return 1.0
        
        total_checks = result[0]
        compliant_count = result[1]
        critical_violations = result[2]
        
        compliance_rate = compliant_count / total_checks
        
        # Severe penalty for critical violations
        if critical_violations > 0:
            compliance_rate *= (1 - (critical_violations * 0.1))
        
        return min(max(compliance_rate, 0), 1)
    
    def check_data_quality(self, dept_id, cursor):
        """
        Assesses reporting accuracy and timeliness
        """
        cursor.execute("""
            SELECT 
                AVG(CASE 
                    WHEN report_submitted_date <= report_due_date THEN 1.0
                    ELSE 0.5
                END) as timeliness_score,
                AVG(data_completeness_pct) as completeness_score,
                AVG(data_accuracy_pct) as accuracy_score
            FROM reporting_submissions
            WHERE dept_id = %s
                AND report_period >= NOW() - INTERVAL '90 days'
        """, (dept_id,))
        
        result = cursor.fetchone()
        
        if not result:
            return 1.0
        
        timeliness = result[0] or 1.0
        completeness = result[1] or 1.0
        accuracy = result[2] or 1.0
        
        # Weighted average
        score = (
            timeliness * 0.3 +
            completeness * 0.3 +
            accuracy * 0.4
        )
        
        return score
    
    def detect_fraud(self, dept_id, cursor):
        """
        Multi-method fraud detection
        """
        alerts = []
        
        # Statistical anomaly detection
        cursor.execute("""
            SELECT 
                transaction_id,
                amount,
                description,
                vendor_name,
                anomaly_score
            FROM (
                SELECT *,
                    ABS((amount - AVG(amount) OVER ()) / STDDEV(amount) OVER ()) as anomaly_score
                FROM department_transactions
                WHERE dept_id = %s
                    AND transaction_date >= NOW() - INTERVAL '30 days'
            ) t
            WHERE anomaly_score > 3
            ORDER BY anomaly_score DESC
            LIMIT 10
        """, (dept_id,))
        
        statistical_anomalies = cursor.fetchall()
        
        for anomaly in statistical_anomalies:
            alerts.append({
                'type': 'statistical_anomaly',
                'transaction_id': anomaly[0],
                'amount': float(anomaly[1]),
                'description': anomaly[2],
                'vendor': anomaly[3],
                'severity': 'high' if anomaly[4] > 5 else 'medium',
                'z_score': float(anomaly[4])
            })
        
        # Duplicate payment detection
        cursor.execute("""
            SELECT 
                vendor_id,
                amount,
                COUNT(*) as duplicate_count,
                ARRAY_AGG(transaction_id) as txn_ids
            FROM department_transactions
            WHERE dept_id = %s
                AND transaction_date >= NOW() - INTERVAL '30 days'
            GROUP BY vendor_id, amount, DATE(transaction_date)
            HAVING COUNT(*) > 1
        """, (dept_id,))
        
        duplicates = cursor.fetchall()
        
        for dup in duplicates:
            alerts.append({
                'type': 'duplicate_payment',
                'vendor_id': dup[0],
                'amount': float(dup[1]),
                'count': dup[2],
                'transaction_ids': dup[3],
                'severity': 'critical'
            })
        
        # Round number analysis (Benford's Law violation)
        cursor.execute("""
            SELECT COUNT(*) FILTER (WHERE amount IN (1000, 5000, 10000, 50000, 100000)) as round_count,
                   COUNT(*) as total_count
            FROM department_transactions
            WHERE dept_id = %s
                AND transaction_date >= NOW() - INTERVAL '30 days'
                AND amount >= 1000
        """, (dept_id,))
        
        round_result = cursor.fetchone()
        if round_result and round_result[1] > 0:
            round_pct = round_result[0] / round_result[1]
            if round_pct > 0.15:  # >15% round numbers is suspicious
                alerts.append({
                    'type': 'benford_violation',
                    'round_number_pct': round_pct,
                    'severity': 'medium',
                    'description': f'{round_pct*100:.1f}% of transactions are round numbers'
                })
        
        return alerts
    
    def assess_performance(self, dept_id, cursor):
        """
        Department performance evaluation
        """
        cursor.execute("""
            SELECT 
                metric_name,
                metric_value,
                target_value,
                performance_rating
            FROM performance_metrics
            WHERE dept_id = %s
                AND metric_date >= NOW() - INTERVAL '30 days'
        """, (dept_id,))
        
        metrics = cursor.fetchall()
        
        performance_summary = {
            'total_metrics': len(metrics),
            'exceeds_count': sum(1 for m in metrics if m[3] == 'Exceeds'),
            'meets_count': sum(1 for m in metrics if m[3] == 'Meets'),
            'below_count': sum(1 for m in metrics if m[3] == 'Below'),
            'critical_count': sum(1 for m in metrics if m[3] == 'Critical')
        }
        
        return performance_summary
    
    def calculate_risk_score(self, financial, compliance, data_quality, fraud_count, performance):
        """
        Composite risk calculation
        """
        # Normalize scores (higher score = lower risk)
        financial_risk = 1 - financial
        compliance_risk = 1 - compliance
        data_risk = 1 - data_quality
        
        # Fraud penalty
        fraud_risk = min(fraud_count * 0.1, 0.5)  # Cap at 50%
        
        # Performance penalty
        if performance['total_metrics'] > 0:
            performance_risk = (
                performance['below_count'] + 
                performance['critical_count'] * 2
            ) / (performance['total_metrics'] * 2)
        else:
            performance_risk = 0
        
        # Weighted composite (higher = more risk)
        composite = (
            financial_risk * 0.35 +
            compliance_risk * 0.25 +
            data_risk * 0.20 +
            fraud_risk * 0.15 +
            performance_risk * 0.05
        )
        
        return composite
    
    def categorize_risk(self, risk_score):
        """Risk level categorization"""
        if risk_score >= 0.75:
            return 'CRITICAL'
        elif risk_score >= 0.50:
            return 'HIGH'
        elif risk_score >= 0.25:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def generate_statewide_report(self):
        """
        Generate consolidated report for all departments
        """
        print("Generating Statewide Audit Report...")
        
        all_audits = []
        
        # Audit each department
        for dept_id in self.departments.keys():
            print(f"  Auditing {dept_id}...")
            audit_result = self.audit_department(dept_id)
            if audit_result:
                all_audits.append(audit_result)
        
        # Sort by risk score (highest risk first)
        all_audits.sort(key=lambda x: x['composite_risk_score'], reverse=True)
        
        # Generate PDF report
        pdf_path = self.create_pdf_report(all_audits)
        
        # Send to State Auditor
        self.send_report(pdf_path, all_audits)
        
        return all_audits
    
    def create_pdf_report(self, audit_results):
        """
        Create comprehensive PDF report
        """
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'CALIFORNIA STATE AUDITOR', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, 'Statewide Department Audit Report', 0, 1, 'C')
        pdf.cell(0, 10, f'Report Date: {self.audit_date.strftime("%Y-%m-%d")}', 0, 1, 'C')
        pdf.ln(10)
        
        # Executive Summary
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'EXECUTIVE SUMMARY', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        critical = sum(1 for a in audit_results if a['risk_level'] == 'CRITICAL')
        high = sum(1 for a in audit_results if a['risk_level'] == 'HIGH')
        medium = sum(1 for a in audit_results if a['risk_level'] == 'MEDIUM')
        low = sum(1 for a in audit_results if a['risk_level'] == 'LOW')
        
        pdf.cell(0, 6, f'Total Departments Audited: {len(audit_results)}', 0, 1)
        pdf.cell(0, 6, f'Critical Risk: {critical}', 0, 1)
        pdf.cell(0, 6, f'High Risk: {high}', 0, 1)
        pdf.cell(0, 6, f'Medium Risk: {medium}', 0, 1)
        pdf.cell(0, 6, f'Low Risk: {low}', 0, 1)
        pdf.ln(10)
        
        # High Risk Departments Table
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'HIGH RISK DEPARTMENTS (Immediate Attention Required)', 0, 1)
        pdf.set_font('Arial', '', 9)
        
        # Table header
        pdf.cell(50, 8, 'Department', 1)
        pdf.cell(30, 8, 'Risk Level', 1)
        pdf.cell(30, 8, 'Financial', 1)
        pdf.cell(30, 8, 'Compliance', 1)
        pdf.cell(30, 8, 'Fraud Alerts', 1, 1)
        
        # Table data
        for audit in audit_results[:20]:  # Top 20 highest risk
            if audit['risk_level'] in ['CRITICAL', 'HIGH']:
                pdf.cell(50, 8, audit['dept_id'], 1)
                pdf.cell(30, 8, audit['risk_level'], 1)
                pdf.cell(30, 8, f"{audit['financial_integrity_score']*100:.1f}%", 1)
                pdf.cell(30, 8, f"{audit['operational_compliance_score']*100:.1f}%", 1)
                pdf.cell(30, 8, str(len(audit['fraud_alerts'])), 1, 1)
        
        # Save PDF
        output_path = f'/tmp/CA_State_Audit_{self.audit_date.strftime("%Y%m%d")}.pdf'
        pdf.output(output_path, 'F')
        
        return output_path
    
    def send_report(self, pdf_path, audit_results):
        """
        Email report to State Auditor
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = os.getenv('EMAIL_USER')
            msg['To'] = os.getenv('STATE_AUDITOR_EMAIL', 'auditor@bsa.ca.gov')
            
            # Count critical issues
            critical = sum(1 for a in audit_results if a['risk_level'] == 'CRITICAL')
            
            if critical > 5:
                subject_prefix = '🔴 CRITICAL'
            elif critical > 0:
                subject_prefix = '🟡 ALERT'
            else:
                subject_prefix = '🟢 NORMAL'
            
            msg['Subject'] = f'{subject_prefix} California Statewide Audit Report - {self.audit_date.strftime("%Y-%m-%d")}'
            
            # Email body
            body = f"""
California State Auditor
Statewide Department Audit Report

SUMMARY:
• Total Departments Audited: {len(audit_results)}
• Critical Risk Departments: {sum(1 for a in audit_results if a['risk_level'] == 'CRITICAL')}
• High Risk Departments: {sum(1 for a in audit_results if a['risk_level'] == 'HIGH')}
• Total Fraud Alerts: {sum(len(a['fraud_alerts']) for a in audit_results)}

{"⚠️ IMMEDIATE ACTION REQUIRED: " + str(critical) + " departments at CRITICAL risk." if critical > 0 else "✓ All departments within acceptable risk parameters."}

Full analysis attached as PDF.

---
This is an automated report from the California State Audit System.
Bureau of State Audits
California State Auditor's Office
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach PDF
            with open(pdf_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
                msg.attach(part)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
                server.sendmail(os.getenv('EMAIL_USER'), msg['To'], msg.as_string())
            
            print(f"✓ Report emailed to {msg['To']}")
            return True
            
        except Exception as e:
            print(f"✗ Email failed: {e}")
            return False
    
    def run(self):
        """Main execution"""
        print("=" * 60)
        print("CALIFORNIA STATE AUDITOR - MASTER AUDIT SYSTEM")
        print("=" * 60)
        print()
        
        if not self.connect_database():
            print("FATAL: Database connection failed")
            return False
        
        print("Database connected.")
        print(f"Auditing {len(self.departments)} state departments...")
        print()
        
        results = self.generate_statewide_report()
        
        print()
        print("=" * 60)
        print("AUDIT COMPLETE")
        print("=" * 60)
        print(f"Departments audited: {len(results)}")
        print(f"Critical risk: {sum(1 for r in results if r['risk_level'] == 'CRITICAL')}")
        print(f"High risk: {sum(1 for r in results if r['risk_level'] == 'HIGH')}")
        print()
        
        self.conn.close()
        return True


def main():
    """Entry point"""
    agent = StateAuditorMasterAgent()
    agent.run()


if __name__ == '__main__':
    main()
