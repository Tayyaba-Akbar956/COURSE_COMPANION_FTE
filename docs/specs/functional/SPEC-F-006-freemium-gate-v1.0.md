# SPEC-F-006-freemium-gate-v1.0

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

This spec defines the Freemium Gate feature that controls access to course content based on user subscription status. Free users get access to Module 1 (Chapters 1-4), while premium users get access to all 24 chapters. This is a critical feature for monetization while providing value to free users.

**Critical Principle:** Access control is enforced server-side (backend), not client-side. ChatGPT gracefully communicates access limitations to users.

## 2. Functional Requirements

### FR-1: Free Tier Access
- Free users can access Module 1 (Chapters 1-4) completely
- Free users can take quizzes for Chapters 1-4
- Free users can track progress for Chapters 1-4
- Free users can use all features within accessible chapters

### FR-2: Premium Tier Access
- Premium users can access all 24 chapters
- Premium users can take all quizzes
- Premium users have full progress tracking
- Premium users get access to future premium features (Phase 2)

### FR-3: Access Verification
- Access checked on every content request
- Access checked before quiz access
- Access checked before progress updates
- Clear error messages when access denied

### FR-4: Upgrade Prompts
- Upgrade prompt shown when free user tries to access premium content
- Upgrade prompt shows value proposition
- Upgrade prompt includes pricing information
- Upgrade prompt is non-intrusive but clear

### FR-5: Graceful Degradation
- Free users not blocked from using app entirely
- Free users can still navigate, search (within free content)
- Free users receive helpful messages, not harsh denials
- Free users encouraged to upgrade, not guilted

### FR-6: Subscription Management
- Users can view their subscription status
- Users can upgrade from free to premium
- Users can see when premium expires (if applicable)
- Users can downgrade (effective at next billing cycle)

## 3. Technical Requirements

### TR-1: Access Control Implementation
- Access control enforced server-side (backend API)
- User subscription status stored in database
- Access checks happen before content served
- JWT tokens include subscription status (cached, not source of truth)

### TR-2: Subscription Status
- Subscription status: `free`, `premium`, `expired`, `cancelled`
- Premium expiration date stored (for time-limited subscriptions)
- Subscription status checked on every API request
- Status cached for 5 minutes (reduce database reads)

### TR-3: Access Control Middleware
- Middleware checks access before route handler
- Middleware extracts user_id from JWT
- Middleware queries subscription status
- Middleware injects access level into request context

### TR-4: Performance
- Access check adds < 50ms to request time (with caching)
- No N+1 queries for access checks
- Batch access checks when loading multiple chapters
- Access control doesn't block concurrent requests

### TR-5: Security
- Access control cannot be bypassed client-side
- API endpoints protected (not just UI)
- Subscription status validated server-side
- Prevent subscription status manipulation

## 4. API Contract

### GET /api/v1/access/check

**Description:** Check user's access level

**Request:**
```http
GET /api/v1/access/check
Authorization: Bearer {user_token}
```

**Response (200 OK - Free User):**
```json
{
  "user_id": "user123",
  "subscription": {
    "status": "free",
    "tier": "free",
    "started_at": "2026-03-15T08:00:00Z",
    "expires_at": null,
    "auto_renew": false
  },
  "access": {
    "accessible_chapters": [1, 2, 3, 4],
    "accessible_modules": [1],
    "total_chapters": 24,
    "accessible_percentage": 16.7,
    "features": {
      "content_access": "free_tier",
      "quiz_access": "free_tier",
      "progress_tracking": "full",
      "search": "free_tier",
      "adaptive_learning": "locked",
      "llm_assessments": "locked"
    }
  },
  "upgrade_available": true,
  "upgrade_url": "/pricing"
}
```

**Response (200 OK - Premium User):**
```json
{
  "user_id": "user123",
  "subscription": {
    "status": "premium",
    "tier": "premium",
    "started_at": "2026-03-01T08:00:00Z",
    "expires_at": "2026-04-01T08:00:00Z",
    "auto_renew": true
  },
  "access": {
    "accessible_chapters": "all",
    "accessible_modules": "all",
    "total_chapters": 24,
    "accessible_percentage": 100,
    "features": {
      "content_access": "full",
      "quiz_access": "full",
      "progress_tracking": "full",
      "search": "full",
      "adaptive_learning": "full",
      "llm_assessments": "full"
    }
  },
  "upgrade_available": false
}
```

### GET /api/v1/access/chapter/{chapter_id}

**Description:** Check if user can access a specific chapter

