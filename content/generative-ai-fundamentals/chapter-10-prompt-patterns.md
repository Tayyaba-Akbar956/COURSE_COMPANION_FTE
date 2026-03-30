# Chapter 10: Prompt Design Patterns and Techniques

## Learning Objectives

By the end of this chapter, you will be able to:
- Master common prompt patterns for various tasks
- Apply few-shot prompting techniques effectively
- Use chain-of-thought prompting for complex reasoning
- Implement role-based prompting for specialized outputs

## Introduction

Now that you understand prompt engineering basics, it's time to build your toolkit of proven patterns and techniques. This chapter covers the most effective prompt designs used by professionals.

Think of these patterns as templates you can adapt for your specific needs.

## Zero-Shot Prompting

**Zero-shot prompting** means asking the model to perform a task without providing examples.

### When to Use Zero-Shot

- ✅ Simple, straightforward tasks
- ✅ Well-known formats (emails, summaries)
- ✅ When you want creative, varied outputs
- ✅ Testing model capabilities

### Examples

**Classification:**
```
Classify the sentiment of this text: "This product exceeded my expectations!"
Options: Positive, Neutral, Negative
```

**Generation:**
```
Write a haiku about artificial intelligence.
```

**Transformation:**
```
Translate to Spanish: "Good morning, how can I help you today?"
```

**Limitations:**
- May not follow complex formats precisely
- Output can be inconsistent
- May miss nuanced requirements

## Few-Shot Prompting

**Few-shot prompting** provides examples to demonstrate the desired pattern.

### Why Few-Shot Works

Examples show the model:
- Expected format
- Level of detail
- Style and tone
- Edge case handling

### Effective Few-Shot Design

**Structure:**
```
[Task description]
[Example 1 input] → [Example 1 output]
[Example 2 input] → [Example 2 output]
[Example 3 input] → [Example 3 output]
[New input to process]
```

**Example: Sentiment Analysis**
```
Classify sentiment as Positive, Neutral, or Negative:

Text: "I love this product!" → Positive
Text: "It's okay, nothing special" → Neutral
Text: "Terrible experience, never again" → Negative
Text: "Could be better but works fine" →
```

**Example: Data Extraction**
```
Extract the company name and CEO from each text:

Text: "Apple Inc., led by CEO Tim Cook, announced..."
Company: Apple Inc.
CEO: Tim Cook

Text: "Microsoft Corporation's CEO Satya Nadella stated..."
Company: Microsoft Corporation
CEO: Satya Nadella

Text: "Google, under Sundar Pichai's leadership, revealed..."
Company: Google
CEO: Sundar Pichai

Text: "Amazon's chief executive Andy Jassy announced..."
Company:
CEO:
```

### Best Practices for Few-Shot

1. **Use 2-5 examples** (diminishing returns after that)
2. **Make examples diverse** (cover different cases)
3. **Ensure examples are correct** (garbage in, garbage out)
4. **Match example format to expected output**
5. **Order examples logically** (simple to complex)

## Chain-of-Thought Prompting

**Chain-of-thought (CoT)** prompting asks the model to show its reasoning step-by-step.

### Why Chain-of-Thought Works

- Forces systematic thinking
- Makes errors easier to spot
- Improves accuracy on complex tasks
- Provides transparency

### Basic CoT Pattern

**Without CoT:**
```
Q: A bat and ball cost $1.10. The bat costs $1 more than the ball.
How much does the ball cost?

A: $0.10 (Wrong!)
```

**With CoT:**
```
Q: A bat and ball cost $1.10. The bat costs $1 more than the ball.
How much does the ball cost?

Let's think step by step:
1. Let x = cost of ball
2. Then x + $1 = cost of bat
3. Total: x + (x + $1) = $1.10
4. 2x + $1 = $1.10
5. 2x = $0.10
6. x = $0.05

A: $0.05 (Correct!)
```

### CoT Triggers

Simple phrases that activate reasoning:

```
"Let's think step by step"
"Work through this systematically"
"Show your reasoning"
"Break this down"
"Explain your thinking"
```

### Complex Problem Example

```
You're evaluating whether to build a feature. Use this framework:

Problem: Users are dropping off during onboarding

Step 1: Define the problem clearly
Step 2: Identify potential causes
Step 3: Propose solutions for each cause
Step 4: Evaluate solutions by impact and effort
Step 5: Recommend the best option

Think through each step before concluding.
```

## Role-Based Prompting

**Role prompting** assigns a persona or expertise level to the model.

### Why Role Prompting Works

- Sets appropriate expertise level
- Guides tone and style
- Provides context for decisions
- Constrains the response space

### Common Roles

| Role | Use Case |
|------|----------|
| **Expert** | "You are a senior software engineer..." |
| **Teacher** | "You are a high school physics teacher..." |
| **Consultant** | "You are a business consultant..." |
| **Critic** | "You are a code reviewer..." |
| **Assistant** | "You are a helpful assistant..." |
| **Character** | "You are Sherlock Holmes..." |

