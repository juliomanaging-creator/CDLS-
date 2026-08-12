// Without CORS:
Website on domain-a.com tries to call your API on domain-b.com
Browser: 🚫 BLOCKED! (security policy)

// With CORS configured:
cors({
  origin: 'https://yourdomain.com',  // Only allow your domain
  credentials: true                   // Allow cookies
})

Browser: ✅ Allowed!