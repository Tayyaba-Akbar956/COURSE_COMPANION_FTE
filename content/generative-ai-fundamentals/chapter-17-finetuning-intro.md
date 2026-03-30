# Chapter 17: Introduction to Fine-tuning

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand what fine-tuning is and when to use it
- Identify appropriate use cases for fine-tuning
- Compare different fine-tuning approaches
- Evaluate fine-tuning requirements and costs

## What is Fine-tuning?

**Fine-tuning:** The process of adapting a pre-trained language model to specific tasks or domains by training it on specialized data.

### Analogy: Medical Training

```
Base Model (Pre-training):
└── Medical school graduate
    ├── Knows general medicine
    ├── Understands human anatomy
    ├── Can diagnose common conditions
    └── Trained on broad medical knowledge

Fine-tuned Model:
└── Specialist (e.g., Cardiologist)
    ├── All general knowledge intact
    ├── Deep expertise in cardiology
    ├── Specialized diagnostic skills
    └── Trained on domain-specific cases
```

### Why Fine-tune?

**Base LLMs are generalists:**
- Good at many tasks
- Jack of all trades, master of none
- May not excel at specialized domains

**Fine-tuned LLMs are specialists:**
- Excellent at specific tasks
- Domain-appropriate language
- Consistent behavior and style

## When to Fine-tune

### Good Use Cases ✅

**1. Domain-Specific Language**
```
Legal:
Base LLM: "The contract says you can't do that."
Fine-tuned: "Section 12.3(b) prohibits such action pursuant to..."

Medical:
Base LLM: "Take this medicine twice a day."
Fine-tuned: "Administer 500mg BID with meals, monitor for hepatotoxicity."
```

**2. Consistent Style/Tone**
```
Brand Voice:
- Always friendly but professional
- Specific terminology
- Consistent formatting
- Company-specific phrases
```

**3. Specialized Tasks**
```
- Code generation for specific frameworks
- Customer support for specific products
- Document classification in specific domains
- Sentiment analysis for industry-specific language
```

**4. Improved Performance**
```
When base model achieves < 80% accuracy on your task
Fine-tuning can often push to 90%+
```

### Poor Use Cases ❌

**1. One-Off Tasks**
```
Don't fine-tune for:
- Single document processing
- Occasional queries
- Tasks solvable with good prompting
```

**2. Rapidly Changing Information**
```
Don't fine-tune for:
- Current events
- Frequently updated policies
- Real-time data

Use RAG instead.
```

**3. Limited Data**
```
Don't fine-tune with:
- Less than 100 examples
- Poor quality examples
- Unrepresentative data
```

## Fine-tuning Approaches

### 1. Full Fine-tuning

**What:** Update all model parameters.

```
┌─────────────────────────────────────────┐
│         Full Fine-tuning                │
├─────────────────────────────────────────┤
│                                         │
│  Pre-trained Model (all layers frozen)  │
│              ↓ unfreeze                 │
│  Pre-trained Model (all layers trainable)│
│              ↓ train                    │
│  Fine-tuned Model                       │
│                                         │
└─────────────────────────────────────────┘
```

**Pros:**
- Maximum adaptation to domain
- Best potential performance

**Cons:**
- Computationally expensive
- Risk of catastrophic forgetting
- Large storage requirements

**Best For:**
- Major domain shifts
- Sufficient data (10,000+ examples)
- Adequate compute budget

### 2. Parameter-Efficient Fine-tuning (PEFT)

**What:** Update only a small subset of parameters.

**Main Approaches:**

#### LoRA (Low-Rank Adaptation)
```
Original: Update all weights (W)
LoRA: Update small matrices (A, B) where W' = W + BA

Benefits:
- 1000x fewer parameters
- Same performance as full fine-tuning
- Easy to swap adapters
```

#### Adapters
```
Insert small neural networks between layers
Train only adapters, freeze main model

Benefits:
- Modular (swap adapters)
- Efficient storage
- Fast training
```

#### Prefix Tuning
```
Add trainable vectors to input
Keep model frozen

Benefits:
- Minimal parameters
- Fast adaptation
```