### Role Prompt Structure

```
You are [ROLE] with [EXPERTISE/BACKGROUND].

Your task is to [TASK].

Approach this as [ROLE] would, using [SPECIFIC METHODS/FRAMEWORKS].

Consider [RELEVANT FACTORS].

Output should be [FORMAT/STYLE].
```

### Examples

**Technical Expert:**
```
You are a senior Python developer with 10 years of experience in web development.

Review this code for:
- Security vulnerabilities
- Performance issues
- Best practices violations

Provide specific, actionable feedback with code examples.
```

**Teacher:**
```
You are a patient middle school science teacher.

Explain how photosynthesis works to a 12-year-old student.

Use:
- Simple language (no jargon)
- Relatable analogies
- One diagram description

Check for understanding with 2 questions at the end.
```

**Business Consultant:**
```
You are a McKinsey business consultant specializing in digital transformation.

Analyze this company's situation:
[Company description]

Provide recommendations using the MECE framework:
- Mutually Exclusive
- Collectively Exhaustive

Structure your response as an executive presentation.
```

## Comparison Pattern

Use this pattern to evaluate options systematically.

### Structure

```
Compare [OPTION A] and [OPTION B] based on:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

For each criterion:
- Evaluate Option A
- Evaluate Option B
- Declare a winner

Conclude with an overall recommendation for [SPECIFIC USE CASE].
```

### Example

```
Compare React and Vue.js for building a dashboard application:

Criteria:
1. Learning curve
2. Performance for data-heavy UIs
3. Ecosystem and library support
4. Hiring availability

For each criterion, provide:
- React's strengths and weaknesses
- Vue's strengths and weaknesses
- Which is better for this use case

Conclude with a recommendation for a startup with 3 developers.
```

## Template Pattern

Create reusable prompt structures with variables.

### Basic Template

```
Template:
"Write a [CONTENT_TYPE] about [TOPIC] for [AUDIENCE].

Key points to cover:
- [POINT_1]
- [POINT_2]
- [POINT_3]

Tone: [TONE]
Length: [LENGTH] words
Format: [FORMAT]"

Usage:
CONTENT_TYPE = blog post introduction
TOPIC = machine learning basics
AUDIENCE = business executives
POINT_1 = What is ML
POINT_2 = Business applications
POINT_3 = Getting started
TONE = Professional but accessible
LENGTH = 200
FORMAT = Paragraphs with subheadings
```

### Advanced Template with Conditionals

```
You are reviewing code submitted by a [EXPERIENCE_LEVEL] developer.

{% if EXPERIENCE_LEVEL == "junior" %}
Provide encouraging feedback. Focus on:
- What they did well
- 1-2 key improvements
- Learning resources

{% elif EXPERIENCE_LEVEL == "senior" %}
Provide direct, detailed feedback. Focus on:
- Architecture decisions
- Performance optimizations
- Edge cases

{% endif %}

Code to review:
```{LANGUAGE}
{CODE}
```
```

## Iterative Refinement Pattern

Use multiple passes to improve outputs.

### Structure

```
Pass 1: Generate initial draft
Pass 2: Critique the draft
Pass 3: Revise based on critique
Pass 4: Polish and finalize
```

### Example

```
PASS 1 - Draft:
"Write a first draft of a product description for wireless earbuds."

PASS 2 - Critique:
"Critique this draft for:
- Clarity of value proposition
- Emotional appeal
- Call to action strength
- Specific improvements needed"

PASS 3 - Revise:
"Revise the product description addressing all critique points.
Make it more compelling and specific."

PASS 4 - Polish:
"Polish the revised description:
- Tighten prose
- Ensure consistent tone
- Verify word count under 150 words"
```

## Code Example: Prompt Pattern Library

