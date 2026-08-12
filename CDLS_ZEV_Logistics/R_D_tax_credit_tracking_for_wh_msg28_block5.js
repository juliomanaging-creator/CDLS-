// Login successful → create token
const token = jwt.sign({ userId: 123 }, SECRET_KEY);
// Token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

// Later, verify token
const decoded = jwt.verify(token, SECRET_KEY);
// decoded = { userId: 123 }