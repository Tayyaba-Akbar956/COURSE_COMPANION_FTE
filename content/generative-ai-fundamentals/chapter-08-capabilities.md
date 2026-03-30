# Chapter 8: LLM Capabilities and Limitations

## Learning Objectives

By the end of this chapter, you will be able to:
- Identify what LLMs do well and where they excel
- Understand common failure modes and limitations
- Recognize hallucination and strategies to mitigate it
- Set appropriate expectations for LLM use in applications

## Introduction

LLMs are remarkably capable—but they're not magic. Understanding what they can and cannot do is essential for building effective applications and avoiding costly mistakes.

In this chapter, we'll explore LLM capabilities and limitations with honesty and precision. You'll learn when to trust LLM outputs, when to verify, and when to use alternative approaches.

## What LLMs Do Well

LLMs excel at tasks involving language understanding and generation:

### 1. Text Generation

**Strengths:**
- ✅ Writing coherent, fluent prose
- ✅ Matching tone and style
- ✅ Generating creative content
- ✅ Maintaining context over long passages

**Examples:**
```
✓ Blog posts and articles
✓ Marketing copy
✓ Creative writing (stories, poems)
✓ Email drafts
✓ Social media content
```

**Quality:** Near-human for most general purposes

### 2. Question Answering

**Strengths:**
- ✅ Answering factual questions (with caveats)
- ✅ Explaining concepts clearly
- ✅ Providing multiple perspectives
- ✅ Adapting explanation to audience level

**Examples:**
```
User: "Explain quantum computing like I'm 10"
LLM: "Imagine a coin that can be both heads AND tails at the same time..."

User: "What's the difference between DNA and RNA?"
LLM: "DNA and RNA are both genetic materials, but DNA is like the master blueprint..."
```

**Caveat:** May hallucinate specific facts—verify important claims

### 3. Summarization

**Strengths:**
- ✅ Condensing long documents
- ✅ Extracting key points
- ✅ Creating executive summaries
- ✅ Multi-document synthesis

**Examples:**
```
Input: 10-page research paper
Output: 3-paragraph summary with key findings

Input: 50 customer reviews
Output: Bullet points of common themes
```

**Quality:** Generally excellent for well-structured text

### 4. Translation

**Strengths:**
- ✅ High-quality translation for major languages
- ✅ Preserving meaning and tone
- ✅ Handling idioms and colloquialisms
- ✅ Context-aware translation

**Supported Languages:** 100+ (quality varies)

**Quality:**
- Major languages (Spanish, French, Chinese): Near-professional
- Low-resource languages: Variable quality

### 5. Code Generation

**Strengths:**
- ✅ Writing common functions and algorithms
- ✅ Completing code from partial implementations
- ✅ Explaining what code does
- ✅ Translating between languages
- ✅ Debugging assistance

**Examples:**
```python
# Prompt: "Write a function to find duplicates in a list"

# LLM generates:
def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

**Quality:** Good for common patterns; requires review for correctness

### 6. Text Classification

**Strengths:**
- ✅ Sentiment analysis
- ✅ Topic categorization
- ✅ Intent detection
- ✅ Zero-shot classification (no training needed)

**Examples:**
```
Text: "This product exceeded my expectations!"
LLM: Sentiment = Positive (confidence: 95%)

Text: "The delivery was delayed by 3 days"
LLM: Topic = Shipping/Delivery
```

**Quality:** Competitive with specialized models for many tasks

### 7. Information Extraction

**Strengths:**
- ✅ Named entity recognition
- ✅ Relationship extraction
- ✅ Structured data from unstructured text
- ✅ Form filling from documents

**Examples:**
```
Input: "John Smith works at Acme Corp as CEO"
Output: {
  "person": "John Smith",
  "company": "Acme Corp",
  "role": "CEO"
}
```

**Quality:** Very good for clear, well-formatted text

### 8. Reasoning (with Limitations)

**Strengths:**
- ✅ Logical deduction (simple to moderate)
- ✅ Mathematical reasoning (basic to intermediate)
- ✅ Step-by-step problem solving
- ✅ Analogical reasoning

**Examples:**
```
Prompt: "If all A are B, and all B are C, are all A are C?"
LLM: "Yes, this is a valid syllogism..."

