# Chapter 22: Building with APIs

## Learning Objectives

By the end of this chapter, you will be able to:
- Compare major AI API providers
- Understand API pricing and limits
- Implement API integration patterns
- Handle errors and rate limits

## API Provider Comparison

### OpenAI API

**Models:**
```
GPT-4 Turbo:
- Input: $0.01 / 1K tokens
- Output: $0.03 / 1K tokens
- Context: 128K tokens
- Best for: Complex reasoning

GPT-4:
- Input: $0.03 / 1K tokens
- Output: $0.06 / 1K tokens
- Context: 8K tokens
- Best for: General purpose

GPT-3.5 Turbo:
- Input: $0.0005 / 1K tokens
- Output: $0.0015 / 1K tokens
- Context: 16K tokens
- Best for: Cost-effective tasks
```

**Rate Limits:**
```
Free tier: 3 RPM (requests per minute), 200 RPD (per day)
Pay-as-you-go: 500 RPM, 50K RPD
Enterprise: Custom limits
```

**Code Example:**
```python
from openai import OpenAI

client = OpenAI(api_key="your-key")

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### Anthropic API

**Models:**
```
Claude 3 Opus:
- Input: $15 / 1M tokens
- Output: $75 / 1M tokens
- Context: 200K tokens
- Best for: Complex tasks

Claude 3 Sonnet:
- Input: $3 / 1M tokens
- Output: $15 / 1M tokens
- Context: 200K tokens
- Best for: Balanced performance

Claude 3 Haiku:
- Input: $0.25 / 1M tokens
- Output: $1.25 / 1M tokens
- Context: 200K tokens
- Best for: Fast, cheap tasks
```

**Code Example:**
```python
import anthropic

client = anthropic.Client(api_key="your-key")

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.content[0].text)
```

### Google Vertex AI

**Models:**
```
Gemini Pro:
- Input: $0.00025 / 1K tokens
- Output: $0.0005 / 1K tokens
- Best for: Google Cloud users

PaLM 2:
- Input: $0.00025 / 1K tokens
- Output: $0.0005 / 1K tokens
- Best for: Text generation
```

**Code Example:**
```python
from google.cloud import aiplatform
from vertexai.language_models import TextGenerationModel

aiplatform.init(project="your-project")
model = TextGenerationModel.from_pretrained("text-bison")

response = model.predict("Hello!")
print(response.text)
```

### Azure OpenAI

**Same models as OpenAI** with Azure infrastructure:
```
GPT-4 Turbo: Same pricing as OpenAI
GPT-4: Same pricing as OpenAI
GPT-3.5 Turbo: Same pricing as OpenAI

