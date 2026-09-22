# CDLS Architecture Overview

## Objective
To provide a secure, auditable, and multi-agent AI framework for evaluating complex government grant applications and clean energy policy compliance under NIST standards.

## Security Boundaries
1. **Perimeter Defense**: Strict input sanitization (NIST SI-10) and path traversal checks (_safe_path CWE-22 mitigation).
2. **Container Isolation**: Non-root execution (USER 10001), root filesystem read-only locks, and cap_drop: ALL.
3. **Audit Immutability**: Cryptographically hashed execution logs stored in the tamper-evident audit vault.
