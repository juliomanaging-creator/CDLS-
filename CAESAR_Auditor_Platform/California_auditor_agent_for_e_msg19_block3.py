def detect_duplicate_invoice(invoice, existing_invoices):
    invoice_hash = hash(invoice)
    if invoice_hash in existing_invoices:
        return "DUPLICATE - DO NOT PAY"
    return "OK"