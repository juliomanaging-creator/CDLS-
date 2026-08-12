# Field-level encryption for medical record numbers
patient_mrn_encrypted = encrypt_phi_field(
    plaintext="MRN-12345678",
    algorithm="AES-256-GCM",
    field_type="medical_record_number"
)

# Access requires:
# - HIPAA authorization role
# - Current training certification
# - Business justification documented
# - Supervisor approval (for bulk access)
# - All access logged immutably