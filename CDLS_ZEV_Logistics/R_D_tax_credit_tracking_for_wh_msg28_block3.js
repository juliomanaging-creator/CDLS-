// Instead of:
const password = "myPassword123"; // BAD!

// We do:
const password = process.env.DB_PASSWORD; // GOOD!