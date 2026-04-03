# X2C API Requirements for Giggle Pro External

This document lists all the X2C platform API endpoints required for the `giggle-pro-external` skill to work properly.

---

## Base URL

```
https://api.x2creel.ai
```

Set via environment variable: `X2C_API_BASE`

---

## Authentication

All requests use API key authentication via header:

```
x-auth: <api_key>
```

API keys should start with `sk_x2c_` prefix.

---

## Required Endpoints

### 1. Validate API Key

**Endpoint:** `GET /api/v1/user/validate`

**Purpose:** Verify that an API key is valid and get basic user info.

**Headers:**
```
x-auth: <api_key>
```

**Response (Success):**
```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "user_id": "user_123",
    "username": "stone@example.com",
    "email": "stone@example.com",
    "status": "active"
  }
}
```

**Response (Error):**
```json
{
  "code": 401,
  "msg": "Invalid API key"
}
```

**Error Codes:**
- `401` - Invalid or expired API key
- `403` - Account suspended
- `404` - User not found

---

### 2. Get Account Balance

**Endpoint:** `GET /api/v1/user/balance`

**Purpose:** Check user's credit balance.

**Headers:**
```
x-auth: <api_key>
```

**Response (Success):**
```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "balance": 1000,
    "currency": "credits"
  }
}
```

**Note:** 1 credit = $0.01 USD

**Error Codes:**
- `401` - Invalid API key
- `404` - User not found

---

### 3. Deduct Credits

**Endpoint:** `POST /api/v1/user/deduct`

**Purpose:** Deduct credits for a service operation (script generation, video generation, etc.)

**Headers:**
```
x-auth: <api_key>
Content-Type: application/json
```

**Request Body:**
```json
{
  "amount": 100,
  "reason": "script_generation",
  "project_id": "proj_abc123",
  "metadata": {
    "operation": "generate-script",
    "duration": 60
  }
}
```

**Fields:**
- `amount` (integer, required) - Credits to deduct
- `reason` (string, required) - Reason code (see below)
- `project_id` (string, required) - Giggle project ID
- `metadata` (object, optional) - Additional info

**Reason Codes:**
- `script_generation` - Script generation (~100 credits)
- `character_generation` - Character generation (~200 credits)
- `image_generation` - Image generation (~50 credits per image)
- `video_generation` - Video generation (~88 credits per video)
- `export` - Video export (~50 credits)

**Response (Success):**
```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "remaining_balance": 900,
    "transaction_id": "tx_456",
    "deducted_amount": 100
  }
}
```

**Error Codes:**
- `401` - Invalid API key
- `402` - Insufficient balance
- `403` - Account suspended
- `404` - User not found

**Error Response (Insufficient Balance):**
```json
{
  "code": 402,
  "msg": "Insufficient balance",
  "data": {
    "balance": 50,
    "required": 100,
    "shortfall": 50
  }
}
```

---

### 4. Get Transaction History (Optional)

**Endpoint:** `GET /api/v1/user/transactions?limit=10&offset=0`

**Purpose:** Retrieve user's transaction history.

**Headers:**
```
x-auth: <api_key>
```

**Query Parameters:**
- `limit` (integer, optional) - Number of records to return (default: 10, max: 100)
- `offset` (integer, optional) - Pagination offset (default: 0)

**Response (Success):**
```json
{
  "code": 200,
  "msg": "Success",
  "data": {
    "transactions": [
      {
        "transaction_id": "tx_456",
        "amount": -100,
        "balance_after": 900,
        "reason": "script_generation",
        "project_id": "proj_abc123",
        "timestamp": "2024-01-15T10:30:00Z",
        "status": "completed"
      },
      {
        "transaction_id": "tx_455",
        "amount": 1000,
        "balance_after": 1000,
        "reason": "topup",
        "timestamp": "2024-01-15T09:00:00Z",
        "status": "completed"
      }
    ],
    "total": 42,
    "limit": 10,
    "offset": 0
  }
}
```

**Note:** This endpoint is optional and used for debugging/user transparency.

---

## Cost Estimation Reference

| Operation | Estimated Cost |
|-----------|----------------|
| Script generation | ~100 credits ($1.00) |
| Character generation (2-4 characters) | ~200 credits ($2.00) |
| Storyboard generation | ~50 credits ($0.50) |
| Image generation (per shot) | ~50 credits ($0.50) |
| Video generation (per shot, 5s) | ~88 credits ($0.88) |
| Export | ~50 credits ($0.50) |
| **Total (12-shot drama)** | ~1200 credits ($12.00) |

---

## Implementation Notes

### Graceful Degradation

The `x2c-account` skill is designed to work even if the X2C API is not yet deployed:

1. **During Development:** If API endpoints return `ENOTFOUND` or `ECONNREFUSED`, the skill:
   - Accepts API keys with format check only (`sk_x2c_*`)
   - Logs warning that API is unavailable
   - Allows operations to proceed (simulated mode)

2. **In Production:** Once the API is deployed:
   - All validation/balance/deduction calls work normally
   - Real enforcement of balance checks
   - Proper error handling

### Security Considerations

- API keys are stored locally in `config.json`
- Keys are masked when displayed (first 6 + last 6 chars shown)
- Never log full keys to console or logs
- Use HTTPS for all API calls
- Validate API key format client-side before calling API

### Error Handling

When balance is insufficient, the skill should:
1. Display clear error message with balance info
2. Show top-up URL: `https://x2creel.ai`
3. Exit gracefully with non-zero status code

When API key is invalid:
1. Display error message
2. Suggest re-binding account
3. Exit gracefully

---

## Testing

### Mock Server (Optional)

For testing, you can run a mock X2C API server:

```javascript
// mock-x2c-api.js
const express = require('express');
const app = express();
app.use(express.json());

let balances = {};

app.get('/api/v1/user/validate', (req, res) => {
  const key = req.headers['x-auth'];
  if (!key || !key.startsWith('sk_x2c_')) {
    return res.status(401).json({ code: 401, msg: 'Invalid API key' });
  }
  res.json({
    code: 200,
    data: {
      user_id: 'test_user',
      username: 'test@example.com',
      status: 'active'
    }
  });
});

app.get('/api/v1/user/balance', (req, res) => {
  const key = req.headers['x-auth'];
  const balance = balances[key] || 10000; // Default 10000 credits
  res.json({ code: 200, data: { balance, currency: 'credits' } });
});

app.post('/api/v1/user/deduct', (req, res) => {
  const key = req.headers['x-auth'];
  const { amount } = req.body;
  let balance = balances[key] || 10000;
  
  if (balance < amount) {
    return res.status(402).json({
      code: 402,
      msg: 'Insufficient balance',
      data: { balance, required: amount, shortfall: amount - balance }
    });
  }
  
  balance -= amount;
  balances[key] = balance;
  
  res.json({
    code: 200,
    data: {
      remaining_balance: balance,
      transaction_id: `tx_${Date.now()}`,
      deducted_amount: amount
    }
  });
});

app.listen(3000, () => console.log('Mock X2C API running on :3000'));
```

Run with:
```bash
X2C_API_BASE=http://localhost:3000 node scripts/x2c-account.js bind --key "sk_x2c_test123"
```

---

## Summary

**Minimum required for MVP:**
1. `POST /api/v1/user/validate` - Validate API keys
2. `GET /api/v1/user/balance` - Check balance
3. `POST /api/v1/user/deduct` - Deduct credits

**Optional for better UX:**
4. `GET /api/v1/user/transactions` - Transaction history

The skill will work in "simulated mode" until these endpoints are deployed.
