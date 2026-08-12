# CALIFORNIA STATE AUDITOR ENTERPRISE SYSTEM - USER GUIDE

**System Name:** CA-AUDIT (California Automated Universal Data Integrity Tracker)  
**Version:** 1.0 Enterprise Edition  
**Classification:** Official California State Government Use  
**Prepared For:** Bureau of State Audits Staff  
**Date:** February 6, 2026  

---

## TABLE OF CONTENTS

1. [Introduction](#introduction)
2. [Quick Start Guide](#quick-start-guide)
3. [User Roles & Permissions](#user-roles--permissions)
4. [Daily Operations](#daily-operations)
5. [Reading Audit Reports](#reading-audit-reports)
6. [Using the Dashboard](#using-the-dashboard)
7. [Department-Specific Auditing](#department-specific-auditing)
8. [Fraud Investigation Procedures](#fraud-investigation-procedures)
9. [Legislative Reporting](#legislative-reporting)
10. [Public Transparency Portal](#public-transparency-portal)
11. [Advanced Features](#advanced-features)
12. [Troubleshooting](#troubleshooting)
13. [Best Practices](#best-practices)
14. [Frequently Asked Questions](#frequently-asked-questions)

---

## INTRODUCTION

### What is CA-AUDIT?

The California State Auditor Enterprise System (CA-AUDIT) is an automated audit platform that provides comprehensive oversight of all 132 California state departments. The system operates 24/7 to ensure:

✅ **Financial Integrity** - Validates every transaction across state government  
✅ **Data Accountability** - Ensures accurate reporting and compliance  
✅ **Fraud Detection** - Identifies anomalies and suspicious patterns  
✅ **Regulatory Compliance** - Tracks adherence to state and federal requirements  
✅ **Public Transparency** - Provides taxpayers with government accountability  

### Who Uses This System?

**Primary Users:**
- California State Auditor and Deputy Auditors
- Bureau of State Audits staff
- Audit managers and analysts
- Department financial liaisons
- Legislative oversight staff

**Secondary Users:**
- Governor's Office
- Department of Finance
- Legislative fiscal committees
- General public (transparency portal)

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│           STATE AUDITOR EXECUTIVE DASHBOARD                 │
│  (State Auditor & Senior Leadership)                        │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
┌─────────────────────────────────────────────────────────────┐
│              CENTRAL AUDIT ENGINE                           │
│  • Master Database (PostgreSQL)                             │
│  • Analytics Engine (Python + R)                            │
│  • Fraud Detection AI                                       │
│  • Report Generation                                        │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
┌─────────────────────────────────────────────────────────────┐
│       DEPARTMENT AUDIT AGENTS (132 Departments)             │
│  Caltrans • CDCR • DOF • EDD • DHCS • CalPERS • UC         │
│  [and 125 more state departments and agencies]             │
└─────────────────────────────────────────────────────────────┘
```

---

## QUICK START GUIDE

### For State Auditor (Day 1)

**Morning Routine (10 minutes):**

1. **Check Daily Brief Email** (arrives 7:00 AM)
   - Review summary statistics
   - Note critical alerts
   - Identify departments needing attention

2. **Open Executive Dashboard**
   - URL: https://audit-admin.ca.gov
   - Login with State ID credentials
   - Review overnight audit results

3. **Prioritize Actions**
   - Critical (red) alerts: Immediate attention
   - High (orange) alerts: Same day review
   - Medium (yellow) alerts: Within 3 days

**Weekly Routine (Friday afternoon):**

1. **Review Weekly Statewide Report** (arrives 4:00 PM)
   - 50+ page comprehensive PDF
   - Department rankings
   - Fraud investigation summaries
   - Legislative briefing section

2. **Prepare for Monday Meetings**
   - Note items for staff discussion
   - Identify departments for deep dive
   - Flag items for legislative reporting

### For Audit Staff (Day 1)

**Getting Started:**

```bash
# 1. Access the System
URL: https://audit.ca.gov
Username: [Your State ID]
Password: [Initial password - will be prompted to change]

# 2. Enable Multi-Factor Authentication (Required)
Settings → Security → Enable MFA
Use authenticator app (Google Authenticator or Microsoft Authenticator)

# 3. Complete Training Modules
Dashboard → Training → Required Modules (4 hours)
- System Overview
- Fraud Detection Basics
- Report Generation
- Security & Compliance

# 4. Request Department Access
Settings → Access Requests → Select Departments
Manager approval required (24-48 hours)
```

**First Day Checklist:**

□ Login successfully  
□ Complete MFA setup  
□ Finish required training (4 hours)  
□ Request department access permissions  
□ Review sample audit reports  
□ Schedule onboarding meeting with manager  

---

## USER ROLES & PERMISSIONS

### Role 1: State Auditor

**Access Level:** Full system access (all 132 departments)

**Capabilities:**
- View all audit reports
- Approve public releases
- Authorize investigations
- Access confidential data
- Override system recommendations
- Testify to Legislature using system data

**Dashboard Features:**
- Statewide overview
- Department rankings
- Trend analysis
- Executive summaries
- Legislative report generator

**Login URL:** https://audit-admin.ca.gov

### Role 2: Deputy State Auditor

**Access Level:** Division-specific or multi-department

**Capabilities:**
- Conduct department audits
- Review fraud alerts
- Approve audit findings
- Assign investigations
- Generate reports for assigned departments
- Department liaison coordination

**Typical Assignment:**
- Financial Audits Division: DOF, Controller, Treasurer, FTB
- Health & Human Services: DHCS, DSS, DDS, DPH
- Transportation & Infrastructure: Caltrans, HSRA, DMV
- Higher Education: UC, CSU, CCC

### Role 3: Principal Auditor

**Access Level:** Department-specific

**Capabilities:**
- Perform detailed audits
- Analyze transactions
- Review compliance events
- Investigate anomalies
- Draft audit reports
- Conduct fieldwork

**Workflow:**
1. Receive assignment from Deputy
2. Access department data
3. Run queries and analytics
4. Document findings
5. Draft recommendations
6. Submit for review

### Role 4: Audit Analyst

**Access Level:** Read-only with analysis tools

**Capabilities:**
- Run standard reports
- Export data for analysis
- Create visualizations
- Track compliance metrics
- Support senior auditors

**Restrictions:**
- Cannot modify audit status
- Cannot approve reports
- Cannot access confidential investigations

### Role 5: Department Liaison

**Access Level:** Their department only

**Capabilities:**
- View audit results for their department
- Submit documentation
- Provide responses to findings
- Track remediation status
- Schedule auditor visits

**Responsibilities:**
- Coordinate with state auditors
- Provide requested documents
- Explain department processes
- Implement recommendations

### Role 6: Legislative Staff

**Access Level:** Published reports only

**Capabilities:**
- Download public reports
- View aggregated statistics
- Request custom analysis
- Track department performance

**Available Reports:**
- Quarterly performance summaries
- Annual comprehensive audits
- Special investigation reports
- Budget analysis documents

### Role 7: Public User

**Access Level:** Public transparency portal

**Capabilities:**
- View department scorecards
- Search expenditures >$10,000
- Download published reports
- Submit whistleblower tips (anonymous)

**Portal URL:** https://audits.ca.gov

---

## DAILY OPERATIONS

### Morning Routine (State Auditor)

**7:00 AM - Daily Brief Arrives**

Email format:
```
From: CA-AUDIT System <noreply@audit.ca.gov>
To: State.Auditor@bsa.ca.gov
Subject: 🟢 CA State Audit Daily Brief - February 6, 2026

OVERNIGHT SUMMARY:
• Departments Audited: 132
• Total Transactions: 45,230
• Critical Risk Departments: 3
• High Risk Departments: 12
• New Fraud Alerts: 5
• Compliance Violations: 8

IMMEDIATE ATTENTION REQUIRED:
1. DHCS - Budget variance 8.2% ($10.2B over allocated)
2. EDD - Duplicate payment pattern detected (3 instances)
3. Caltrans - Contract bid compliance issue (Case #2026-1234)

WEEKLY TREND:
• Average integrity score: 96.8% (↑0.3%)
• Fraud detection rate: 5.2 alerts/day (↓1.1)
• Compliance rate: 94.1% (↑2.1%)

ACCESS FULL DASHBOARD: https://audit-admin.ca.gov
VIEW DETAILED REPORT: [Attached PDF]
```

**7:15 AM - Review Dashboard**

1. Login to executive dashboard
2. Review "Critical Alerts" section
3. Check department risk heatmap
4. Note any new fraud investigations

**7:30 AM - Prioritize Day's Work**

Priority matrix:
```
CRITICAL (Handle Today):
• DHCS budget variance investigation
• EDD duplicate payment review
• Approve fraud investigation escalation

HIGH (Handle This Week):
• Caltrans contract compliance follow-up
• CalPERS quarterly performance review
• UC system procurement audit prep

MEDIUM (Handle This Month):
• DMV efficiency study
• DOF annual comprehensive audit
• Legislative testimony preparation
```

### Audit Staff Daily Workflow

**8:00 AM - Access Department Dashboard**

```
1. Login to https://audit.ca.gov

2. Navigate to "My Departments"
   Example: Health & Human Services Division
   - DHCS (Dept of Health Care Services)
   - DSS (Dept of Social Services)
   - DPH (Dept of Public Health)

3. Review Overnight Alerts
   Click: Dashboard → Alerts → Last 24 Hours
   
4. Sort by Priority
   Filter: Critical → High → Medium
```

**8:30 AM - Investigate Critical Alerts**

Example workflow for DHCS budget variance:

```
Step 1: Access Transaction Details
Dashboard → DHCS → Transactions → Filter by Date Range

Step 2: Run Variance Analysis
Tools → Financial Analysis → Budget vs. Actual
Time Period: Current Quarter
Account Codes: All

Step 3: Identify Anomalies
Output shows:
• Medi-Cal payments: $62.1B (Expected: $57.3B) = +8.4% variance
• Administrative costs: $1.2B (Expected: $1.1B) = +9.1% variance

Step 4: Drill Down
Click on Medi-Cal line item
Review top 50 largest transactions
Sort by variance percentage

Step 5: Document Findings
Tools → Report Generator → Variance Analysis Report
Add screenshots, data tables, preliminary conclusions

Step 6: Escalate if Needed
If fraud suspected: Tools → Create Fraud Alert
If compliance issue: Tools → Create Compliance Event
```

**Throughout the Day - Monitor Updates**

System provides real-time updates:
- New transactions flagged (push notifications)
- Fraud detection alerts (email + dashboard)
- Compliance violation events (requires acknowledgment)
- Department responses to findings

**5:00 PM - End of Day Summary**

Complete daily log:
```
Daily Activity Log Template:

Date: [Date]
Auditor: [Name]
Departments: [List]

ALERTS REVIEWED: [Count]
- Critical: [Number] - Status: [Resolved/Pending/Escalated]
- High: [Number] - Status: [Resolved/Pending/Escalated]

INVESTIGATIONS INITIATED: [Count]
- Fraud alerts: [Number]
- Compliance issues: [Number]

REPORTS GENERATED: [List]

MEETINGS/CALLS:
- Department liaisons: [List]
- Management: [Topics]

TOMORROW'S PRIORITIES:
1. [Item]
2. [Item]
3. [Item]

NOTES:
[Any relevant observations or concerns]
```

---

## READING AUDIT REPORTS

### Report Types

**1. Daily Brief (Email)**
- Arrives: 7:00 AM daily
- Length: 1-2 pages
- Audience: State Auditor
- Format: Text email + PDF attachment

**2. Weekly Statewide Report (PDF)**
- Arrives: Friday 4:00 PM
- Length: 50-75 pages
- Audience: State Auditor, Governor, Legislature
- Format: Comprehensive PDF with charts

**3. Monthly Department Deep Dive**
- Schedule: Rotating (each dept gets 1/month)
- Length: 40-60 pages
- Audience: Department leadership + State Auditor
- Format: Detailed analysis with recommendations

**4. Quarterly Legislative Report**
- Schedule: End of each quarter
- Length: 100-150 pages
- Audience: Legislative fiscal committees
- Format: Performance metrics + findings

**5. Annual Comprehensive Audit**
- Schedule: End of fiscal year
- Length: 500+ pages
- Audience: Public, Legislature, Governor
- Format: All departments, full year review

### Understanding the Weekly Statewide Report

**Page 1-2: Executive Summary**

```
Example:

CALIFORNIA STATE AUDITOR
Weekly Statewide Audit Report
Week Ending: February 6, 2026

OVERVIEW:
Total Departments Audited: 132
Total Transactions Reviewed: 316,610
Total Dollar Amount: $4.2 billion

RISK DISTRIBUTION:
Critical Risk: 3 departments (2.3%)
High Risk: 12 departments (9.1%)
Medium Risk: 35 departments (26.5%)
Low Risk: 82 departments (62.1%)

CRITICAL FINDINGS:
1. Department of Health Care Services (DHCS)
   Issue: Budget overrun in Medi-Cal program
   Amount: $4.9 billion over quarterly allocation
   Status: Investigation in progress
   
2. Employment Development Department (EDD)
   Issue: Duplicate payment pattern detected
   Amount: $2.3 million potentially affected
   Status: Fraud investigation initiated
   
3. Department of Transportation (Caltrans)
   Issue: Contract bid compliance violation
   Contract: CA-2026-1234 ($45M highway project)
   Status: Legal review requested

TOP PERFORMERS:
1. Department of Finance (DOF)
   Integrity Score: 99.2%
   Zero compliance violations
   
2. State Controller
   Integrity Score: 98.8%
   Exemplary financial controls

STATEWIDE METRICS:
Average Integrity Score: 96.8%
Compliance Rate: 94.1%
Fraud Detection Rate: 5.2 alerts/day
Budget Variance (statewide): -0.3% (under budget)
```

**Page 3-7: Department Rankings**

Table format:
```
RANK | DEPT ID  | DEPARTMENT NAME              | BUDGET    | INTEGRITY | RISK   |
-----|----------|------------------------------|-----------|-----------|--------|
1    | DOF      | Department of Finance        | $500M     | 99.2%     | LOW    |
2    | CONTROL  | State Controller             | $250M     | 98.8%     | LOW    |
3    | FTB      | Franchise Tax Board          | $1.1B     | 98.5%     | LOW    |
...
130  | EDD      | Employment Development       | $17B      | 88.2%     | HIGH   |
131  | DHCS     | Health Care Services         | $124B     | 85.1%     | CRITICAL|
132  | [DEPT]   | [Withheld - Investigation]   | [Amount]  | [Score]   | CRITICAL|
```

**Page 8-17: High-Risk Findings**

Detailed analysis of each critical/high-risk department:

```
DEPARTMENT: Health Care Services (DHCS)
BUDGET: $124 billion (largest state department)
INTEGRITY SCORE: 85.1% (Below 95% threshold)
RISK LEVEL: CRITICAL

FINDINGS:

Finding 1: Medi-Cal Payment Variance
• Expected Quarterly Spend: $57.3 billion
• Actual Quarterly Spend: $62.1 billion
• Variance: +$4.9 billion (+8.4%)
• Root Cause: Enrollment surge exceeding projections
• Recommendation: Request supplemental appropriation

Finding 2: Provider Payment Processing Delays
• Target: 30-day payment cycle
• Actual: 47-day average
• Impact: Provider complaints, potential penalties
• Root Cause: System capacity limitations
• Recommendation: IT infrastructure upgrade

Finding 3: Data Quality Issues
• Claims with missing data: 3.2%
• Duplicate records: 1.8%
• Impact: Reconciliation difficulties
• Recommendation: Enhanced data validation

FRAUD ALERTS: 2
• Alert FA-2026-0234: Potential duplicate provider payments ($1.2M)
• Alert FA-2026-0245: Unusual billing pattern (Provider #45782)

COMPLIANCE STATUS: 3 violations
• Federal reporting deadline missed (1/15/2026)
• State mandate SB 104 partial compliance
• HIPAA audit finding (minor - corrected)

DEPARTMENT RESPONSE:
[Attached separately - 5 pages]

AUDITOR RECOMMENDATIONS:
1. [Priority 1 - Immediate]
2. [Priority 2 - 30 days]
3. [Priority 3 - 90 days]

NEXT REVIEW: February 13, 2026 (weekly monitoring)
```

**Page 18-25: Fraud Investigations**

```
FRAUD INVESTIGATION SUMMARY

ACTIVE INVESTIGATIONS: 12
• Critical (potential >$1M): 3
• High (potential $100K-$1M): 5
• Medium (potential <$100K): 4

INVESTIGATION #FA-2026-0234
Department: DHCS
Alert Date: February 1, 2026
Detection Method: Duplicate Payment Algorithm
Estimated Loss: $1.2 million
Status: In Progress (35% complete)

Description:
System identified 47 instances of duplicate provider payments over 
a 6-month period. Same provider ID, same date of service, same 
procedure codes, different claim numbers. Pattern suggests either:
(a) System processing error, or
(b) Intentional duplicate submission by provider

Investigation Steps Completed:
✓ Confirmed duplicates in payment database
✓ Cross-referenced with provider records
✓ Interviewed DHCS payment processing staff
□ Provider interview (scheduled 2/10/2026)
□ Legal review
□ Recovery action plan

Investigator: Principal Auditor [Name]
Estimated Completion: February 28, 2026

[12 total investigations listed with similar detail]
```

**Page 26-35: Compliance Status**

```
REGULATORY COMPLIANCE OVERVIEW

FEDERAL REQUIREMENTS:
• Total Compliance Checks: 847
• Compliant: 798 (94.2%)
• Non-Compliant: 49 (5.8%)
• Under Review: 15

CRITICAL NON-COMPLIANCE ITEMS:
1. DHCS - Federal Medicaid reporting deadline missed
2. EDD - DOL unemployment data submission late
3. Caltrans - FHWA environmental compliance gap

STATE REQUIREMENTS:
• Total Compliance Checks: 1,243
• Compliant: 1,175 (94.5%)
• Non-Compliant: 68 (5.5%)

POLICY ADHERENCE:
• State Administrative Manual: 96.8% compliance
• Department of Finance procedures: 97.2%
• Procurement rules: 93.1%
```

**Page 36-45: Performance Metrics**

Charts and tables showing:
- Budget execution rates by department
- Service delivery metrics
- Efficiency indicators
- Outcome measurements
- Year-over-year comparisons

**Page 46-50: Legislative Section**

Tailored for Assembly Budget Committee and Senate Budget & Fiscal Review:
- Budget variance analysis
- Program effectiveness assessments
- Cost-benefit summaries
- Recommendations for legislative action

**Page 51+: Appendices**

- Detailed data tables
- Methodology explanations
- Glossary of terms
- Contact information
- Links to full documentation

---

## USING THE DASHBOARD

### Accessing the Dashboard

**URLs by Role:**

| Role | URL | Access Level |
|------|-----|--------------|
| State Auditor | https://audit-admin.ca.gov | Full access |
| Deputy/Principal Auditor | https://audit.ca.gov | Department-specific |
| Department Liaison | https://audit.ca.gov/dept | Own department only |
| Legislative Staff | https://audit.ca.gov/legislative | Published reports |
| Public | https://audits.ca.gov | Public transparency |

**Login Process:**

```
1. Navigate to appropriate URL
2. Enter State ID credentials
3. Complete MFA challenge (authenticator app)
4. Dashboard loads (5-10 seconds)
```

### Dashboard Layout (State Auditor View)

```
┌──────────────────────────────────────────────────────────────┐
│  [CA State Seal]  CALIFORNIA STATE AUDITOR          [Profile]│
│  Enterprise Audit System                           [Logout]  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  STATEWIDE OVERVIEW                          Last Updated: 2m│
│                                                               │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐│
│  │ Departments │ │ Transactions│ │   Critical  │ │  Fraud  ││
│  │   Audited   │ │    Today    │ │   Alerts    │ │ Alerts  ││
│  │             │ │             │ │             │ │         ││
│  │     132     │ │   45,230    │ │      3      │ │    5    ││
│  │   (100%)    │ │  ($4.2B)    │ │   (2.3%)    │ │ (0.01%) ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘│
│                                                               │
│  DEPARTMENT RISK HEATMAP                     [View All]      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ [Critical: 3] [High: 12] [Medium: 35] [Low: 82]     │   │
│  │                                                       │   │
│  │ DHCS ████ EDD ████ DEPT███                          │   │
│  │ [Click department for details]                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  RECENT ALERTS                               [Acknowledge]   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 🔴 CRITICAL - DHCS Budget Variance $4.9B            │   │
│  │    2 hours ago • Status: Investigating               │   │
│  │                                                       │   │
│  │ 🟡 HIGH - EDD Duplicate Payment Pattern             │   │
│  │    5 hours ago • Status: Fraud Investigation        │   │
│  │                                                       │   │
│  │ 🟡 HIGH - Caltrans Contract Compliance Issue        │   │
│  │    8 hours ago • Status: Legal Review                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  QUICK ACTIONS                                               │
│  [Generate Report] [View Department] [Create Investigation] │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Key Dashboard Features

**1. Department Selector**

Click any department to drill down:
```
Department: DHCS (Dept of Health Care Services)
├─ Overview
│  ├─ Budget: $124B
│  ├─ Employees: 5,000
│  ├─ Integrity Score: 85.1%
│  └─ Risk Level: CRITICAL
│
├─ Transactions
│  ├─ Last 24 Hours: 8,234 ($2.1B)
│  ├─ Last 7 Days: 57,638 ($14.7B)
│  ├─ Last 30 Days: 247,112 ($63.2B)
│  └─ Fiscal YTD: 1,235,560 ($310.5B)
│
├─ Alerts
│  ├─ Critical: 1 (Budget variance)
│  ├─ High: 2 (Fraud patterns)
│  ├─ Medium: 5 (Compliance issues)
│  └─ Low: 12 (Minor anomalies)
│
├─ Compliance
│  ├─ Federal: 94.2% compliant
│  ├─ State: 95.8% compliant
│  ├─ Policy: 96.1% compliant
│  └─ Violations: 3 active
│
├─ Fraud Detection
│  ├─ Active Investigations: 2
│  ├─ Closed (30 days): 5
│  ├─ False Positives: 8
│  └─ Confirmed Fraud: 1 ($120K recovered)
│
└─ Reports
   ├─ Daily Summaries
   ├─ Weekly Reviews
   ├─ Monthly Deep Dive
   └─ Custom Reports
```

**2. Transaction Search**

Powerful search capabilities:
```
Search Transactions

Date Range: [Start Date] to [End Date]
Department: [Select or All]
Amount Range: $[Min] to $[Max]
Transaction Type: [Expenditure/Revenue/Payroll/Grant/etc.]
Vendor: [Search by name or ID]
Status: [Verified/Review/Exception/All]

Advanced Filters:
□ Anomaly flags only
□ Fraud risk score > [0.5]
□ Integrity score < [0.95]
□ Blockchain verified
□ Compliance issues

[Search] [Clear] [Export Results]
```

**3. Analytics Tools**

Built-in analysis features:
```
Analytics Dashboard

├─ Trend Analysis
│  • Time series visualization
│  • Department comparisons
│  • Budget vs. actual tracking
│  • Seasonal patterns
│
├─ Risk Assessment
│  • Department risk scores
│  • Fraud probability models
│  • Compliance forecasting
│  • Variance predictions
│
├─ Performance Metrics
│  • Program effectiveness
│  • Service delivery quality
│  • Cost efficiency
│  • Outcome measurements
│
└─ Custom Reports
   • SQL query builder
   • Report templates
   • Export formats (PDF, Excel, CSV)
   • Scheduled delivery
```

**4. Real-Time Alerts**

Configurable notification system:
```
Alert Preferences

Email Notifications:
☑ Critical alerts (immediate)
☑ High alerts (within 1 hour)
☐ Medium alerts (daily digest)
☐ Low alerts (weekly summary)

Dashboard Notifications:
☑ Push notifications (requires browser permission)
☑ Sound alerts for critical issues
☑ Badge counters on tabs

SMS Notifications (Optional):
☐ Critical only (after-hours)
Phone: [___-___-____]

Alert Filters:
Departments: [Select specific departments]
Amount Threshold: Alerts for transactions > $[Amount]
Fraud Score: Alert if probability > [0.7]

[Save Preferences]
```

---

## DEPARTMENT-SPECIFIC AUDITING

### Conducting a Department Audit

**Step-by-Step Process:**

**Step 1: Prepare for Audit**

```
Pre-Audit Checklist:

□ Review previous audit reports
□ Check current risk assessment
□ Identify known issues or concerns
□ Review department organizational chart
□ Obtain recent budget documents
□ Schedule initial meeting with department liaison
□ Prepare audit notification letter
□ Assemble audit team
□ Set timeline and milestones
```

**Step 2: Initial Data Review**

Access department data in system:
```
Dashboard → [Department Name] → Overview

Review:
1. Transaction Volume
   • Daily average
   • Weekly trends
   • Monthly comparisons
   • Year-over-year growth

2. Financial Summary
   • Budget allocation
   • Expenditures to date
   • Revenue collected (if applicable)
   • Variance analysis

3. Compliance Status
   • Recent violations
   • Remediation status
   • Open issues
   • Historical compliance rate

4. Fraud Alerts
   • Active investigations
   • Closed cases
   • Pattern recognition results
   • Risk scoring

5. Performance Metrics
   • Program outcomes
   • Service delivery stats
   • Efficiency measures
   • Quality indicators
```

**Step 3: Run Standard Audit Queries**

```sql
-- Example: Top 100 Largest Transactions
SELECT 
    transaction_id,
    transaction_date,
    amount,
    vendor_name,
    description,
    integrity_score,
    audit_status
FROM department_transactions
WHERE dept_id = 'DHCS'
    AND transaction_date >= '2025-07-01'  -- FY start
ORDER BY amount DESC
LIMIT 100;

-- Example: Flagged Transactions
SELECT 
    transaction_id,
    amount,
    description,
    integrity_score,
    anomaly_flags,
    fraud_risk_score
FROM department_transactions
WHERE dept_id = 'DHCS'
    AND (
        integrity_score < 0.95 
        OR audit_status = 'exception'
        OR fraud_risk_score > 0.5
    )
ORDER BY fraud_risk_score DESC, integrity_score ASC;

-- Example: Vendor Analysis
SELECT 
    vendor_id,
    vendor_name,
    COUNT(*) as transaction_count,
    SUM(amount) as total_paid,
    AVG(integrity_score) as avg_integrity,
    COUNT(CASE WHEN audit_status = 'exception' THEN 1 END) as exceptions
FROM department_transactions
WHERE dept_id = 'DHCS'
    AND transaction_date >= '2025-07-01'
GROUP BY vendor_id, vendor_name
HAVING COUNT(*) > 10
ORDER BY total_paid DESC;
```

**Step 4: Fieldwork**

Conduct on-site review:
```
Fieldwork Activities:

1. Interview Key Personnel
   • Department director
   • Chief financial officer
   • Budget manager
   • Procurement officer
   • Program managers

2. Review Documentation
   • Contracts and agreements
   • Procurement files
   • Budget worksheets
   • Policy manuals
   • Previous audit responses

3. Test Internal Controls
   • Approval processes
   • Segregation of duties
   • Reconciliation procedures
   • IT access controls
   • Physical security

4. Sample Testing
   • Select random sample of transactions
   • Verify supporting documentation
   • Validate approval signatures
   • Check compliance with policies

5. Data Analytics
   • Run additional queries
   • Test fraud detection algorithms
   • Validate system calculations
   • Cross-reference external data sources
```

**Step 5: Document Findings**

Use system's report generator:
```
Tools → Report Generator → Department Audit

Template Sections:
1. Executive Summary
2. Scope and Methodology
3. Background
4. Findings and Recommendations
   • Finding 1: [Title]
     - Condition: [What was found]
     - Criteria: [What should be]
     - Cause: [Why it happened]
     - Effect: [Impact/risk]
     - Recommendation: [How to fix]
     - Department Response: [Their reply]
     - Auditor's Evaluation: [Assessment]
   • Finding 2: [Title]
   • [etc.]
5. Positive Observations
6. Appendices

[Generate Draft] [Submit for Review] [Finalize]
```

**Step 6: Issue Report**

```
Report Distribution Workflow:

1. Draft Completion
   ↓
2. Supervisor Review (2-3 days)
   ↓
3. Department Response Period (15 business days)
   ↓
4. Incorporate Department Response
   ↓
5. Legal Review (if needed)
   ↓
6. State Auditor Approval
   ↓
7. Public Release (if applicable)
   ↓
8. Legislative Notification
   ↓
9. Post-Release Follow-Up
```

---

## FRAUD INVESTIGATION PROCEDURES

### When to Initiate a Fraud Investigation

**Triggers:**

1. **System-Generated Alerts**
   - Fraud risk score >0.7
   - Statistical anomalies (Z-score >5)
   - Pattern recognition match
   - ML model prediction

2. **Manual Flags**
   - Auditor identifies suspicious pattern
   - Department reports potential fraud
   - Whistleblower complaint
   - External tip (law enforcement, media)

3. **Threshold Violations**
   - Single transaction >$1M with anomalies
   - Cumulative vendor payments >$10M with red flags
   - Employee with >100 exceptions
   - Department with >50 critical violations

### Investigation Process

**Phase 1: Initial Assessment (1-3 days)**

```
Step 1: Review Alert Details
Dashboard → Fraud Alerts → [Alert ID]

Alert Information:
- Alert Type: [Statistical/Pattern/ML/Whistleblower]
- Detection Date: [Date]
- Department: [Name]
- Estimated Loss: $[Amount]
- Confidence Level: [Percentage]
- Flagged Transactions: [Count]

Step 2: Preliminary Analysis
- Review transaction details
- Check vendor/employee history
- Search for similar patterns
- Assess materiality and risk

Step 3: Decision Point
□ Dismiss as false positive (document reason)
□ Flag for monitoring (set 30-day watch)
□ Initiate formal investigation (proceed to Phase 2)

[Make Decision] [Add Notes]
```

**Phase 2: Formal Investigation (2-8 weeks)**

```
Investigation Workflow:

1. Case Assignment
   • Assign lead investigator
   • Form investigation team (if needed)
   • Set timeline and milestones
   • Notify department (if appropriate)

2. Evidence Gathering
   Tools → Investigation → Create Case File

   Evidence Types:
   □ Transaction records
   □ Supporting documentation
   □ Email correspondence
   □ Interview notes
   □ Surveillance data (if applicable)
   □ External records (banks, vendors, etc.)

3. Secure Evidence Chain
   • Upload to case file system
   • Generate evidence hash
   • Blockchain anchor for immutability
   • Restrict access (need-to-know only)

4. Interviews
   Interview Log Template:
   
   Date: [Date]
   Interviewee: [Name], [Title]
   Interviewer(s): [Names]
   Location: [Place]
   Time: [Start] to [End]
   
   Purpose: [Brief description]
   
   Questions and Responses:
   [Detailed notes]
   
   Documents Provided:
   [List]
   
   Next Steps:
   [Action items]
   
   Signed: _________________ Date: _______

5. Analysis
   • Cross-reference evidence
   • Timeline construction
   • Network analysis (if collusion suspected)
   • Financial impact calculation
   • Probability assessment

6. Findings Documentation
   Investigation Report Sections:
   
   A. Case Summary
   B. Investigative Steps Taken
   C. Evidence Summary
   D. Analysis and Findings
   E. Probable Cause Determination
   F. Estimated Loss Calculation
   G. Recommendations
   H. Exhibits (evidence)
```

**Phase 3: Resolution (2-4 weeks)**

```
Resolution Options:

1. No Fraud Found
   • Document findings
   • Close investigation
   • Review detection algorithm (if false positive)
   • Archive case file

2. Fraud Confirmed - Internal
   • Refer to department for disciplinary action
   • Recommend control improvements
   • Initiate recovery process
   • Monitor remediation

3. Fraud Confirmed - Criminal
   • Prepare criminal referral package
   • Coordinate with law enforcement
     (AG's Office, District Attorney, FBI)
   • Preserve evidence
   • Provide expert testimony if needed

4. Fraud Suspected - Insufficient Evidence
   • Document preliminary findings
   • Set monitoring watch
   • Request additional resources
   • Plan follow-up investigation

Recovery Actions:
□ Demand letter to responsible party
□ Garnishment of wages/payments
□ Civil lawsuit
□ Insurance claim
□ Refer to Department of Justice
```

### Fraud Investigation Tools in System

**1. Network Analysis**

```
Tools → Fraud Investigation → Network Analysis

Purpose: Identify collusion patterns

Inputs:
- Employee ID or Vendor ID
- Date range
- Transaction minimum

Output:
- Visual network diagram
- Connection strength scores
- Suspicious relationship flags
- Community detection results

Example Result:
"Employee #12345 has unusually high transaction volume 
with Vendor #ABC-Corp ($2.3M over 6 months). Same employee 
also processes payments for Vendor #XYZ-Inc, which shares 
the same bank account as ABC-Corp. Potential shell company 
scheme."
```

**2. Timeline Builder**

```
Tools → Fraud Investigation → Timeline

Creates chronological view of:
- Transactions
- Approvals
- Communications
- Key events

Useful for:
- Identifying sequence of events
- Finding gaps or inconsistencies
- Presenting to prosecutors/judges
- Board/legislative testimony
```

**3. Benford's Law Analysis**

```
Tools → Fraud Investigation → Benford Analysis

Tests first-digit distribution of transaction amounts

Normal Distribution:
1: 30.1%
2: 17.6%
3: 12.5%
4: 9.7%
5: 7.9%
[etc.]

Suspicious if Chi-Square test p-value < 0.05

Example Alert:
"Department XYZ shows abnormal first-digit distribution
(p < 0.001). Excess of 5's and 0's suggests artificial 
round-number transactions. Recommend investigation."
```

**4. Duplicate Detection**

```
Tools → Fraud Investigation → Duplicate Finder

Search Criteria:
□ Same vendor + amount + date
□ Same vendor + amount (any date within X days)
□ Similar description (fuzzy match)
□ Same bank account (different vendor names)

Results:
Shows potential duplicate pairs with confidence scores
```

---

## LEGISLATIVE REPORTING

### Required Reports to Legislature

**1. Quarterly Performance Report**

**Recipients:**
- Assembly Budget Committee
- Assembly Budget Subcommittees (relevant)
- Senate Budget and Fiscal Review Committee
- Senate Budget Subcommittees (relevant)

**Due Dates:**
- Q1: October 30
- Q2: January 30
- Q3: April 30
- Q4: July 30

**Contents:**
```
I. EXECUTIVE SUMMARY (5 pages)
   • Statewide overview
   • Key findings
   • Critical issues
   • Recommendations

II. BUDGET ANALYSIS (15 pages)
   • Revenue vs. projections
   • Expenditure analysis
   • Variance explanations
   • Fund balance status

III. DEPARTMENT PERFORMANCE (30 pages)
   • By cabinet/agency
   • Budget execution rates
   • Program effectiveness
   • Service delivery metrics

IV. COMPLIANCE REPORT (10 pages)
   • Statutory requirements
   • Budget language compliance
   • Audit findings
   • Remediation status

V. FRAUD & WASTE DETECTION (5 pages)
   • Investigations summary
   • Recoveries
   • Prevention measures
   • Control improvements

VI. APPENDICES
   • Detailed data tables
   • Methodology
   • Department responses
```

**Generation in System:**
```
Reports → Legislative → Quarterly Performance

1. Select Quarter: [Q1/Q2/Q3/Q4]
2. Select Fiscal Year: [2025-26]
3. Template: [Standard Quarterly]
4. Include: 
   ☑ All departments
   ☑ Budget analysis
   ☑ Compliance status
   ☑ Fraud summary
   ☐ Detailed appendices (separate document)

[Generate Draft] [Review] [Submit to State Auditor]
```

**2. Annual Comprehensive Audit**

**Recipient:** General public, Legislature, Governor

**Due Date:** November 30 (following fiscal year end)

**Length:** 500-700 pages

**Process:**
```
Timeline:
July 1: FY ends
July-August: Data compilation and preliminary analysis
September: Department audits and fieldwork
October: Draft report preparation
November 1-15: Review and approval process
November 30: Public release

System Generation:
Reports → Legislative → Annual Comprehensive Audit

Components:
□ Statewide financial summary
□ All 132 department summaries
□ Major findings and recommendations
□ Fraud and waste report
□ Five-year trend analysis
□ Performance metrics dashboard
□ Legislative recommendations

[Generate] (Processing time: ~30 minutes for full report)
```

**3. Special Investigation Reports**

**Trigger:** Significant fraud, waste, or abuse finding

**Timeline:** As needed

**Process:**
```
1. State Auditor determines public interest
2. Investigation completion
3. Legal review
4. Department response period (15 days)
5. Report finalization
6. Legislative notification (72 hours advance)
7. Public release
8. Legislative hearing (if requested)

System Support:
Reports → Special Investigation Report

Template includes:
• Background
• Scope and methodology
• Findings
• Evidence summary
• Recommendations
• Department response
• Auditor's evaluation
• Corrective action plan
```

### Testifying to Legislature

**Preparation Using System:**

```
Tools → Legislative Testimony → Prep Package

Generates:
1. Executive Summary (1-page)
2. Talking Points (bullet format)
3. Anticipated Questions & Answers
4. Supporting Data Slides
5. Detailed Backup Materials

Example Package:

TESTIMONY: Assembly Budget Committee
DATE: February 15, 2026
TOPIC: Department of Health Care Services Budget Variance

TALKING POINTS:
• DHCS budget variance of $4.9B over quarterly allocation
• Primary cause: Medi-Cal enrollment surge (8.2% above projection)
• Not fraud or waste - legitimate program growth
• Requires supplemental appropriation
• Recommend enhanced enrollment forecasting

ANTICIPATED QUESTIONS:
Q: Why didn't the department request a budget augmentation earlier?
A: [Prepared response with data]

Q: How can we prevent this in the future?
A: [Recommendations with examples from other states]

Q: Is any of this money recoverable?
A: [Analysis of recoupment options]

SUPPORTING DATA:
[Charts and tables ready for projection]
```

---

## PUBLIC TRANSPARENCY PORTAL

### Portal Overview

**URL:** https://audits.ca.gov

**Purpose:** Provide taxpayers with access to government accountability data

**Available to Public (No Login Required):**

```
┌────────────────────────────────────────────────────────┐
│  CALIFORNIA STATE AUDITOR - PUBLIC TRANSPARENCY PORTAL  │
│  "Ensuring Accountability for California Taxpayers"    │
├────────────────────────────────────────────────────────┤
│                                                         │
│  [Search Box: Department, Vendor, Transaction, etc.]   │
│                                                         │
│  QUICK LINKS:                                          │
│  • Department Scorecards                               │
│  • Expenditure Search (Transactions >$10,000)         │
│  • Published Audit Reports                             │
│  • Performance Metrics                                 │
│  • Submit Whistleblower Tip (Anonymous)                │
│                                                         │
│  FEATURED REPORTS:                                     │
│  📄 2025-26 Annual Comprehensive Audit (Nov 30, 2025) │
│  📄 UC System Financial Audit (Jan 15, 2026)          │
│  📄 Caltrans Contract Compliance Report (Feb 1, 2026)  │
│                                                         │
│  STATEWIDE STATISTICS:                                 │
│  Total State Budget: $308 billion                      │
│  Departments Monitored: 132                            │
│  Transactions Audited (YTD): 14.2 million             │
│  Fraud Prevented (Est.): $47.3 million                │
│                                                         │
└────────────────────────────────────────────────────────┘
```

### Public Features

**1. Department Scorecards**

```
Example: Department of Transportation (Caltrans)

┌────────────────────────────────────────────┐
│  CALTRANS - DEPARTMENT SCORECARD            │
├────────────────────────────────────────────┤
│  Budget: $15.7 billion                      │
│  Employees: 20,000                          │
│                                             │
│  FISCAL YEAR 2025-26 PERFORMANCE:          │
│                                             │
│  Financial Integrity:     ████████░░ 89%   │
│  Budget Execution:        ██████████ 98%   │
│  Compliance Rating:       █████████░ 94%   │
│  Service Delivery:        ███████░░░ 87%   │
│                                             │
│  RECENT AUDIT FINDINGS: 3                  │
│  • Contract bid compliance (Feb 2026)      │
│  • Procurement delays (Jan 2026)           │
│  • Maintenance backlog (Dec 2025)          │
│                                             │
│  TREND: Improving ↗                        │
│                                             │
│  [View Full Report] [Download Data]        │
└────────────────────────────────────────────┘
```

**2. Expenditure Search**

```
Search Government Spending

All transactions over $10,000 are publicly searchable:

Filters:
Department: [Select or All]
Date Range: [Start] to [End]
Amount: $[Min] to $[Max]
Vendor: [Search]
Category: [Procurement/Payroll/Grant/etc.]

Example Search: "Tesla"

Results (15 transactions):
┌────────────────────────────────────────────────────┐
│ Date       | Dept    | Vendor       | Amount       │
├────────────┼─────────┼──────────────┼──────────────┤
│ 01/15/2026 | Caltrans| Tesla Inc    | $8,500,000   │
│ Purpose: Fleet vehicles (15 Tesla Semi trucks)     │
│ Contract: CA-2026-EV-001                           │
│ [View Details]                                      │
├────────────────────────────────────────────────────┤
│ 12/03/2025 | CHP     | Tesla Inc    | $2,100,000   │
│ Purpose: Police vehicles (30 Model Y)              │
│ [View Details]                                      │
└────────────────────────────────────────────────────┘

[Export Results (CSV)] [Download Report (PDF)]
```

**3. Whistleblower Portal**

```
┌──────────────────────────────────────────────┐
│  SUBMIT CONFIDENTIAL TIP                     │
├──────────────────────────────────────────────┤
│  Your identity will be protected by law.     │
│  (California Whistleblower Protection Act)   │
│                                              │
│  Type of Concern:                            │
│  ○ Fraud                                     │
│  ○ Waste                                     │
│  ○ Abuse                                     │
│  ○ Corruption                                │
│  ○ Safety Violation                          │
│  ○ Other                                     │
│                                              │
│  Department/Agency: [Select or type]         │
│                                              │
│  Description:                                │
│  [Text area - 2000 character limit]          │
│                                              │
│  Supporting Documents (Optional):            │
│  [Upload - Encrypted transmission]           │
│                                              │
│  Contact Information (Optional):             │
│  If you provide contact info, investigators  │
│  may reach out for additional information.   │
│  This is optional and anonymous submissions  │
│  are accepted.                               │
│                                              │
│  Email: [Optional]                           │
│  Phone: [Optional]                           │
│                                              │
│  [Submit Anonymously] [Cancel]               │
│                                              │
│  Your submission will generate a tracking    │
│  number. You can check status at:            │
│  https://audits.ca.gov/tip-status           │
└──────────────────────────────────────────────┘
```

### Managing Public Portal (Staff)

**Backend Access:**

```
Admin → Public Portal Management

Content Management:
• Update featured reports
• Post new scorecards
• Moderate comments (if enabled)
• Review analytics

Data Publication:
• Schedule report releases
• Set access permissions
• Redact confidential information
• Generate public-friendly summaries

Whistleblower Tips:
• Review submissions
• Assign to investigators
• Track status
• Respond to tipsters (if contact provided)

Analytics:
• Page views
• Report downloads
• Search queries
• User demographics (aggregated)
```

---

## ADVANCED FEATURES

### Custom SQL Queries

**For Advanced Users:**

```
Tools → Advanced → SQL Query Builder

Safety Features:
• Read-only access
• Query timeout (60 seconds)
• Result limit (10,000 rows)
• No DROP/DELETE/UPDATE commands
• Audit log of all queries

Example Queries:

-- Find vendors paid by multiple departments
SELECT 
    vendor_name,
    COUNT(DISTINCT dept_id) as dept_count,
    COUNT(*) as transaction_count,
    SUM(amount) as total_paid
FROM department_transactions
WHERE transaction_date >= '2025-07-01'
GROUP BY vendor_name
HAVING COUNT(DISTINCT dept_id) > 5
ORDER BY total_paid DESC;

-- Identify potential duplicate payments
SELECT 
    t1.transaction_id as txn1,
    t2.transaction_id as txn2,
    t1.vendor_id,
    t1.amount,
    t1.transaction_date as date1,
    t2.transaction_date as date2,
    ABS(t1.transaction_date - t2.transaction_date) as days_apart
FROM department_transactions t1
JOIN department_transactions t2 
    ON t1.vendor_id = t2.vendor_id
    AND t1.amount = t2.amount
    AND t1.dept_id = t2.dept_id
    AND t1.transaction_id < t2.transaction_id
WHERE ABS(t1.transaction_date - t2.transaction_date) <= 7
ORDER BY t1.amount DESC;

-- Budget execution rate by department
SELECT 
    d.dept_name,
    d.annual_budget,
    SUM(t.amount) as spent_ytd,
    (SUM(t.amount) / d.annual_budget * 100) as pct_spent,
    CASE 
        WHEN (SUM(t.amount) / d.annual_budget) > 0.85 THEN 'High'
        WHEN (SUM(t.amount) / d.annual_budget) > 0.70 THEN 'On Track'
        ELSE 'Low'
    END as burn_rate
FROM state_departments d
LEFT JOIN department_transactions t 
    ON d.dept_id = t.dept_id
    AND t.transaction_date >= '2025-07-01'
WHERE d.active = TRUE
GROUP BY d.dept_id, d.dept_name, d.annual_budget
ORDER BY pct_spent DESC;

[Execute Query] [Save Query] [Export Results]
```

### API Access

**For Developers and Researchers:**

```
Developer Portal: https://api.audit.ca.gov

Authentication:
• API key required (request from admin)
• Rate limit: 1,000 requests/hour
• HTTPS only
• OAuth 2.0 supported

Endpoints:

GET /v1/departments
Returns list of all 132 departments

GET /v1/departments/{dept_id}
Returns department details

GET /v1/departments/{dept_id}/transactions
Returns transactions (paginated)
Parameters: start_date, end_date, limit, offset

GET /v1/departments/{dept_id}/compliance
Returns compliance events

GET /v1/reports
Returns published audit reports

GET /v1/fraud-alerts
Returns public fraud summaries (redacted)

Example Request:
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "https://api.audit.ca.gov/v1/departments/CALTRANS/transactions?start_date=2025-01-01&limit=100"

Example Response:
{
  "dept_id": "CALTRANS",
  "transactions": [
    {
      "transaction_id": "uuid-here",
      "date": "2025-01-15",
      "amount": 8500000.00,
      "vendor": "Tesla Inc",
      "description": "Fleet vehicles - 15 Tesla Semi trucks",
      "integrity_score": 0.98
    },
    ...
  ],
  "total_count": 45230,
  "page": 1,
  "per_page": 100
}
```

### Scheduled Reports

**Automate Report Delivery:**

```
Reports → Schedule Report

Report Type: [Select template]
Frequency: 
○ Daily
○ Weekly (Select day: [Mon/Tue/etc.])
○ Monthly (Select date: [1-31])
○ Quarterly

Recipients:
[Email addresses, comma-separated]

Format:
☑ PDF
☑ Excel
☐ CSV

Filters:
Department: [Select or All]
Date Range: [Rolling X days] or [Fixed dates]
Include: [Checkboxes for sections]

[Create Schedule] [Test Run] [Cancel]
```

### Data Export

**Bulk Export Options:**

```
Tools → Data Export

Export Type:
○ Transaction data
○ Compliance events
○ Fraud alerts
○ Performance metrics
○ Reconciliation events

Time Range:
Start: [Date]
End: [Date]

Departments: [Select or All]

Format:
○ CSV (recommended for large datasets)
○ Excel (max 1M rows)
○ JSON
○ SQL dump

Compression: ☑ ZIP file

[Generate Export] (Processing time: ~5-30 minutes)
[Email when complete]
```

---

## TROUBLESHOOTING

### Common Issues

**Issue 1: Cannot Login**

```
Symptoms:
• "Invalid credentials" error
• Account locked message
• MFA not working

Solutions:
1. Verify username (should be State ID)
2. Reset password: Login page → "Forgot Password"
3. Check MFA app time sync
4. Clear browser cache
5. Try different browser
6. Contact IT helpdesk: (916) 445-0255

Security Note:
Account locks after 5 failed attempts (30-minute lockout)
```

**Issue 2: Slow Dashboard Performance**

```
Symptoms:
• Pages load slowly (>10 seconds)
• Timeouts
• Charts not rendering

Solutions:
1. Check internet connection speed
2. Clear browser cache
3. Reduce date range in queries
4. Use filters to limit results
5. Schedule large reports instead of real-time
6. Contact support if persistent

System Status: status.audit.ca.gov
```

**Issue 3: Report Generation Fails**

```
Symptoms:
• "Error generating report"
• Incomplete PDF
• Missing data

Solutions:
1. Verify date range is valid
2. Check department selection
3. Reduce scope (fewer departments/shorter time)
4. Try different template
5. Export as CSV instead
6. Contact support with error code

Error Codes:
E001: Database timeout (reduce scope)
E002: Permission denied (check access level)
E003: Invalid parameters (verify inputs)
```

**Issue 4: Missing Transactions**

```
Symptoms:
• Expected transactions not appearing
• Data gaps in timeline
• Count mismatch with department

Possible Causes:
1. Transaction below minimum threshold ($10K for public)
2. Confidential classification
3. Processing delay (up to 24 hours)
4. Department hasn't submitted data
5. Fiscal system integration issue

Resolution:
1. Check transaction threshold
2. Verify date range
3. Wait 24 hours for processing
4. Contact department liaison
5. File data quality issue: Tools → Report Issue
```

**Issue 5: Fraud Alert False Positive**

```
Symptoms:
• Alert generated but investigation finds no fraud
• Benford's Law violation but legitimate
• Duplicate payment is actually legitimate

Process:
1. Document investigation findings
2. Mark alert as "False Positive"
3. Add detailed notes explaining why
4. Flag for algorithm review

System Learning:
False positives are used to improve ML models
Feedback loop enhances future detection accuracy
```

### Getting Help

**Support Tiers:**

```
Tier 1: Help Desk
• Email: audit-support@bsa.ca.gov
• Phone: (916) 445-0255
• Hours: Mon-Fri, 8 AM - 5 PM PT
• Response: Within 4 hours

Tier 2: Technical Support
• For complex technical issues
• Escalated from Tier 1
• Response: Within 8 hours

Tier 3: Development Team
• For system bugs or feature requests
• Escalated from Tier 2
• Response: Within 24 hours

Emergency Support (After Hours):
• Critical security issues only
• Phone: (916) 445-URGENT
• State Auditor approval required
```

**Creating Support Tickets:**

```
Help → Submit Support Ticket

Priority:
○ Critical (system down, security breach)
○ High (major functionality broken)
○ Medium (feature not working as expected)
○ Low (question, enhancement request)

Category:
○ Login/Access
○ Data/Reporting
○ Performance
○ Training
○ Other

Description:
[Detailed description of issue]

Steps to Reproduce:
[What you did when error occurred]

Screenshots:
[Attach if helpful]

[Submit] [Cancel]

Ticket Tracking:
You'll receive a ticket number via email
Check status: Help → My Tickets
```

---

## BEST PRACTICES

### For Auditors

**1. Daily Routine**
```
Morning (30 minutes):
□ Check overnight alerts
□ Review dashboard summary
□ Prioritize critical issues
□ Update supervisor on status

Throughout Day:
□ Respond to alerts within SLA
  - Critical: 2 hours
  - High: Same day
  - Medium: 3 days
□ Document all findings in system
□ Follow up on pending items

End of Day (15 minutes):
□ Complete daily activity log
□ Set tomorrow's priorities
□ Escalate unresolved critical issues
```

**2. Investigation Quality**
```
Always:
✓ Document everything in case file
✓ Maintain evidence chain of custody
✓ Use system tools for analysis
✓ Cross-reference multiple data sources
✓ Get supervisor review before closing

Never:
✗ Work offline without documenting
✗ Share confidential info outside system
✗ Delete or modify original evidence
✗ Make accusations without proof
✗ Bypass approval workflows
```

**3. Report Writing**
```
Characteristics of Good Reports:
• Clear and concise
• Factual and objective
• Well-organized
• Supported by evidence
• Actionable recommendations
• Professional tone

Use Templates:
System provides templates for consistency
Customize as needed but maintain structure

Peer Review:
Always have colleague review before submission
```

### For Department Liaisons

**1. Responding to Findings**
```
Timeline:
• 15 business days to respond to draft report
• Extension possible (request in writing)

Response Should Include:
□ Agreement or disagreement with each finding
□ Explanation of disagreement (with evidence)
□ Corrective action plan
□ Responsible person/office
□ Implementation timeline
□ Resources needed

Template Available:
Reports → Department Response Template
```

**2. Providing Documentation**
```
When Auditors Request Documents:
• Respond within 5 business days
• Provide complete, unredacted versions
• Include metadata (dates, authors, etc.)
• Upload to secure system portal
• Don't email confidential documents

If Document Doesn't Exist:
• Explain why in writing
• Suggest alternative evidence
• Don't create documents after the fact
```

**3. Implementing Recommendations**
```
Track in System:
Dashboard → Recommendations → Track Implementation

For Each Recommendation:
□ Assign responsible person
□ Set target completion date
□ Create milestones
□ Update progress monthly
□ Upload evidence of completion
□ Request auditor verification

System automatically notifies auditors of updates
```

### For State Auditor

**1. Strategic Oversight**
```
Weekly Reviews:
• High-risk department trends
• Statewide fraud patterns
• Legislative priorities
• Public transparency metrics

Monthly Reviews:
• Department deep dive reports
• Audit team productivity
• System performance metrics
• Stakeholder feedback

Quarterly Reviews:
• Strategic plan progress
• Budget vs. actual
• Staffing needs
• Technology enhancements
```

**2. Legislative Relations**
```
Best Practices:
• Advance notification of significant findings
• Provide draft reports for review
• Offer briefings before public release
• Respond promptly to requests
• Testify with data-driven insights

Use System Tools:
• Legislative dashboard
• Testimony prep package
• Trend analysis
• Comparative data
```

**3. Public Communications**
```
Press Release Checklist:
□ Approved by legal counsel
□ Coordinated with Governor's office
□ Facts verified in system
□ Department response included
□ Report available on website
□ Media kit prepared

System Support:
Communications → Press Release Generator
Includes: Summary, key findings, quotes, data visuals
```

---

## FREQUENTLY ASKED QUESTIONS

**General System Questions**

**Q: How current is the data in the system?**
A: Transaction data is updated nightly. Most data is less than 24 hours old. Real-time data is available for some systems with direct integration.

**Q: Can I access the system from home?**
A: Yes, via VPN connection. Contact IT for VPN setup. Multi-factor authentication required.

**Q: What browsers are supported?**
A: Chrome, Firefox, Safari, and Edge (latest versions). Internet Explorer not supported.

**Q: Is there a mobile app?**
A: Not currently. The web interface is mobile-responsive but full functionality requires desktop browser.

**Q: Can I export data to Excel?**
A: Yes. Most reports and queries have export options in CSV or XLSX format.

**Audit-Specific Questions**

**Q: How are departments selected for deep-dive audits?**
A: Based on risk assessment (calculated daily), legislative requests, statutory requirements, and State Auditor discretion.

**Q: What is the difference between an audit and an investigation?**
A: Audits are planned reviews of department operations and finances. Investigations are triggered by specific fraud allegations or anomalies.

**Q: How long does a typical department audit take?**
A: Standard audit: 8-12 weeks. Deep dive: 12-16 weeks. Special investigations: 2-6 months depending on complexity.

**Q: Can departments see their real-time audit data?**
A: Department liaisons have read-only access to their own department's dashboard showing compliance status and flagged transactions.

**Q: What happens if a department disagrees with audit findings?**
A: They provide a formal response (included in final report). State Auditor evaluates the response and may modify findings or recommendations.

**Fraud Detection Questions**

**Q: How accurate is the fraud detection?**
A: Statistical methods: 95%+ accuracy. ML models: 92-96% accuracy (improving with more data). Human review required for all alerts.

**Q: How many fraud investigations are typical?**
A: Average 40-60 active investigations at any time. 70-80% are resolved as false positives or minor control issues. 20-30% result in referrals or recoveries.

**Q: What is the average recovery amount?**
A: $50M+ per year in prevented/recovered funds. Individual cases range from $10K to $5M+.

**Q: Who investigates fraud cases?**
A: Bureau of State Audits investigators, with support from department internal affairs, Attorney General, and law enforcement as needed.

**Q: Are whistleblowers protected?**
A: Yes, under California Whistleblower Protection Act. Retaliation is illegal and subject to penalties.

**Technical Questions**

**Q: What database does the system use?**
A: PostgreSQL 15+ with TimescaleDB for time-series data.

**Q: Is the data encrypted?**
A: Yes. AES-256 at rest, TLS 1.3 in transit.

**Q: How is data backed up?**
A: Daily full backups, hourly incrementals, 10-year retention. Geographic redundancy (Sacramento primary, LA secondary, AWS GovCloud tertiary).

**Q: Can the system handle increased transaction volume?**
A: Yes. Designed for 10M+ transactions per month. Currently processing 3-4M/month.

**Q: Is there an API for external systems?**
A: Yes. REST API available with authentication. Rate limits apply. Contact admin for API key.

**Compliance Questions**

**Q: What laws govern the State Auditor's authority?**
A: California Government Code sections 8543-8547.5, Public Contract Code, and statutory audit mandates for specific programs.

**Q: Can the State Auditor audit local governments?**
A: Only when specifically authorized by statute (e.g., special districts, certain grants). Most local government audits done by county auditors.

**Q: How are audit findings enforced?**
A: No direct enforcement power, but recommendations carry significant weight. Legislature can mandate compliance. Attorney General can prosecute fraud.

**Q: Are all audit reports public?**
A: Most are public under California Public Records Act. Exceptions: ongoing investigations, personnel matters, law enforcement sensitive, legally privileged.

**Q: How long are records retained?**
A: 10 years minimum per Government Code. Longer for fraud cases. Permanent retention for significant findings.

---

## APPENDICES

### Appendix A: Glossary of Terms

**Anomaly Score**: Numerical measure (0-1) of how unusual a transaction is compared to normal patterns. Higher scores indicate greater deviation.

**Benford's Law**: Mathematical principle stating that in naturally occurring datasets, the first digit 1 appears about 30% of the time, 2 appears 17.6%, etc. Violations suggest artificial number generation.

**Blockchain Anchor**: Process of recording a cryptographic hash of data on a blockchain to create immutable proof of its existence at a specific time.

**Compliance Event**: Documented instance of department adherence to (or violation of) a specific requirement (regulatory, policy, legal, or contractual).

**False Positive**: Fraud alert that upon investigation is determined not to be fraud. Used to improve detection algorithms.

**Integrity Score**: Composite measure (0-100%) of transaction data quality based on three-way reconciliation and validation checks.

**IQR (Interquartile Range)**: Statistical method for identifying outliers. Data points beyond 1.5 × IQR from the quartiles are flagged as anomalies.

**Isolation Forest**: Machine learning algorithm for unsupervised anomaly detection. Identifies outliers by how easily they can be separated from normal data.

**Reconciliation**: Process of comparing data from multiple independent sources (fiscal system, bank statements, general ledger) to ensure consistency.

**Risk Score**: Calculated measure (0-1) of department's probability of significant financial, compliance, or operational issues.

**Three-Way Reconciliation**: Validation of transactions by comparing three independent data sources.

**Z-Score**: Statistical measure of how many standard deviations a data point is from the mean. Z-scores >3 or <-3 are typically anomalous.

### Appendix B: System Shortcuts

**Keyboard Shortcuts**

```
Navigation:
Ctrl+H : Home/Dashboard
Ctrl+D : My Departments
Ctrl+R : Reports
Ctrl+A : Alerts
Ctrl+S : Search

Actions:
Ctrl+N : New investigation
Ctrl+E : Export current view
Ctrl+P : Print/Save as PDF
Ctrl+F : Find in page

Time Savers:
Ctrl+1 : Today's data
Ctrl+7 : Last 7 days
Ctrl+3 : Last 30 days
Ctrl+Q : Current quarter
Ctrl+Y : Current fiscal year
```

**Quick Filters**

```
Dashboard View:
Click department risk badge to filter:
• Red = Critical only
• Orange = High + Critical
• Yellow = Medium + High + Critical
• Green = All (unfilter)

Transaction List:
Click column header to sort
Shift+Click to multi-sort
Right-click header for filter options
```

### Appendix C: Contact Information

**Bureau of State Audits**
621 Capitol Mall, Suite 1200  
Sacramento, CA 95814  

**Main Office:** (916) 445-0255  
**Fax:** (916) 323-0913  
**Email:** contactus@bsa.ca.gov  

**System Support:**
**Email:** audit-support@bsa.ca.gov  
**Phone:** (916) 445-0255  
**Hours:** Monday-Friday, 8:00 AM - 5:00 PM PT  

**Emergency (After Hours):**
**Phone:** (916) 445-URGENT (8743)  
*For critical security issues only*

**Legislative Liaison:**
**Email:** legislative@bsa.ca.gov  
**Phone:** (916) 445-0255 x3001  

**Public Information Officer:**
**Email:** publicinfo@bsa.ca.gov  
**Phone:** (916) 445-0255 x3002  

**Whistleblower Hotline:**
**Phone:** 1-800-952-5665 (toll-free, anonymous)  
**Online:** https://audits.ca.gov/submit-tip  

---

**END OF USER GUIDE**

*This guide is updated quarterly. Current version: 1.0 (February 2026)*  
*Next update: May 2026*  
*Send feedback to: audit-support@bsa.ca.gov*
