// Stop hackers from trying 10,000 passwords
rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5 // 5 login attempts max
});