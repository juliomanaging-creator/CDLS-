import os
from pathlib import Path

# Path Configuration
ROOT_DIR = Path(r"C:\Projects\AWS AGENT")
KB_DIR = ROOT_DIR / "knowledge_base"

# Sample 2026 Audit Scenarios
test_files = {
    "aws": [
        ("security_audit_2026.md", "Critical AWS Firewall update scheduled for 2026-05-20. Review required by 2026-05-15."),
        ("lambda_compliance.md", "Serverless patches must be verified before the 2026-08-10 deadline."),
        ("s3_encryption_check.md", "New S3 bucket encryption standards go live on 2026-09-01.")
    ],
    "legal": [
        ("privacy_v2.md", "Data privacy regulation updates finalized for 2026-11-30."),
        ("retention_policy.md", "Updated document retention policy takes effect 2026-12-15.")
    ],
    "finance": [
        ("tax_prep_2026.md", "Fiscal year 2026 tax preparation starts 2026-02-01."),
        ("audit_window.md", "External finance audit window: 2026-03-15 to 2026-04-15.")
    ]
}

def generate_test_data():
    print("🚀 Generating 2026 Sample Audit Data...")
    for sector, files in test_files.items():
        sector_path = KB_DIR / sector
        sector_path.mkdir(parents=True, exist_ok=True)
        
        for filename, content in files:
            file_path = sector_path / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {filename.replace('_', ' ').title()}\n\n{content}")
            print(f"✅ Created: {file_path}")

if __name__ == "__main__":
    generate_test_data()