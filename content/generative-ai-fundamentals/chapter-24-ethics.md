# Chapter 24: Ethics, Safety, and Responsible AI

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand AI ethics principles
- Identify potential harms and biases
- Implement safety measures
- Practice responsible AI development

## AI Ethics Principles

### Core Principles

**1. Fairness**
```
AI systems should:
✓ Treat all users equally
✓ Not discriminate based on protected characteristics
✓ Be accessible to diverse users
✓ Avoid perpetuating historical biases
```

**2. Transparency**
```
AI systems should:
✓ Be clear about AI involvement
✓ Explain decisions when possible
✓ Disclose limitations
✓ Provide information about training data
```

**3. Accountability**
```
AI developers should:
✓ Take responsibility for outputs
✓ Provide recourse for harms
✓ Maintain human oversight
✓ Enable auditing
```

**4. Privacy**
```
AI systems should:
✓ Protect user data
✓ Minimize data collection
✓ Enable user control
✓ Follow data protection regulations
```

**5. Safety**
```
AI systems should:
✓ Not cause harm
✓ Be reliable and robust
✓ Fail gracefully
✓ Have appropriate safeguards
```

## Potential Harms and Biases

### Types of Bias

**1. Historical Bias**
```
Problem: Training data reflects historical inequalities

Example:
- Hiring data shows preference for male candidates
- AI learns to downgrade female candidates

Mitigation:
- Audit training data for biases
- Use debiasing techniques
- Monitor outputs for discrimination
```

**2. Representation Bias**
```
Problem: Underrepresentation of certain groups

Example:
- Facial recognition trained mostly on light-skinned faces
- Poor performance on dark-skinned individuals

Mitigation:
- Ensure diverse training data
- Test across demographic groups
- Set performance requirements for all groups
```

**3. Measurement Bias**
```
Problem: Proxy variables don't measure what intended

Example:
- Using zip code as proxy for creditworthiness
- Correlates with race due to historical segregation

Mitigation:
- Carefully select features
- Audit proxy variables
- Use direct measures when possible
```

**4. Aggregation Bias**
```
Problem: One model doesn't fit all groups

Example:
- Medical diagnosis model trained on general population
- Performs poorly on specific ethnic groups

Mitigation:
- Stratify evaluation by group
- Consider separate models for different groups
- Monitor performance disparities
```

### Harmful Content Categories

```
1. Hate Speech
   - Racist, sexist, or discriminatory content
   - Dehumanizing language
   - Calls for violence

2. Harassment
   - Threatening messages
   - Unwanted sexual content
   - Bullying behavior

3. Misinformation
   - False medical advice
   - Election misinformation
   - Conspiracy theories

4. Dangerous Activities
   - Self-harm instructions
   - Violence promotion
   - Illegal activity guidance

5. Privacy Violations
   - Doxxing assistance
   - Personal information exposure
   - Stalking facilitation
```

## Safety Measures

### Content Filtering

**Input Filtering:**
```python
def filter_input(prompt: str) -> Tuple[bool, str]:
    """Check if input violates policies"""
    
    blocked_categories = [
        'hate_speech',
        'harassment',
        'self_harm',
        'violence',
        'sexual_content',
    ]
    
    # Use moderation API
    moderation = openai.Moderation.create(input=prompt)
    flagged = moderation.results[0].flagged
    
    if flagged:
        categories = moderation.results[0].categories
        violated = [cat for cat, is_flagged in categories.items() if is_flagged]
        return False, f"Content violates: {', '.join(violated)}"
    
    return True, "OK"

# Usage
allowed, message = filter_input(user_prompt)
if not allowed:
    return "I cannot help with that request."
```

**Output Filtering:**
```python
def filter_output(response: str) -> str:
    """Filter harmful content from output"""
    
    # Check for PII
    pii_patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b\d{16}\b',  # Credit card
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
    ]
    
    for pattern in pii_patterns:
        response = re.sub(pattern, '[REDACTED]', response)
    
    # Check for harmful content
    if contains_harmful_content(response):
        return "I apologize, but I cannot provide that information."
    
    return response
```

### Access Controls

```python
from functools import wraps
from typing import List

def require_role(allowed_roles: List[str]):
    """Require specific user roles"""
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.role not in allowed_roles:
                raise PermissionError(
                    f"Access denied. Required: {allowed_roles}, Got: {user.role}"
                )
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

def rate_limit(max_requests: int, window_seconds: int):
    """Rate limit per user"""
    def decorator(func):
        @wraps(func)
        def wrapper(user_id, *args, **kwargs):
            key = f"rate_limit:{user_id}"
            current = redis.incr(key)
            if current == 1:
                redis.expire(key, window_seconds)
            if current > max_requests:
                raise RateLimitExceeded("Too many requests")
            return func(user_id, *args, **kwargs)
        return wrapper
    return decorator

# Usage
@require_role(['admin', 'premium'])
@rate_limit(max_requests=100, window_seconds=60)
def generate_content(user, prompt):
    return ai.generate(prompt)
```

### Audit Trails

