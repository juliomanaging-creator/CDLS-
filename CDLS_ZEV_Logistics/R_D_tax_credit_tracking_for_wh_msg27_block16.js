// .env file:
DB_PASSWORD=super_secret_123
JWT_SECRET=another_secret_key
API_KEY=gasbuddy_api_key_xyz

// In code:
process.env.DB_PASSWORD // "super_secret_123"
process.env.JWT_SECRET   // "another_secret_key"

// Why this matters:
// ✅ Secrets never committed to GitHub
// ✅ Different secrets for dev/production
// ✅ Easy to change without editing code