**Request:**
```http
GET /api/v1/access/chapter/5
Authorization: Bearer {user_token}
```

**Response (200 OK - Access Granted):**
```json
{
  "chapter_id": 5,
  "chapter_title": "What are LLMs?",
  "access_granted": true,
  "reason": "user_has_premium_access",
  "user_tier": "premium"
}
```

**Response (403 Forbidden - Access Denied):**
```json
{
  "error": "access_denied",
  "chapter_id": 5,
  "chapter_title": "What are LLMs?",
  "access_granted": false,
  "reason": "chapter_requires_premium",
  "user_tier": "free",
  "accessible_chapters": [1, 2, 3, 4],
  "upgrade": {
    "available": true,
    "url": "/pricing",
    "message": "Upgrade to Premium to access this chapter",
    "benefits": [
      "Access all 24 chapters",
      "Unlimited quiz attempts",
      "Full progress tracking",
      "Certificate of completion"
    ]
  }
}
```

### POST /api/v1/access/upgrade

**Description:** Upgrade user to premium

**Request:**
```http
POST /api/v1/access/upgrade
Authorization: Bearer {user_token}
Content-Type: application/json

{
  "tier": "premium",
  "payment_method_id": "pm_123456",
  "coupon_code": null
}
```

**Response (200 OK - Upgrade Successful):**
```json
{
  "success": true,
  "subscription": {
    "status": "premium",
    "tier": "premium",
    "started_at": "2026-03-29T12:00:00Z",
    "expires_at": "2026-04-29T12:00:00Z",
    "auto_renew": true,
    "amount": 999,
    "currency": "usd"
  },
  "access_updated": {
    "accessible_chapters": "all",
    "accessible_modules": "all",
    "features_unlocked": ["adaptive_learning", "llm_assessments"]
  },
  "receipt_url": "https://payments.example.com/receipt/abc123"
}
```

**Response (400 Bad Request - Payment Failed):**
```json
{
  "error": "payment_failed",
  "message": "Your payment could not be processed. Please try a different payment method.",
  "payment_error_code": "card_declined",
  "retry_available": true
}
```

### GET /api/v1/access/pricing

**Description:** Get pricing information

**Request:**
```http
GET /api/v1/access/pricing
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "plans": [
    {
      "tier": "free",
      "name": "Free",
      "price": 0,
      "currency": "usd",
      "billing_period": "forever",
      "features": [
        "Access to Module 1 (4 chapters)",
        "Basic quizzes",
        "Progress tracking",
        "ChatGPT tutoring"
      ],
      "limitations": [
        "No access to Chapters 5-24",
        "No adaptive learning",
        "No LLM assessments",
        "No certificate"
      ],
      "current_plan": true
    },
    {
      "tier": "premium",
      "name": "Premium",
      "price": 999,
      "currency": "usd",
      "billing_period": "month",
      "features": [
        "Access all 24 chapters",
        "Unlimited quiz attempts",
        "Full progress tracking",
        "Adaptive learning path",
        "LLM-graded assessments",
        "Certificate of completion"
      ],
      "popular": true,
      "current_plan": false
    },
    {
      "tier": "pro",
      "name": "Pro",
      "price": 1999,
      "currency": "usd",
      "billing_period": "month",
      "features": [
        "Everything in Premium",
        "Priority support",
        "Downloadable resources",
        "Advanced analytics",
        "1-on-1 AI mentoring"
      ],
      "current_plan": false
    },
    {
      "tier": "team",
      "name": "Team",
      "price": 4999,
      "currency": "usd",
      "billing_period": "month",
      "features": [
        "Everything in Pro",
        "Up to 5 team seats",
        "Team progress dashboard",
        "Admin controls",
        "Priority support"
      ],
      "current_plan": false
    }
  ],
  "special_offers": [
    {
      "code": "STUDENT20",
      "description": "20% off for students",
      "discount_percentage": 20,
      "applicable_tiers": ["premium", "pro"]
    }
  ]
}
```

### DELETE /api/v1/access/subscription

**Description:** Cancel subscription (effective at end of billing period)

**Request:**
```http
DELETE /api/v1/access/subscription
Authorization: Bearer {user_token}
```

**Response (200 OK - Cancellation Scheduled):**
```json
{
  "success": true,
  "subscription": {
    "status": "cancelled",
    "tier": "premium",
    "expires_at": "2026-04-29T12:00:00Z",
    "cancelled_at": "2026-03-29T12:00:00Z",
    "access_until": "2026-04-29T12:00:00Z"
  },
  "message": "Your subscription will remain active until 2026-04-29. You will not be charged after this date."
}
```

