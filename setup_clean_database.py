"""
CDLS Platform: Production Database Initializer & Dataset Seeder
Creates clean, relational tables for IP assets, IRC § 41 logs, and VDR token ledgers.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path("cdls_master_catalog.db")

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS patent_assets (
    fig_num INTEGER PRIMARY KEY,
    fig_key TEXT UNIQUE NOT NULL,
    cluster_id INTEGER NOT NULL,
    cluster_name TEXT NOT NULL,
    archetype TEXT NOT NULL,
    title TEXT NOT NULL,
    technical_domain TEXT NOT NULL,
    claim_independent TEXT NOT NULL,
    source_uri TEXT NOT NULL,
    source_sheet TEXT,
    source_row TEXT,
    last_validated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reference_numerals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fig_num INTEGER NOT NULL,
    numeral TEXT NOT NULL,
    component_label TEXT NOT NULL,
    technical_description TEXT NOT NULL,
    FOREIGN KEY (fig_num) REFERENCES patent_assets(fig_num) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rd_experimentation_logs (
    log_id TEXT PRIMARY KEY,
    fig_num INTEGER NOT NULL,
    uncertainty_statement TEXT NOT NULL,
    experimental_procedure TEXT NOT NULL,
    tested_parameters TEXT NOT NULL,
    validation_metrics TEXT NOT NULL,
    audit_status TEXT CHECK(audit_status IN ('VERIFIED', 'IN_TEST', 'REJECTED')),
    FOREIGN KEY (fig_num) REFERENCES patent_assets(fig_num) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vdr_access_ledger (
    token_hash TEXT PRIMARY KEY,
    recipient_email TEXT NOT NULL,
    document_name TEXT NOT NULL,
    active_status INTEGER DEFAULT 1 CHECK(active_status IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP
);
"""

