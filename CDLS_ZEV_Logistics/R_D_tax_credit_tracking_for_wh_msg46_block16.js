// In your Node.js code
const fs = require('fs');
const path = require('path');

const carrierData = JSON.parse(
  fs.readFileSync(
    path.join(__dirname, 'data/sample-data/carrier_cost_data.json'),
    'utf8'
  )
);