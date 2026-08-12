const express = require('express');
const app = express();
app.get('/api/cities', (req, res) => {
  res.json({ cities: [...] });
});