// First request (slow):
GET /api/cities → Check cache → Not found → Query database (200ms)
→ Store in cache → Return to user

// Second request (fast):
GET /api/cities → Check cache → Found! (2ms) → Return to user

// Result: 100x faster!