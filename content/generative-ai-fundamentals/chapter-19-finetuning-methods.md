# Chapter 19: Fine-tuning Methods and Techniques

## Learning Objectives

By the end of this chapter, you will be able to:
- Implement full fine-tuning approach
- Apply parameter-efficient methods (LoRA, QLoRA)
- Compare fine-tuning techniques
- Set up fine-tuning pipelines

## Full Fine-tuning

### Process Overview

```
1. Load pre-trained model
2. Unfreeze all layers
3. Prepare training data
4. Configure training hyperparameters
5. Train on domain data
6. Evaluate and save
```

### Code Example: Full Fine-tuning

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import load_dataset
import torch

# Load model and tokenizer
model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Prepare dataset
dataset = load_dataset("json", data_files="training_data.jsonl")

# Tokenize
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
    fp16=True,
    gradient_checkpointing=True,
)

# Initialize trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
)

# Train
trainer.train()

# Save
trainer.save_model("./fine-tuned-model")
```

## LoRA (Low-Rank Adaptation)

### How LoRA Works

```
Instead of updating all weights W:
W' = W + ΔW (expensive)

LoRA uses low-rank decomposition:
ΔW = BA where B and A are small matrices

W' = W + BA (efficient)

Example for 7B model:
- Full fine-tuning: 7 billion parameters
- LoRA: ~10 million parameters (0.1%)
```

### LoRA Configuration

```python
from peft import LoraConfig, get_peft_model, TaskType

# LoRA configuration
lora_config = LoraConfig(
    r=16,  # Rank (smaller = fewer params)
    lora_alpha=32,  # Scaling factor
    target_modules=["q_proj", "v_proj"],  # Which layers to adapt
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Apply to model
model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()
# Output: "trainable params: 8,912,896 || all params: 7,000,000,000 || trainable%: 0.127%"
```

### LoRA Training

```python
from transformers import TrainingArguments, Trainer

# Training arguments (similar to full fine-tuning)
training_args = TrainingArguments(
    output_dir="./lora-model",
    num_train_epochs=3,
    per_device_train_batch_size=8,  # Can use larger batch
    gradient_accumulation_steps=2,
    learning_rate=1e-4,  # Higher LR than full fine-tuning
    warmup_steps=50,
    logging_steps=10,
    save_steps=100,
    fp16=True,
)

# Trainer
trainer = Trainer(
    model=model,  # LoRA-wrapped model
    args=training_args,
    train_dataset=tokenized_dataset["train"],
)

# Train
trainer.train()

# Save LoRA adapter (much smaller than full model)
model.save_pretrained("./lora-adapter")
```

## QLoRA (Quantized LoRA)

### What is QLoRA?

**Quantized LoRA:** Combines LoRA with 4-bit quantization for even lower memory usage.

```
Memory Usage Comparison:
- Full fine-tuning (7B): ~80GB GPU memory
- LoRA (7B): ~24GB GPU memory
- QLoRA (7B): ~12GB GPU memory
```

### QLoRA Setup

```python
from transformers import BitsAndBytesConfig
from peft import prepare_model_for_kbit_training

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

# Prepare for training
model = prepare_model_for_kbit_training(model)

# Add LoRA adapter
model = get_peft_model(model, lora_config)

# Train (same as LoRA)
trainer = Trainer(model=model, args=training_args, train_dataset=dataset)
trainer.train()
```

## Method Comparison

| Method | Parameters | Memory (7B) | Training Time | Performance |
|--------|------------|-------------|---------------|-------------|
| **Full** | 100% | 80GB | Slow | Best |
| **LoRA** | 0.1-1% | 24GB | Fast | Very Good |
| **QLoRA** | 0.1-1% | 12GB | Fast | Good |

## Code Example: Complete Fine-tuning Pipeline

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, BitsAndBytesConfig
from datasets import load_dataset
from dataclasses import dataclass

@dataclass
class FineTuningConfig:
    model_name: str
    use_lora: bool = True
    use_qlora: bool = False
    lora_r: int = 16
    lora_alpha: int = 32
    batch_size: int = 4
    learning_rate: float = 1e-4
    num_epochs: int = 3
    output_dir: str = "./fine-tuned-model"

class FineTuningPipeline:
    """Complete fine-tuning pipeline"""
    
    def __init__(self, config: FineTuningConfig):
        self.config = config
        self.model = None
        self.tokenizer = None
        self.trainer = None
    
    def load_model(self):
        """Load model with appropriate configuration"""
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        if self.config.use_qlora:
            # QLoRA: 4-bit quantization
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                quantization_config=bnb_config,
                device_map="auto"
            )
            self.model = prepare_model_for_kbit_training(self.model)
        else:
            # Standard loading
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
        
        # Apply LoRA if requested
        if self.config.use_lora:
            lora_config = LoraConfig(
                r=self.config.lora_r,
                lora_alpha=self.config.lora_alpha,
                target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
                lora_dropout=0.05,
                bias="none",
                task_type="CAUSAL_LM"
            )
            self.model = get_peft_model(self.model, lora_config)
            self.model.print_trainable_parameters()
    
    def prepare_data(self, data_path: str):
        """Load and tokenize training data"""
        dataset = load_dataset("json", data_files=data_path)
        
        def tokenize(example):
            return self.tokenizer(
                example["text"],
                truncation=True,
                max_length=512,
                padding="max_length"
            )
        
        return dataset.map(tokenize, batched=True)
    
    def train(self, train_dataset, eval_dataset=None):
        """Train the model"""
        training_args = TrainingArguments(
            output_dir=self.config.output_dir,
            num_train_epochs=self.config.num_epochs,
            per_device_train_batch_size=self.config.batch_size,
            gradient_accumulation_steps=4,
            learning_rate=self.config.learning_rate,
            warmup_steps=50,
            logging_steps=10,
            save_steps=100,
            fp16=True,
            gradient_checkpointing=self.config.use_qlora,
        )
        
        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
        )
        
        self.trainer.train()
    
    def save(self, path: str):
        """Save fine-tuned model"""
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        print(f"Model saved to {path}")

# Usage
config = FineTuningConfig(
    model_name="meta-llama/Llama-2-7b-hf",
    use_lora=True,
    use_qlora=True,  # Use QLoRA for memory efficiency
    lora_r=16,
    batch_size=4,
    output_dir="./my-fine-tuned-model"
)

pipeline = FineTuningPipeline(config)
pipeline.load_model()

train_data = pipeline.prepare_data("training_data.jsonl")
pipeline.train(train_data)
pipeline.save("./final-model")
```

## Key Takeaways

- **Full fine-tuning** updates all parameters (best performance, highest cost)
- **LoRA** updates small matrices (great balance of performance and efficiency)
- **QLoRA** adds quantization (lowest memory, good for consumer GPUs)
- **PEFT libraries** simplify implementation
- **Choose method** based on resources and requirements

## Glossary

- **Rank (r):** LoRA hyperparameter controlling adapter size
- **Quantization:** Reducing numerical precision to save memory
- **Adapter:** Small trainable module inserted into model
- **PEFT:** Parameter-Efficient Fine-Tuning

## Quiz Questions

**1. What percentage of parameters does LoRA typically update?**

A) 100%
B) 50%
C) 10%
D) 0.1-1%