Benefits:
- Azure integration
- Enterprise SLAs
- Data residency options
```

**Code Example:**
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://your-resource.openai.azure.com/",
    api_key="your-key",
    api_version="2024-02-15-preview"
)

response = client.chat.completions.create(
    model="your-deployment-name",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Pricing and Cost Optimization

### Cost Calculation

```python
def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Calculate API cost"""
    pricing = {
        'gpt-4-turbo': (0.01/1000, 0.03/1000),
        'gpt-4': (0.03/1000, 0.06/1000),
        'gpt-3.5-turbo': (0.0005/1000, 0.0015/1000),
        'claude-3-opus': (15/1000000, 75/1000000),
        'claude-3-sonnet': (3/1000000, 15/1000000),
        'claude-3-haiku': (0.25/1000000, 1.25/1000000),
    }
    
    input_price, output_price = pricing.get(model, (0, 0))
    return (input_tokens * input_price) + (output_tokens * output_price)

# Example
cost = calculate_cost('gpt-4-turbo', input_tokens=1000, output_tokens=500)
print(f"Cost: ${cost:.4f}")  # $0.025
```

### Cost Optimization Strategies

**1. Choose Right Model**
```
Use GPT-3.5/Claude Haiku for:
- Simple tasks
- High volume
- Cost-sensitive applications

Use GPT-4/Claude Opus for:
- Complex reasoning
- High-stakes decisions
- Quality-critical tasks
```

**2. Optimize Prompts**
```
Before: "I would like you to please write a very detailed and comprehensive explanation about machine learning..."
After: "Explain machine learning in detail."

Savings: 30-50% on input tokens
```

**3. Cache Responses**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_generate(prompt_hash: str) -> str:
    """Cache frequent responses"""
    if prompt_hash in cache:
        return cache[prompt_hash]
    response = call_api(get_prompt(prompt_hash))
    cache[prompt_hash] = response
    return response
```

**4. Use Streaming**
```
Benefits:
- Lower latency perception
- Can stop early if satisfied
- Better user experience
```

## API Integration Patterns

### 1. Retry with Exponential Backoff

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_with_retry(api_func, *args, **kwargs):
    """Call API with automatic retry"""
    return api_func(*args, **kwargs)

# Usage
response = call_with_retry(client.chat.completions.create, **params)
```

### 2. Rate Limit Handling

```python
import time
from datetime import datetime, timedelta

class RateLimiter:
    """Handle rate limits"""
    
    def __init__(self, rpm: int, rpd: int):
        self.rpm = rpm
        self.rpd = rpd
        self.minute_requests = []
        self.day_requests = []
    
    def wait_if_needed(self):
        """Wait if approaching rate limits"""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        day_ago = now - timedelta(days=1)
        
        # Clean old requests
        self.minute_requests = [t for t in self.minute_requests if t > minute_ago]
        self.day_requests = [t for t in self.day_requests if t > day_ago]
        
        # Check limits
        if len(self.minute_requests) >= self.rpm:
            sleep_time = 60 - (now - self.minute_requests[0]).seconds
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        if len(self.day_requests) >= self.rpd:
            raise Exception("Daily limit reached")
        
        # Record request
        self.minute_requests.append(now)
        self.day_requests.append(now)

# Usage
limiter = RateLimiter(rpm=500, rpd=50000)
limiter.wait_if_needed()
response = call_api()
```

### 3. Fallback Strategy

```python
def call_with_fallback(primary_model: str, fallback_model: str, prompt: str) -> str:
    """Try primary model, fall back if needed"""
    try:
        return call_api(model=primary_model, prompt=prompt)
    except RateLimitError:
        print(f"Rate limited on {primary_model}, falling back to {fallback_model}")
        return call_api(model=fallback_model, prompt=prompt)
    except Exception as e:
        print(f"Error: {e}, using fallback")
        return call_api(model=fallback_model, prompt=prompt)
```

### 4. Multi-Provider Setup

```python
class MultiProviderClient:
    """Use multiple API providers"""
    
    def __init__(self):
        self.openai = OpenAI(api_key="...")
        self.anthropic = anthropic.Client(api_key="...")
        self.providers = ['openai', 'anthropic']
        self.current_provider = 0
    
    def generate(self, prompt: str) -> str:
        """Generate with automatic provider switching"""
        for _ in range(len(self.providers)):
            provider = self.providers[self.current_provider]
            
            try:
                if provider == 'openai':
                    response = self.openai.chat.completions.create(...)
                else:
                    response = self.anthropic.messages.create(...)
                
                return response
            
            except Exception as e:
                print(f"{provider} failed: {e}")
                self.current_provider = (self.current_provider + 1) % len(self.providers)
        
        raise Exception("All providers failed")
```

## Error Handling

### Common Errors

```python
from openai import (
    RateLimitError,
    AuthenticationError,
    APIConnectionError,
    Timeout,
    APIError
)

def handle_api_call(prompt: str) -> str:
    """Robust API call with error handling"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    except RateLimitError:
        # Wait and retry
        time.sleep(60)
        return handle_api_call(prompt)
    
    except AuthenticationError:
        logger.error("Invalid API key")
        return "Authentication error. Please check your API key."
    
    except APIConnectionError:
        logger.error("Connection error")
        return "Connection error. Please try again."
    
    except Timeout:
        logger.error("Request timeout")
        return "Request timed out. Please try again."
    
    except APIError as e:
        logger.error(f"API error: {e}")
        return f"API error: {str(e)}"
```

## Code Example: Production API Client

```python
from openai import OpenAI, RateLimitError
from typing import Dict, Optional
import time
from dataclasses import dataclass

@dataclass
class APIConfig:
    api_key: str
    model: str = "gpt-4-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = 30
    max_retries: int = 3

