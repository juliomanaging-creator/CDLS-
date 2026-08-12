body('email')
  .isEmail() // Must be valid email
  .normalizeEmail() // Clean it up
  .withMessage('Invalid email')