```python
class AuditLogger:
    """Log all AI interactions for auditing"""
    
    def log_generation(
        self,
        user_id: str,
        prompt: str,
        response: str,
        model: str,
        timestamp: datetime
    ):
        """Log content generation"""
        db.audit_logs.insert({
            'event_type': 'generation',
            'user_id': user_id,
            'prompt': prompt,
            'response': response,
            'model': model,
            'timestamp': timestamp,
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent
        })
    
    def log_moderation(
        self,
        content: str,
        flagged: bool,
        categories: List[str],
        action_taken: str
    ):
        """Log moderation decisions"""
        db.audit_logs.insert({
            'event_type': 'moderation',
            'content': content,
            'flagged': flagged,
            'categories': categories,
            'action_taken': action_taken,
            'timestamp': datetime.utcnow()
        })
    
    def get_user_history(self, user_id: str, days: int = 30) -> List[Dict]:
        """Get user's audit history"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        return db.audit_logs.find({
            'user_id': user_id,
            'timestamp': {'$gte': cutoff}
        })
```

## Responsible AI Development

### Development Guidelines

**1. Impact Assessment**
```
Before launching:
□ Identify potential misuse scenarios
□ Assess harm severity and likelihood
□ Plan mitigation strategies
□ Define success metrics beyond engagement
□ Establish review processes
```

**2. Diverse Teams**
```
Include perspectives from:
✓ Different backgrounds
✓ Different abilities
✓ Different geographies
✓ Domain experts
✓ Affected communities
```

**3. Testing and Validation**
```
Test for:
□ Bias across demographic groups
□ Edge cases and adversarial inputs
□ Harmful output scenarios
□ Privacy violations
□ Security vulnerabilities
```

**4. Documentation**
```
Document:
□ Model capabilities and limitations
□ Training data sources
□ Known biases
□ Intended use cases
□ Contraindicated uses
□ Monitoring plans
```

### User Communication

**Clear Disclosure:**
```
✓ "This content was generated by AI"
✓ "AI may make mistakes. Verify important information."
✓ "We use AI to power this feature"
✓ Link to AI policy and limitations
```

**Feedback Mechanisms:**
```python
def collect_feedback(
    response_id: str,
    feedback_type: str,  # 'accurate', 'inaccurate', 'harmful', 'biased'
    user_comment: str = None
):
    """Collect user feedback on AI outputs"""
    
    db.feedback.insert({
        'response_id': response_id,
        'type': feedback_type,
        'comment': user_comment,
        'timestamp': datetime.utcnow()
    })
    
    # Escalate serious issues
    if feedback_type in ['harmful', 'biased']:
        alert_team(f"User reported {feedback_type} content", response_id)
```

## Code Example: Responsible AI Framework

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SafetyCheck:
    name: str
    passed: bool
    risk_level: RiskLevel
    details: str

