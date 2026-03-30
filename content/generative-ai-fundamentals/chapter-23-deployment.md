# Chapter 23: Deployment and Production Considerations

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand production requirements for AI applications
- Learn deployment strategies
- Implement monitoring and logging
- Plan for scale and reliability

## Production Requirements

### Reliability

**Uptime Targets:**
```
Service Level Objective (SLO):
- 99% uptime = 3.65 days downtime/year
- 99.9% uptime = 8.76 hours downtime/year
- 99.99% uptime = 52.6 minutes downtime/year
- 99.999% uptime = 5.26 minutes downtime/year

Target: 99.9% for most AI applications
```

**Redundancy:**
```
✓ Multiple availability zones
✓ Backup API providers
✓ Database replication
✓ Load balancing
```

### Security

**Key Considerations:**
```
Authentication:
- API key management
- User authentication (OAuth, JWT)
- Rate limiting per user

Data Protection:
- Encryption in transit (HTTPS/TLS)
- Encryption at rest
- PII handling policies
- Data retention policies

Access Control:
- Role-based access (RBAC)
- Principle of least privilege
- Audit logging
```

### Compliance

**Common Requirements:**
```
GDPR (EU):
- User consent for data processing
- Right to deletion
- Data portability
- Privacy by design

HIPAA (Healthcare):
- PHI protection
- Access controls
- Audit trails
- Business Associate Agreements

SOC 2:
- Security controls
- Availability
- Processing integrity
- Confidentiality
```

## Deployment Strategies

### 1. Cloud Deployment Options

**Serverless (AWS Lambda, Vercel, Cloud Functions):**
```
Pros:
✓ No infrastructure management
✓ Auto-scaling
✓ Pay per use
✓ Fast deployment

Cons:
✗ Cold starts
✗ Limited control
✗ Cost at scale

Best for: MVPs, variable traffic, microservices
```

**Container (Docker + Kubernetes):**
```
Pros:
✓ Full control
✓ Portable
✓ Scalable
✓ Consistent environments

Cons:
✗ Complex setup
✗ Requires DevOps expertise
✗ Higher management overhead

Best for: Large-scale, complex applications
```

**Platform as a Service (Railway, Heroku, Render):**
```
Pros:
✓ Easy deployment
✓ Managed infrastructure
✓ Good balance of control/simplicity

Cons:
✗ Less flexible than containers
✗ Higher cost than raw infrastructure

Best for: Startups, small teams
```

### 2. CI/CD Pipeline

```yaml
# GitHub Actions Example
name: Deploy AI Application

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest tests/ --cov=app
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          docker build -t ai-app .
          docker push registry/ai-app:latest
          kubectl rollout restart deployment/ai-app
```

### 3. Blue-Green Deployment

```
Blue (current)          Green (new)
┌─────────────┐         ┌─────────────┐
│  Version 1  │         │  Version 2  │
│  (active)   │         │  (staging)  │
└─────────────┘         └─────────────┘
       ↓                        ↓
  Route traffic           Test thoroughly
       ↓                        ↓
       └──────────┬─────────────┘
                  ↓
           Switch traffic
                  ↓
       ┌─────────────┐
       │  Version 2  │
       │  (active)   │
       └─────────────┘

Benefits:
✓ Zero downtime
✓ Easy rollback
✓ Safe deployment
```

## Monitoring and Logging

### Key Metrics to Track

```python
from dataclasses import dataclass
from typing import Dict
import time

@dataclass
class AIMetrics:
    # Performance
    latency_p50: float
    latency_p95: float
    latency_p99: float
    
    # Quality
    avg_response_length: float
    error_rate: float
    fallback_rate: float
    
    # Usage
    requests_per_minute: float
    tokens_per_request: float
    cost_per_request: float
    
    # Business
    user_satisfaction: float
    completion_rate: float
```

### Logging Implementation

```python
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ai_app.log')
    ]
)

logger = logging.getLogger(__name__)

class AILogger:
    """Structured logging for AI applications"""
    
    @staticmethod
    def log_request(
        request_id: str,
        user_id: str,
        prompt: str,
        model: str
    ):
        """Log incoming request"""
        logger.info(json.dumps({
            'event': 'request',
            'request_id': request_id,
            'user_id': user_id,
            'prompt_length': len(prompt),
            'model': model,
            'timestamp': datetime.utcnow().isoformat()
        }))
    
    @staticmethod
    def log_response(
        request_id: str,
        response: str,
        tokens_used: int,
        latency_ms: float,
        cost: float
    ):
        """Log AI response"""
        logger.info(json.dumps({
            'event': 'response',
            'request_id': request_id,
            'response_length': len(response),
            'tokens_used': tokens_used,
            'latency_ms': latency_ms,
            'cost': cost,
            'timestamp': datetime.utcnow().isoformat()
        }))
    
    @staticmethod
    def log_error(
        request_id: str,
        error: str,
        error_type: str
    ):
        """Log error"""
        logger.error(json.dumps({
            'event': 'error',
            'request_id': request_id,
            'error': error,
            'error_type': error_type,
            'timestamp': datetime.utcnow().isoformat()
        }))

# Usage
AILogger.log_request(
    request_id="req-123",
    user_id="user-456",
    prompt="Write an email",
    model="gpt-4"
)
```

### Alerting

