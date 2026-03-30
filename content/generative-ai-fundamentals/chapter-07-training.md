# Chapter 7: Training and Pre-training LLMs

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand the pre-training process and objectives
- Learn about training data sources and preparation
- Explain the difference between pre-training and fine-tuning
- Discuss computational requirements and costs of training LLMs

## Introduction

Training a large language model is one of the most complex and resource-intensive endeavors in modern technology. It requires massive datasets, enormous computational power, and sophisticated engineering.

In this chapter, we'll demystify the training process. You'll learn how models like GPT-4 and Claude are created, what data they're trained on, and why it costs millions of dollars.

## The Two-Phase Training Process

LLMs go through two distinct training phases:

```
┌─────────────────────────────────────────────────────────┐
│              LLM TRAINING PIPELINE                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PHASE 1: PRE-TRAINING                                  │
│  ─────────────────                                      │
│  Goal: Learn general language patterns                  │
│  Data: Massive, diverse text corpus (TBs of data)       │
│  Task: Predict next token (self-supervised)             │
│  Duration: Weeks to months                              │
│  Cost: $1M - $100M+                                     │
│  Output: Base model (e.g., GPT-3 base)                  │
│                                                         │
│  ↓                                                      │
│                                                         │
│  PHASE 2: FINE-TUNING                                   │
│  ────────────────                                       │
│  Goal: Align with human preferences                     │
│  Data: Curated examples (human-generated)               │
│  Task: Follow instructions, be helpful                  │
│  Duration: Days to weeks                                │
│  Cost: $10K - $1M                                       │
│  Output: Instruction-tuned model (e.g., ChatGPT)        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Phase 1: Pre-Training

### Training Objective

**Self-Supervised Learning:** The model learns by predicting the next token in a sequence.

```
Input Text: "The cat sat on the ___"

Model Prediction: "mat" (correct) or "couch" (also reasonable)

Loss Function: Cross-entropy between prediction and actual next token

Goal: Minimize prediction error across billions of examples
```

**Why This Works:**
- No human labeling required (data labels itself)
- Learns grammar, facts, reasoning patterns
- Scales to massive datasets

### Training Data Sources

LLMs are trained on diverse internet-scale data:

```
Typical Training Data Composition:
├── Web Scrapes (Common Crawl, etc.) ......... 50-60%
├── Books (Project Gutenberg, etc.) .......... 10-15%
├── Wikipedia ................................ 5-10%
├── News Articles ............................ 5-10%
├── Code (GitHub, etc.) ...................... 5-10%
├── Forums & Q&A (Reddit, Stack Overflow) .... 5-10%
└── Other (social media, etc.) ............... 5%

Total Size: 100GB - 10TB+ of text (before filtering)
Total Tokens: 100 billion - 10+ trillion
```

### Data Processing Pipeline

Raw data requires extensive processing:

```
Step 1: Collection
────────────────────────────────────────
- Web scraping (Common Crawl, custom scrapers)
- API access (Wikipedia, news sites)
- Licensed datasets (books, academic papers)
- Open source repositories (GitHub)


Step 2: Filtering
────────────────────────────────────────
Remove:
✗ Low-quality content
✗ Duplicate text
✗ Toxic/harmful content
✗ Personal information
✗ Copyrighted material (sometimes)

Keep:
✓ High-quality, informative text
✓ Diverse topics and styles
✓ Multiple languages (but mostly English)


Step 3: Tokenization
────────────────────────────────────────
- Convert text to tokens (numbers)
- Build vocabulary (30K-100K tokens)
- Handle special characters, whitespace


Step 4: Quality Scoring
────────────────────────────────────────
- Score each document for quality
- Prioritize high-quality sources
- Weight sampling accordingly


Step 5: Deduplication
────────────────────────────────────────
- Remove exact duplicates
- Remove near-duplicates (fuzzy matching)
- Prevent model from memorizing
```

### The Training Loop

Simplified view of the training process:

```python
# Pseudocode for LLM training

# Initialize model
model = TransformerModel(
    vocab_size=50000,
    d_model=768,
    num_layers=12,
    num_heads=12
)

# Load training data
dataset = load_tokenized_data("training_data.jsonl")

# Training loop
for epoch in range(num_epochs):
    for batch in dataset:
        # Forward pass
        input_tokens = batch["input_ids"]
        target_tokens = batch["target_ids"]
        
        predictions = model(input_tokens)
        
        # Calculate loss
        loss = cross_entropy_loss(predictions, target_tokens)
        
        # Backward pass (backpropagation)
        loss.backward()
        
        # Update model parameters
        optimizer.step()
        optimizer.zero_grad()
        
        # Log progress
        if step % 100 == 0:
            print(f"Step {step}, Loss: {loss.item()}")
        
        step += 1

