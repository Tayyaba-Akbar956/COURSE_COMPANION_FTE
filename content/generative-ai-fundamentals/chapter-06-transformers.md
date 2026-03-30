# Chapter 6: How LLMs Work: Transformers Architecture

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand the transformer architecture components and their roles
- Explain how self-attention mechanism works
- Distinguish between encoder and decoder architectures
- Visualize how transformers process text step-by-step

## Introduction

You know that LLMs use the Transformer architecture—but what does that actually mean? How does a transformer turn your prompt into a coherent response?

In this chapter, we'll open the black box and explore the inner workings of transformers. You don't need a deep learning background—we'll build understanding from the ground up with clear explanations and visual diagrams.

By the end, you'll understand the architecture that powers ChatGPT, Claude, and all modern LLMs.

## Why Transformers Were Revolutionary

Before transformers (pre-2017), sequence models had a fundamental limitation:

### The Sequential Processing Problem

**Recurrent Neural Networks (RNNs)** processed text one word at a time:

```
RNN Processing:
"The cat sat on the mat"
 ↓
Process "The" → hidden state
 ↓
Process "cat" → hidden state (includes "The")
 ↓
Process "sat" → hidden state (includes "The cat")
 ↓
...and so on

Problem: Information from early words gets diluted
```

**Limitations:**
- ❌ Slow (can't parallelize)
- ❌ Forgets early context in long sequences
- ❌ Struggles with long-range dependencies

### The Transformer Solution

Transformers process **all words simultaneously** using self-attention:

```
Transformer Processing:
"The cat sat on the mat"
 ↓
Process ALL words at once
 ↓
Self-attention connects related words:
- "cat" ↔ "sat" (who sat?)
- "on" ↔ "mat" (on what?)

Result: Full context, parallel processing
```

**Advantages:**
- ✅ Fast (parallel processing)
- ✅ Remembers all context equally
- ✅ Handles long-range dependencies

## Transformer Architecture Overview

Let's explore the complete transformer architecture:

```
┌─────────────────────────────────────────────────────┐
│                    TRANSFORMER                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Input Text → Tokenization → Token Embeddings       │
│                        ↓                             │
│  ┌────────────────────────────────────────────┐     │
│  │         Encoder Stack (N layers)            │     │
│  │  ┌──────────────────────────────────────┐  │     │
│  │  │  Multi-Head Self-Attention           │  │     │
│  │  │  ↓                                    │  │     │
│  │  │  Add & Normalize                      │  │     │
│  │  │  ↓                                    │  │     │
│  │  │  Feed-Forward Network                 │  │     │
│  │  │  ↓                                    │  │     │
│  │  │  Add & Normalize                      │  │     │
│  │  └──────────────────────────────────────┘  │     │
│  │  (Repeated N times, e.g., N=12 for GPT-3)  │     │
│  └────────────────────────────────────────────┘     │
│                        ↓                             │
│  ┌────────────────────────────────────────────┐     │
│  │         Decoder Stack (N layers)            │     │
│  │  (Similar structure + cross-attention)      │     │
│  └────────────────────────────────────────────┘     │
│                        ↓                             │
│  Output Probabilities → Select Next Token           │
│                        ↓                             │
│  Repeat until complete → Final Output               │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Key Components Explained

### 1. Token Embeddings

**Purpose:** Convert tokens (numbers) into meaningful vectors.

```
Vocabulary: {"The": 1, "cat": 2, "sat": 3, "on": 4, "mat": 5}

Input: "The cat sat" → [1, 2, 3]

Embedding Layer:
[1, 2, 3] → Look up each token's vector
 ↓
[
  [0.2, -0.5, 0.8, ...],  # "The" vector (dimension: 768+)
  [0.1, 0.3, -0.2, ...],  # "cat" vector
  [-0.4, 0.6, 0.1, ...]   # "sat" vector
]
```

**Key Points:**
- Each token → high-dimensional vector (e.g., 768 dimensions)
- Learned during training
- Similar meanings → similar vectors

### 2. Positional Encodings

**Problem:** Transformers process all words simultaneously, so they lose word order information.

**Solution:** Add positional information to embeddings.

```
Token Embeddings:      [0.2, -0.5, 0.8, ...]  # "cat"
Positional Encoding: + [0.1, 0.1, 0.0, ...]  # Position 2
                      ──────────────────────
Final Embedding:       [0.3, -0.4, 0.8, ...]
```

**Positional Encoding Formula:**
```
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

Where:
- pos = position in sequence
- i = dimension index
- d_model = embedding dimension
```

**Why This Works:**
- Each position gets a unique encoding
- Model can learn relative positions
- Works for any sequence length

### 3. Self-Attention Mechanism

**The Heart of Transformers**

Self-attention allows each word to "look at" all other words and decide which are most relevant.

**Intuition:**
```
Sentence: "The cat sat on the mat because it was tired"

When processing "it", attention helps answer:
- What does "it" refer to?
- Attention weights: "cat" (high), "mat" (low)
- Model learns "it" refers to "cat"
```

**How It Works (Step-by-Step):**

```
Step 1: Create Query, Key, Value vectors for each word
──────────────────────────────────────────────────────
For each token embedding, create three vectors:
- Query (Q): What am I looking for?
- Key (K): What do I contain?
- Value (V): What information do I carry?

"The" → Q_the, K_the, V_the
"cat" → Q_cat, K_cat, V_cat
"sat" → Q_sat, K_sat, V_sat


Step 2: Calculate Attention Scores
──────────────────────────────────────────────────────
For each word pair, calculate compatibility:

Score("cat", "sat") = Q_cat · K_sat (dot product)

Higher score = more relevant connection


Step 3: Normalize Scores (Softmax)
──────────────────────────────────────────────────────
Convert scores to probabilities (sum to 1):

Attention Weights for "cat":
- "The": 0.1
- "cat": 0.2
- "sat": 0.5  ← highest (cat performed action)
- "on": 0.1
- "mat": 0.1


Step 4: Weighted Sum of Values
──────────────────────────────────────────────────────
Combine information from all words:

Output("cat") = 0.1×V_the + 0.2×V_cat + 0.5×V_sat + 0.1×V_on + 0.1×V_mat

Result: "cat" representation now includes information about "sat"
```

**Mathematical Formula:**
```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V

Where:
- Q = Query matrix
- K = Key matrix
- V = Value matrix
- d_k = dimension of Key vectors
- √d_k = scaling factor (prevents large values)
```

### 4. Multi-Head Attention

**Idea:** Instead of one attention mechanism, run multiple in parallel.

```
Single Attention:
Input → [Attention Head] → Output

Multi-Head Attention:
              ┌→ [Head 1] ─┐
              ├→ [Head 2] ─┤
Input → Split ┤→ [Head 3] ─┤→ Combine → Output
              ├→ [Head 4] ─┤
              └→ [Head 8] ─┘
```

**Why Multiple Heads?**

Each head learns different relationships:

```
Sentence: "The cat sat on the mat"

Head 1 (Syntactic): Focuses on grammar
- "cat" → "sat" (subject-verb)

Head 2 (Semantic): Focuses on meaning
- "cat" → "mat" (related objects)

Head 3 (Positional): Focuses on nearby words
- "sat" → "on" (adjacent words)

Combined: Rich, multi-faceted understanding
```

### 5. Feed-Forward Networks

**Purpose:** Process and transform the attention outputs.

```
After Multi-Head Attention:
 ↓
Feed-Forward Network (per position):
┌─────────────────────────────┐
│  Linear Layer (expand)      │
│  ↓                          │
│  ReLU Activation (non-linear)│
│  ↓                          │
│  Linear Layer (project back)│
└─────────────────────────────┘
 ↓
Output to next layer
```

**Structure:**
```python
# Simplified feed-forward network
class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        self.linear1 = nn.Linear(d_model, d_ff)  # Expand (e.g., 512 → 2048)
        self.linear2 = nn.Linear(d_ff, d_model)  # Project back
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.linear1(x)
        x = self.relu(x)
        x = self.linear2(x)
        return x
```

### 6. Add & Normalize (Residual Connections)

**Problem:** Deep networks suffer from vanishing gradients.

**Solution:** Add residual connections and layer normalization.

```
Residual Connection:
Input ─────────────┬────────→ Output
                   ↓
            [Sub-layer: Attention or FFN]
                   ↓
            Add: Input + Sub-layer Output
                   ↓
            Normalize: LayerNorm()


Diagram:
         ┌──────────────────────┐
Input ──→│  Add (x + F(x))      │──→ Norm ──→ Output
         │       ↑              │
         └───────┼──────────────┘
                 ↓
            [Sub-layer F(x)]
```

**Benefits:**
- ✅ Gradients flow directly through skip connection
- ✅ Prevents vanishing gradient problem
- ✅ Enables training very deep models

## Encoder vs. Decoder Architectures

Transformers come in three configurations:

### 1. Encoder-Only (BERT-style)

```
Input → [Encoder Stack] → Representations
                          ↓
                    [Classification Head]
                          ↓
                    Output (classification)
```

**Characteristics:**
- Sees entire input at once (bidirectional)
- Excellent for understanding tasks
- Used for: Classification, extraction, analysis

**Examples:** BERT, RoBERTa, DistilBERT

### 2. Decoder-Only (GPT-style)

```
Input → [Decoder Stack] → Next Token Prediction
                           ↓
                     Generate token
                           ↓
                     Append to input
                           ↓
                     Repeat until complete
```

**Characteristics:**
- Processes left-to-right (unidirectional)
- Excellent for generation tasks
- Used for: Text generation, conversation, code

**Examples:** GPT-3, GPT-4, Llama, Claude

### 3. Encoder-Decoder (T5-style)

```
Input → [Encoder] → Representations → [Decoder] → Output
                     ↓                    ↑
              (full context)        (generates output)
```

**Characteristics:**
- Encoder understands full input
- Decoder generates output
- Used for: Translation, summarization, QA

**Examples:** T5, BART, Seq2Seq models

## How Generation Works (Step-by-Step)

Let's trace how a decoder-only model (like GPT) generates text:

```
Prompt: "Once upon a"

Step 1: Process prompt through transformer
────────────────────────────────────────────
"Once upon a" → Tokenize → [101, 205, 103]
 ↓
Embed → Positional Encode → Transformer Layers
 ↓
Output logits for next token

Step 2: Sample next token
────────────────────────────────────────────
Logits → Softmax → Probabilities:
- "time": 0.85
- "more": 0.10
- "these": 0.03
- ...

Sample: "time" (highest probability)

Step 3: Append and repeat
────────────────────────────────────────────
New input: "Once upon a time"
 ↓
Repeat Steps 1-2
 ↓
Next token: " there" (probability 0.72)

Step 4: Continue until stop condition
────────────────────────────────────────────
Continue generating until:
- Max tokens reached
- Stop token generated
- Stop sequence detected

Final output: "Once upon a time there lived a king..."
```

## Code Example: Building a Simple Transformer

```python
import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    """Add positional information to embeddings"""
    
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        
        # Create positional encoding matrix
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * 
                            (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        self.register_buffer('pe', pe.unsqueeze(0))
    
    def forward(self, x):
        return x + self.pe[:, :x.size(1)]


class SelfAttention(nn.Module):
    """Multi-head self-attention mechanism"""
    
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_model = d_model
        self.head_dim = d_model // num_heads
        
        self.query = nn.Linear(d_model, d_model)
        self.key = nn.Linear(d_model, d_model)
        self.value = nn.Linear(d_model, d_model)
        self.output = nn.Linear(d_model, d_model)
    
    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.shape
        
        # Create Q, K, V matrices
        Q = self.query(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.key(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.value(x).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        
        # Calculate attention scores
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        
        # Apply mask (for decoder)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # Softmax and weighted sum
        attention = torch.softmax(scores, dim=-1)
        context = torch.matmul(attention, V)
        
        # Combine heads
        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        
        return self.output(context)


class TransformerBlock(nn.Module):
    """Single transformer block (attention + feed-forward)"""
    
    def __init__(self, d_model, num_heads, d_ff):
        super().__init__()
        
        self.attention = SelfAttention(d_model, num_heads)
        self.feed_forward = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )
        
        self.layer_norm1 = nn.LayerNorm(d_model)
        self.layer_norm2 = nn.LayerNorm(d_model)
    
    def forward(self, x, mask=None):
        # Attention with residual connection
        attention_output = self.attention(x, mask)
        x = self.layer_norm1(x + attention_output)
        
        # Feed-forward with residual connection
        ff_output = self.feed_forward(x)
        x = self.layer_norm2(x + ff_output)
        
        return x


# Example usage
d_model = 512
num_heads = 8
d_ff = 2048
num_layers = 6

# Create transformer
embedding = nn.Embedding(10000, d_model)
pos_encoding = PositionalEncoding(d_model)
transformer_blocks = nn.ModuleList([
    TransformerBlock(d_model, num_heads, d_ff) 
    for _ in range(num_layers)
])

# Process input
input_tokens = torch.randint(0, 10000, (1, 20))  # batch_size=1, seq_len=20
x = embedding(input_tokens)
x = pos_encoding(x)

# Pass through transformer layers
for block in transformer_blocks:
    x = block(x)

print(f"Output shape: {x.shape}")  # (1, 20, 512)
```

## Key Takeaways

- **Transformers process all words simultaneously** using self-attention
- **Self-attention** allows each word to attend to relevant words in the sequence
- **Multi-head attention** captures different types of relationships
- **Positional encodings** preserve word order information
- **Encoder-only** models excel at understanding; **Decoder-only** at generation
- **Residual connections** enable training deep models
- **Generation** works by predicting one token at a time, autoregressively

## Glossary

- **Transformer:** Neural network architecture using self-attention
- **Self-Attention:** Mechanism allowing tokens to attend to other tokens
- **Query (Q):** What a token is looking for
- **Key (K):** What information a token contains
- **Value (V):** The actual information content
- **Multi-Head Attention:** Multiple attention mechanisms in parallel
- **Positional Encoding:** Information added to preserve word order
- **Encoder:** Transformer component for understanding
- **Decoder:** Transformer component for generation
- **Feed-Forward Network:** Neural network applied at each position
- **Residual Connection:** Skip connection that adds input to output
- **Layer Normalization:** Normalizes activations across features
- **Autoregressive:** Generating one token at a time, conditioned on previous

## Quiz Questions

**1. What is the primary advantage of transformers over RNNs?**

A) Transformers are smaller
B) Transformers can process all words in parallel
C) Transformers don't need training data
D) Transformers are easier to understand

**Correct Answer:** B

**Explanation:** Transformers process all words simultaneously using self-attention, enabling parallel computation and better handling of long-range dependencies.

---

**2. What is the purpose of positional encodings?**

A) To make the model faster
B) To provide word order information
C) To reduce memory usage
D) To improve accuracy

**Correct Answer:** B

**Explanation:** Since transformers process all words simultaneously, positional encodings are added to preserve information about word order and position.

---

**3. In self-attention, what do Query, Key, and Value represent?**

A) Different types of input data
B) Three different models
C) Different aspects of attention computation
D) Training, validation, and test sets

**Correct Answer:** C

**Explanation:** Query represents what a token is looking for, Key represents what it contains, and Value is the actual information. These are used to compute attention weights.

---

**4. Why do transformers use multi-head attention?**

A) To process multiple inputs simultaneously
B) To capture different types of relationships
C) To reduce computational cost
D) To make the model smaller

**Correct Answer:** B

**Explanation:** Multiple attention heads allow the model to attend to different relationships simultaneously (e.g., syntactic, semantic, positional).

---

**5. Which architecture is best suited for text generation?**

A) Encoder-only
B) Decoder-only
C) Encoder-decoder
D) RNN

**Correct Answer:** B

**Explanation:** Decoder-only architectures (like GPT) are designed for autoregressive generation, processing left-to-right and predicting the next token.

---

**6. What is the purpose of residual (skip) connections?**

A) To reduce model size
B) To enable training deep networks by preventing vanishing gradients
C) To speed up inference
D) To improve tokenization

**Correct Answer:** B

**Explanation:** Residual connections allow gradients to flow directly through the network, enabling training of very deep transformer models.

---

**7. How does a decoder-only model generate text?**

A) All at once in parallel
B) One token at a time, autoregressively
C) By retrieving from a database
D) By copying from the input

**Correct Answer:** B

**Explanation:** Decoder-only models generate text autoregressively—one token at a time, with each new token conditioned on all previously generated tokens.

---

## Further Reading

- **"Attention Is All You Need"** - Original transformer paper: https://arxiv.org/abs/1706.03762
- **The Illustrated Transformer** - Jay Alammar's visual guide: https://jalammar.github.io/illustrated-transformer/
- **Transformers from Scratch** - Code implementation: https://e2eml.school/transformers.html
- **Hugging Face Transformers Course** - Comprehensive tutorials: https://huggingface.co/course

---

**Ready to go deeper?** Continue to Chapter 7 to learn how LLMs are trained from scratch!
