const { Pool } = require('pg');
const db = new Pool({ /* connection info */ });
const result = await db.query('SELECT * FROM cities');