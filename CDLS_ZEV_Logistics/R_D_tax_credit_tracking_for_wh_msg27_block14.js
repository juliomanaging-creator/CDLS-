// Connect to database:
const pool = new Pool({
  host: 'localhost',
  database: 'ca_dealer_logistics',
  user: 'your_user',
  password: 'your_password'
});

// Run queries:
const result = await pool.query(
  'SELECT * FROM cities WHERE region = $1',
  ['Central Valley']
);

// Get results:
console.log(result.rows); // Array of cities