# Chapter 20: Evaluating Fine-tuned Models

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand evaluation metrics for fine-tuned models
- Implement evaluation methodologies
- Set up testing pipelines
- Monitor model performance in production

## Evaluation Metrics

### Classification Tasks

**Accuracy:**
```
Accuracy = Correct Predictions / Total Predictions

Example:
90 correct out of 100 = 90% accuracy
```

**Precision, Recall, F1:**
```
Precision = True Positives / (True Positives + False Positives)
Recall = True Positives / (True Positives + False Negatives)
F1 = 2 × (Precision × Recall) / (Precision + Recall)

Use F1 when:
- Class imbalance exists
- Both false positives and false negatives matter
```

**Confusion Matrix:**
```
              Predicted
              Yes    No
Actual Yes    45     5    (5 false negatives)
       No     3     47    (3 false positives)
```

### Generation Tasks

**Perplexity:**
```
Measures how well model predicts test data
Lower = better

Formula:
Perplexity = exp(-1/N × Σ log P(word_i))

Good perplexity:
- Base models: 10-30
- Fine-tuned: 5-20 (domain-specific)
```

**BLEU Score (for translation/summarization):**
```
Measures similarity to reference text
Range: 0-1 (higher = better)

BLEU-4 (4-gram): Most common
- < 0.2: Poor
- 0.2-0.4: Fair
- 0.4-0.6: Good
- > 0.6: Excellent
```

**ROUGE Score (for summarization):**
```
ROUGE-1: Unigram overlap
ROUGE-2: Bigram overlap
ROUGE-L: Longest common subsequence

Range: 0-1 (higher = better)
Good ROUGE-L: > 0.4
```

### Human Evaluation

**Criteria:**
```
1. Relevance (1-5): How relevant is the response?
2. Accuracy (1-5): Is the information correct?
3. Coherence (1-5): Is the response well-structured?
4. Fluency (1-5): Is the language natural?
5. Helpfulness (1-5): Does it help the user?
```

**Evaluation Template:**
```python
@dataclass
class HumanEvaluation:
    sample_id: str
    query: str
    response: str
    relevance: int  # 1-5
    accuracy: int  # 1-5
    coherence: int  # 1-5
    fluency: int  # 1-5
    helpfulness: int  # 1-5
    comments: str
```

## Evaluation Methodologies

### Hold-out Test Set

```python
from sklearn.model_selection import train_test_split

# Split data
train_data, test_data = train_test_split(
    dataset,
    test_size=0.2,  # 20% for testing
    random_state=42
)

# Train on train_data
# Evaluate on test_data (never seen during training)
```

### Cross-Validation

```python
from sklearn.model_selection import KFold
import numpy as np

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = []

for train_idx, val_idx in kf.split(data):
    train_data = data[train_idx]
    val_data = data[val_idx]
    
    # Train and evaluate
    model = train(train_data)
    score = evaluate(model, val_data)
    scores.append(score)

print(f"Average score: {np.mean(scores):.3f} (+/- {np.std(scores):.3f})")
```

### A/B Testing

```python
# Compare fine-tuned vs base model
def ab_test(model_a, model_b, test_queries, evaluator):
    results = {'a_wins': 0, 'b_wins': 0, 'ties': 0}
    
    for query in test_queries:
        response_a = model_a.generate(query)
        response_b = model_b.generate(query)
        
        winner = evaluator.compare(response_a, response_b)
        
        if winner == 'A':
            results['a_wins'] += 1
        elif winner == 'B':
            results['b_wins'] += 1
        else:
            results['ties'] += 1
    
    return results

# Usage
results = ab_test(base_model, fine_tuned_model, test_queries, human_evaluator)
print(f"Fine-tuned wins: {results['b_wins']}/{len(test_queries)}")
```

## Testing Pipelines

### Automated Evaluation

