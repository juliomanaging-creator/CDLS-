// Receives requests:
GET /api/cities → Show all cities
POST /api/auth/login → Log user in
PUT /api/routes/123 → Update route

// Routes them to right handlers:
app.get('/api/cities', cityController.getAllCities);
app.post('/api/auth/login', authController.login);

// Sends responses:
res.json({ success: true, data: cities });