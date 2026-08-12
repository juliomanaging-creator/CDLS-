// Normal request:
GET /api/cities?region=Central Valley

// Attack attempt:
GET /api/cities?region=Central Valley&region='; DROP TABLE cities; --&region=All

// Without hpp:
Server gets confused, might process malicious query

// With hpp:
Takes first parameter only, ignores duplicates
region = "Central Valley" (safe)