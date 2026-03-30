# Chapter 9: Introduction to Prompt Engineering

## Learning Objectives

By the end of this chapter, you will be able to:
- Define prompt engineering and explain its importance
- Understand basic prompting principles and best practices
- Learn common prompt patterns and when to use them
- Write effective prompts for various tasks

## Introduction

You have a powerful LLM at your fingertips. But how do you communicate with it effectively? The answer lies in **prompt engineering**—the art and science of crafting inputs that elicit the best outputs from AI models.

In this chapter, you'll learn the fundamentals of prompt engineering. Whether you're building applications or just using ChatGPT, these skills will make you more effective.

## What is Prompt Engineering?

**Prompt Engineering:** The practice of designing and optimizing inputs (prompts) to guide AI models toward desired outputs.

### Why Does Prompting Matter?

The same model can produce vastly different results based on how you ask:

```
Prompt 1 (Vague):
"Write about AI"

Output 1:
"AI is a broad field. It has many applications..."
(Generic, unhelpful)


Prompt 2 (Specific):
"Write a 200-word introduction to generative AI for high school students.
Include one real-world example and explain why it matters."

Output 2:
"Generative AI is a type of artificial intelligence that can create new content..."
(Focused, appropriate, useful)
```

**Key Insight:** Better prompts = Better outputs

### The Prompt Engineering Mindset

Think of prompt engineering as **programming with natural language**:

```
Traditional Programming:
- Write code in Python/Java
- Compiler executes code
- Output is deterministic

Prompt Engineering:
- Write instructions in English
- LLM "executes" instructions
- Output is probabilistic (may vary)
```

## Basic Prompting Principles

Follow these principles for more effective prompts:

### 1. Be Specific and Clear

**Vague Prompt:**
```
"Help me with marketing"
```

**Specific Prompt:**
```
"Write 5 email subject lines for a product launch campaign.
Product: New project management software
Target audience: Small business owners
Tone: Professional but friendly"
```

**Why It Works:**
- Clear task definition
- Specific context provided
- Audience and tone specified

### 2. Provide Context

**Without Context:**
```
"Summarize this"
```

**With Context:**
```
"Summarize the following article for a busy executive who needs
the key points in under 2 minutes. Focus on actionable insights."
```

**Why It Works:**
- Explains the purpose
- Defines the audience
- Sets expectations

### 3. Specify the Format

**Unspecified:**
```
"List marketing channels"
```

**Specified:**
```
"List 10 marketing channels in a table with columns:
- Channel name
- Best for (audience type)
- Estimated cost (low/medium/high)
- Time to see results"
```

**Why It Works:**
- Clear output structure
- Easy to use results
- Saves post-processing time

### 4. Use Examples (Few-Shot Prompting)

**Zero-Shot (No Examples):**
```
"Convert these to formal language:
'Hey, what's up?'"
```

**Few-Shot (With Examples):**
```
"Convert informal to formal language:

Informal: 'Gonna be late'
Formal: 'I will be arriving late'

Informal: 'That's awesome!'
Formal: 'That is excellent!'

Informal: 'Hey, what's up?'
Formal:"
```

**Why It Works:**
- Shows the pattern clearly
- Reduces ambiguity
- Improves consistency

### 5. Assign a Role

**Without Role:**
```
"Explain quantum computing"
```

**With Role:**
```
"You are a high school physics teacher. Explain quantum computing
to a 15-year-old student who is curious but has no physics background."
```

**Why It Works:**
- Sets appropriate level
- Defines communication style
- Guides the approach

## Common Prompt Patterns

Here are essential patterns you'll use frequently:

### Pattern 1: Instruction Pattern

**Structure:**
```
[Task description]
[Context/background]
[Output format]
```

**Example:**
```
"Write a product description for our new wireless headphones.

Product features:
- 30-hour battery life
- Active noise cancellation
- Comfortable over-ear design

Format: 150 words, enthusiastic tone, highlight benefits not just features"
```

### Pattern 2: Question-Answer Pattern

**Structure:**
```
[Question]
[Context for answering]
[Format for answer]
```

**Example:**
```
"What are the main differences between GPT-4 and Claude?

Focus on:
- Capabilities
- Pricing
- Best use cases

Present as a comparison table."
```

### Pattern 3: Template Pattern

**Structure:**
```
"Fill in this template:

Dear [Recipient],

I am writing to [purpose]. [Main message].

Thank you for [action].

Best regards,
[Name]"
```

**Example:**
```
"Fill in this template for a job application follow-up:

Dear [Recipient],
I am writing to [purpose]. [Main message].
Thank you for [action].
Best regards,
[Name]

Context: Following up on software engineer interview last week"
```

### Pattern 4: Comparison Pattern

**Structure:**
```
"Compare [A] and [B] based on:
- Criterion 1
- Criterion 2
- Criterion 3

Conclude with a recommendation for [specific use case]"
```

**Example:**
```
"Compare MySQL and PostgreSQL based on:
- Performance
- Scalability
- Ease of use
- Community support

Recommend for a startup building a web application."
```

### Pattern 5: Step-by-Step Pattern

**Structure:**
```
"Complete this task step by step:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Show your work for each step."
```

**Example:**
```
"Debug this Python function step by step:

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

1. Identify potential issues
2. Explain each issue
3. Provide corrected code"
```

## Common Mistakes to Avoid

### Mistake 1: Being Too Vague

**Bad:**
```
"Write something about climate change"
```

**Good:**
```
"Write a 300-word blog post introduction about how climate change
affects agriculture in California. Include statistics if available."
```

### Mistake 2: Overloading the Prompt

