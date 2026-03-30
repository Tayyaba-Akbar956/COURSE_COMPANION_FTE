# Chapter 3: Key Concepts and Terminology

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand essential terminology used in generative AI
- Explain core concepts like tokens, prompts, and models
- Distinguish between different types of AI models
- Navigate technical discussions about generative AI with confidence

## Introduction

Generative AI comes with its own vocabulary. Terms like "tokens," "transformers," "fine-tuning," and "hallucination" have specific meanings in this context. This chapter builds your vocabulary so you can confidently discuss and work with generative AI.

Let's decode the jargon!

## Core Concepts

### 1. Tokens and Tokenization

**Token:** The basic unit of text that a model processes. Tokens can be:
- Whole words: "cat", "running"
- Parts of words: "ing", "un", "able"
- Characters: "a", "!", " "
- Special symbols: `<start>`, `<end>`

**Tokenization:** The process of converting text into tokens.

**Example:**
```
Text: "Generative AI is amazing!"

Tokens: ["Gener", "ative", " AI", " is", " amazing", "!"]
```

**Why Tokens Matter:**
- Models have **token limits** (e.g., 4,096 tokens)
- **Cost** is often calculated per token
- **Speed** depends on token count
- Different models use different tokenization schemes

**Token Approximation:**
- ~1 token ≈ 4 characters in English
- ~1 token ≈ 0.75 words
- 1,000 tokens ≈ 750 words

### 2. Prompts and Completions

**Prompt:** The input you give to a generative AI model.

**Completion:** The output the model generates in response.

**Example:**
```
Prompt: "Write a tagline for a coffee shop"

Completion: "Wake up to greatness. ☕"
```

**Types of Prompts:**

| Type | Example | Use Case |
|------|---------|----------|
| **Instruction** | "Summarize this article" | Direct commands |
| **Question** | "What is machine learning?" | Q&A |
| **Completion** | "The future of AI is..." | Text continuation |
| **Few-shot** | "A→1, B→2, C→?" | Pattern learning |
| **Role-play** | "Act as a teacher..." | Persona-based |

### 3. Models and Parameters

**Model:** The trained AI system that generates content. Think of it as a complex mathematical function that takes input (prompt) and produces output (completion).

**Parameters:** Internal variables that the model learns during training. More parameters generally mean more capability.

**Model Sizes:**
- **Small:** < 1 billion parameters (fast, limited)
- **Medium:** 1-10 billion parameters (balanced)
- **Large:** 10-100 billion parameters (capable)
- **Very Large:** 100+ billion parameters (most capable)

**Example Models:**
```
GPT-3:     175 billion parameters
GPT-4:     ~1 trillion (estimated)
Llama 2:   7B, 13B, 70B variants
Claude:    ~100 billion (estimated)
```

### 4. Training and Inference

**Training:** The process of teaching a model by exposing it to vast amounts of data.

```
Training Process:
1. Collect massive dataset (text, images, etc.)
2. Model processes the data
3. Adjusts internal parameters to predict patterns
4. Repeat billions of times
5. Result: Trained model
```

**Inference:** Using a trained model to generate outputs.

```
Inference Process:
1. User provides prompt
2. Model processes prompt
3. Model generates completion
4. Output returned to user
```

**Key Differences:**

| Training | Inference |
|----------|-----------|
| Takes weeks/months | Takes milliseconds |
| Costs millions | Costs fractions of cents |
| Done once by creators | Done every time you use AI |
| Requires massive compute | Runs on modest hardware |

### 5. Temperature and Sampling

**Temperature:** A setting that controls randomness in generation.

```
Low Temperature (0.1-0.3):
- More focused, deterministic
- Same prompt → similar outputs
- Good for: factual Q&A, code

High Temperature (0.7-1.0):
- More creative, diverse
- Same prompt → varied outputs
- Good for: creative writing, brainstorming
```

**Sampling Methods:**

| Method | Description | Use Case |
|--------|-------------|---------|
| **Greedy** | Always picks most likely token | Code, math |
| **Top-k** | Samples from k most likely tokens | General use |
| **Top-p (Nucleus)** | Samples from tokens covering p% probability | Creative tasks |
| **Beam Search** | Explores multiple sequences | Translation |

### 6. Context Window

**Context Window:** The maximum amount of text a model can consider at once.

**Examples:**
- GPT-3: 4,096 tokens (~3,000 words)
- GPT-4: 8,192 tokens (~6,000 words)
- Claude: 100,000 tokens (~75,000 words)

