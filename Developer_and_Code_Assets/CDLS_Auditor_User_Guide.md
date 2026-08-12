# CDLS AUDITOR AGENT - COMPLETE USER GUIDE

**Version:** 2.0 - CalPERS Grade  
**Last Updated:** February 6, 2026  
**For:** Rebecca McNeil (COO & State Auditor), Operations Team  

---

## TABLE OF CONTENTS

1. [Quick Start Guide](#quick-start-guide)
2. [System Overview](#system-overview)
3. [Installation & Setup](#installation--setup)
4. [Daily Operations](#daily-operations)
5. [Reading Audit Reports](#reading-audit-reports)
6. [Using the Dashboard](#using-the-dashboard)
7. [Understanding Metrics](#understanding-metrics)
8. [Taking Action on Alerts](#taking-action-on-alerts)
9. [Advanced Features](#advanced-features)
10. [Troubleshooting](#troubleshooting)
11. [Analytics Capabilities](#analytics-capabilities)
12. [Frequently Asked Questions](#frequently-asked-questions)

---

## QUICK START GUIDE

### For Rebecca McNeil (Weekly Report Recipient)

**What You Get:**
- Every Friday at 4:00 PM: Email with PDF audit report
- 24/7 Access: Real-time dashboard at http://localhost:5000

**Quick Actions:**

```
┌─────────────────────────────────────────────────────────────┐
│ IF YOU SEE...              │ DO THIS...                     │
├────────────────────────────┼────────────────────────────────┤
│ 🟢 NORMAL in subject       │ Review PDF, no urgent action   │
│ 🟡 ALERT in subject        │ Review flagged transactions    │
│ 🔴 CRITICAL in subject     │ Immediate investigation needed │
└────────────────────────────┴────────────────────────────────┘
```

**First-Time Setup (5 minutes):**
1. Download the `.tar.gz` file
2. Extract: `tar -xzf CDLS_Auditor_Agent_v2.0_Complete.tar.gz`
3. Configure: `cp .env.example .env` and edit with your credentials
4. Deploy: `./deploy_setup.sh`
5. Wait for first email Friday at 4 PM

---

## SYSTEM OVERVIEW

### What This System Does

The CDLS Auditor Agent is your automated financial watchdog that:

✅ **Validates Every Transaction** - Checks 1,000+ transactions per week  
✅ **Detects Anomalies** - Flags irregularities before they become problems  
✅ **Monitors Compliance** - Tracks CA Competes ($1.22M) and HVIP ($330K/Semi)  
✅ **Provides Evidence** - Blockchain-verified audit trails for CalPERS  
✅ **Saves Time** - Automates 60+ hours of manual audit work per month  

### Three-Way Reconciliation

Every transaction is verified across three independent data sources:

```
     OPERATIONAL               FINANCIAL              ENVIRONMENTAL
    (Physical Proof)         (Payment Proof)          (Energy Proof)
         │                         │                        │
         ├─ GPS coordinates        ├─ $HAUL tokens         ├─ CESAR discharge
         ├─ Load manifest          ├─ USD payments         ├─ CAISO settlement
         └─ Driver signature       └─ $CARBON minting      └─ Battery SOC
                                   │
                                   ▼
                          INTEGRITY SCORE (0-100%)
                                   │
                          ┌────────┴────────┐
                          │                 │
                    ≥95%: VERIFIED    <85%: EXCEPTION
```

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    CDLS AUDITOR AGENT                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 WEEKLY REPORTS          📈 LIVE DASHBOARD                │
│  • PDF with charts          • Real-time metrics              │
│  • Email delivery           • Exception feed                 │
│  • Recommendations          • Alert monitoring               │
│                                                               │
│  🔍 ANALYTICS ENGINE        ⚡ DATA SOURCES                   │
│  • Python + Matplotlib      • PostgreSQL database            │
│  • R (optional advanced)    • Blockchain ledger              │
│  • Statistical models       • CESAR controllers              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## INSTALLATION & SETUP

### Prerequisites Checklist

Before starting, ensure you have:

```
□ Ubuntu 24.04 or macOS 14+ (or similar Unix system)
□ Python 3.8 or higher
□ PostgreSQL 15+ database (with ca_auditor database created)
□ Gmail account with App Password enabled
□ Database credentials (host, username, password)
□ Network access to CDLS platform systems
```

### Step 1: Extract the Package

```bash
# Download CDLS_Auditor_Agent_v2.0_Complete.tar.gz to your computer

# Extract
cd ~/Downloads  # or wherever you downloaded it
tar -xzf CDLS_Auditor_Agent_v2.0_Complete.tar.gz

# Navigate into directory
cd cdls-auditor-complete
```

### Step 2: Configure Credentials

**Create your configuration file:**

```bash
# Copy the template
cp .env.example .env

# Edit with your favorite editor
nano .env    # or: vim .env, code .env, etc.
```

**Fill in these required fields:**

```bash
# === DATABASE SETTINGS ===
DB_HOST=your-database-hostname.com       # Example: db.cdls.com
DB_NAME=ca_auditor
DB_USER=auditor
DB_PASS=YourSecureDatabasePassword123!

# === EMAIL SETTINGS ===
EMAIL_USER=rebecca.mcneil@gmail.com      # Your Gmail address
EMAIL_PASS=abcd efgh ijkl mnop           # 16-char App Password (see below)
EMAIL_RECEIVER=rebecca.mcneil@cdls.com   # Where to send reports
EMAIL_CC=julio.mcneil@cdls.com,james.wood@cdls.com  # Optional CC recipients
```

**🔑 How to Get Gmail App Password:**

1. Go to: https://myaccount.google.com/apppasswords
2. Sign in with your Google account
3. Click "Select app" → Choose "Mail"
4. Click "Select device" → Choose "Other" and type "CDLS Auditor"
5. Click "Generate"
6. Copy the 16-character code (format: `abcd efgh ijkl mnop`)
7. Paste into `.env` file under `EMAIL_PASS`

### Step 3: Run Automated Deployment

```bash
# Make the script executable
chmod +x deploy_setup.sh

# Run deployment
./deploy_setup.sh
```

**You'll see this output:**

```
=========================================
CDLS AUDITOR AGENT - DEPLOYMENT
CalPERS-Grade Institutional Readiness
=========================================

Checking Python installation... ✓ Python 3.11 detected
Installing Python dependencies... ✓ Dependencies installed
Checking configuration file... ✓ Configuration found
Securing configuration file... ✓ Permissions set
Creating directory structure... ✓ Directories created
Testing database connection... ✓ Database connection successful
Scheduling automated reports... ✓ Cron job scheduled
  Schedule: Every Friday at 4:00 PM
  Log file: /path/to/logs/cron.log

Start real-time dashboard? (y/n):
```

**Choose:**
- Type `y` to start the dashboard (recommended for Rebecca)
- Type `n` to skip (you can start it later)

**Then:**

```
Run test audit now? (y/n):
```

- Type `y` to generate your first report immediately
- Type `n` to wait for Friday

### Step 4: Verify Installation

**Check your email** - If you ran the test, you should receive:
- Email from: CDLS Audit Agent
- Subject: 🟢/🟡/🔴 CDLS Weekly Audit Report
- Attachment: PDF report

**Check the dashboard** - If you started it:
- Open browser to: http://localhost:5000
- You should see the live monitoring interface

---

## DAILY OPERATIONS

### For Rebecca McNeil (Primary Auditor)

**Your Weekly Routine:**

```
┌─────────────┬──────────────────────────────────────────────┐
│ DAY         │ ACTIVITY                                     │
├─────────────┼──────────────────────────────────────────────┤
│ Monday      │ • Check dashboard for weekend activity       │
│             │ • Review any critical alerts                 │
├─────────────┼──────────────────────────────────────────────┤
│ Tuesday-Thu │ • Monitor dashboard periodically             │
│             │ • Respond to any regulatory alerts           │
├─────────────┼──────────────────────────────────────────────┤
│ Friday 4PM  │ • Receive weekly audit report email          │
│             │ • Review PDF (15-20 minutes)                 │
│             │ • Follow up on critical exceptions           │
│             │ • Forward to Julio/James if needed           │
├─────────────┼──────────────────────────────────────────────┤
│ As Needed   │ • Run manual audit: python3 auditor_logic.py │
│             │ • Check dashboard during board meetings      │
└─────────────┴──────────────────────────────────────────────┘
```

**Daily Dashboard Check (2 minutes):**

1. Open: http://localhost:5000
2. Glance at 4 metric cards (top of page)
3. Scan regulatory alerts section
4. If anything is red/critical → Investigate immediately
5. If all green → Continue with your day

**When You See Critical Alerts:**

```
IMMEDIATE ACTION CHECKLIST:
□ Note the transaction IDs
□ Check blockchain verification hashes
□ Contact operations team about flagged transactions
□ Review CESAR controller logs for energy variances
□ Document findings in audit log
□ Escalate to Julio if >5 critical exceptions
```

### For Operations Team

**When Rebecca Escalates an Exception:**

1. **Locate Transaction Details**
   ```bash
   # Query database for specific transaction
   psql -d ca_auditor -c "SELECT * FROM transaction_reconciliation WHERE transaction_id = 'a7c3f2e1-4b...';"
   ```

2. **Review Three-Way Data**
   - GPS telemetry from Route Optimization Agent
   - Energy discharge from CESAR controller
   - Payment settlement from Financial Analytics Agent

3. **Investigate Variance**
   - GPS Variance >5% → Check route accuracy, traffic delays
   - Energy Variance >5% → Verify CESAR calibration, battery health
   - Financial Variance >5% → Reconcile payment timing, token settlement

4. **Document Resolution**
   ```bash
   # Update exception notes
   psql -d ca_auditor -c "UPDATE transaction_reconciliation 
      SET exception_notes = 'Resolved: GPS variance due to route detour for road closure' 
      WHERE transaction_id = 'a7c3f2e1-4b...';"
   ```

---

## READING AUDIT REPORTS

### Report Structure (7 Pages)

**Page 1: Executive Summary**
- 4 visual metric cards
- Risk level assessment (Low/Medium/High)
- Key findings bullet points

**Page 2: Regulatory Compliance Alerts**
- CA Competes job creation tracking
- HVIP mileage monitoring
- Other regulatory flags

**Page 3: Variance Exception Details**
- Table of 25 worst-performing transactions
- Color-coded by severity

**Page 4: Statistical Analysis**
- 4 professional charts with visualizations

**Page 5: Critical Exception Spotlight**
- Detailed breakdown of urgent issues

**Page 6: Auditor Recommendations**
- Prioritized action items

**Page 7: Blockchain Verification**
- Merkle roots and transaction hashes

### Understanding the Executive Summary

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Total Txns (7d) │ Flagged Review  │ Critical Except │ Avg Integrity   │
│                 │                 │                 │                 │
│      1,247      │       23        │        2        │     96.1%       │
│                 │                 │                 │                 │
│   [GOOD ✓]      │  [WARNING ⚠]    │  [CRITICAL !]   │   [GOOD ✓]      │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

**What Each Metric Means:**

**Total Transactions (7d)**
- Total hauls processed in last 7 days
- Benchmark: 1,000-1,500 per week (normal operations)
- Green if within range

**Flagged for Review**
- Transactions with integrity score <95%
- Acceptable: <5% of total
- Warning: 5-10% of total
- Critical: >10% of total

**Critical Exceptions**
- Transactions with integrity score <85%
- Acceptable: 0-1
- Warning: 2-5
- Critical: >5 (immediate escalation to Julio)

**Avg Integrity Score**
- Mean integrity across all transactions
- Excellent: >97%
- Good: 95-97%
- Concerning: 90-95%
- Critical: <90%

### Risk Level Interpretation

```
┌───────────┬──────────────┬────────────────────────────────┐
│ Risk Level│ Indicator    │ What It Means                  │
├───────────┼──────────────┼────────────────────────────────┤
│ LOW       │ 🟢 GREEN     │ All systems normal             │
│           │              │ • 0-1 critical exceptions      │
│           │              │ • <5% flagged                  │
│           │              │ • Avg integrity >95%           │
├───────────┼──────────────┼────────────────────────────────┤
│ MEDIUM    │ 🟡 YELLOW    │ Some issues need attention     │
│           │              │ • 2-5 critical exceptions      │
│           │              │ • 5-10% flagged                │
│           │              │ • Avg integrity 90-95%         │
├───────────┼──────────────┼────────────────────────────────┤
│ HIGH      │ 🔴 RED       │ Immediate action required      │
│           │              │ • >5 critical exceptions       │
│           │              │ • >10% flagged                 │
│           │              │ • Avg integrity <90%           │
└───────────┴──────────────┴────────────────────────────────┘
```

### Reading the Charts (Page 4)

**Chart 1: Integrity Score Distribution (Histogram)**
- Shows how transactions cluster by integrity score
- Look for: Most bars should be at 95-100% range
- Red flag: Large bars in the <90% range

**Chart 2: Mean Variance by Type (Bar Chart)**
- Compares GPS, Energy, and Financial variances
- Look for: All bars below 5% threshold line
- Red flag: Any bar above 5% indicates systemic issue

**Chart 3: Daily Transaction Volume (Line Chart)**
- Shows 7-day trend of transaction count
- Look for: Consistent volume, upward trajectory
- Red flag: Sudden drops (operational issues)

**Chart 4: Status Distribution (Pie Chart)**
- Breakdown of Verified/Review/Exception percentages
- Look for: 90%+ green (verified)
- Red flag: Red slice >5% (too many exceptions)

### Action Items from Recommendations

**Priority Levels:**

**CRITICAL** → Act within 24 hours
- Example: "2 transactions require immediate manual review"
- Action: Assign to operations team, track resolution

**HIGH** → Act within 3 days
- Example: "23 transactions flagged for review"
- Action: Review patterns, implement preventive measures

**MEDIUM** → Act within 1 week
- Example: "Average integrity below threshold"
- Action: Process improvement review

**STRATEGIC** → Act within 1 month
- Example: "CA Competes requires 2 additional hires"
- Action: Update recruitment timeline

---

## USING THE DASHBOARD

### Accessing the Dashboard

**URL:** http://localhost:5000  
**Access:** 24/7 from any device on the network  
**Browser:** Chrome, Firefox, Safari, Edge (modern browsers)

### Dashboard Layout

```
┌──────────────────────────────────────────────────────────────┐
│  🔍 CDLS AUDITOR DASHBOARD                    🟡 LIVE DEMO   │
│  Real-time platform monitoring for Rebecca McNeil            │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐│
│  │Txns Today │  │  Flagged  │  │ Critical  │  │Avg Integr.││
│  │    247    │  │    12     │  │     2     │  │   96.8%   ││
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘│
│                                                               │
│  ⚠️ REGULATORY COMPLIANCE ALERTS (24h)         [Refresh]    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ HIGH: CA Competes Job Creation Tracking              │   │
│  │ Need 2 additional hires by Q2                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  📊 LIVE EXCEPTION FEED                        [Refresh]    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ TxID      │Time   │Integrity│GPS%│Engy%│Fin%│Status │   │
│  │ a7c3f2e.. │14:32  │ 82.3%   │9.2 │11.5 │8.7 │EXCEPT │   │
│  │ b4d8e5f.. │14:15  │ 89.7%   │6.8 │5.2  │7.1 │REVIEW │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  Last updated: Just now • Auto-refresh: 30s                  │
└──────────────────────────────────────────────────────────────┘
```

### Dashboard Features

**Auto-Refresh (Every 30 seconds)**
- Metrics update automatically
- No manual refresh needed
- Fresh data indicator shows "Just now"

**Manual Refresh Buttons**
- Click "Refresh" on any section
- Forces immediate data update
- Useful during active monitoring

**Color Coding**
- **Green cards** = Good metrics
- **Orange cards** = Warning metrics
- **Red cards** = Critical metrics
- Matches email report color scheme

**Integrity Score Bars**
- Visual progress bars show transaction health
- Green: >95%, Orange: 85-95%, Red: <85%
- Quick visual scan capability

### Dashboard Best Practices

**Morning Check (5 minutes):**
1. Open dashboard
2. Scan 4 metric cards - any red?
3. Review regulatory alerts - any new?
4. Check exception feed - any patterns?
5. If all green → Close and continue

**During Board Meetings:**
- Pull up dashboard on projector
- Show real-time platform health
- Demonstrate institutional-grade monitoring
- Answer questions with live data

**When Investigating Issues:**
1. Keep dashboard open in browser tab
2. Cross-reference transaction IDs
3. Monitor live feed for related exceptions
4. Export data if needed (right-click table → copy)

---

## UNDERSTANDING METRICS

### Integrity Score Deep Dive

**Formula:**
```
Integrity = (GPS_Score × 0.3) + (Energy_Score × 0.4) + (Financial_Score × 0.3)

Where each component score:
  Component_Score = 1 - (Variance_Percentage / 100)
```

**Example Calculation:**

```
Transaction: Haul from Sacramento to San Francisco (350 miles)

EXPECTED VALUES:
GPS Distance: 350 miles
Energy Discharge: 595 kWh (1.7 kWh/mile)
Payment: $424.68 ($400 haul + $24.68 carbon credit)

ACTUAL VALUES:
GPS Distance: 358 miles (variance: 2.3%)
Energy Discharge: 612 kWh (variance: 2.9%)
Payment: $433.10 (variance: 2.0%)

CALCULATION:
GPS_Score = 1 - (2.3/100) = 0.977
Energy_Score = 1 - (2.9/100) = 0.971
Financial_Score = 1 - (2.0/100) = 0.980

Integrity = (0.977 × 0.3) + (0.971 × 0.4) + (0.980 × 0.3)
          = 0.2931 + 0.3884 + 0.2940
          = 0.9755
          = 97.55%

STATUS: VERIFIED ✓ (>95%)
```

**Why Different Weights?**
- Energy (40%) - Highest weight because it's hardest to fake
- GPS (30%) - Physical proof, but can have legitimate variance
- Financial (30%) - Important but derivative of other two

### Variance Thresholds Explained

```
VARIANCE LEVEL    │ PERCENTAGE │ INTERPRETATION
──────────────────┼────────────┼─────────────────────────────
Excellent         │ 0-2%       │ Normal operational variation
Acceptable        │ 2-5%       │ Within tolerance, monitor
Concerning        │ 5-10%      │ Investigate cause
Critical          │ >10%       │ Data integrity issue
```

**Common Causes of Variance:**

**GPS Variance:**
- Traffic detours or route changes
- GPS signal loss in tunnels/urban canyons
- Data transmission delays
- Manual route adjustments

**Energy Variance:**
- Battery degradation
- Weather conditions (cold = higher consumption)
- Driving behavior (speed, acceleration)
- CESAR controller calibration drift

**Financial Variance:**
- Payment timing mismatches
- Blockchain settlement delays
- Token price fluctuations
- Fee calculation differences

---

## TAKING ACTION ON ALERTS

### Alert Types & Responses

**1. CA Competes Tax Credit Alerts**

```
ALERT: "Current headcount at 18. Need 2 hires by Q2."
FINANCIAL IMPACT: $1.22M at risk
```

**Action Steps:**
1. Review current hiring pipeline
2. Accelerate recruitment timeline
3. Document compliance efforts
4. Update Julio on progress weekly
5. Set reminder 30 days before Q2 deadline

**2. HVIP Voucher Alerts**

```
ALERT: "Vehicle SEMI-0042 at 68% of annual mileage requirement"
FINANCIAL IMPACT: $330K voucher at risk
```

**Action Steps:**
1. Check SEMI-0042 utilization schedule
2. Increase route assignments for this vehicle
3. Ensure 100% California-only operation
4. Project to 25,000 miles by year-end
5. Flag for monthly tracking

**3. Transaction Integrity Alerts**

```
ALERT: "Transaction a7c3f2e1 has 82.3% integrity score"
REQUIRES: Immediate investigation
```

**Action Steps:**
1. Pull transaction details from database
2. Review GPS telemetry logs
3. Check CESAR controller data
4. Verify blockchain settlement
5. Document root cause
6. Update transaction notes

### Escalation Matrix

```
┌──────────────────┬───────────────┬────────────────────────┐
│ SEVERITY         │ ESCALATE TO   │ TIMELINE               │
├──────────────────┼───────────────┼────────────────────────┤
│ 1-2 exceptions   │ Ops team      │ Resolve within 3 days  │
│ 3-5 exceptions   │ Rebecca       │ Review within 1 day    │
│ >5 exceptions    │ Julio/James   │ Immediate call         │
│                  │               │                        │
│ CA Competes risk │ HR + Julio    │ Accelerate hiring      │
│ HVIP risk        │ Fleet Mgr     │ Adjust utilization     │
│ Fraud suspected  │ Legal + Julio │ Immediate investigation│
└──────────────────┴───────────────┴────────────────────────┘
```

---

## ADVANCED FEATURES

### Running Manual Audits

**When to Run Manually:**
- Before board meetings (get latest data)
- After major system changes
- When investigating specific time periods
- For month-end reporting

**How to Run:**

```bash
cd /path/to/cdls-auditor-complete
python3 auditor_logic.py
```

**Output:**
```
Starting CDLS Audit Agent...
Database connected.
Fetching exception data...
Found 23 exceptions to review.
Generating PDF report...
Report generated: /tmp/CDLS_Audit_20260206_1430.pdf
Sending email...
✓ Email sent successfully.
Audit cycle complete.
```

### Custom Date Ranges

**Modify the SQL query in `auditor_logic.py`:**

```python
# Line ~95 - Change the date filter
cur.execute("""
    SELECT * FROM institutional_audit_view
    WHERE haul_timestamp >= '2026-01-01'  -- Start date
      AND haul_timestamp < '2026-02-01'   -- End date
    ORDER BY integrity_score ASC
""")
```

### Exporting Data

**Export Exception List:**

```bash
psql -d ca_auditor -c "COPY (
    SELECT * FROM institutional_audit_view
) TO '/tmp/exceptions.csv' CSV HEADER;"
```

**Export for Excel Analysis:**

```bash
psql -d ca_auditor -c "COPY (
    SELECT 
        transaction_id,
        haul_timestamp,
        integrity_score,
        gps_variance_pct,
        energy_variance_pct,
        financial_variance_pct,
        reconciliation_status
    FROM transaction_reconciliation
    WHERE created_at >= NOW() - INTERVAL '30 days'
) TO '/tmp/monthly_audit.csv' CSV HEADER;"
```

### Blockchain Verification

**Verify Audit Trail Integrity:**

```bash
# This would be done through the blockchain interface
# The PDF reports include merkle roots for verification

# Example verification URL (from report):
https://etherscan.io/tx/0x7f9a3b2c4d5e6f8a9b0c1d2e3f4a5b6c...
```

---

## ANALYTICS CAPABILITIES

### Current Analytics Stack

**Built-In (Python + Matplotlib):**
✅ Histogram - Integrity score distribution  
✅ Bar charts - Variance comparison  
✅ Line charts - Time series trends  
✅ Pie charts - Status breakdowns  
✅ Statistical summaries - Mean, median, std dev  

**What's Included:**
- All charts auto-generated in weekly PDF
- Professional publication-quality graphics
- Color-coded for instant interpretation
- No additional configuration needed

### R Integration (Optional Advanced Analytics)

**Currently:** R is mentioned in the original spec but NOT included in the deployed system

**Why R Was Proposed:**
- Advanced statistical modeling (Monte Carlo simulations)
- Anomaly detection algorithms (IQR, Z-score, time-series)
- Complex financial projections
- Institutional-grade statistical rigor

**Current Status:** Python (matplotlib + numpy) handles all analytics needs for standard operations

---

## FREQUENTLY ASKED QUESTIONS

### General Questions

**Q: How often do reports run?**  
A: Automatically every Friday at 4:00 PM. You can also run manually anytime.

**Q: Can I change the schedule?**  
A: Yes, edit the cron job: `crontab -e` and modify the timing.

**Q: Who receives the reports?**  
A: Configured in `.env` file under `EMAIL_RECEIVER` and `EMAIL_CC`.

**Q: Is the data secure?**  
A: Yes - TLS email encryption, blockchain verification, audit trails logged.

### Technical Questions

**Q: What if the database connection fails?**  
A: The system retries 3 times, then logs the error. Check database credentials in `.env`.

**Q: Can I access historical reports?**  
A: Yes, all execution history is in the `audit_execution_log` database table.

**Q: How do I add more recipients?**  
A: Edit `.env` and add email addresses to `EMAIL_CC` (comma-separated).

**Q: What happens if a report fails?**  
A: Errors are logged to `logs/cron.log`. The system will try again next Friday.

### Operational Questions

**Q: How do I know if the system is working?**  
A: Check `logs/cron.log` for execution confirmations, or run manually to test.

**Q: Can I run reports for custom date ranges?**  
A: Yes, modify the SQL query dates in `auditor_logic.py` (see Advanced Features).

**Q: How do I stop the reports?**  
A: Remove the cron job: `crontab -e` and delete the CDLS line, then save.

**Q: Can I customize the PDF format?**  
A: Yes, edit `auditor_logic.py` - the AuditReport class controls formatting.

---

## TROUBLESHOOTING

See full troubleshooting guide in main README.md or contact:
**Email:** engineering@californiadealerlogistics.com

---

**END OF USER GUIDE**

*This guide covers standard operations. For advanced customization, see the technical documentation or contact engineering support.*