```python
class AlertManager:
    """Manage alerts for production issues"""
    
    def __init__(self, slack_webhook: str, pagerduty_key: str):
        self.slack_webhook = slack_webhook
        self.pagerduty_key = pagerduty_key
    
    def check_and_alert(self, metrics: AIMetrics):
        """Check metrics and send alerts"""
        alerts = []
        
        # High error rate
        if metrics.error_rate > 0.05:  # 5%
            alerts.append(f"High error rate: {metrics.error_rate:.2%}")
        
        # High latency
        if metrics.latency_p95 > 5000:  # 5 seconds
            alerts.append(f"High P95 latency: {metrics.latency_p95:.0f}ms")
        
        # High cost
        if metrics.cost_per_request > 0.10:  # $0.10
            alerts.append(f"High cost per request: ${metrics.cost_per_request:.4f}")
        
        # Send alerts
        for alert in alerts:
            self.send_slack_alert(f"⚠️ {alert}")
            self.trigger_pagerduty(alert)
    
    def send_slack_alert(self, message: str):
        """Send Slack notification"""
        import requests
        requests.post(self.slack_webhook, json={'text': message})
    
    def trigger_pagerduty(self, incident: str):
        """Trigger PagerDuty incident"""
        # Implementation depends on PagerDuty API
        pass
```

## Scaling Considerations

### Horizontal Scaling

```
Load Balancer
     ↓
┌────┼────┐
│    │    │
↓    ↓    ↓
[App] [App] [App]  ← Multiple instances
│    │    │
└────┼────┘
     ↓
[Database/Cache]

Benefits:
✓ Handle more traffic
✓ Redundancy
✓ Zero-downtime updates
```

### Caching Strategy

```python
import redis
from functools import wraps
import hashlib

class CacheManager:
    """Redis-based caching"""
    
    def __init__(self, redis_url: str):
        self.redis = redis.Redis.from_url(redis_url)
    
    def cache_response(self, ttl: int = 3600):
        """Decorator to cache AI responses"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key
                key_data = f"{func.__name__}:{args}:{kwargs}"
                cache_key = f"ai_response:{hashlib.md5(key_data.encode()).hexdigest()}"
                
                # Try cache
                cached = self.redis.get(cache_key)
                if cached:
                    return json.loads(cached)
                
                # Call function
                result = func(*args, **kwargs)
                
                # Store in cache
                self.redis.setex(
                    cache_key,
                    ttl,
                    json.dumps(result)
                )
                
                return result
            return wrapper
        return decorator

# Usage
cache = CacheManager("redis://localhost:6379")

@cache.cache_response(ttl=3600)
def generate_response(prompt: str, model: str) -> Dict:
    return call_ai_api(prompt, model)
```

### Database Optimization

```
Indexing:
✓ Index frequently queried fields
✓ Composite indexes for common queries
✓ Avoid over-indexing (slows writes)

Connection Pooling:
✓ Reuse connections
✓ Configure pool size based on load
✓ Monitor connection usage

Query Optimization:
✓ Use SELECT specific columns
✓ Avoid N+1 queries
✓ Use pagination for large results
```

## Code Example: Production Deployment Configuration

```yaml
# docker-compose.yml for local development
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/aidb
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
      - redis
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 2G

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=aidb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api

volumes:
  postgres_data:
  redis_data:
```

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-app
  template:
    metadata:
      labels:
        app: ai-app
    spec:
      containers:
      - name: ai-app
        image: registry/ai-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: database-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: openai-key
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Key Takeaways

- **Plan for reliability** with redundancy and monitoring
- **Secure everything** - APIs, data, access
- **Monitor continuously** - latency, errors, costs
- **Scale horizontally** for growth
- **Cache aggressively** to reduce costs
- **Automate deployments** with CI/CD
- **Alert proactively** before issues affect users

## Glossary

- **SLO:** Service Level Objective
- **CI/CD:** Continuous Integration/Continuous Deployment
- **Blue-Green:** Deployment strategy with two environments
- **Horizontal Scaling:** Adding more instances
- **Connection Pooling:** Reusing database connections

## Quiz Questions

**1. What uptime does 99.9% SLO represent?**

A) 3.65 days downtime/year
B) 8.76 hours downtime/year
C) 52.6 minutes downtime/year
D) 5.26 minutes downtime/year

**Correct Answer:** B

**Explanation:** 99.9% uptime equals approximately 8.76 hours of allowed downtime per year.

---

**2. What is the benefit of blue-green deployment?**

A) Cheaper infrastructure
B) Zero downtime deployments
C) Faster builds
D) Simpler code

**Correct Answer:** B

**Explanation:** Blue-green deployment allows switching traffic between versions instantly, enabling zero-downtime updates.

---

**3. What metric is MOST important for AI API monitoring?**

A) Number of deployments
B) Error rate and latency
C) Code coverage
D) Number of features

**Correct Answer:** B

**Explanation:** Error rate and latency directly impact user experience and should be closely monitored.

---

**4. How does caching help AI applications?**

A) Makes AI smarter
B) Reduces API costs and latency for repeated requests
C) Increases model accuracy
D) Reduces code complexity

**Correct Answer:** B

**Explanation:** Caching avoids redundant API calls, reducing both costs and response times.

---

**5. What is horizontal scaling?**

A) Making servers more powerful
B) Adding more server instances
C) Reducing server count
D) Scaling database only

**Correct Answer:** B

**Explanation:** Horizontal scaling adds more instances to handle increased load, vs. vertical scaling which makes individual servers more powerful.

---

## Further Reading

- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **Docker Best Practices**: https://docs.docker.com/develop/
- **Monitoring AI Systems** - Arize: https://arize.com/blog/

---

**Continue to Chapter 24** for ethics, safety, and responsible AI!