**Pros:**
- Much cheaper than full fine-tuning
- Less catastrophic forgetting
- Multiple adapters for different tasks

**Cons:**
- Slightly lower performance than full fine-tuning
- More complex setup

**Best For:**
- Most production use cases
- Limited compute budget
- Multiple domain adaptations

### 3. Instruction Tuning

**What:** Fine-tune on instruction-following examples.

```
Example Format:
{
  "instruction": "Summarize this article",
  "input": "Article text here...",
  "output": "Summary text here..."
}
```

**Benefits:**
- Better at following instructions
- More helpful responses
- Improved task completion

**Best For:**
- Chatbots and assistants
- Task-oriented applications
- Improving general helpfulness

## Fine-tuning Requirements

### Data Requirements

| Approach | Minimum Examples | Recommended | Optimal |
|----------|-----------------|-------------|---------|
| **Full Fine-tuning** | 1,000 | 10,000+ | 100,000+ |
| **LoRA/PEFT** | 100 | 1,000+ | 10,000+ |
| **Instruction Tuning** | 500 | 5,000+ | 50,000+ |

**Data Quality Matters:**
```
✓ Diverse examples covering edge cases
✓ Correct, high-quality outputs
✓ Consistent formatting
✓ Representative of real use

✗ Noisy or incorrect labels
✗ Inconsistent formatting
✗ Biased or unrepresentative
✗ Too similar (low diversity)
```

### Compute Requirements

| Model Size | Full Fine-tuning | LoRA |
|------------|-----------------|------|
| **7B** | 40GB GPU, $100s | 24GB GPU, $10s |
| **13B** | 80GB GPU, $1,000s | 40GB GPU, $100s |
| **70B** | Multi-GPU, $10,000s | 80GB GPU, $1,000s |

**Cloud Options:**
- Google Colab (free/cheap for small models)
- AWS SageMaker
- Azure ML
- RunPod, Lambda Labs (cost-effective)

### Time Requirements

```
Small models (7B) with LoRA:
- Training: 1-4 hours
- Evaluation: 1-2 hours
- Total: Same day

Large models (70B) with LoRA:
- Training: 1-3 days
- Evaluation: 1 day
- Total: Few days

Full fine-tuning:
- Add 5-10x to above estimates
```

## Fine-tuning Process Overview

```
┌─────────────────────────────────────────────────────────┐
│              FINE-TUNING PIPELINE                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Data Collection                                     │
│     └── Gather domain-specific examples                 │
│                                                         │
│  2. Data Preparation                                    │
│     └── Clean, format, split train/test/val             │
│                                                         │
│  3. Model Selection                                     │
│     └── Choose base model and fine-tuning method        │
│                                                         │
│  4. Training                                            │
│     └── Fine-tune on training data                      │
│                                                         │
│  5. Evaluation                                          │
│     └── Test on held-out data                           │
│                                                         │
│  6. Deployment                                          │
│     └── Deploy fine-tuned model                         │
│                                                         │
│  7. Monitoring                                          │
│     └── Track performance in production                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Code Example: Fine-tuning Decision Framework

```python
from dataclasses import dataclass
from typing import Dict

@dataclass
class FineTuningDecision:
    use_fine_tuning: bool
    approach: str
    reasoning: str
    estimated_cost: str
    estimated_time: str

def evaluate_fine_tuning_need(
    task_description: str,
    num_examples: int,
    budget: str,  # "low", "medium", "high"
    performance_requirement: float,
    base_model_accuracy: float
) -> FineTuningDecision:
    """Evaluate whether fine-tuning is appropriate"""
    
    # Check if fine-tuning is needed
    if base_model_accuracy >= performance_requirement:
        return FineTuningDecision(
            use_fine_tuning=False,
            approach="N/A",
            reasoning="Base model already meets requirements",
            estimated_cost="$0",
            estimated_time="N/A"
        )
    
    if num_examples < 50:
        return FineTuningDecision(
            use_fine_tuning=False,
            approach="N/A",
            reasoning="Insufficient data. Use prompting or collect more data.",
            estimated_cost="$0",
            estimated_time="N/A"
        )
    
    # Determine approach
    if budget == "low":
        approach = "LoRA/PEFT"
        cost = "$10-$100"
        time = "1-4 hours"
    elif budget == "medium":
        approach = "LoRA/PEFT or Full (small model)"
        cost = "$100-$1,000"
        time = "4-24 hours"
    else:  # high
        approach = "Full fine-tuning or LoRA (large model)"
        cost = "$1,000-$10,000+"
        time = "1-7 days"
    
    return FineTuningDecision(
        use_fine_tuning=True,
        approach=approach,
        reasoning=f"Base model ({base_model_accuracy:.0%}) below target ({performance_requirement:.0%}). Fine-tuning recommended.",
        estimated_cost=cost,
        estimated_time=time
    )