# Save model
save_model(model, "trained_model.pt")
```

### Training Infrastructure

**Hardware Requirements:**

```
Training GPT-3 Scale Model (175B parameters):
├── GPUs: 10,000+ NVIDIA A100 (40GB or 80GB)
├── Interconnect: High-speed NVLink, InfiniBand
├── Memory: 400TB+ GPU memory total
├── Storage: 100TB+ fast SSD storage
└── Network: 400 Gbps+ interconnect

Training Time: 3-6 months (with optimizations)
Power Consumption: 10-50 MW (megawatts)
```

**Distributed Training:**

```
Data Parallelism:
- Split batch across multiple GPUs
- Each GPU has full model
- Gradients synchronized

Model Parallelism:
- Split model layers across GPUs
- Each GPU has portion of model
- Required for very large models

Pipeline Parallelism:
- Split model into stages
- Different stages process different micro-batches
- Improves GPU utilization
```

### Training Costs

**Estimated Costs for Different Model Sizes:**

| Model Size | Parameters | Training Cost | Time |
|------------|------------|---------------|------|
| Small | 100M - 1B | $1K - $10K | Hours |
| Medium | 1B - 10B | $10K - $100K | Days |
| Large | 10B - 100B | $100K - $1M | Weeks |
| Very Large | 100B - 1T | $1M - $10M | Months |
| Frontier | 1T+ | $10M - $100M+ | Months |

**Cost Breakdown:**
- Compute (GPU time): 70-80%
- Engineering team: 10-15%
- Data collection/processing: 5-10%
- Infrastructure: 5%

### Training Challenges

**1. Catastrophic Forgetting**
```
Problem: Model forgets earlier knowledge when learning new patterns

Solution: Careful data mixing, replay buffers
```

**2. Loss Spikes**
```
Problem: Sudden increases in training loss

Solution: Reduce learning rate, gradient clipping
```

**3. Divergence**
```
Problem: Training becomes unstable, loss explodes

Solution: Careful hyperparameter tuning, warmup
```

**4. Compute Failures**
```
Problem: GPU failures during long training runs

Solution: Checkpointing, fault tolerance
```

## Phase 2: Fine-Tuning

After pre-training, the base model is capable but not optimized for helpful interactions.

### Why Fine-Tune?

**Base Model Limitations:**
```
Base Model (GPT-3):
User: "What's the capital of France?"
Model: "The capital of France is Paris. What's the capital of Germany?"

Problem: Continues text instead of answering helpfully
```

**Fine-Tuned Model (ChatGPT):**
```
User: "What's the capital of France?"
Model: "The capital of France is Paris."

Better: Direct, helpful answer
```

### Fine-Tuning Approaches

**1. Supervised Fine-Tuning (SFT)**

```
Process:
1. Collect high-quality instruction-response pairs
2. Train model to predict responses given instructions
3. Model learns to follow instructions

Data Example:
{
  "instruction": "Write a poem about the ocean",
  "response": "Waves crash upon the sandy shore..."
}

Dataset Size: 10K - 100K examples
```

**2. Reward Modeling**

```
Process:
1. Generate multiple responses for each prompt
2. Humans rate responses (1-5 stars)
3. Train reward model to predict human ratings

Reward Model:
Input: (prompt, response)
Output: Quality score (scalar)
```

**3. Reinforcement Learning from Human Feedback (RLHF)**

```
Process:
1. Use reward model as objective
2. Fine-tune policy model with RL
3. Model maximizes reward (human approval)

Algorithm: PPO (Proximal Policy Optimization)

Result: Model that produces human-preferred outputs
```

### Fine-Tuning Data Requirements

```
High-Quality Fine-Tuning Data:
├── Diverse prompts (questions, tasks, conversations)
├── High-quality responses (accurate, helpful, safe)
├── Multiple difficulty levels
├── Various domains (science, art, code, etc.)
└── Safety examples (handling harmful requests)

Dataset Sizes:
- SFT: 10K - 100K examples
- RLHF: 10K - 100K ratings
```

### Fine-Tuning Costs

```
Fine-Tuning Costs (vs. Pre-training):

Pre-training: $1M - $100M
Fine-tuning:  $10K - $1M

Ratio: Fine-tuning is ~1-10% of pre-training cost
```

## Code Example: Fine-Tuning with Hugging Face

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import load_dataset

# Load pre-trained model
model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Load fine-tuning dataset
dataset = load_dataset("json", data_files="instructions.jsonl")

# Tokenize dataset
def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )

tokenized_dataset = dataset.map(tokenize, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./fine-tuned-model",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    warmup_steps=100,
    logging_steps=10,
    save_steps=100,
    fp16=True,  # Mixed precision
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
)

# Start fine-tuning
trainer.train()

# Save fine-tuned model
trainer.save_model("./fine-tuned-model")
tokenizer.save_pretrained("./fine-tuned-model")
```

