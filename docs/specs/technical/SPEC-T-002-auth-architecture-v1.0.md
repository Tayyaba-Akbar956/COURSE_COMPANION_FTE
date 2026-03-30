# SPEC-T-002-auth-architecture-v1.0

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

This spec defines the authentication and authorization architecture for the Course Companion FTE application. We use Supabase Auth for user management with support for magic links, OAuth (Google, GitHub), and email/password authentication.

## 2. Authentication Provider

**Technology:** Supabase Auth  
**Rationale:**
- Free tier generous (50,000 MAUs)
- Multiple auth methods out-of-the-box
- JWT tokens with automatic refresh
- Row Level Security (RLS) integration
- Built-in user management dashboard
- Secure password handling
- OAuth providers pre-configured

## 3. Authentication Methods

### 3.1 Magic Links (Primary)
- User enters email
- System sends magic link email
- User clicks link, logged in automatically
- No password required
- Most secure (no password reuse)

### 3.2 OAuth (Secondary)
- Google OAuth 2.0
- GitHub OAuth 2.0
- One-click authentication
- Profile information imported

### 3.3 Email/Password (Fallback)
- Traditional email/password signup
- Password requirements enforced
- Password reset via email
- Available if user prefers

## 4. Authentication Flow

### 4.1 Signup Flow

```
User enters email → Supabase Auth → Magic link sent → User clicks link → 
JWT issued → Backend validates JWT → User session created → Redirect to dashboard
```

### 4.2 Login Flow

```
User enters email → Supabase Auth → Magic link sent → User clicks link → 
JWT issued → Backend validates JWT → User session created → Redirect to dashboard
```

### 4.3 OAuth Flow

```
User clicks "Sign in with Google" → Redirect to Google → User consents → 
Redirect back to app → JWT issued → Backend validates JWT → User session created
```

### 4.4 Token Refresh Flow

```
Access token expires (1 hour) → Frontend detects 401 → 
Use refresh token to get new access token → Retry original request
```

## 5. JWT Token Structure

### 5.1 Access Token (1 hour expiry)

```json
{
  "aud": "authenticated",
  "exp": 1679900000,
  "sub": "user-uuid-here",
  "email": "user@example.com",
  "phone": "",
  "app_metadata": {
    "subscription_tier": "free",
    "subscription_status": "active"
  },
  "user_metadata": {
    "full_name": "John Doe",
    "avatar_url": "https://..."
  },
  "role": "authenticated",
  "aal": "aal1",
  "amr": [
    {
      "method": "otp",
      "timestamp": 1679896400
    }
  ],
  "session_id": "session-uuid-here",
  "iss": "https://your-project.supabase.co/auth/v1",
  "iat": 1679896400
}
```

### 5.2 Refresh Token (30 day expiry)
- Stored securely in httpOnly cookie
- Used to obtain new access tokens
- Rotated on each use (security)
- Revoked on logout

## 6. Backend Authentication

### 6.1 JWT Validation Middleware

```python
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
import os

app = FastAPI()
security = HTTPBearer()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Validate JWT token and return user info
    """
    token = credentials.credentials
    
    try:
        # Validate token with Supabase
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {
            "user_id": user.id,
            "email": user.email,
            "app_metadata": user.app_metadata,
            "user_metadata": user.user_metadata
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

# Usage in routes
@app.get("/api/v1/users/me/progress")
async def get_user_progress(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    # Fetch progress for user_id
```

### 6.2 Optional Authentication

Some endpoints work for both authenticated and anonymous users:

```python
async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict | None:
    """
    Return user info if token valid, None otherwise
    """
    try:
        token = credentials.credentials
        user_response = supabase.auth.get_user(token)
        if user_response.user:
            return {
                "user_id": user_response.user.id,
                "email": user_response.user.email
            }
    except:
        pass
    return None

@app.get("/api/v1/chapters/{chapter_id}")
async def get_chapter(
    chapter_id: int,
    current_user: dict | None = Depends(get_optional_user)
):
    # Chapter content available to all
    # But progress tracking requires auth
```