Prompt: "John is taller than Mary. Mary is taller than Sue. Who is shortest?"
LLM: "Sue is the shortest."
```

**Limitation:** Performance degrades with complex, multi-step reasoning

## Common Failure Modes

Understanding where LLMs fail is as important as knowing where they succeed:

### 1. Hallucination

**Definition:** Generating false information that sounds plausible.

**Examples:**
```
❌ "The Eiffel Tower was completed in 1892." (Actually 1889)

❌ "According to a 2023 study by Harvard researchers..." (No such study)

❌ "Python's print() function returns the printed value." (Returns None)
```

**Why It Happens:**
- Model predicts plausible text, not factual truth
- Training data may contain errors
- No mechanism to verify claims
- Pressure to produce confident-sounding answers

**Mitigation Strategies:**
```
✓ Fact-check important claims
✓ Use retrieval-augmented generation (RAG)
✓ Ask model to cite sources
✓ Use model for drafting, not final facts
✓ Implement verification pipelines
```

### 2. Reasoning Errors

**Definition:** Making logical mistakes, especially on complex problems.

**Examples:**
```
Prompt: "A bat and ball cost $1.10. The bat costs $1 more than the ball. 
How much does the ball cost?"

Wrong Answer: "The ball costs $0.10" (Common intuitive error)
Correct Answer: "The ball costs $0.05" (Ball=$0.05, Bat=$1.05, Total=$1.10)
```

**Why It Happens:**
- Models don't truly "reason" like humans
- Pattern matching vs. logical deduction
- No internal world model
- Susceptible to cognitive biases in training data

**Mitigation:**
```
✓ Break problems into steps
✓ Ask for chain-of-thought reasoning
✓ Verify with specialized tools (calculators, solvers)
✓ Don't rely on LLMs for critical calculations
```

### 3. Context Window Limitations

**Definition:** Forgetting or misusing information outside the attention window.

**Problem:**
```
Model with 4K token context:
- Can only "see" ~3,000 words at a time
- Information beyond that is inaccessible
- May lose track in long conversations
```

**Symptoms:**
- Contradicting earlier statements
- Forgetting user preferences
- Missing information from earlier in document

**Mitigation:**
```
✓ Use models with larger context windows
✓ Implement retrieval systems
✓ Summarize and compress conversation history
✓ Chunk long documents
```

### 4. Bias and Fairness Issues

**Definition:** Perpetuating or amplifying societal biases present in training data.

**Examples:**
```
Prompt: "The doctor said..."
Biased Output: "...he would perform the surgery" (assumes doctor is male)

Prompt: "The nurse said..."
Biased Output: "...she would prepare the patient" (assumes nurse is female)
```

**Why It Happens:**
- Training data reflects historical biases
- Model learns statistical associations
- No inherent understanding of fairness

**Mitigation:**
```
✓ Use debiased models when available
✓ Implement output filtering
✓ Provide diverse examples in prompts
✓ Monitor for biased outputs
✓ Human review for sensitive applications
```

### 5. Knowledge Cutoffs

**Definition:** Not knowing about events after training data cutoff.

**Example:**
```
Model trained on data until September 2021:

User: "Who won the 2022 World Cup?"
LLM: "I don't have information about events after my training cutoff in September 2021."
```

**Why It Happens:**
- Models are trained on static datasets
- Cannot access real-time information
- Knowledge is "frozen" at training time

**Mitigation:**
```
✓ Use models with recent training data
✓ Implement retrieval from current sources
✓ Be transparent about cutoff dates
✓ Combine with search tools
```

### 6. Prompt Sensitivity

**Definition:** Small changes in prompting lead to very different outputs.

**Example:**
```
Prompt 1: "Write a short essay about climate change"
Output: Balanced, informative essay