## Training Best Practices

### Data Quality

```
✓ Use high-quality, curated data
✓ Remove duplicates and low-quality content
✓ Balance topics and domains
✓ Filter harmful content
✓ Include diverse perspectives
```

### Training Stability

```
✓ Gradient clipping (prevent exploding gradients)
✓ Learning rate warmup (gradually increase LR)
✓ Learning rate decay (decrease LR over time)
✓ Careful initialization (Xavier, He initialization)
✓ Mixed precision training (faster, less memory)
```

### Monitoring

```
✓ Track training loss (should decrease)
✓ Monitor validation loss (detect overfitting)
✓ Check gradient norms (detect instability)
✓ Sample model outputs (qualitative evaluation)
✓ Track hardware utilization (efficiency)
```

## Key Takeaways

- **Pre-training** learns general language patterns from massive datasets
- **Fine-tuning** aligns models with human preferences
- **Training data** comes from diverse internet sources (web, books, code)
- **Training costs** range from thousands to hundreds of millions of dollars
- **Distributed training** across thousands of GPUs is required for large models
- **RLHF** (Reinforcement Learning from Human Feedback) produces helpful assistants
- **Data quality** is as important as model architecture

## Glossary

- **Pre-training:** Initial training on general text data
- **Fine-tuning:** Secondary training on specific tasks or preferences
- **Self-Supervised Learning:** Learning from data without human labels
- **Token:** Basic unit of text processed by models
- **Cross-Entropy Loss:** Measures difference between prediction and target
- **Backpropagation:** Algorithm for computing gradients
- **Gradient:** Direction and rate of change for optimization
- **Distributed Training:** Training across multiple devices
- **Data Parallelism:** Splitting batches across devices
- **Model Parallelism:** Splitting model across devices
- **RLHF:** Reinforcement Learning from Human Feedback
- **Reward Model:** Model that predicts human preferences
- **PPO:** Proximal Policy Optimization (RL algorithm)

## Quiz Questions

**1. What is the primary objective of pre-training?**

A) To learn specific tasks
B) To predict the next token in sequences
C) To align with human preferences
D) To reduce model size

**Correct Answer:** B

**Explanation:** Pre-training uses self-supervised learning where the model predicts the next token, learning general language patterns in the process.

---

**2. Which of the following is NOT a common source of training data?**

A) Web scrapes
B) Books
C) Private emails
D) Wikipedia

**Correct Answer:** C

**Explanation:** Private emails are not used due to privacy concerns. Training data comes from publicly available sources.

---

**3. Approximately how much does it cost to train a frontier model (100B+ parameters)?**

A) $1,000 - $10,000
B) $10,000 - $100,000
C) $100,000 - $1M
D) $1M - $100M+

**Correct Answer:** D

**Explanation:** Training frontier models requires thousands of GPUs running for months, costing millions to hundreds of millions of dollars.

---

**4. What is the purpose of fine-tuning?**

A) To make the model larger
B) To align the model with human preferences
C) To increase training time
D) To add more parameters

**Correct Answer:** B

**Explanation:** Fine-tuning adapts the base model to be more helpful, following instructions and producing human-preferred outputs.

---

**5. What does RLHF stand for?**

A) Random Learning from Huge Files
B) Reinforcement Learning from Human Feedback
C) Rapid Language Half-Training Framework
D) Real-time Language Handling Function

**Correct Answer:** B

**Explanation:** RLHF (Reinforcement Learning from Human Feedback) uses human preferences to guide model fine-tuning.

---

**6. Why is distributed training necessary for large models?**

A) To make training slower
B) Because models are too large to fit on a single GPU
C) To reduce data quality
D) To increase costs

**Correct Answer:** B

**Explanation:** Large models (100B+ parameters) require hundreds of GBs of memory, necessitating distribution across many GPUs.

---

## Further Reading

- **"Language Models are Few-Shot Learners"** - GPT-3 training details: https://arxiv.org/abs/2005.14165
- **Hugging Face Course** - Chapter on fine-tuning: https://huggingface.co/course/chapter7
- **Anthropic RLHF Paper** - Fine-tuning methodology: https://arxiv.org/abs/2204.05862
- **Common Crawl** - Training data source: https://commoncrawl.org/

---

**Continue your learning!** Move on to Chapter 8 to understand LLM capabilities and limitations in depth.