SAMPLE_DATASETS = {
    "patent_assets": [
        (
            1, "FIG_1", 1, "Cluster 1: Electro-Mechanical Fleet Systems",
            "Mechanical Breakaway & Retention Assembly",
            "N52 High-Amperage Quick-Disconnect Charging Interface",
            "Heavy-Duty Commercial EV Charging Hardware",
            "Claim 1: An electro-mechanical fast-disconnect coupling apparatus comprising: a dielectric housing (12); a permanent rare-earth magnet array (16) providing calibrated axial retention exceeding 100 lbf during vibrational loading and decoupling under manual lever tension exceeding 25 lbf; and an optical safety interlock (20) configured to signal DC contactors to trip in sub-10ms intervals prior to electrical separation.",
            "CDLS_RD_Time_Tracker_MERGED_FULL.xlsx#Hardware_Sprints!Row_14",
            "Hardware_Sprints", "14", datetime.now(timezone.utc)
        ),
        (
            2, "FIG_2", 1, "Cluster 1: Electro-Mechanical Fleet Systems",
            "Electrical Vehicle-to-Grid (V2G) Architecture",
            "360 kWh Mobile LFP Battery Trailer with Autonomous Demand Dispatch",
            "Grid-Tied Commercial Energy Storage",
            "Claim 2: A mobile grid-support power distribution system comprising: a DOT-compliant trailer enclosure (20); an onboard energy storage pack (22) providing at least 360 kWh across 120 parallel LFP strings; a bidirectional inverter (24) communicating via IEEE 15118-20 protocols; and an automated microgrid dispatch controller (26).",
            "CDLS_RD_Time_Tracker_MERGED_FULL.xlsx#Grid_Testing!Row_32",
            "Grid_Testing", "32", datetime.now(timezone.utc)
        ),
        (
            3, "FIG_3", 2, "Cluster 2: Cryptographic Audit Engine (JUDAS AI)",
            "Cryptographic Zero-Knowledge Audit Engine",
            "Multi-Spectral Boundary Portal with Edge Vision & zk-SNARK Verification",
            "Fleet Transfer Custody Verification",
            "Claim 3: A verifiable cryptographic inspection system comprising: an optical sensor array (32) positioned at a transfer portal boundary; an edge inference engine (34) computing defect bounding coordinates; an uncompressed pixel matrix dual-hash pipeline (36); and a zero-knowledge commitment module (38) generating non-repudiation proofs.",
            "CDLS_RD_Time_Tracker_MERGED_FULL.xlsx#Vision_Models!Row_88",
            "Vision_Models", "88", datetime.now(timezone.utc)
        ),
        (
            4, "FIG_4", 3, "Cluster 3: Adaptive Route & Fleet Intelligence",
            "Three-Layer Stochastic Route Intelligence",
            "CARI Adaptive Predictive Lead-Route Engine with MCMC Optimization",
            "Fleet Dispatch Telematics & Logistics",
            "Claim 4: A multi-tier adaptive route optimization system comprising: a first regularized regression engine (42) filtering macroeconomic freight volatility; a second Markov Chain Monte Carlo sampler (44) executing stochastic iterations against real-time CAISO Locational Marginal Pricing feeds; and a third stabilization layer (48) enforcing FMCSA 49 CFR Part 395 rest constraints.",
            "CDLS_RD_Time_Tracker_MERGED_FULL.xlsx#Route_Engines!Row_104",
            "Route_Engines", "104", datetime.now(timezone.utc)
        ),
        (
            5, "FIG_5", 4, "Cluster 4: Regulatory Compliance & Data Security",
            "Regulatory Gateway & Multi-Tenant Cryptographic Isolation",
            "Automated CARB Clean Truck Check Gateway with AAD-Bound AEAD Key Store",
            "State Zero-Emission Fleet Compliance",
            "Claim 5: A multi-tenant regulatory compliance apparatus comprising: a dealer DMS interface (52); a cryptographic isolation vault (54) encrypting tenant records with separate Authenticated Additional Data keys; a statutory rule engine (56) evaluating vehicle compliance under 13 CCR §§ 2195–2199; and an automated dispatch gateway (58).",
            "CDLS_RD_Time_Tracker_MERGED_FULL.xlsx#CARB_Gateways!Row_142",
            "CARB_Gateways", "142", datetime.now(timezone.utc)
        )
    ],
    "reference_numerals": [
        (1, "12", "Male Coupler Housing", "Dielectric structural body containing bus pin guides and thermal conduits."),
        (1, "14", "Vehicle Receptacle Interface", "Chassis-mounted flush receiver with guided chamfered docking channels."),
        (1, "16", "Permanent Magnet Array", "N52 neodymium magnet configuration calibrated for dynamic road retention."),
        (1, "18", "DC High-Amperage Bus Terminals", "Dual solid-copper power conductors with insulated spring-loaded sliding contact sleeves."),
        (1, "20", "Optical Interlock Safety Loop", "Closed-circuit optical emitter/detector triggering sub-10ms high-voltage de-energization."),
        (2, "20", "Mobile Trailer Platform", "Weather-sealed DOT-compliant trailer enclosure with integrated fire barriers."),
        (2, "22", "Parallel LFP Storage Pack", "360 kWh Lithium Iron Phosphate array structured in 120 parallel strings with per-cell monitoring."),
        (2, "24", "Bidirectional Inverter Core", "38.4 kW high-efficiency bidirectional DC/AC inverter adhering to IEEE 15118-20 and UL 9741."),
        (3, "32", "High-Resolution Optical Array", "Multi-angle imaging sensors capturing calibrated high-fidelity structural surface records."),
        (3, "38", "zk-SNARK Prover Engine", "Pedersen vector commitment engine proving inspection compliance without exposing raw imagery.")
    ],
    "rd_experimentation_logs": [
        (
            "LOG-2026-C1-001", 1,
            "Determining whether permanent N52 magnetic arrays can resist Class 8 vehicle vibration without unseating while maintaining <25 lbf manual lever disconnect force.",
            "Benchmarked axial holding force across 5 prototypes using pneumatic tension fixtures and 3-axis vibration tables (SAE J1455 profile).",
            "Magnetic flux gap (0.5mm - 2.0mm), Cam lever mechanical advantage (3:1 vs 4:1), Vibrational acceleration (2.5G to 5.0G).",
            "Zero false disconnects at 4.2G vibration; manual pedal release recorded at 21.4 lbf.",
            "VERIFIED"
        ),
        (
            "LOG-2026-C3-004", 4,
            "Eliminating driver dispatch hunting caused by volatile hourly day-ahead CAISO Locational Marginal Pricing changes.",
            "Executed 10,000-run Metropolis-Hastings MCMC probability iterations alongside deterministic variant hash assignments.",
            "LMP delta ($25/MWh - $350/MWh), Driver remaining duty cycle (2h - 8h), State-of-Charge buffer floor (15%).",
            "Route churn reduced by 87% while maintaining energy cost savings within 3.2% of unconstrained theoretical maximum.",
            "VERIFIED"
        )
    ]
}

def seed_database():
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"[*] Removed existing database: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(SCHEMA_SQL)
    print("[*] Schema executed successfully.")

    cur.executemany(
        "INSERT INTO patent_assets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        SAMPLE_DATASETS["patent_assets"]
    )
    cur.executemany(
        "INSERT INTO reference_numerals (fig_num, numeral, component_label, technical_description) VALUES (?, ?, ?, ?)",
        SAMPLE_DATASETS["reference_numerals"]
    )
    cur.executemany(
        "INSERT INTO rd_experimentation_logs VALUES (?, ?, ?, ?, ?, ?, ?)",
        SAMPLE_DATASETS["rd_experimentation_logs"]
    )

    conn.commit()
    conn.close()
    print(f"[SUCCESS] Clean database initialized with sample datasets: {DB_PATH.resolve()}")

if __name__ == "__main__":
    seed_database()