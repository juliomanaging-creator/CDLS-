// Attack attempt:
{
  "email": { "$gt": "" },  // MongoDB operator
  "password": "anything"
}
// This would return all users!

// After sanitization:
{
  "email": "gt",  // Operators removed
  "password": "anything"
}
// Now it's just searching for email = "gt" (harmless)