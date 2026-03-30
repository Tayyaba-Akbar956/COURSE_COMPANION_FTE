# SPEC-A-004-auth-apis-v1.0

## Status
- [x] Draft
- [ ] Pending Approval
- [ ] Approved
- [ ] In Progress
- [ ] Completed
- [ ] Deprecated

## Metadata
- **Created:** 2026-03-29
- **Author:** Qwen Code (AI Builder)
- **Approved By:** [Pending User Approval]
- **Version:** 1.0.0

## 1. Overview

This spec defines the API contract for authentication endpoints including signup, login, OAuth, token refresh, and logout using Supabase Auth.

## 2. API Endpoints

### 2.1 POST /api/v1/auth/signup

**Description:** Create new user account (magic link)

**Request Body:**
```json
{
  "email": "user@example.com",
  "auth_method": "magic_link"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Magic link sent to user@example.com",
  "email": "user@example.com"
}
```

**Errors:** 400 (Invalid Email), 429 (Rate Limited)

---

### 2.2 POST /api/v1/auth/login

**Description:** Login with magic link

**Request Body:**
```json
{
  "email": "user@example.com",
  "auth_method": "magic_link"
}
```

**Response (200 OK):** Same as signup

---

### 2.3 POST /api/v1/auth/oauth/{provider}

**Description:** Initiate OAuth login

**Path Parameters:** `provider` (google, github)

**Response (200 OK):**
```json
{
  "success": true,
  "oauth_url": "https://accounts.google.com/o/oauth2/auth?..."
}
```

---

### 2.4 POST /api/v1/auth/refresh

**Description:** Refresh access token

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

**Errors:** 401 (Invalid Refresh Token)

---

### 2.5 POST /api/v1/auth/logout

**Description:** Logout user (revoke refresh token)

**Request Body:**
```json
{
  "revoke_all_sessions": false
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### 2.6 GET /api/v1/auth/me

**Description:** Get current user info

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user_id": "uuid-here",
    "email": "user@example.com",
    "full_name": "John Doe",
    "subscription_tier": "free",
    "created_at": "2026-03-15T08:00:00Z"
  }
}
```

**Errors:** 401 (Unauthorized)

---

### 2.7 POST /api/v1/auth/password/reset

**Description:** Request password reset (email/password users)

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset link sent to user@example.com"
}
```

---

## 3. Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| POST /auth/signup | 5 | per minute |
| POST /auth/login | 5 | per minute |
| POST /auth/refresh | 10 | per minute |
| POST /auth/password/reset | 3 | per hour |

## 4. Testing Requirements

```python
def test_auth_api_signup():
    """Should send magic link on signup"""
    # Act: POST /api/v1/auth/signup
    # Assert: 200 OK, magic link sent

def test_auth_api_login():
    """Should send magic link on login"""
    # Act: POST /api/v1/auth/login
    # Assert: 200 OK, magic link sent

def test_auth_api_jwt_validation():
    """Valid JWT should grant access"""
    # Act: GET /api/v1/auth/me with valid token
    # Assert: 200 OK, user info

def test_auth_api_invalid_jwt():
    """Invalid JWT should be rejected"""
    # Act: GET /api/v1/auth/me with invalid token
    # Assert: 401 Unauthorized

def test_auth_api_refresh():
    """Refresh token should obtain new access token"""
    # Act: POST /api/v1/auth/refresh
    # Assert: 200 OK, new access token

def test_auth_api_logout():
    """Logout should revoke refresh token"""
    # Act: POST /api/v1/auth/logout
    # Assert: 200 OK, token invalidated

def test_auth_api_rate_limiting():
    """Should rate limit auth attempts"""
    # Act: 6 signup requests in 1 minute
    # Assert: 429 on 6th request
```

## 5. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Auth APIs Spec (SPEC-A-004-auth-apis-v1.0)  
**Why:** Defines authentication endpoints for user management  
**Files Affected:** `docs/specs/api/SPEC-A-004-auth-apis-v1.0.md`

**Key Decisions:**
- Supabase Auth for all authentication
- Magic links as primary method
- OAuth (Google, GitHub) supported
- JWT tokens (1-hour expiry)
- Rate limiting to prevent abuse

**Do you approve?** (Yes/No/Modify)

---

**Progress:** API Specs: 4/5 Complete. Remaining: A-005 (Search)
