logger.error('Database connection failed', { error: err });
logger.info('User logged in', { userId: 123 });
logger.warn('API rate limit exceeded', { ip: '1.2.3.4' });