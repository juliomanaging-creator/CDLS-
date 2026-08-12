// User registers with password: "MyPassword123"
const hashedPassword = await bcrypt.hash("MyPassword123", 12);
// Stored in database: "$2a$12$KIXxqF7..."

// When user logs in:
const isValid = await bcrypt.compare("MyPassword123", hashedPassword);
// Returns: true (password matches)

// If hacker steals database:
// They see: "$2a$12$KIXxqF7..." 
// Can't reverse it back to "MyPassword123"
// Would take 100+ years to crack with supercomputer