```python
class ModelEvaluator:
    """Automated model evaluation"""
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def evaluate_classification(self, test_data) -> Dict:
        """Evaluate classification task"""
        from sklearn.metrics import accuracy_score, f1_score, classification_report
        
        predictions = []
        true_labels = []
        
        for example in test_data:
            inputs = self.tokenizer(example['text'], return_tensors='pt')
            outputs = self.model(**inputs)
            pred = outputs.logits.argmax().item()
            
            predictions.append(pred)
            true_labels.append(example['label'])
        
        return {
            'accuracy': accuracy_score(true_labels, predictions),
            'f1': f1_score(true_labels, predictions, average='weighted'),
            'report': classification_report(true_labels, predictions)
        }
    
    def evaluate_generation(self, test_data, metric='perplexity') -> Dict:
        """Evaluate generation task"""
        import torch
        
        results = {}
        
        if metric == 'perplexity':
            total_loss = 0
            num_batches = 0
            
            for example in test_data:
                inputs = self.tokenizer(example['text'], return_tensors='pt')
                with torch.no_grad():
                    outputs = self.model(**inputs, labels=inputs['input_ids'])
                    total_loss += outputs.loss.item()
                    num_batches += 1
            
            avg_loss = total_loss / num_batches
            results['perplexity'] = np.exp(avg_loss)
        
        return results

# Usage
evaluator = ModelEvaluator(fine_tuned_model, tokenizer)
classification_results = evaluator.evaluate_classification(test_data)
print(f"Accuracy: {classification_results['accuracy']:.3f}")
```

### Continuous Evaluation

```python
class ContinuousEvaluator:
    """Monitor model performance in production"""
    
    def __init__(self, model, threshold: float = 0.8):
        self.model = model
        self.threshold = threshold
        self.metrics_history = []
    
    def evaluate_batch(self, queries: List[str], expected: List[str]) -> Dict:
        """Evaluate on batch of queries"""
        responses = [self.model.generate(q) for q in queries]
        
        # Calculate metrics
        accuracy = sum(r == e for r, e in zip(responses, expected)) / len(queries)
        
        # Track over time
        self.metrics_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'accuracy': accuracy,
            'batch_size': len(queries)
        })
        
        # Alert if below threshold
        if accuracy < self.threshold:
            self.send_alert(accuracy)
        
        return {'accuracy': accuracy, 'alert_sent': accuracy < self.threshold}
    
    def send_alert(self, accuracy: float):
        """Send alert for low performance"""
        print(f"⚠️ ALERT: Model accuracy ({accuracy:.2f}) below threshold ({self.threshold})")
```

## Production Monitoring

### Key Metrics to Track

```python
@dataclass
class ProductionMetrics:
    # Performance
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    
    # Quality
    accuracy: float
    user_satisfaction: float  # From feedback
    
    # Usage
    queries_per_minute: float
    cache_hit_rate: float
    
    # Errors
    error_rate: float
    fallback_rate: float
```

### Monitoring Dashboard

```python
import matplotlib.pyplot as plt
import pandas as pd

class MonitoringDashboard:
    """Create monitoring visualizations"""
    
    def __init__(self, metrics_log: str):
        self.metrics = pd.read_json(metrics_log, lines=True)
    
    def plot_accuracy_over_time(self):
        """Plot accuracy trend"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.metrics['timestamp'], self.metrics['accuracy'])
        plt.axhline(y=0.85, color='r', linestyle='--', label='Threshold')
        plt.title('Model Accuracy Over Time')
        plt.xlabel('Date')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.savefig('accuracy_trend.png')
    
    def plot_latency_distribution(self):
        """Plot latency distribution"""
        plt.figure(figsize=(10, 6))
        plt.hist(self.metrics['latency_ms'], bins=50)
        plt.title('Latency Distribution')
        plt.xlabel('Latency (ms)')
        plt.ylabel('Frequency')
        plt.savefig('latency_dist.png')
```

## Code Example: Complete Evaluation Pipeline

