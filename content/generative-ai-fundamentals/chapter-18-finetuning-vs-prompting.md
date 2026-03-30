# Chapter 18: When to Fine-tune vs. Prompt Engineering

## Learning Objectives

By the end of this chapter, you will be able to:
- Compare fine-tuning and prompt engineering approaches
- Understand trade-offs of each approach
- Make informed decisions on which approach to use
- Evaluate cost-benefit analysis for each method

## Decision Framework

### Quick Decision Matrix

| Factor | Choose Prompt Engineering | Choose Fine-tuning |
|--------|--------------------------|-------------------|
| **Budget** | Low ($0-$100) | Medium-High ($100+) |
| **Timeline** | Immediate | Days to weeks |
| **Data Available** | None needed | 100+ examples |
| **Performance Need** | Good enough | Optimal |
| **Task Complexity** | Simple-Moderate | Complex/Specialized |
| **Updates Needed** | Frequent | Infrequent |
| **Customization** | Basic | Deep |

## Detailed Comparison

### Prompt Engineering

**What It Is:**
Crafting effective inputs to guide model behavior without changing model weights.

**Best For:**
```
✓ Quick prototyping
✓ Tasks the base model already does well
✓ Frequently changing requirements
✓ Limited or no training data
✓ Tight budgets
✓ Multiple different tasks
```

**Limitations:**
```
✗ May not achieve highest accuracy
✗ Inconsistent on complex tasks
✗ Requires prompt maintenance
✗ Limited customization depth
✗ Token overhead for few-shot examples
```

**Cost Structure:**
```
- Development time: Hours to days
- Infrastructure: $0 (use existing APIs)
- Per-query cost: Standard API rates
- Maintenance: Ongoing prompt optimization
```

### Fine-tuning

**What It Is:**
Training model on domain-specific data to adapt behavior.

**Best For:**
```
✓ Domain-specific language
✓ Consistent style/tone requirements
✓ Specialized tasks
✓ High accuracy requirements
✓ Stable, well-defined tasks
✓ Sufficient training data
```

**Limitations:**
```
✗ Requires training data
✗ Upfront time investment
✗ Compute costs
✗ Less flexible to changes
✗ Risk of catastrophic forgetting
```

**Cost Structure:**
```
- Development: Days to weeks
- Training: $10-$10,000+ (one-time)
- Per-query cost: Same or lower (if self-hosted)
- Maintenance: Retraining for updates
```

## Head-to-Head Comparison

### Accuracy

```
Simple Tasks:
├── Prompt Engineering: 80-90%
└── Fine-tuning: 85-92%
    └── Marginal gain, may not justify cost

Complex/Specialized Tasks:
├── Prompt Engineering: 60-75%
└── Fine-tuning: 85-95%
    └── Significant gain, often justifies cost
```

### Consistency

```
Prompt Engineering:
- Output varies with prompt wording
- Few-shot helps but adds tokens
- May drift over time

Fine-tuning:
- Consistent behavior across queries
- Built-in understanding
- Stable over time
```

### Flexibility

```
Prompt Engineering:
✓ Change behavior instantly
✓ Easy A/B testing
✓ Adapt to new tasks immediately

Fine-tuning:
✗ Requires retraining for changes
✗ Expensive to iterate
✗ New task = new fine-tuning
```

### Cost Analysis

**Example: Customer Support Bot**

```
Prompt Engineering Approach:
├── Setup: 2 days engineering time ($2,000)
├── Training: $0
├── Per-query: $0.002 (API cost)
└── Monthly (10K queries): $20

Fine-tuning Approach (LoRA):
├── Setup: 1 week ($5,000)
├── Training: $500 (one-time)
├── Per-query: $0.002 (API) or $0.0005 (self-hosted)
└── Monthly (10K queries): $20 (API) or $5 (self-hosted)

Break-even: ~25 months for self-hosting cost savings
```

## Hybrid Approaches

### Best of Both Worlds

**1. Fine-tune + Prompt**
```
Fine-tune for:
- Domain knowledge
- Consistent style

Prompt for:
- Task-specific instructions
- Dynamic context
```

**2. RAG + Fine-tune**
```
RAG provides:
- Current information
- Specific documents

Fine-tuning provides:
- Domain language
- Task expertise
```