```python
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class PromptPattern:
    name: str
    description: str
    template: str
    
    def render(self, **kwargs) -> str:
        return self.template.format(**kwargs)


class PromptLibrary:
    """Collection of reusable prompt patterns"""
    
    def __init__(self):
        self.patterns = {}
        self._load_patterns()
    
    def _load_patterns(self):
        """Load common prompt patterns"""
        
        # Few-shot classification
        self.patterns['few_shot_classify'] = PromptPattern(
            name="Few-Shot Classification",
            description="Classify with examples",
            template="""Classify {task_type} as {options}:

{examples}

{input}
Classification: """
        )
        
        # Chain of thought
        self.patterns['chain_of_thought'] = PromptPattern(
            name="Chain of Thought",
            description="Step-by-step reasoning",
            template="""{problem}

Let's think step by step:
1. 
"""
        )
        
        # Role-based
        self.patterns['role_expert'] = PromptPattern(
            name="Role-Based Expert",
            description="Expert persona prompting",
            template="""You are a {role} with {experience} years of experience.

Your task: {task}

Approach this using {framework} methodology.

Provide your answer in {format} format.
"""
        )
        
        # Comparison
        self.patterns['comparison'] = PromptPattern(
            name="Comparison",
            description="Compare multiple options",
            template="""Compare {options} for {use_case}.

Evaluation criteria:
{criteria}

For each option, evaluate against all criteria.
Then recommend the best option with justification.
"""
        )
        
        # Template
        self.patterns['template'] = PromptPattern(
            name="Template",
            description="Reusable template",
            template="""Write a {content_type} about {topic}.

Audience: {audience}
Key points:
{key_points}

Tone: {tone}
Length: {length} words
Format: {format}
"""
        )
    
    def get(self, name: str) -> PromptPattern:
        """Get a pattern by name"""
        if name not in self.patterns:
            raise ValueError(f"Pattern '{name}' not found")
        return self.patterns[name]
    
    def list_patterns(self) -> List[str]:
        """List available patterns"""
        return list(self.patterns.keys())


# Usage
library = PromptLibrary()

# Use few-shot pattern
few_shot = library.get('few_shot_classify')
prompt = few_shot.render(
    task_type="sentiment",
    options="Positive, Neutral, Negative",
    examples="""
"I love this!" → Positive
"It's okay" → Neutral
"I hate it" → Negative
""",
    input="This is amazing!"
)

# Use chain of thought
cot = library.get('chain_of_thought')
prompt = cot.render(
    problem="If 5 machines take 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?"
)

# Use role-based pattern
role = library.get('role_expert')
prompt = role.render(
    role="security engineer",
    experience="15",
    task="Review this authentication code",
    framework="OWASP",
    format="bullet points with code fixes"
)
```

## Key Takeaways

- **Zero-shot** works for simple, well-defined tasks
- **Few-shot** improves consistency and format adherence
- **Chain-of-thought** enhances reasoning on complex problems
- **Role-based** sets appropriate expertise and tone
- **Comparison** patterns enable systematic evaluation
- **Templates** provide reusable structures
- **Iterative refinement** produces higher quality outputs
- **Combine patterns** for complex tasks

## Glossary

- **Zero-Shot Prompting:** Asking without examples
- **Few-Shot Prompting:** Providing examples in the prompt
- **Chain-of-Thought:** Prompting for step-by-step reasoning
- **Role Prompting:** Assigning a persona to the model
- **Template:** Reusable prompt structure
- **Iterative Refinement:** Multi-pass improvement process
- **MECE:** Mutually Exclusive, Collectively Exhaustive (consulting framework)

## Quiz Questions

**1. When is few-shot prompting MOST beneficial?**

A) For simple tasks the model already knows well
B) When you need consistent format or style
C) When you want creative, varied outputs
D) For yes/no questions

**Correct Answer:** B

**Explanation:** Few-shot prompting is most beneficial when you need the model to follow a specific format, style, or pattern consistently.

---

**2. What is the primary benefit of chain-of-thought prompting?**

A) It makes responses shorter
B) It improves accuracy on complex reasoning tasks
C) It reduces computational cost
D) It makes the model faster

**Correct Answer:** B

**Explanation:** Chain-of-thought prompting forces systematic reasoning, which significantly improves accuracy on complex problems.

---

**3. Which is the BEST example of role prompting?**

A) "Write an email"
B) "You are a senior marketing director. Write a persuasive email to potential clients."
C) "Write a good email"
D) "Email writing"

**Correct Answer:** B

**Explanation:** Role prompting assigns a specific persona with expertise, which guides the tone, depth, and approach of the response.

---

**4. How many examples should you typically provide in few-shot prompting?**

A) 1
B) 2-5
C) 10-20
D) 50+

**Correct Answer:** B

**Explanation:** 2-5 examples typically provide enough pattern information without diminishing returns. More examples rarely add value.

---

**5. What phrase triggers chain-of-thought reasoning?**

A) "Answer quickly"
B) "Let's think step by step"
C) "Give me the final answer"
D) "No explanation needed"

**Correct Answer:** B

**Explanation:** "Let's think step by step" is a well-known trigger that activates the model's reasoning capabilities.

---

**6. What is the main advantage of template patterns?**

A) They're shorter to write
B) They're reusable and consistent
C) They produce more creative outputs
D) They're easier to understand

**Correct Answer:** B

**Explanation:** Templates provide reusable structures that ensure consistency across multiple uses while allowing variable substitution.

---

## Further Reading

- **Prompt Engineering Guide** - Few-shot and CoT: https://github.com/dair-ai/Prompt-Engineering-Guide
- **Chain-of-Thought Paper** - Wei et al.: https://arxiv.org/abs/2201.11903
- **Learn Prompting** - Pattern library: https://learnprompting.org/
- **Prompt Design Patterns** - Comprehensive collection: https://prompts.ai/

---

**Continue building your skills!** Move on to Chapter 11 for advanced prompting strategies!