## 7. Authorization Rules

### 7.1 Content Access

| Endpoint | Free User | Premium User | Anonymous |
|----------|-----------|--------------|-----------|
| GET /chapters (list) | ✅ Free chapters only | ✅ All chapters | ✅ Free chapters only |
| GET /chapters/{id} (1-4) | ✅ Access | ✅ Access | ❌ Auth required |
| GET /chapters/{id} (5-24) | ❌ Denied | ✅ Access | ❌ Auth required |
| GET /search | ✅ Free content only | ✅ All content | ❌ Auth required |

### 7.2 Progress Tracking

| Endpoint | Free User | Premium User | Anonymous |
|----------|-----------|--------------|-----------|
| GET /progress | ✅ Own progress | ✅ Own progress | ❌ Auth required |
| PUT /progress | ✅ Own progress | ✅ Own progress | ❌ Auth required |
| POST /quiz/submit | ✅ Free chapters | ✅ All chapters | ❌ Auth required |

### 7.3 Subscription Management

| Endpoint | Free User | Premium User | Anonymous |
|----------|-----------|--------------|-----------|
| GET /access/check | ✅ Own status | ✅ Own status | ❌ Auth required |
| POST /access/upgrade | ✅ Can upgrade | ❌ Already premium | ❌ Auth required |
| DELETE /access/subscription | ❌ No subscription | ✅ Can cancel | ❌ Auth required |

## 8. API Contract

### POST /api/v1/auth/signup

**Description:** Create new user account (magic link)

**Request:**
```http
POST /api/v1/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": null,
  "auth_method": "magic_link"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Magic link sent to user@example.com",
  "email": "user@example.com",
  "auth_method": "magic_link"
}
```

### POST /api/v1/auth/login

**Description:** Login with magic link

**Request:**
```http
POST /api/v1/auth/login
Content-Type: application/json

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

### POST /api/v1/auth/callback

**Description:** Handle magic link callback (frontend route)

**Request:**
```http
GET /api/v1/auth/callback?access_token=xxx&refresh_token=yyy&expires_in=3600
```

**Response:** Redirect to dashboard with tokens stored

### POST /api/v1/auth/oauth/{provider}

**Description:** Initiate OAuth login

**Request:**
```http
POST /api/v1/auth/oauth/google
```

**Response (200 OK):**
```json
{
  "success": true,
  "oauth_url": "https://accounts.google.com/o/oauth2/auth?..."
}
```

### POST /api/v1/auth/refresh

**Description:** Refresh access token

**Request:**
```http
POST /api/v1/auth/refresh
Content-Type: application/json

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

### POST /api/v1/auth/logout

**Description:** Logout user (revoke refresh token)

**Request:**
```http
POST /api/v1/auth/logout
Authorization: Bearer {access_token}

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

### GET /api/v1/auth/me

**Description:** Get current user info

**Request:**
```http
GET /api/v1/auth/me
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "user_id": "uuid-here",
  "email": "user@example.com",
  "full_name": "John Doe",
  "avatar_url": "https://...",
  "subscription_tier": "free",
  "created_at": "2026-03-15T08:00:00Z"
}
```

## 9. Security Considerations

### 9.1 Token Storage

**Frontend:**
- Access token: Memory only (not localStorage)
- Refresh token: httpOnly cookie (not accessible to JavaScript)
- Prevents XSS token theft

**Backend:**
- Never log tokens
- Validate tokens on every request
- Use HTTPS only

### 9.2 Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/auth/signup")
@limiter.limit("5/minute")
async def signup(request: Request):
    # Prevent signup spam
```

**Limits:**
- Signup/Login: 5 requests per minute per IP
- Token refresh: 10 requests per minute per user
- Password reset: 3 requests per hour per email

### 9.3 Password Requirements (if used)

```python
import re

def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password meets requirements
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"
```

### 9.4 CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",  # Production
        "http://localhost:3000",         # Development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 10. Database Integration

### 10.1 Supabase Auth Hooks

Automatically create user record in public.users table:

```sql
-- Function to create user record after signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id, email, full_name, created_at, updated_at)
  VALUES (
    NEW.id,
    NEW.email,
    NEW.raw_user_meta_data->>'full_name',
    NOW(),
    NOW()
  );
  
  -- Create free subscription
  INSERT INTO public.subscriptions (user_id, tier, status)
  VALUES (NEW.id, 'free', 'free');
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger on auth.users
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();
```

### 10.2 User Subscription Check

```python
async def check_premium_access(user_id: str, chapter_id: int) -> bool:
    """
    Check if user has premium access to chapter
    """
    # Get chapter's free status
    chapter = await get_chapter(chapter_id)
    if chapter.is_free:
        return True
    
    # Check user subscription
    subscription = await get_subscription(user_id)
    if subscription.tier in ['premium', 'pro', 'team'] and subscription.status == 'active':
        return True
    
    return False
```

## 11. Testing Requirements

### Test Scenarios

```python
def test_auth_magic_link_signup():
    """User should be able to signup with magic link"""
    # Arrange: New email
    # Act: POST /api/v1/auth/signup with email
    # Assert: 200 OK, magic link sent message

def test_auth_magic_link_login():
    """Existing user should be able to login with magic link"""
    # Arrange: Existing user email
    # Act: POST /api/v1/auth/login with email
    # Assert: 200 OK, magic link sent message

def test_auth_jwt_validation():
    """Valid JWT should grant access to protected endpoints"""
    # Arrange: Valid access token
    # Act: GET /api/v1/auth/me with token
    # Assert: 200 OK, user info returned

def test_auth_invalid_jwt():
    """Invalid JWT should be rejected"""
    # Arrange: Expired/invalid token
    # Act: GET /api/v1/auth/me with invalid token
    # Assert: 401 Unauthorized

def test_auth_token_refresh():
    """Refresh token should obtain new access token"""
    # Arrange: Valid refresh token
    # Act: POST /api/v1/auth/refresh
    # Assert: 200 OK, new access token returned

def test_auth_logout():
    """Logout should revoke refresh token"""
    # Arrange: Logged in user
    # Act: POST /api/v1/auth/logout
    # Assert: 200 OK, refresh token invalidated

def test_auth_oauth_google():
    """Google OAuth should initiate login flow"""
    # Arrange: Valid OAuth request
    # Act: POST /api/v1/auth/oauth/google
    # Assert: 200 OK, OAuth URL returned

def test_auth_rate_limiting():
    """Too many auth attempts should be rate limited"""
    # Arrange: Make 10 signup requests in 1 minute
    # Act: POST /api/v1/auth/signup (10 times)
    # Assert: 429 Too Many Requests on 6th request
```

## 12. Open Questions

1. **Session Duration:** Should we offer "Remember me" option (30-day sessions vs 1-hour)?
2. **Multi-Factor Auth:** Should we implement MFA for premium users (Phase 2)?
3. **Email Templates:** Should we customize magic link emails or use Supabase defaults?
4. **Anonymous Access:** Should some content be available without any authentication?
5. **Social Features:** Should we support viewing other users' profiles (opt-in)?

## 13. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Auth Architecture Spec (SPEC-T-002-auth-architecture-v1.0)  
**Why:** Defines how users authenticate and authorize access to the application  
**Files Affected:** 
- `docs/specs/technical/SPEC-T-002-auth-architecture-v1.0.md`

**Key Decisions:**
- Supabase Auth (free tier, 50K MAUs)
- Magic links as primary auth method
- OAuth (Google, GitHub) as secondary
- Email/password as fallback
- JWT tokens (1-hour access, 30-day refresh)
- Row Level Security for data protection
- Rate limiting on auth endpoints

**Do you approve this spec?** (Yes/No/Modify)

---

**Progress Update:**
- ✅ Phase 1 Feature Specs: 6/6 Complete
- ✅ Technical Specs: 2/3 Complete (SPEC-T-001, T-002 done, T-003 remaining)
- ⏳ API Specs: 0/5 Pending
