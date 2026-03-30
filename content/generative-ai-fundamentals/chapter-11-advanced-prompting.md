# Chapter 11: Advanced Prompting Strategies

## Learning Objectives

By the end of this chapter, you will be able to:
- Apply tree of thoughts for complex problem solving
- Implement retrieval-augmented prompting
- Design effective multi-turn conversations
- Decompose complex tasks into manageable prompts

## Tree of Thoughts Prompting

**Tree of Thoughts (ToT)** extends chain-of-thought by exploring multiple reasoning paths.

### How ToT Works

```
Problem
├── Approach 1
│   ├── Step 1a → Evaluate
│   └── Step 1b → Evaluate
├── Approach 2
│   ├── Step 2a → Evaluate
│   └── Step 2b → Evaluate
└── Select best path → Solution
```

### ToT Prompt Structure

```
Problem: {complex_problem}

Generate 3 different approaches to solve this.

For each approach:
1. Outline the steps
2. Identify potential issues
3. Evaluate feasibility (1-10)
4. Estimate resources needed

After evaluating all approaches:
- Select the best one
- Explain why it's superior
- Provide detailed implementation steps
```

### Example: Product Strategy

```
Problem: Should our startup build a mobile app or focus on web?

Generate 3 perspectives:
1. Mobile-first approach
2. Web-first approach  
3. Hybrid approach

For each, evaluate:
- Market reach
- Development cost
- User experience
- Maintenance burden
- Time to market

Recommend the best approach for a B2B SaaS startup with 5 developers.
```

## Retrieval-Augmented Prompting

**Retrieval-Augmented Generation (RAG)** combines LLMs with external knowledge sources.

### Why Use RAG?

- Access to current information
- Domain-specific knowledge
- Reduced hallucination
- Citable sources

### RAG Prompt Pattern

```
Context from knowledge base:
{retrieved_documents}

Based ONLY on the context above, answer:
{question}

If the answer isn't in the context, say "I don't have information about that in the provided documents."

Cite specific sections when possible.
```

### Example: Company Policy Q&A

```
Context:
[Document 1: Employee Handbook Section 3.2]
"PTO Policy: Full-time employees accrue 15 days of paid time off annually. Accrual begins on the first day of employment. PTO must be approved by your manager at least 2 weeks in advance."

[Document 2: Benefits Guide]
"Health insurance coverage begins on the 1st of the month following 30 days of employment."

Question: "When does my health insurance start and how much PTO do I get?"

Answer based on the context above:
```

## Multi-Turn Conversation Design

Effective multi-turn conversations maintain context and coherence.

### Conversation State Management

```
Turn 1: User asks about Python
Turn 2: User asks "What about JavaScript?" (implicit: compared to Python)
Turn 3: User asks "Which is easier?" (implicit: Python vs JavaScript)
```

### Best Practices

**1. Explicit Context Carrying**
```
System: "You are helping a beginner learn programming.
Previous topics discussed: Python basics, variables, loops.
Current question relates to these topics."
```

**2. Summarization for Long Conversations**
```
"Based on our conversation so far:
- You want to build a web scraper
- You're using Python
- You've tried BeautifulSoup but encountered errors
- Now asking about alternatives

Given this context, here's my recommendation..."
```

**3. Clarification When Ambiguous**
```
User: "Can it handle large files?"

Good response: "To clarify, are you asking about:
A) The web scraper we discussed?
B) Python in general?
C) A specific library?"
```

## Task Decomposition

Breaking complex tasks into sequential prompts.

### Decomposition Pattern

```
Complex Task → Subtask 1 → Subtask 2 → Subtask 3 → Final Output
```

### Example: Market Research Report

```
STEP 1 - Define scope:
"List the key questions a market research report should answer for a new fitness app targeting seniors."

STEP 2 - Gather information:
"For each question from Step 1, identify:
- What data sources would provide answers
- Whether data is publicly available
- Estimated research time"

STEP 3 - Analyze:
"Based on available data sources, analyze:
- Market size for senior fitness apps
- Key competitors
- Unmet needs"

STEP 4 - Synthesize:
"Create a 2-page executive summary with:
- Market opportunity
- Recommended features
- Go-to-market strategy"
```

### Parallel Decomposition

For tasks that can be done in parallel:

```
Generate 5 different:
- Version A: Focus on cost benefits
- Version B: Focus on time savings
- Version C: Focus on quality improvements
- Version D: Focus on innovation
- Version E: Focus on customer satisfaction

Then combine the best elements from each into one final version.
```

