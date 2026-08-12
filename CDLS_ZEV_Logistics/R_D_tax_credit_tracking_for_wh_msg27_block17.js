// Different log levels:
logger.error('Database connection failed!');   // Critical
logger.warn('Rate limit approaching');         // Warning
logger.info('User logged in');                 // Info
logger.debug('Query took 150ms');              // Debug

// Logs to multiple places:
- Console (during development)
- File: logs/app.log (for review)
- File: logs/error.log (errors only)
- External service: Datadog/Splunk (production)

// Formatted output:
2025-12-16 22:45:23 [ERROR] Database connection failed!
2025-12-16 22:45:25 [INFO] Server started on port 3000
2025-12-16 22:45:30 [WARN] Rate limit: 95/100 requests used