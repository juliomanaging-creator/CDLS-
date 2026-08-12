from agents.r_audit_dev import RAuditDevAgent

# Initialize agent
agent = RAuditDevAgent(
    model="claude-3-5-sonnet-20241022",
    output_dir="/opt/ca-audit-system/r-analytics"
)

print("✓ R-AUDIT-DEV Agent ready")