**3. Ensemble**
```
Use prompt engineering for:
- Simple queries
- Edge cases

Use fine-tuned model for:
- Core use cases
- High-stakes decisions
```

## Decision Trees

### Technical Decision Tree

```
Start
├── Do you have training data?
│   ├── No → Use Prompt Engineering
│   └── Yes (100+ examples) → Continue
│
├── Is base model accuracy acceptable?
│   ├── Yes (>85%) → Use Prompt Engineering
│   └── No → Continue
│
├── Do you need current/real-time info?
│   ├── Yes → Use RAG (not fine-tuning)
│   └── No → Continue
│
├── Is task stable (won't change often)?
│   ├── No → Use Prompt Engineering
│   └── Yes → Continue
│
├── Do you have budget ($500+)?
│   ├── No → Use Prompt Engineering
│   └── Yes → Fine-tuning may be worthwhile
```

### Business Decision Tree

```
Start
├── What's your timeline?
│   ├── < 1 week → Prompt Engineering
│   └── 2+ weeks → Continue
│
├── What's your budget?
│   ├── < $500 → Prompt Engineering
│   ├── $500-$5,000 → LoRA Fine-tuning
│   └── $5,000+ → Full Fine-tuning possible
│
├── How critical is accuracy?
│   ├── Nice to have → Prompt Engineering
│   └── Business critical → Fine-tuning
│
├── Will requirements change?
│   ├── Frequently → Prompt Engineering
│   └── Rarely → Fine-tuning
```

## Code Example: Comparison Framework

```python
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ApproachComparison:
    prompt_engineering_score: int
    fine_tuning_score: int
    recommendation: str
    reasoning: List[str]

def compare_approaches(
    num_training_examples: int,
    budget_usd: int,
    timeline_days: int,
    accuracy_requirement: float,
    task_stability: str,  # "stable" or "changing"
    domain_specificity: str  # "general" or "specialized"
) -> ApproachComparison:
    """Compare prompt engineering vs fine-tuning"""
    
    reasoning = []
    pe_score = 0
    ft_score = 0
    
    # Data availability
    if num_training_examples < 100:
        pe_score += 3
        reasoning.append("Insufficient training data for fine-tuning")
    elif num_training_examples < 1000:
        pe_score += 1
        ft_score += 2
        reasoning.append("Limited data favors light fine-tuning")
    else:
        ft_score += 3
        reasoning.append("Sufficient data for fine-tuning")
    
    # Budget
    if budget_usd < 500:
        pe_score += 3
        reasoning.append("Low budget favors prompt engineering")
    elif budget_usd < 5000:
        ft_score += 2
        reasoning.append("Medium budget allows LoRA fine-tuning")
    else:
        ft_score += 3
        reasoning.append("High budget enables full fine-tuning")
    
    # Timeline
    if timeline_days < 7:
        pe_score += 3
        reasoning.append("Short timeline favors prompt engineering")
    else:
        ft_score += 2
        reasoning.append("Timeline allows fine-tuning")
    
    # Accuracy requirement
    if accuracy_requirement < 0.85:
        pe_score += 2
        reasoning.append("Moderate accuracy achievable with prompting")
    else:
        ft_score += 3
        reasoning.append("High accuracy may require fine-tuning")
    
    # Task stability
    if task_stability == "changing":
        pe_score += 3
        reasoning.append("Changing requirements favor prompt engineering")
    else:
        ft_score += 2
        reasoning.append("Stable task justifies fine-tuning investment")
    
    # Domain specificity
    if domain_specificity == "general":
        pe_score += 2
        reasoning.append("General domain works well with prompting")
    else:
        ft_score += 3
        reasoning.append("Specialized domain benefits from fine-tuning")
    
    # Recommendation
    if pe_score > ft_score:
        recommendation = "Prompt Engineering"
    elif ft_score > pe_score:
        recommendation = "Fine-tuning"
    else:
        recommendation = "Either (consider hybrid approach)"
    
    return ApproachComparison(
        prompt_engineering_score=pe_score,
        fine_tuning_score=ft_score,
        recommendation=recommendation,
        reasoning=reasoning
    )

# Usage
comparison = compare_approaches(
    num_training_examples=5000,
    budget_usd=2000,
    timeline_days=14,
    accuracy_requirement=0.90,
    task_stability="stable",
    domain_specificity="specialized"
)

print(f"Recommendation: {comparison.recommendation}")
print(f"Scores - PE: {comparison.prompt_engineering_score}, FT: {comparison.fine_tuning_score}")
print("\nReasoning:")
for r in comparison.reasoning:
    print(f"- {r}")
```