```python
from typing import Dict, List
from dataclasses import dataclass
import json

@dataclass
class EvaluationReport:
    model_name: str
    dataset: str
    metrics: Dict
    samples_evaluated: int
    timestamp: str

def evaluate_fine_tuned_model(
    model,
    tokenizer,
    test_data_path: str,
    task_type: str = "classification"
) -> EvaluationReport:
    """Complete evaluation pipeline"""
    
    # Load test data
    with open(test_data_path, 'r') as f:
        test_data = [json.loads(line) for line in f]
    
    # Prepare evaluator
    if task_type == "classification":
        from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
        
        predictions = []
        true_labels = []
        
        for example in test_data:
            inputs = tokenizer(example['text'], return_tensors='pt', truncation=True)
            outputs = model(**inputs)
            pred = outputs.logits.argmax().item()
            
            predictions.append(pred)
            true_labels.append(example['label'])
        
        metrics = {
            'accuracy': accuracy_score(true_labels, predictions),
            'f1': f1_score(true_labels, predictions, average='weighted'),
            'confusion_matrix': confusion_matrix(true_labels, predictions).tolist()
        }
    
    elif task_type == "generation":
        import torch
        
        total_loss = 0
        for example in test_data:
            inputs = tokenizer(example['text'], return_tensors='pt')
            with torch.no_grad():
                outputs = model(**inputs, labels=inputs['input_ids'])
                total_loss += outputs.loss.item()
        
        avg_loss = total_loss / len(test_data)
        metrics = {
            'perplexity': np.exp(avg_loss),
            'avg_loss': avg_loss
        }
    
    return EvaluationReport(
        model_name=model.config._name_or_path,
        dataset=test_data_path,
        metrics=metrics,
        samples_evaluated=len(test_data),
        timestamp=datetime.utcnow().isoformat()
    )

# Usage
report = evaluate_fine_tuned_model(
    model=fine_tuned_model,
    tokenizer=tokenizer,
    test_data_path="test_data.jsonl",
    task_type="classification"
)

print(f"Evaluation Report")
print(f"================")
print(f"Model: {report.model_name}")
print(f"Samples: {report.samples_evaluated}")
print(f"Metrics:")
for metric, value in report.metrics.items():
    print(f"  {metric}: {value}")
```

## Key Takeaways

- **Choose metrics** appropriate for your task type
- **Use hold-out test sets** for unbiased evaluation
- **Human evaluation** complements automated metrics
- **Monitor continuously** in production
- **Track trends** not just point-in-time scores
- **Set thresholds** for alerts and action

## Glossary

- **Perplexity:** Measure of how well model predicts data
- **BLEU/ROUGE:** Metrics for text generation quality
- **Cross-Validation:** Evaluation using multiple data splits
- **A/B Testing:** Comparing two models on same tasks
- **Confusion Matrix:** Table showing prediction breakdown

## Quiz Questions

**1. What does perplexity measure?**

A) How confused users are
B) How well model predicts test data
C) Model size
D) Training time

**Correct Answer:** B

**Explanation:** Perplexity measures how well a probability model predicts a sample. Lower is better.

---

**2. When should you use F1 score instead of accuracy?**

A) Always
B) When you have class imbalance
C) For generation tasks
D) Never

**Correct Answer:** B

**Explanation:** F1 score is better for imbalanced datasets where accuracy can be misleading.

---

**3. What is the purpose of a hold-out test set?**

A) To train the model
B) To provide unbiased evaluation
C) To increase dataset size
D) To speed up training

**Correct Answer:** B

**Explanation:** Hold-out test sets provide unbiased evaluation on data the model never saw during training.

---

**4. What BLEU score range indicates "Good" quality?**

A) < 0.2
B) 0.2-0.4
C) 0.4-0.6
D) > 0.8

**Correct Answer:** C

**Explanation:** BLEU scores of 0.4-0.6 are considered good, though this varies by task.

---

**5. What should you do if production accuracy drops below threshold?**

A) Ignore it
B) Send alert and investigate
C) Immediately retrain
D) Shut down the system

**Correct Answer:** B

**Explanation:** Set up alerts for threshold violations, then investigate the cause before taking action.

---

## Further Reading

- **Evaluation Metrics** - Hugging Face: https://huggingface.co/docs/evaluate
- **BLEU/ROUGE Explanation**: https://en.wikipedia.org/wiki/BLEU
- **ML Monitoring** - Arize AI: https://arize.com/blog/

---

**🎉 Module 5 Complete!** Continue to Module 6 for AI application development!