Prompt 2: "Write a short essay about the climate change hoax"
Output: May generate misleading content (follows premise)
```

**Why It Happens:**
- Model tries to satisfy the prompt
- No strong internal fact-checking
- Susceptible to framing effects

**Mitigation:**
```
✓ Careful prompt design
✓ Test prompts with variations
✓ Add guardrails and constraints
✓ Review outputs before publishing
```

### 7. Lack of True Understanding

**Definition:** Appearing to understand without genuine comprehension.

**Example:**
```
User: "If I put my laundry in the oven, will it get clean?"
LLM: "No, ovens are designed for cooking, not cleaning clothes..."

(Seems like understanding, but really just pattern matching from text)
```

**Why It Matters:**
- Can fail on novel situations
- No common sense reasoning
- Cannot truly verify claims against reality

## Setting Appropriate Expectations

### What to Expect from LLMs

```
✅ Good for:
- First drafts and brainstorming
- Explaining concepts
- Summarizing information
- Generating variations
- Answering general questions
- Code assistance
- Creative tasks

⚠️ Use with caution for:
- Factual claims (verify)
- Mathematical calculations (double-check)
- Legal/medical advice (consult experts)
- Sensitive decisions (human oversight)

❌ Not suitable for:
- High-stakes decisions without review
- Real-time information (without retrieval)
- Tasks requiring true understanding
- Replacing human expertise
```

### Production Readiness Checklist

Before deploying LLM applications:

```
□ Fact-checking pipeline for factual claims
□ Human review for sensitive outputs
□ Error handling for model failures
□ Rate limiting and cost monitoring
□ Output filtering for safety
□ Logging and monitoring
□ User feedback mechanism
□ Fallback to human agents
□ Clear user communication about AI use
```

## Code Example: Detecting Hallucination

```python
from openai import OpenAI
import requests

client = OpenAI()

