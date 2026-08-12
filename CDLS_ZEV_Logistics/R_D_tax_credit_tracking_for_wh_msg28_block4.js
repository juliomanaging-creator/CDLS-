// User enters: "password123"
// We store: "$2a$12$vXj8hD.../kLmQp8Rvx9nOeU7i"
// Even we can't decrypt it back!
const hash = await bcrypt.hash("password123", 12);