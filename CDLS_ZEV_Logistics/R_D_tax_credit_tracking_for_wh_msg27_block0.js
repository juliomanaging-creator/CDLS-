// Without helmet:
Response headers: (basic, vulnerable)

// With helmet:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
// ... 8 more security headers