## Real-World Examples

### Example 1: Startup MVP

**Scenario:**
- Building AI customer support
- 2 weeks to launch
- $1,000 budget
- No training data yet

**Decision:** Prompt Engineering
```
Why:
✓ Fast deployment
✓ No data needed
✓ Low cost
✓ Can iterate based on user feedback

Plan:
1. Build with prompts
2. Collect conversation data
3. Fine-tune later if needed
```

### Example 2: Legal Document Analysis

**Scenario:**
- Law firm document review
- 50,000 labeled documents
- Need 95%+ accuracy
- $50,000 budget

**Decision:** Fine-tuning
```
Why:
✓ Specialized domain language
✓ High accuracy requirement
✓ Abundant training data
✓ Budget allows

Plan:
1. Fine-tune on legal documents
2. Validate on held-out set
3. Deploy with human review
```

### Example 3: E-commerce Product Descriptions

**Scenario:**
- Generate product descriptions
- Brand voice consistency needed
- 500 example descriptions
- Weekly product updates

**Decision:** Hybrid (Fine-tune + Prompt)
```
Why:
✓ Fine-tune for brand voice
✓ Prompt for product specifics
✓ Best of both approaches

Plan:
1. Fine-tune on brand examples
2. Use prompts for product details
3. Maintain consistency + flexibility
```

## Key Takeaways

- **Prompt Engineering** for speed, flexibility, low cost
- **Fine-tuning** for accuracy, specialization, consistency
- **Evaluate** data, budget, timeline, requirements
- **Hybrid approaches** often provide best results
- **Start simple** (prompting) and escalate if needed
- **Consider total cost** not just upfront investment

## Glossary

- **Decision Framework:** Structured approach to choosing methods
- **Break-even Point:** When fine-tuning cost savings offset investment
- **Hybrid Approach:** Combining multiple techniques
- **Total Cost of Ownership:** All costs over solution lifetime

## Quiz Questions

**1. When is prompt engineering the BETTER choice?**

A) When you have 10,000 training examples
B) When you need to deploy in 2 days with no data
C) When you need 95% accuracy on specialized tasks
D) When you have $50,000 budget

**Correct Answer:** B

**Explanation:** Prompt engineering is ideal for rapid deployment with no training data.

---

**2. What is a key advantage of fine-tuning over prompt engineering?**

A) Faster deployment
B) Lower cost
C) Better consistency and domain expertise
D) More flexibility

**Correct Answer:** C

**Explanation:** Fine-tuning provides consistent behavior and domain-specific knowledge that prompting can't match.

---

**3. When should you use a hybrid approach?**

A) Never, pick one or the other
B) When you need both domain expertise and flexibility
C) When you have no budget
D) When you need immediate deployment

**Correct Answer:** B

**Explanation:** Hybrid approaches combine fine-tuning (for domain expertise) with prompting (for flexibility).

---

**4. What's the MINIMUM recommended training examples for considering fine-tuning?**

A) 10
B) 100
C) 1,000
D) 10,000

**Correct Answer:** B

**Explanation:** While 1,000+ is better, LoRA fine-tuning can work with as few as 100 examples.

---

**5. Which factor MOST strongly suggests prompt engineering?**

A) High accuracy requirements
B) Specialized domain
C) Frequently changing requirements
D) Large budget

**Correct Answer:** C

**Explanation:** Frequently changing requirements favor prompt engineering's flexibility over fine-tuning's fixed nature.

---

## Further Reading

- **Prompt Engineering vs Fine-tuning** - Weights & Biases: https://wandb.ai/authors/llm-reports/reports/Prompt-Engineering-vs-Fine-Tuning
- **When to Fine-tune** - Hugging Face: https://huggingface.co/blog/fine-tuning
- **Cost Analysis** - Mosaic ML: https://www.mosaicml.com/blog/llm-fine-tuning

---

**Continue to Chapter 19** to learn specific fine-tuning methods and techniques!
