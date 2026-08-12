httpOnly: true,     // JavaScript can't access (stops XSS)
secure: true,       // Only sent over HTTPS
sameSite: 'strict', // Blocks CSRF attacks
maxAge: 7 days      // Auto-expires