**Why It Matters:**
- Determines how much conversation history the model remembers
- Affects how long documents it can process
- Larger context = more capable but more expensive

### 7. Embeddings

**Embedding:** A numerical representation of text (or other data) that captures meaning.

**Concept:** Similar meanings → Similar numerical vectors

**Visualization:**
```
King  - Man   + Woman  = Queen

[0.9, 0.1, 0.8] - [0.8, 0.2, 0.1] + [0.2, 0.9, 0.3] ≈ [0.3, 0.8, 1.0]
```

**Applications:**
- Search (find similar content)
- Recommendations
- Clustering related documents
- Semantic understanding

### 8. Fine-tuning

**Fine-tuning:** Training an already-trained model on specific data for a specific purpose.

**Analogy:**
- **Base Model:** Medical school graduate (general knowledge)
- **Fine-tuned:** Specialist surgeon (specific expertise)

**When to Fine-tune:**
- ✅ You have domain-specific data
- ✅ You need consistent style/format
- ✅ Base model doesn't perform well enough
- ❌ You just need a few examples (use prompting instead)

**Fine-tuning Process:**
```
1. Start with pre-trained model
2. Collect domain-specific examples
3. Train on this smaller dataset
4. Model adapts to domain
5. Test and deploy
```

### 9. Hallucination

**Hallucination:** When a model generates false or nonsensical information that seems plausible.

**Examples:**
```
❌ "The Eiffel Tower was built in 1892." (Actually 1889)
❌ "According to a 2023 Harvard study..." (No such study)
❌ "Python's print() function returns a value." (It returns None)
```

**Why It Happens:**
- Model predicts plausible text, not factual truth
- Training data may contain errors
- Model has no way to verify facts

**Mitigation:**
- Fact-check important claims
- Use retrieval-augmented generation (RAG)
- Ask model to cite sources
- Don't rely on AI for critical facts without verification

### 10. Zero-shot, One-shot, and Few-shot Learning

**Zero-shot:** Model performs task without any examples.
```
Prompt: "Translate to French: Hello"
Output: "Bonjour"
```

**One-shot:** Model sees one example.
```
Prompt: 
"English: Good morning → French: Bonjour
English: Hello → French: ?"
Output: "Bonjour"
```

**Few-shot:** Model sees several examples.
```
Prompt:
"English: Cat → French: Chat
English: Dog → French: Chien
English: Bird → French: Oiseau
English: Fish → French: ?"
Output: "Poisson"
```

## Model Architectures

### Transformer

The architecture powering modern LLMs.

**Key Components:**
- **Self-Attention:** Weights importance of different words
- **Feed-Forward Networks:** Process information
- **Layer Normalization:** Stabilizes training
- **Positional Encoding:** Tracks word order

**Advantages:**
- Parallel processing (fast training)
- Handles long-range dependencies
- Scales well to large sizes

### Encoder vs. Decoder

**Encoder (e.g., BERT):**
- Reads entire text at once
- Excellent for understanding
- Used for: Classification, extraction, analysis

**Decoder (e.g., GPT):**
- Generates text one token at a time
- Excellent for generation
- Used for: Writing, conversation, code

**Encoder-Decoder (e.g., T5, BART):**
- Combines both approaches
- Used for: Translation, summarization

## Important Distinctions

### Narrow AI vs. General AI

**Narrow AI (ANI):**
- Excels at specific tasks
- All current AI systems
- Examples: ChatGPT, DALL-E, AlphaGo