## 5. User Stories

### US-1: Free User Accessing Free Content
**As a** free user  
**I want** to access Module 1 without restrictions  
**So that** I can evaluate the course quality

**Acceptance Criteria:**
- [ ] Can access Chapters 1-4 without prompts
- [ ] Can take quizzes for Chapters 1-4
- [ ] Can track progress normally
- [ ] No upgrade prompts within free content

### US-2: Free User Encountering Premium Content
**As a** free user browsing the course  
**I want** to know when I've reached premium content  
**So that** I understand why I can't access it

**Acceptance Criteria:**
- [ ] Clear message that chapter requires premium
- [ ] Upgrade option presented
- [ ] Pricing information available
- [ ] Can continue browsing free content

### US-3: Free User Deciding to Upgrade
**As a** free user who wants full access  
**I want** to upgrade to premium easily  
**So that** I can access all chapters

**Acceptance Criteria:**
- [ ] Upgrade button visible and accessible
- [ ] Pricing page shows all plans clearly
- [ ] Payment process is secure and simple
- [ ] Access granted immediately after payment
- [ ] Receipt provided

### US-4: Premium User Accessing Content
**As a** premium user  
**I want** to access all chapters without restrictions  
**So that** I can learn at my own pace

**Acceptance Criteria:**
- [ ] All 24 chapters accessible
- [ ] No access denied messages
- [ ] Premium status recognized consistently
- [ ] Can access premium features

### US-5: User Managing Subscription
**As a** premium user  
**I want** to view and manage my subscription  
**So that** I know when I'll be charged

**Acceptance Criteria:**
- [ ] Can view subscription status
- [ ] Can see next billing date
- [ ] Can cancel subscription
- [ ] Cancellation effective at end of period
- [ ] Can downgrade to free

### US-6: Expired Premium User
**As a** user whose premium expired  
**I want** to know my access has changed  
**So that** I understand why I can't access premium content

**Acceptance Criteria:**
- [ ] Clear notification of expiration
- [ ] Access reverts to free tier
- [ ] Option to renew presented
- [ ] Previous progress still visible

## 6. Acceptance Criteria

### Functional Tests
- [ ] Free user can access Chapters 1-4
- [ ] Free user cannot access Chapters 5-24
- [ ] Premium user can access all chapters
- [ ] Access check returns correct accessible chapters
- [ ] Upgrade prompt shown at access boundary
- [ ] Upgrade process grants access immediately
- [ ] Subscription cancellation works correctly
- [ ] Expired subscription reverts to free tier
- [ ] Access control enforced server-side
- [ ] Clear error messages for access denied

### Non-Functional Tests
- [ ] Access check adds < 50ms to requests
- [ ] Access control cannot be bypassed
- [ ] Subscription status cached appropriately
- [ ] No N+1 queries for access checks
- [ ] Graceful handling of payment failures
- [ ] Clear, non-hostile messaging to free users

## 7. Dependencies

### Internal Dependencies
- SPEC-F-001-content-delivery-v1.0.md (content access)
- SPEC-T-002-auth-architecture-v1.0.md (user authentication)
- SPEC-A-004-auth-apis-v1.0.md (JWT validation)

### External Dependencies
- Supabase PostgreSQL (subscription storage)
- Stripe or similar (payment processing)
- Supabase Auth (user management)

## 8. Out of Scope

This spec does NOT cover:
- Payment processing implementation (use Stripe or similar)
- Refund policy enforcement (handled by payment processor)
- Invoice generation (handled by payment processor)
- Dunning management (failed payment retries, Phase 3)
- Promotional code validation beyond simple codes
- Corporate/enterprise billing (Phase 3)
- Gift subscriptions (Phase 3)
- Scholarship/discounted access programs (Phase 3)

## 9. Testing Requirements

### Test Scenarios

#### Test 1: Free User Access Check
```python
def test_freemium_gate_free_user_access_check():
    """Free user should have access to Chapters 1-4 only"""
    # Arrange: Create free user
    # Act: GET /api/v1/access/check
    # Assert: accessible_chapters=[1,2,3,4], tier=free
```

#### Test 2: Free User Accessing Free Chapter
```python
def test_freemium_gate_free_user_accessing_free_chapter():
    """Free user should be granted access to Chapter 1"""
    # Arrange: Free user, GET /api/v1/access/chapter/1
    # Act: Check access
    # Assert: access_granted=true, reason=user_in_free_tier
```

