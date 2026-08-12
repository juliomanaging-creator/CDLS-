// User sends: { "email": { "$gt": "" } } // Attack!
// Sanitizer changes to: { "email": "[object Object]" } // Safe!