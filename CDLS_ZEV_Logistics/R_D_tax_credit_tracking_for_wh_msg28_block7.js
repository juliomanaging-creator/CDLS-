// Instead of querying database every time:
const cities = await redis.get('cities'); // Instant!
// vs
const cities = await db.query('SELECT * FROM cities'); // Slower