#### Test 3: Free User Accessing Premium Chapter
```python
def test_freemium_gate_free_user_accessing_premium_chapter():
    """Free user should be denied access to Chapter 5"""
    # Arrange: Free user, GET /api/v1/access/chapter/5
    # Act: Check access
    # Assert: 403 Forbidden, upgrade prompt included
```

#### Test 4: Premium User Accessing Premium Chapter
```python
def test_freemium_gate_premium_user_accessing_premium_chapter():
    """Premium user should be granted access to Chapter 5"""
    # Arrange: Premium user, GET /api/v1/access/chapter/5
    # Act: Check access
    # Assert: access_granted=true, reason=user_has_premium
```

#### Test 5: Upgrade Process
```python
def test_freemium_gate_upgrade_process():
    """User upgrading from free to premium should gain access immediately"""
    # Arrange: Free user, POST /api/v1/access/upgrade with valid payment
    # Act: Process upgrade
    # Assert: subscription status=premium, accessible_chapters=all
```

#### Test 6: Payment Failure Handling
```python
def test_freemium_gate_payment_failure():
    """Failed payment should return clear error message"""
    # Arrange: User with declined card, POST /api/v1/access/upgrade
    # Act: Process payment (will fail)
    # Assert: 400 Bad Request, payment_failed error, retry_available=true
```

#### Test 7: Subscription Cancellation
```python
def test_freemium_gate_subscription_cancellation():
    """User cancelling subscription should retain access until expiry"""
    # Arrange: Premium user, DELETE /api/v1/access/subscription
    # Act: Cancel subscription
    # Assert: status=cancelled, expires_at set, access_until matches
```

#### Test 8: Expired Subscription Reverts to Free
```python
def test_freemium_gate_expired_subscription_reverts():
    """Expired premium subscription should revert to free tier"""
    # Arrange: User with expired premium subscription
    # Act: GET /api/v1/access/check
    # Assert: tier=free, accessible_chapters=[1,2,3,4]
```

### Coverage Requirements
- Minimum 90% code coverage
- All access control endpoints tested
- Payment flow tested (success and failure)
- Edge cases (expired, cancelled, grace period) tested
- Security tests (cannot bypass access control)

## 10. Open Questions

1. **Free Tier Extent:** Should free tier be Chapters 1-3 (original hackathon doc) or Chapters 1-4 (full Module 1)?
2. **Trial Period:** Should we offer a 7-day or 14-day premium trial for new users?
3. **Grace Period:** Should there be a grace period after payment failure before access is revoked?
4. **Proration:** Should we prorate upgrades/downgrades mid-billing-cycle?
5. **Lifetime Access:** Should we offer a one-time payment for lifetime access (vs. subscription only)?

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Freemium Gate Spec (SPEC-F-006-freemium-gate-v1.0)  
**Why:** Defines access control based on subscription status (core Phase 1 feature for monetization)  
**Files Affected:** 
- `docs/specs/functional/SPEC-F-006-freemium-gate-v1.0.md`

**Key Decisions:**
- Free tier: Module 1 (Chapters 1-4) - full module, not partial
- Premium tier: All 24 chapters + all features
- Access control enforced server-side (backend API)
- Clear, non-hostile messaging to free users
- Upgrade prompts at access boundary
- Multiple pricing tiers (Free, Premium $9.99/mo, Pro $19.99/mo, Team $49.99/mo)
- Subscription management (view, upgrade, cancel)
- Payment processing via Stripe (or similar)

**Do you approve this spec?** (Yes/No/Modify)

---

## ✅ **ALL PHASE 1 FEATURE SPECS COMPLETE!**

### Summary of Phase 1 Feature Specs Created:

| Spec # | Feature | Status |
|--------|---------|--------|
| SPEC-F-000 | Course Outline | ✅ Complete |
| SPEC-F-001 | Content Delivery | ✅ Complete |
| SPEC-F-002 | Navigation | ✅ Complete |
| SPEC-F-003 | Grounded Q&A | ✅ Complete |
| SPEC-F-004 | Rule-Based Quizzes | ✅ Complete |
| SPEC-F-005 | Progress Tracking | ✅ Complete |
| SPEC-F-006 | Freemium Gate | ✅ Complete |

**Next Steps:**
1. Await your approval on all specs
2. Create Technical Specs (SPEC-T-001, T-002, T-003)
3. Create API Specs (SPEC-A-001 through A-005)
4. Begin backend implementation with tests

**What would you like me to work on next?**
