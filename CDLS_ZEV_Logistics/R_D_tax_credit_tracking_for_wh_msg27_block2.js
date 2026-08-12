// When user logs in successfully:
const token = jwt.sign(
  { id: user.id, email: user.email, role: "dealer" },
  "your-secret-key",
  { expiresIn: "7d" }
);
// Token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

// On every request, browser sends token:
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

// Server verifies:
const decoded = jwt.verify(token, "your-secret-key");
// If valid: Allow access
// If expired or tampered: Deny access