**Correct Answer:** D

**Explanation:** LoRA updates only 0.1-1% of parameters through low-rank decomposition.

---

**2. What is the main benefit of QLoRA over LoRA?**

A) Better accuracy
B) Lower memory usage through quantization
C) Faster training
D) Simpler implementation

**Correct Answer:** B

**Explanation:** QLoRA combines LoRA with 4-bit quantization, reducing memory usage by ~50% compared to LoRA.

---

**3. Which LoRA hyperparameter controls adapter size?**

A) lora_alpha
B) r (rank)
C) learning_rate
D) batch_size

**Correct Answer:** B

**Explanation:** The rank (r) parameter controls the size of LoRA adapters. Higher r = more parameters.

---

**4. What GPU memory is needed for QLoRA fine-tuning of a 7B model?**

A) 80GB
B) 40GB
C) 24GB
D) ~12GB

**Correct Answer:** D

**Explanation:** QLoRA enables fine-tuning 7B models on ~12GB GPU memory through 4-bit quantization.

---

**5. When should you use full fine-tuning over LoRA?**

A) Always - it's the best
B) When you need maximum performance and have resources
C) When you have limited memory
D) When you need fast training

**Correct Answer:** B

**Explanation:** Full fine-tuning provides best performance but requires significant resources. Use when performance is critical and resources allow.

---

## Further Reading

- **LoRA Paper**: https://arxiv.org/abs/2106.09685
- **QLoRA Paper**: https://arxiv.org/abs/2305.14314
- **PEFT Documentation**: https://huggingface.co/docs/peft
- **Fine-tuning Guide**: https://huggingface.co/docs/transformers/training

---

**Continue to Chapter 20** to learn how to evaluate fine-tuned models!