class ProductionAPIClient:
    """Production-ready API client"""
    
    def __init__(self, config: APIConfig):
        self.config = config
        self.client = OpenAI(api_key=config.api_key)
        self.request_count = 0
        self.total_cost = 0.0
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict:
        """Generate with full error handling and tracking"""
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        for attempt in range(self.config.max_retries):
            try:
                start_time = time.time()
                
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    temperature=kwargs.get('temperature', self.config.temperature),
                    max_tokens=kwargs.get('max_tokens', self.config.max_tokens),
                    timeout=self.config.timeout
                )
                
                latency = time.time() - start_time
                
                # Track usage
                self.request_count += 1
                cost = self._calculate_cost(
                    response.usage.prompt_tokens,
                    response.usage.completion_tokens
                )
                self.total_cost += cost
                
                return {
                    'success': True,
                    'content': response.choices[0].message.content,
                    'usage': {
                        'prompt_tokens': response.usage.prompt_tokens,
                        'completion_tokens': response.usage.completion_tokens,
                        'total_tokens': response.usage.total_tokens
                    },
                    'latency_ms': latency * 1000,
                    'cost': cost
                }
            
            except RateLimitError:
                if attempt < self.config.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    time.sleep(wait_time)
                else:
                    return {
                        'success': False,
                        'error': 'Rate limit exceeded',
                        'retry_after': 60
                    }
            
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e)
                }
        
        return {'success': False, 'error': 'Max retries exceeded'}
    
    def _calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate API cost"""
        pricing = {
            'gpt-4-turbo': (0.01/1000, 0.03/1000),
            'gpt-4': (0.03/1000, 0.06/1000),
            'gpt-3.5-turbo': (0.0005/1000, 0.0015/1000),
        }
        
        input_price, output_price = pricing.get(self.config.model, (0, 0))
        return (prompt_tokens * input_price) + (completion_tokens * output_price)
    
    def get_usage_report(self) -> Dict:
        """Get usage statistics"""
        return {
            'total_requests': self.request_count,
            'total_cost': self.total_cost,
            'avg_cost_per_request': self.total_cost / self.request_count if self.request_count > 0 else 0
        }

# Usage
config = APIConfig(api_key="your-key", model="gpt-4-turbo")
client = ProductionAPIClient(config)

result = client.generate("Write a haiku about AI")
if result['success']:
    print(f"Response: {result['content']}")
    print(f"Cost: ${result['cost']:.4f}")
    print(f"Latency: {result['latency_ms']:.2f}ms")
else:
    print(f"Error: {result['error']}")

# Get usage report
report = client.get_usage_report()
print(f"Total requests: {report['total_requests']}")
print(f"Total cost: ${report['total_cost']:.2f}")
```

## Key Takeaways

- **Choose providers** based on cost, performance, and requirements
- **Implement retry logic** with exponential backoff
- **Handle rate limits** gracefully
- **Track usage and costs** for budgeting
- **Use fallbacks** for reliability
- **Cache responses** to reduce costs

## Glossary

- **RPM:** Requests Per Minute (rate limit)
- **RPD:** Requests Per Day (rate limit)
- **Exponential Backoff:** Increasing wait times between retries
- **Fallback:** Alternative when primary fails

## Quiz Questions

**1. Which model is MOST cost-effective for simple tasks?**

A) GPT-4
B) GPT-3.5 Turbo
C) Claude Opus
D) Any model costs the same

**Correct Answer:** B

**Explanation:** GPT-3.5 Turbo is significantly cheaper than GPT-4 while still handling simple tasks well.

---

**2. What is the best practice for handling rate limits?**

A) Stop the application
B) Retry immediately
C) Retry with exponential backoff
D) Switch to a different API key

**Correct Answer:** C

**Explanation:** Exponential backoff (waiting progressively longer) is the standard approach for rate limit handling.

---

**3. How can you reduce API costs?**

A) Use longer prompts
B) Cache frequent responses
C) Always use the most expensive model
D) Make more requests

**Correct Answer:** B

**Explanation:** Caching avoids redundant API calls for the same inputs, reducing costs significantly.

---

**4. What should you do if all API providers fail?**

A) Crash the application
B) Return a graceful error message
C) Keep retrying forever
D) Ignore the error

**Correct Answer:** B

**Explanation:** Always handle failures gracefully with clear error messages to users.

---

**5. Which factor is LEAST important when choosing an API provider?**

A) Pricing
B) Rate limits
C) Model capabilities
D) Company logo

**Correct Answer:** D

**Explanation:** The company logo has no impact on your application's performance or costs.

---

## Further Reading

- **OpenAI Pricing**: https://openai.com/pricing
- **Anthropic Pricing**: https://www.anthropic.com/pricing
- **API Best Practices** - Stripe: https://stripe.com/docs/api

---

**Continue to Chapter 23** to learn about deployment and production!