**Bad:**
```
"Write a blog post about AI, include history, current applications,
future predictions, ethical considerations, interview an expert,
add code examples, make it funny, keep it under 500 words,
optimize for SEO, add images..."
```

**Good:**
```
"Write a 500-word blog post introduction about AI applications in healthcare.
Focus on diagnostic tools. Tone: Professional but accessible."
```

### Mistake 3: Not Specifying Constraints

**Bad:**
```
"Generate ideas for a startup"
```

**Good:**
```
"Generate 10 startup ideas for the education technology space.
Each idea should:
- Target K-12 students
- Use AI in some way
- Be feasible for a small team
- Have clear monetization potential"
```

### Mistake 4: Ignoring the Audience

**Bad:**
```
"Explain how transformers work"
```

**Good:**
```
"Explain how transformer neural networks work to a software engineer
who knows basic machine learning but hasn't studied NLP.
Use analogies where helpful. Avoid heavy math."
```

## Code Example: Prompt Template System

```python
from typing import Dict, Any

class PromptTemplate:
    """Reusable prompt template with variable substitution"""
    
    def __init__(self, template: str):
        self.template = template
    
    def render(self, **kwargs) -> str:
        """Render template with provided variables"""
        return self.template.format(**kwargs)


# Define templates
EMAIL_TEMPLATE = PromptTemplate("""
Write a professional email with the following parameters:

Purpose: {purpose}
Recipient: {recipient}
Sender: {sender}
Key points to include:
{key_points}

Tone: {tone}
Length: {length} words
""")

CODE_REVIEW_TEMPLATE = PromptTemplate("""
Review the following code for:
- Bugs and errors
- Performance issues
- Code style and best practices
- Security concerns

Code:
```{language}
{code}
```

Provide specific suggestions with corrected code examples.
""")

# Use templates
email_prompt = EMAIL_TEMPLATE.render(
    purpose="Request a meeting to discuss project timeline",
    recipient="Project Manager",
    sender="Development Team Lead",
    key_points="- Current sprint behind schedule\n- Need to discuss resource allocation\n- Propose meeting next week",
    tone="Professional but collaborative",
    length="150"
)

code_review_prompt = CODE_REVIEW_TEMPLATE.render(
    language="python",
    code="""
def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
"""
)

print(email_prompt)
print(code_review_prompt)
```

## Best Practices Summary

### DO ✅
- Be specific and clear about what you want
- Provide relevant context and background
- Specify the desired output format
- Use examples to illustrate patterns
- Assign roles when appropriate
- Break complex tasks into steps
- Iterate and refine based on results

### DON'T ❌
- Be vague or ambiguous
- Overload with too many requirements
- Assume the model knows your context
- Expect perfect results on first try
- Forget to specify constraints
- Ignore the target audience

## Key Takeaways

- **Prompt engineering** is designing inputs to get better outputs from LLMs
- **Be specific**—clear instructions produce better results
- **Provide context** so the model understands the situation
- **Specify format** to get usable outputs
- **Use examples** (few-shot prompting) for consistency
- **Assign roles** to guide tone and approach
- **Avoid common mistakes** like vagueness and overloading
- **Iterate**—refine prompts based on results

## Glossary

- **Prompt:** The input text you give to an LLM
- **Prompt Engineering:** The practice of designing effective prompts
- **Zero-Shot Prompting:** Asking without examples
- **Few-Shot Prompting:** Providing examples in the prompt
- **Role Prompting:** Assigning a persona or role to the model
- **Template:** Reusable prompt structure with variables
- **Context:** Background information provided to the model
- **Constraints:** Limitations and requirements for the output

## Quiz Questions

**1. What is prompt engineering?**

A) Building prompts for nuclear weapons
B) The practice of designing inputs to guide AI models toward desired outputs
C) Writing code to automate prompt generation
D) Engineering software for AI systems

**Correct Answer:** B

**Explanation:** Prompt engineering is the practice of crafting effective inputs (prompts) to get better outputs from AI models.

---

**2. Which prompt is MOST likely to produce useful results?**

A) "Write about marketing"
B) "Write 5 email subject lines for a product launch, targeting small business owners"
C) "Do marketing stuff"
D) "Help me"

**Correct Answer:** B

**Explanation:** Specific prompts with clear tasks, context, and audience produce the most useful results.

---

**3. What is few-shot prompting?**

A) Using the model a few times
B) Providing a few examples in the prompt to illustrate the desired pattern
C) Prompting with only a few words
D) Testing a few different prompts

**Correct Answer:** B

**Explanation:** Few-shot prompting involves providing examples in the prompt to show the model what pattern to follow.

---

**4. Why should you assign a role in prompts?**

A) To make the AI feel important
B) To set the appropriate level, tone, and approach for the response
C) To limit what the AI can say
D) It doesn't serve any purpose

**Correct Answer:** B

**Explanation:** Role assignment (e.g., "You are a high school teacher") guides the model to use appropriate language, depth, and style.

---

**5. What is a common mistake in prompt engineering?**

A) Being too specific
B) Providing too much context
C) Being vague and ambiguous
D) Using examples

**Correct Answer:** C

**Explanation:** Vagueness leads to generic, unhelpful outputs. Specific, clear prompts produce better results.

---

## Further Reading

- **Prompt Engineering Guide** - DAIR.AI: https://github.com/dair-ai/Prompt-Engineering-Guide
- **Learn Prompting** - Comprehensive course: https://learnprompting.org/
- **OpenAI Prompt Engineering Best Practices**: https://platform.openai.com/docs/guides/prompt-engineering
- **Prompt Engineering Institute**: https://www.promptengineering.org/

---

**Ready to practice?** Continue to Chapter 10 to learn advanced prompt design patterns and techniques!