## Code Example: Advanced Prompt Chaining

```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PromptStep:
    name: str
    prompt_template: str
    output_key: str

class PromptChain:
    """Chain multiple prompts with output passing"""
    
    def __init__(self, steps: List[PromptStep]):
        self.steps = steps
        self.context = {}
    
    def execute(self, initial_input: Dict) -> Dict:
        """Execute prompt chain"""
        self.context.update(initial_input)
        
        for step in self.steps:
            # Render prompt with current context
            prompt = step.prompt_template.format(**self.context)
            
            # Get LLM response (simulated)
            response = self._call_llm(prompt)
            
            # Store in context for next steps
            self.context[step.output_key] = response
        
        return self.context
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM API (placeholder)"""
        # In production: call actual LLM API
        return f"[LLM response to: {prompt[:50]}...]"


# Example: Content creation pipeline
steps = [
    PromptStep(
        name="outline",
        prompt_template="Create an outline for a blog post about {topic}. Target audience: {audience}",
        output_key="outline"
    ),
    PromptStep(
        name="draft",
        prompt_template="Write a first draft using this outline:\n{outline}",
        output_key="draft"
    ),
    PromptStep(
        name="critique",
        prompt_template="Critique this draft for clarity, engagement, and accuracy:\n{draft}",
        output_key="critique"
    ),
    PromptStep(
        name="revise",
        prompt_template="Revise the draft addressing these critique points:\n{critique}\n\nOriginal draft:\n{draft}",
        output_key="final"
    )
]

chain = PromptChain(steps)

result = chain.execute({
    "topic": "Getting started with prompt engineering",
    "audience": "software developers"
})

print(result['final'])
```

## Key Takeaways

- **Tree of Thoughts** explores multiple reasoning paths
- **RAG prompting** grounds responses in retrieved knowledge
- **Multi-turn design** maintains context across conversation
- **Task decomposition** breaks complex work into steps
- **Prompt chaining** automates multi-step workflows
- **Parallel decomposition** generates variations efficiently

## Glossary

- **Tree of Thoughts (ToT):** Exploring multiple reasoning approaches
- **Retrieval-Augmented Generation (RAG):** Combining LLM with external knowledge
- **Multi-Turn Conversation:** Dialogue spanning multiple exchanges
- **Task Decomposition:** Breaking complex tasks into subtasks
- **Prompt Chaining:** Sequential prompt execution with output passing

## Quiz Questions

**1. What is the main advantage of Tree of Thoughts prompting?**

A) It's faster than chain-of-thought
B) It explores multiple approaches before committing to one
C) It requires fewer tokens
D) It works only for math problems

**Correct Answer:** B

**Explanation:** Tree of Thoughts explores multiple reasoning paths and evaluates each before selecting the best approach.

---

**2. What problem does RAG prompting solve?**

A) Makes responses shorter
B) Provides access to current and domain-specific knowledge
C) Reduces API costs
D) Makes the model run faster

**Correct Answer:** B

**Explanation:** RAG grounds responses in retrieved documents, providing access to current information and reducing hallucination.

---

**3. In multi-turn conversations, what is crucial for coherence?**

A) Using the same tone throughout
B) Maintaining and referencing context from previous turns
C) Keeping responses the same length
D) Never asking clarifying questions

**Correct Answer:** B

**Explanation:** Maintaining context across turns is essential for coherent multi-turn conversations.

---

**4. When should you decompose a task?**

A) Always, for every task
B) When the task is complex and can be broken into clearer subtasks
C) Never, let the model figure it out
D) Only for coding tasks

**Correct Answer:** B

**Explanation:** Task decomposition is most valuable for complex tasks that benefit from structured, step-by-step approaches.

---

**5. What is prompt chaining?**

A) Using multiple LLMs simultaneously
B) Connecting prompts where output from one becomes input to the next
C) Writing prompts in a list
D) Repeating the same prompt multiple times

**Correct Answer:** B

**Explanation:** Prompt chaining executes multiple prompts in sequence, with each step's output feeding into the next.

---

## Further Reading

- **Tree of Thoughts Paper**: https://arxiv.org/abs/2305.10601
- **RAG Best Practices**: https://python.langchain.com/docs/use_cases/question_answering/
- **Conversation Design**: https://conversationdesign.io/

---

**Continue to Chapter 12** to learn prompt optimization and production best practices!