# Usage
decision = evaluate_fine_tuning_need(
    task_description="Legal document classification",
    num_examples=5000,
    budget="medium",
    performance_requirement=0.90,
    base_model_accuracy=0.75
)

print(f"Use Fine-tuning: {decision.use_fine_tuning}")
print(f"Approach: {decision.approach}")
print(f"Reasoning: {decision.reasoning}")
print(f"Estimated Cost: {decision.estimated_cost}")
print(f"Estimated Time: {decision.estimated_time}")
```

## Key Takeaways

- **Fine-tuning adapts** general models to specific domains
- **Best for** domain language, consistent style, specialized tasks
- **Not for** rapidly changing info or one-off tasks
- **Full fine-tuning** updates all parameters (expensive)
- **PEFT/LoRA** updates few parameters (cost-effective)
- **Data requirements** range from 100 to 100,000+ examples
- **Evaluate carefully** before committing to fine-tuning

## Glossary

- **Fine-tuning:** Adapting pre-trained models to specific tasks
- **Catastrophic Forgetting:** Losing general capabilities during fine-tuning
- **PEFT:** Parameter-Efficient Fine-Tuning
- **LoRA:** Low-Rank Adaptation (PEFT method)
- **Adapters:** Small trainable modules inserted into model
- **Instruction Tuning:** Fine-tuning on instruction-following examples

## Quiz Questions

**1. What is the primary purpose of fine-tuning?**

A) To make models larger
B) To adapt general models to specific domains or tasks
C) To reduce model size
D) To make models faster

**Correct Answer:** B

**Explanation:** Fine-tuning adapts pre-trained models to perform better on specific tasks or domains.

---

**2. When should you NOT fine-tune?**

A) When you need domain-specific language
B) When you have 10,000 examples
C) When you need current, rapidly changing information
D) When you need consistent style

**Correct Answer:** C

**Explanation:** For rapidly changing information, use RAG instead. Fine-tuning is static once trained.

---

**3. What is LoRA?**

A) A type of full fine-tuning
B) A parameter-efficient fine-tuning method
C) A data collection technique
D) A model evaluation metric

**Correct Answer:** B

**Explanation:** LoRA (Low-Rank Adaptation) is a PEFT method that updates only small matrices, reducing parameters by 1000x.

---

**4. What is the MINIMUM recommended examples for LoRA fine-tuning?**

A) 10
B) 100
C) 1,000
D) 10,000

**Correct Answer:** B

**Explanation:** LoRA can work with as few as 100 examples, though 1,000+ is recommended for better results.

---

**5. What is catastrophic forgetting?**

A) When the model forgets training data
B) When fine-tuning causes loss of general capabilities
C) When the model becomes too slow
D) When training takes too long

**Correct Answer:** B

**Explanation:** Catastrophic forgetting occurs when fine-tuning causes the model to lose capabilities it had before fine-tuning.

---

## Further Reading

- **LoRA Paper**: https://arxiv.org/abs/2106.09685
- **Hugging Face Fine-tuning Guide**: https://huggingface.co/docs/transformers/training
- **PEFT Library**: https://huggingface.co/docs/peft
- **Fine-tuning Best Practices**: https://magazine.sebastianraschka.com/p/practical-recommendations-for-fine-tuning

---

**Continue to Chapter 18** to learn when to fine-tune vs. use prompt engineering!