class ResponsibleAIFramework:
    """Framework for responsible AI development"""
    
    def __init__(self):
        self.audit_logger = AuditLogger()
        self.moderation_api = OpenAIModeration()
    
    def pre_generation_checks(self, prompt: str, user: User) -> List[SafetyCheck]:
        """Run safety checks before generation"""
        checks = []
        
        # Check 1: Content moderation
        moderation = self.moderation_api.create(input=prompt)
        checks.append(SafetyCheck(
            name="Input Moderation",
            passed=not moderation.results[0].flagged,
            risk_level=RiskLevel.HIGH if moderation.results[0].flagged else RiskLevel.LOW,
            details=str(moderation.results[0].categories)
        ))
        
        # Check 2: Rate limiting
        request_count = self.get_request_count(user.id, window_minutes=60)
        rate_exceeded = request_count >= user.rate_limit
        checks.append(SafetyCheck(
            name="Rate Limit",
            passed=not rate_exceeded,
            risk_level=RiskLevel.MEDIUM if rate_exceeded else RiskLevel.LOW,
            details=f"Requests: {request_count}/{user.rate_limit}"
        ))
        
        # Check 3: Sensitive topics
        sensitive_topics = ['medical', 'legal', 'financial']
        contains_sensitive = any(topic in prompt.lower() for topic in sensitive_topics)
        checks.append(SafetyCheck(
            name="Sensitive Topic",
            passed=not contains_sensitive,
            risk_level=RiskLevel.MEDIUM if contains_sensitive else RiskLevel.LOW,
            details="Contains sensitive topic" if contains_sensitive else "No sensitive topics"
        ))
        
        return checks
    
    def post_generation_checks(
        self,
        response: str,
        prompt: str,
        checks: List[SafetyCheck]
    ) -> Tuple[bool, str]:
        """Decide whether to return response"""
        
        # Block if any HIGH or CRITICAL risk
        high_risk = [c for c in checks if c.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        if high_risk:
            return False, f"Blocked due to: {', '.join(c.name for c in high_risk)}"
        
        # Add disclaimer for MEDIUM risk
        medium_risk = [c for c in checks if c.risk_level == RiskLevel.MEDIUM]
        if medium_risk:
            disclaimer = self.get_disclaimer(medium_risk)
            response = f"{disclaimer}\n\n{response}"
        
        # Log for auditing
        self.audit_logger.log_generation(
            user_id=current_user.id,
            prompt=prompt,
            response=response,
            model=self.model_name,
            timestamp=datetime.utcnow()
        )
        
        return True, response
    
    def get_disclaimer(self, checks: List[SafetyCheck]) -> str:
        """Get appropriate disclaimer"""
        check_names = [c.name for c in checks]
        
        if 'Sensitive Topic' in check_names:
            return "⚠️ This information is for general guidance only. Please consult a professional for specific advice."
        
        return ""
    
    def generate_safely(self, user: User, prompt: str) -> Dict:
        """Generate with full safety checks"""
        
        # Pre-generation checks
        checks = self.pre_generation_checks(prompt, user)
        
        # Decide whether to proceed
        allowed, message = self.post_generation_checks("", prompt, checks)
        if not allowed:
            return {
                'success': False,
                'error': message,
                'blocked': True
            }
        
        # Generate
        response = self.ai.generate(prompt)
        
        # Post-generation checks
        allowed, final_response = self.post_generation_checks(response, prompt, checks)
        
        return {
            'success': allowed,
            'response': final_response if allowed else message,
            'checks_passed': len([c for c in checks if c.passed]),
            'total_checks': len(checks)
        }

# Usage
framework = ResponsibleAIFramework()

result = framework.generate_safely(user, prompt)
if result['success']:
    print(result['response'])
else:
    print(f"Blocked: {result['error']}")
```

## Key Takeaways

- **Fairness, transparency, accountability** are core ethics principles
- **Bias can enter** at multiple stages - audit continuously
- **Implement safety measures** - filtering, access controls, audit trails
- **Conduct impact assessments** before launching
- **Communicate clearly** about AI use and limitations
- **Collect feedback** and act on it
- **Responsible AI** is ongoing commitment, not one-time fix

## Glossary

- **Algorithmic Bias:** Systematic unfairness in AI outputs
- **Moderation:** Filtering harmful content
- **Audit Trail:** Record of all AI interactions
- **Impact Assessment:** Evaluation of potential harms
- **Rate Limiting:** Restricting number of requests

## Quiz Questions

**1. Which is NOT a core AI ethics principle?**

A) Fairness
B) Transparency
C) Profitability
D) Accountability

**Correct Answer:** C

**Explanation:** Profitability is a business goal, not an ethics principle. Core principles include fairness, transparency, accountability, privacy, and safety.

---

**2. What is historical bias?**

A) Bias in old software versions
B) Training data reflecting historical inequalities
C) Bias against historians
D) Bias in historical documents only

**Correct Answer:** B

**Explanation:** Historical bias occurs when training data reflects past discrimination or inequalities, which the AI then learns and perpetuates.

---

**3. What should you do if AI generates harmful content?**

A) Ignore it
B) Block it and log for review
C) Show it with a warning
D) Blame the user

**Correct Answer:** B

**Explanation:** Harmful content should be blocked from reaching users and logged for review and system improvement.

---

**4. Why is diverse team representation important?**

A) It's required by law
B) Different perspectives help identify biases and harms
C) It makes hiring easier
D) It reduces costs

**Correct Answer:** B

**Explanation:** Diverse teams bring different perspectives that help identify potential biases, harms, and edge cases that homogeneous teams might miss.

---

**5. What is the purpose of audit trails?**

A) To slow down the system
B) To enable accountability and investigation
C) To increase storage costs
D) To make the code complex

**Correct Answer:** B

**Explanation:** Audit trails enable accountability, investigation of issues, and continuous improvement by recording all AI interactions.

---

## Further Reading

- **AI Ethics Guidelines** - EU Commission: https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai
- **Responsible AI Practices** - Google: https://ai.google/responsibilities/
- **Partnership on AI**: https://partnershiponai.org/
- **AI Now Institute**: https://ainowinstitute.org/

---

## 🎉 Course Complete!

**Congratulations!** You've completed all 24 chapters of Generative AI Fundamentals.

### What You've Learned:

**Module 1: Foundations**
- What generative AI is and how it evolved
- Key concepts and terminology
- Real-world applications

**Module 2: LLMs**
- How large language models work
- Transformer architecture
- Training and capabilities

**Module 3: Prompt Engineering**
- Prompt design patterns
- Advanced prompting strategies
- Optimization techniques

**Module 4: RAG**
- Building retrieval-augmented systems
- Vector databases and embeddings
- Production best practices

**Module 5: Fine-tuning**
- When and how to fine-tune
- LoRA and parameter-efficient methods
- Evaluation techniques

**Module 6: Applications**
- AI-native design
- API integration
- Deployment and production
- Ethics and responsible AI

### Next Steps:

1. **Build projects** to apply your knowledge
2. **Stay current** - AI evolves rapidly
3. **Join communities** - Learn from others
4. **Practice responsibly** - Consider ethics in all you build

**Thank you for learning with us!** 🚀
