-- Core tables
CREATE TABLE quotes (
    quote_id UUID PRIMARY KEY,
    customer_email VARCHAR(255),
    vehicle_vin VARCHAR(17),
    status VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE documents (
    document_id UUID PRIMARY KEY,
    quote_id UUID REFERENCES quotes(quote_id),
    document_type VARCHAR(50),
    file_path VARCHAR(255),
    upload_date TIMESTAMP,
    verified BOOLEAN
);

CREATE TABLE status_updates (
    update_id UUID PRIMARY KEY,
    quote_id UUID REFERENCES quotes(quote_id),
    status VARCHAR(50),
    message TEXT,
    timestamp TIMESTAMP
);