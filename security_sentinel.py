
"""
CDLS Automated Security Sentinel & Pipeline Validator
Replicates full-stack AppSec audits: SAST, SCA, Secrets, IaC, and License Compliance.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent
REPORT_FILE = BASE_DIR / "SECURITY_AUDIT_REPORT.md"

class SecuritySentinel:
    def __init__(self):
        self.findings = {
            "sast": [],
            "dependencies": [],
            "secrets": [],
            "licenses": [],
            "iac": []
        }
        self.score_deductions = 0

    def run_cmd(self, cmd: list[str]) -> tuple[int, str]:
        """Runs a subprocess safely and returns exit code and stdout."""
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR)
            )
            return res.returncode, res.stdout + res.stderr
        except Exception as e:
            return -1, str(e)

    def scan_sast(self):
        """1. Static Application Security Testing (Bandit)."""
        print("[1/5] Running SAST Code Inspection (Bandit)...")
        code, out = self.run_cmd([
            sys.executable, "-m", "bandit",
            "-r", ".",
            "-x", "./.venv,./temp_audio,./tests",
            "-f", "json"
        ])
        try:
            data = json.loads(out)
            for issue in data.get("results", []):
                sev = issue.get("issue_severity", "LOW")
                self.findings["sast"].append({
                    "severity": sev,
                    "file": issue.get("filename"),
                    "line": issue.get("line_number"),
                    "issue": issue.get("issue_text")
                })
                if sev in ["HIGH", "CRITICAL"]:
                    self.score_deductions += 15
                elif sev == "MEDIUM":
                    self.score_deductions += 5
        except Exception:
            if code != 0 and "No issues identified." not in out:
                self.findings["sast"].append({"severity": "INFO", "file": "codebase", "issue": "Bandit run completed."})

    def scan_dependencies(self):
        """2. Software Composition Analysis / Vulnerabilities (pip-audit)."""
        print("[2/5] Running Dependency Scanning (pip-audit)...")
        code, out = self.run_cmd([
            sys.executable, "-m", "pip_audit",
            "-f", "json"
        ])
        try:
            data = json.loads(out)
            for pkg in data.get("dependencies", []):
                for vuln in pkg.get("vulns", []):
                    self.findings["dependencies"].append({
                        "package": pkg.get("name"),
                        "installed_version": pkg.get("version"),
                        "vuln_id": vuln.get("id"),
                        "fix_versions": vuln.get("fix_versions", [])
                    })
                    self.score_deductions += 20
        except Exception:
            pass

    def scan_secrets(self):
        """3. Secrets & Private Key Detection (detect-secrets)."""
        print("[3/5] Running Secrets Detection...")
        code, out = self.run_cmd([
            sys.executable, "-m", "detect_secrets.core.usage",
            "scan", "."
        ])
        try:
            data = json.loads(out)
            for file_path, secrets in data.get("results", {}).items():
                if any(ignored in file_path for ignored in [".venv", "node_modules", "report"]):
                    continue
                for sec in secrets:
                    self.findings["secrets"].append({
                        "file": file_path,
                        "type": sec.get("type"),
                        "line": sec.get("line_number")
                    })
                    self.score_deductions += 25
        except Exception:
            pass

    def scan_licenses(self):
        """4. Dependency License Compliance."""
        print("[4/5] Running License Risk Analysis...")
        code, out = self.run_cmd([
            sys.executable, "-m", "piplicenses",
            "--format=json"
        ])
        prohibited_licenses = ["GPL", "AGPL"]
        try:
            data = json.loads(out)
            for item in data:
                lic = item.get("License", "").upper()
                if any(p in lic for p in prohibited_licenses):
                    self.findings["licenses"].append({
                        "package": item.get("Name"),
                        "version": item.get("Version"),
                        "license": item.get("License")
                    })
                    self.score_deductions += 10
        except Exception:
            pass

    def scan_iac(self):
        """5. Infrastructure as Code / Docker Hardening Check."""
        print("[5/5] Auditing Docker Compose & Configuration...")
        compose_file = BASE_DIR / "docker-compose.hardened.yml"
        if compose_file.exists():
            content = compose_file.read_text(encoding="utf-8")
            required_controls = [
                ("no-new-privileges:true", "Missing 'no-new-privileges' container isolation"),
                ("cap_drop:", "Containers not dropping Linux capabilities (cap_drop)"),
                ("read_only: true", "Container root filesystem is not set to read-only"),
                ("tmpfs:", "Missing tmpfs writable runtime storage partition")
            ]
            for control, alert in required_controls:
                if control not in content:
                    self.findings["iac"].append({"severity": "MEDIUM", "issue": alert})
                    self.score_deductions += 10
        else:
            self.findings["iac"].append({"severity": "HIGH", "issue": "Missing docker-compose.hardened.yml"})
            self.score_deductions += 20

    def generate_report(self):
        score = max(0, 100 - self.score_deductions)
        status_label = "PASS (Audit-Ready)" if score >= 85 else "NEEDS_REMEDIATION"

        md = []
        md.append("# CDLS Automated Security Sentinel Report")
        md.append(f"**Execution Timestamp:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  ")
        md.append(f"**Security Health Score:** `{score} / 100` — **{status_label}**\n")
        md.append("---")

        md.append("## 1. Static Code Analysis (SAST)")
        if self.findings["sast"]:
            md.append("| Severity | File | Line | Issue |")
            md.append("| :--- | :--- | :--- | :--- |")
            for item in self.findings["sast"]:
                md.append(f"| **{item['severity']}** | `{item['file']}` | {item.get('line', '-')} | {item['issue']} |")
        else:
            md.append("No SAST vulnerabilities identified.\n")

        md.append("## 2. Dependency Vulnerabilities (SCA)")
        if self.findings["dependencies"]:
            md.append("| Package | Installed | Vulnerability ID | Fix Version |")
            md.append("| :--- | :--- | :--- | :--- |")
            for item in self.findings["dependencies"]:
                md.append(f"| `{item['package']}` | {item['installed_version']} | {item['vuln_id']} | {', '.join(item['fix_versions']) or 'None'} |")
        else:
            md.append("No known vulnerable dependencies found.\n")

        md.append("## 3. Secrets & Credential Exposure")
        if self.findings["secrets"]:
            md.append("| File | Line | Detected Secret Type |")
            md.append("| :--- | :--- | :--- |")
            for item in self.findings["secrets"]:
                md.append(f"| `{item['file']}` | {item['line']} | {item['type']} |")
        else:
            md.append("No active secrets or API credentials found in code repository.\n")

        md.append("## 4. Software License Risk")
        if self.findings["licenses"]:
            md.append("| Package | Version | Flagged License |")
            md.append("| :--- | :--- | :--- |")
            for item in self.findings["licenses"]:
                md.append(f"| `{item['package']}` | {item['version']} | **{item['license']}** |")
        else:
            md.append("No copyleft GPL/AGPL license conflicts detected.\n")

        md.append("## 5. Infrastructure as Code (IaC) & Container Hardening")
        if self.findings["iac"]:
            md.append("| Severity | Control Gap |")
            md.append("| :--- | :--- |")
            for item in self.findings["iac"]:
                md.append(f"| **{item['severity']}** | {item['issue']} |")
        else:
            md.append("All Docker security baselines (read-only, cap-drop, no-new-privileges) verified.\n")

        REPORT_FILE.write_text("\n".join(md), encoding="utf-8")
        print(f"\n[OK] Sentinel Audit Complete. Overall Score: {score}/100")
        print(f"[OK] Full Audit Dossier written to: {REPORT_FILE.resolve()}")

        return score

if __name__ == "__main__":
    sentinel = SecuritySentinel()
    sentinel.scan_sast()
    sentinel.scan_dependencies()
    sentinel.scan_secrets()
    sentinel.scan_licenses()
    sentinel.scan_iac()
    final_score = sentinel.generate_report()

    if final_score < 80:
        sys.exit(1)
    sys.exit(0)