**General AI (AGI):**
- Human-level intelligence across all domains
- Theoretical (doesn't exist yet)
- Can learn any intellectual task

**Superintelligent AI (ASI):**
- Surpasses human intelligence
- Purely theoretical
- Subject of philosophical debate

### Generative AI vs. LLM

**Generative AI:** Umbrella term for all AI that creates content
- Includes: LLMs, image generators, music AI, code AI

**LLM (Large Language Model):** Specific type of generative AI for text
- Examples: GPT-4, Claude, Llama

**Relationship:**
```
Generative AI (broad category)
├── LLMs (text)
├── Image Models (DALL-E, Midjourney)
├── Audio Models (music, speech)
└── Video Models
```

### Prompt Engineering vs. Fine-tuning

| Prompt Engineering | Fine-tuning |
|-------------------|-------------|
| Craft better inputs | Train model on data |
| Quick, cheap | Time-consuming, expensive |
| Flexible, adaptable | Specialized, consistent |
| Works for most cases | Needed for niche tasks |

## Code Example: Working with Tokens

```python
import tiktoken

# Load tokenizer for a specific model
encoder = tiktoken.encoding_for_model("gpt-4")

# Count tokens
text = "Generative AI is transforming how we work and create."
tokens = encoder.encode(text)
print(f"Token count: {len(tokens)}")  # Output: Token count: 12

# Decode tokens back to text
decoded = encoder.decode(tokens)
print(f"Decoded: {decoded}")

# Check token limit
MAX_TOKENS = 8192
if len(tokens) < MAX_TOKENS:
    print("✓ Within token limit")
else:
    print("✗ Exceeds token limit")
```

## Code Example: Temperature Effects

```python
from openai import OpenAI

client = OpenAI()

prompt = "Write a creative tagline for a bookstore"

# Low temperature (focused)
response1 = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)
print(f"Low temp: {response1.choices[0].message.content}")
# Output: "Where Stories Begin."

# High temperature (creative)
response2 = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.9
)
print(f"High temp: {response2.choices[0].message.content}")
# Output: "Get Lost in the Stacks. Find Yourself in the Stories."
```

## Key Takeaways

- **Tokens** are the basic units of text; models have token limits
- **Prompts** are inputs; **completions** are outputs
- **Models** have **parameters** that determine capability
- **Training** creates models; **inference** uses them
- **Temperature** controls randomness in generation
- **Context window** limits how much text model can consider
- **Embeddings** represent meaning numerically
- **Fine-tuning** adapts models to specific domains
- **Hallucination** is when AI generates false but plausible information
- **Zero/One/Few-shot** refers to number of examples provided

## Glossary

- **Token:** Basic unit of text processed by models
- **Tokenization:** Converting text into tokens
- **Prompt:** Input given to generative AI
- **Completion:** Output generated by AI
- **Model:** Trained AI system
- **Parameters:** Internal variables learned during training
- **Training:** Teaching model on data
- **Inference:** Using trained model
- **Temperature:** Controls randomness in generation
- **Context Window:** Maximum text model can consider
- **Embedding:** Numerical representation capturing meaning
- **Fine-tuning:** Training pre-trained model on specific data
- **Hallucination:** AI generating false but plausible information
- **Zero-shot:** Performing task without examples
- **Few-shot:** Performing task with examples
- **Transformer:** Neural network architecture using self-attention
- **Encoder:** Model component for understanding text
- **Decoder:** Model component for generating text
- **Narrow AI:** AI specialized for specific tasks
- **AGI:** Hypothetical human-level AI

## Quiz Questions

**1. Approximately how many words is 1,000 tokens?**

A) 500 words
B) 750 words
C) 1,000 words
D) 1,500 words

**Correct Answer:** B

**Explanation:** 1,000 tokens is approximately 750 words in English, as 1 token ≈ 0.75 words.

---

**2. What does temperature control in generative AI?**

A) How fast the model runs
B) How many tokens the model generates
C) How random or deterministic the output is
D) How much context the model remembers

**Correct Answer:** C

**Explanation:** Temperature controls randomness. Low temperature = focused/deterministic; High temperature = creative/diverse.

---

**3. Which architecture powers modern large language models?**

A) Convolutional Neural Network (CNN)
B) Recurrent Neural Network (RNN)
C) Transformer
D) Generative Adversarial Network (GAN)

**Correct Answer:** C

**Explanation:** The Transformer architecture, introduced in 2017, powers all modern large language models like GPT-4, Claude, and Llama.

---

**4. What is hallucination in the context of generative AI?**

A) When the model generates images instead of text
B) When the model generates false information that seems plausible
C) When the model refuses to answer a question
D) When the model takes too long to respond

**Correct Answer:** B

**Explanation:** Hallucination refers to AI generating confident-sounding but false or nonsensical information.

---

**5. What is the difference between training and inference?**

A) Training is for text; inference is for images
B) Training creates the model; inference uses the model
C) Training is fast; inference is slow
D) There is no difference

**Correct Answer:** B

**Explanation:** Training is the process of teaching the model (takes weeks, done once). Inference is using the trained model to generate outputs (takes milliseconds, done every use).

---

## Further Reading

- **Tokenization Guide** - Hugging Face: https://huggingface.co/docs/tokenizers
- **Prompt Engineering Guide** - DAIR.AI: https://github.com/dair-ai/Prompt-Engineering-Guide
- **Transformer Explained** - Jay Alammar: https://jalammar.github.io/illustrated-transformer/
- **Embeddings Visualized** - TensorFlow Projector: https://projector.tensorflow.org/

---

**Ready to apply these concepts?** Continue to Chapter 4 to explore real-world applications and use cases of generative AI!
