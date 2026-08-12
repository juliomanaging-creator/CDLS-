// Email validation:
Input: "julio@dealer.com" ✅ Valid
Input: "not-an-email" ❌ Rejected
Input: "<script>alert('hacked')</script>" ❌ Rejected

// Route distance validation:
Input: 127.4 ✅ Valid (positive number)
Input: -50 ❌ Rejected (can't be negative)
Input: "abc" ❌ Rejected (must be number)
Input: 999999 ❌ Rejected (too large, unrealistic)

// Payload vehicles:
Input: 7 ✅ Valid (0-15 range)
Input: 20 ❌ Rejected (exceeds hauler capacity)
Input: "'; DROP TABLE users; --" ❌ Rejected (SQL injection attempt)