def fact_check_response(claim: str) -> dict:
    """
    Simple fact-checking using search.
    In production, use proper fact-checking APIs.
    """
    
    # Search for the claim
    search_query = f"fact check: {claim}"
    search_results = search_web(search_query)
    
    # Ask LLM to evaluate
    prompt = f"""
    Claim: "{claim}"
    
    Search Results:
    {search_results}
    
    Is this claim supported by evidence?
    Respond with: SUPPORTED, CONTRADICTED, or UNVERIFIED
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    verdict = response.choices[0].message.content.strip()
    
    return {
        "claim": claim,
        "verdict": verdict,
        "sources": search_results
    }

def generate_with_verification(prompt: str) -> dict:
    """Generate response and fact-check claims"""
    
    # Generate initial response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    generated_text = response.choices[0].message.content
    
    # Extract factual claims (simplified)
    claims = extract_claims(generated_text)
    
    # Fact-check each claim
    fact_checks = []
    for claim in claims[:5]:  # Check up to 5 claims
        fact_check = fact_check_response(claim)
        fact_checks.append(fact_check)
    
    return {
        "response": generated_text,
        "fact_checks": fact_checks,
        "confidence": calculate_confidence(fact_checks)
    }

# Usage
result = generate_with_verification(
    "Who won the Nobel Prize in Physics in 2023?"
)

print(f"Response: {result['response']}")
print(f"Confidence: {result['confidence']}")
```

## Best Practices for Working with LLMs

### Prompt Design

```
✓ Be specific and clear
✓ Provide context when needed
✓ Use examples (few-shot prompting)
✓ Specify format requirements
✓ Set constraints (length, tone, style)
✓ Ask for reasoning (chain-of-thought)
```

### Output Validation

```
✓ Fact-check important claims
✓ Verify code before running
✓ Review for bias and fairness
✓ Check for consistency
✓ Test edge cases
```

### Risk Mitigation

```
✓ Implement content filters
✓ Log all interactions
✓ Provide user feedback mechanism
✓ Have human escalation path
✓ Be transparent about AI use
✓ Regular auditing for issues
```

## Key Takeaways

- **LLMs excel at** text generation, summarization, translation, and code assistance
- **Hallucination is real**—always verify important factual claims
- **Reasoning is limited**—don't rely on LLMs for complex calculations
- **Knowledge has cutoffs**—models don't know recent events without retrieval
- **Bias exists**—monitor and filter outputs for sensitive applications
- **Set appropriate expectations**—LLMs are powerful tools, not omniscient oracles
- **Human oversight is essential** for high-stakes applications

## Glossary

- **Hallucination:** Generating false but plausible-sounding information
- **Knowledge Cutoff:** Date after which model has no knowledge
- **Context Window:** Maximum text length model can process at once
- **Bias:** Systematic unfairness in outputs reflecting training data biases
- **Chain-of-Thought:** Prompting technique asking model to show reasoning
- **Zero-Shot:** Performing task without examples
- **Retrieval-Augmented Generation (RAG):** Combining LLM with external knowledge
- **Fact-Checking:** Verifying claims against reliable sources

## Quiz Questions

**1. Which task is LLMs BEST suited for?**

A) Real-time stock trading decisions
B) Writing first drafts of blog posts
C) Diagnosing medical conditions
D) Calculating complex mathematics

**Correct Answer:** B

**Explanation:** LLMs excel at text generation tasks like writing drafts. They should not be used for medical diagnosis, financial trading, or complex calculations without expert oversight.

---

**2. What is hallucination in the context of LLMs?**

A) When the model generates images instead of text
B) When the model generates false information that sounds plausible
C) When the model refuses to answer
D) When the model takes too long to respond

**Correct Answer:** B

**Explanation:** Hallucination refers to LLMs confidently stating false information that sounds reasonable but is incorrect or made up.

---

**3. Why do LLMs have knowledge cutoffs?**

A) Because they forget information over time
B) Because they are trained on static datasets up to a certain date
C) Because of memory limitations
D) Because of licensing restrictions

**Correct Answer:** B

**Explanation:** LLMs are trained on fixed datasets collected up to a specific date. They cannot know about events after that cutoff without external retrieval.

---

**4. Which mitigation strategy is MOST effective for reducing hallucination?**

A) Using a larger model
B) Asking the model to be more confident
C) Using retrieval-augmented generation (RAG)
D) Providing more examples in the prompt

**Correct Answer:** C

**Explanation:** RAG grounds the model's responses in retrieved factual content, significantly reducing hallucination compared to relying solely on the model's internal knowledge.

---

**5. What is a key limitation of LLM reasoning?**

A) LLMs can only reason in English
B) LLMs don't truly reason—they pattern match
C) LLMs can only do simple addition
D) LLMs refuse to do reasoning tasks

**Correct Answer:** B

**Explanation:** LLMs don't have genuine reasoning capabilities; they recognize patterns from training data. This limits their reliability on novel or complex reasoning tasks.

---

**6. When should you use human review with LLM outputs?**

A) Never—LLMs are always accurate
B) Only for creative writing
C) For high-stakes decisions and sensitive applications
D) Only when the model requests it

**Correct Answer:** C

**Explanation:** Human oversight is essential for high-stakes applications (medical, legal, financial) and sensitive content to catch errors, bias, and inappropriate outputs.

---

## Further Reading

- **"Survey of Hallucination in Natural Language Generation"** - Comprehensive review: https://arxiv.org/abs/2209.06034
- **Anthropic's Constitutional AI** - Safety and alignment: https://arxiv.org/abs/2212.08073
- **Google's Responsible AI Practices** - Guidelines: https://ai.google/responsibilities/
- **Partnership on AI** - Best practices and research: https://partnershiponai.org/

---

**🎉 Congratulations! You've completed Module 2!**

You now understand:
- ✅ What LLMs are and how they work
- ✅ Transformer architecture and self-attention
- ✅ How LLMs are trained and fine-tuned
- ✅ Capabilities and limitations of LLMs

**Next Steps:**
- Continue to Module 3 to master Prompt Engineering
- Take the Module 2 quiz to test your knowledge
- Consider upgrading to Premium for full course access!
