# Chapter 16: RAG Best Practices and Optimization

## Learning Objectives

By the end of this chapter, you will be able to:
- Optimize retrieval quality and relevance
- Apply production best practices for RAG systems
- Troubleshoot common RAG issues
- Monitor and improve RAG performance

## Retrieval Quality Optimization

### Chunk Size Optimization

**The Goldilocks Problem:**
```
Too Small (< 100 tokens):
- Loses context
- Fragmented meaning
- Too many chunks to retrieve

Too Large (> 1000 tokens):
- Dilutes relevance
- Includes irrelevant information
- Wastes context window

Just Right (200-500 tokens):
- Preserves context
- Maintains coherence
- Efficient retrieval
```

**Finding Optimal Chunk Size:**

```python
def evaluate_chunk_size(documents: List[str], chunk_sizes: List[int]) -> Dict:
    """Test different chunk sizes"""
    results = {}
    
    for size in chunk_sizes:
        chunker = TextChunker(chunk_size=size, overlap=size//10)
        
        # Create chunks
        all_chunks = []
        for doc in documents:
            chunks = chunker.chunk_recursive(doc)
            all_chunks.extend(chunks)
        
        # Evaluate
        results[size] = {
            'num_chunks': len(all_chunks),
            'avg_chunk_length': np.mean([len(c.split()) for c in all_chunks]),
            'retrieval_score': test_retrieval_quality(all_chunks)
        }
    
    return results

# Test range of sizes
results = evaluate_chunk_size(
    documents=test_docs,
    chunk_sizes=[100, 200, 300, 500, 800, 1000]
)

# Find best
best_size = max(results.keys(), key=lambda k: results[k]['retrieval_score'])
print(f"Optimal chunk size: {best_size}")
```

**Recommendations by Content Type:**

| Content Type | Recommended Chunk Size | Overlap |
|--------------|----------------------|---------|
| **FAQ/Short docs** | 100-200 tokens | 20 tokens |
| **Articles/Blog posts** | 300-500 tokens | 50 tokens |
| **Technical docs** | 400-600 tokens | 100 tokens |
| **Books/Long form** | 500-800 tokens | 100 tokens |

### Top-k Selection

**How many documents to retrieve?**

```
Too Few (k < 3):
- May miss relevant information
- Low recall

Too Many (k > 10):
- Overwhelms LLM context
- Includes irrelevant content
- Higher costs

Sweet Spot (k = 3-7):
- Good coverage
- Manageable context
- Cost-effective
```

**Dynamic Top-k:**
```python
def dynamic_top_k(query_embedding, vector_store, 
                  threshold: float = 0.7, max_k: int = 10) -> List:
    """Retrieve variable number of documents based on similarity"""
    
    # Get many candidates
    candidates = vector_store.search(query_embedding, top_k=max_k * 2)
    
    # Filter by threshold
    relevant = [(doc, score) for doc, score in candidates if score >= threshold]
    
    # Return top results (at least 1, at most max_k)
    return relevant[:max_k] if relevant else candidates[:1]

# Usage: adapts to query difficulty
results = dynamic_top_k(query_embedding, vector_store, threshold=0.65)
```

### Re-ranking Strategies

**Problem:** Initial retrieval may not be optimally ordered.

**Solution:** Re-rank retrieved documents with more sophisticated scoring.

```python
class Reranker:
    """Re-rank retrieved documents"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def rerank(self, query: str, documents: List[Dict], top_k: int = 5) -> List[Dict]:
        """Use LLM to score relevance"""
        scored_docs = []
        
        for doc in documents:
            # Ask LLM to score relevance
            prompt = f"""
            Query: {query}
            
            Document: {doc['content'][:500]}
            
            On a scale of 0-10, how relevant is this document to the query?
            Respond with only a number.
            """
            
            score = int(self.llm.generate(prompt).strip())
            scored_docs.append((doc, score))
        
        # Sort by score
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        return [doc for doc, score in scored_docs[:top_k]]

# Usage in RAG pipeline
retrieved = vector_store.search(query_embedding, top_k=10)
reranked = reranker.rerank(query, [doc for doc, _ in retrieved], top_k=5)
```

**Cross-Encoder Reranking (More Efficient):**
```python
from sentence_transformers import CrossEncoder

class CrossEncoderReranker:
    """Fast neural reranker"""
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)
    
    def rerank(self, query: str, documents: List[str], top_k: int = 5) -> List[int]:
        """Score and rank documents"""
        # Create query-document pairs
        pairs = [[query, doc] for doc in documents]
        
        # Get relevance scores
        scores = self.model.predict(pairs)
        
        # Rank by score
        ranked_indices = np.argsort(scores)[::-1][:top_k]
        
        return ranked_indices

# Usage
reranker = CrossEncoderReranker()
top_indices = reranker.rerank(query, doc_texts, top_k=5)
top_docs = [documents[i] for i in top_indices]
```

## Production Best Practices

### 1. Caching Strategies

**Cache frequent queries:**
```python
from functools import lru_cache
import hashlib

class RAGCache:
    """Cache RAG responses"""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
    
    def _hash(self, query: str) -> str:
        return hashlib.md5(query.encode()).hexdigest()
    
    def get(self, query: str) -> Optional[str]:
        """Get cached response"""
        key = self._hash(query)
        return self.cache.get(key)
    
    def set(self, query: str, response: str):
        """Cache response"""
        if len(self.cache) >= self.max_size:
            # Remove oldest
            self.cache.pop(next(iter(self.cache)))
        
        self.cache[self._hash(query)] = response

# Usage in RAG system
cache = RAGCache(max_size=500)

def query_with_cache(query: str) -> str:
    # Check cache first
    cached = cache.get(query)
    if cached:
        return cached
    
    # Generate response
    response = rag_system.query(query)
    
    # Cache it
    cache.set(query, response)
    
    return response
```

### 2. Query Preprocessing

**Clean and normalize queries:**
```python
def preprocess_query(query: str) -> str:
    """Preprocess query for better retrieval"""
    
    # Remove unnecessary words
    stop_words = {'what', 'is', 'the', 'a', 'an', 'how', 'do', 'does'}
    words = query.split()
    filtered = [w for w in words if w.lower() not in stop_words]
    
    # Fix common typos
    corrections = {
        'pyton': 'python',
        'machne': 'machine',
        'learing': 'learning'
    }
    corrected = [corrections.get(w.lower(), w) for w in filtered]
    
    # Expand abbreviations
    expansions = {
        'ml': 'machine learning',
        'ai': 'artificial intelligence',
        'nlp': 'natural language processing'
    }
    expanded = [expansions.get(w.lower(), w) for w in corrected]
    
    return ' '.join(expanded)

# Usage
raw_query = "What is the ML pipeline for NLP?"
processed_query = preprocess_query(raw_query)
# Result: "machine learning pipeline natural language processing"
```

### 3. Response Quality Checks

**Validate responses before returning:**
```python
def validate_response(response: str, query: str, documents: List[Dict]) -> Dict:
    """Check response quality"""
    checks = {
        'length_ok': 50 <= len(response.split()) <= 500,
        'has_citation': '[' in response and ']' in response,
        'addresses_query': any(word in response.lower() for word in query.lower().split()),
        'no_hallucination': not any(phrase in response for phrase in [
            "I think", "probably", "might be", "I'm not sure"
        ])
    }
    
    quality_score = sum(checks.values()) / len(checks)
    
    return {
        'valid': quality_score >= 0.75,
        'score': quality_score,
        'checks': checks
    }

# Usage
result = rag_system.query(query)
validation = validate_response(result['answer'], query, result['sources'])

if not validation['valid']:
    # Regenerate or flag for review
    result = regenerate_response(query, result['sources'])
```

### 4. Monitoring and Logging

**Track RAG system performance:**
```python
import logging
from datetime import datetime

class RAGMonitor:
    """Monitor RAG system"""
    
    def __init__(self, log_file: str = 'rag_logs.jsonl'):
        self.log_file = log_file
        self.metrics = {
            'total_queries': 0,
            'avg_latency': 0,
            'avg_retrieval_score': 0,
            'cache_hit_rate': 0
        }
    
    def log_query(self, query: str, response: str, 
                  retrieval_scores: List[float], latency: float,
                  cache_hit: bool = False):
        """Log a query"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'query': query,
            'response_length': len(response),
            'retrieval_scores': retrieval_scores,
            'latency_ms': latency * 1000,
            'cache_hit': cache_hit
        }
        
        # Append to log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Update metrics
        self._update_metrics(log_entry)
    
    def _update_metrics(self, entry: Dict):
        """Update running metrics"""
        self.metrics['total_queries'] += 1
        
        # Update averages (simplified)
        n = self.metrics['total_queries']
        self.metrics['avg_latency'] = (
            (self.metrics['avg_latency'] * (n-1) + entry['latency_ms']) / n
        )
        self.metrics['avg_retrieval_score'] = (
            (self.metrics['avg_retrieval_score'] * (n-1) + 
             np.mean(entry['retrieval_scores'])) / n
        )
    
    def get_dashboard(self) -> Dict:
        """Get current metrics"""
        return self.metrics

# Usage
monitor = RAGMonitor()

# In query handler
start_time = time.time()
result = rag_system.query(query)
latency = time.time() - start_time

monitor.log_query(
    query=query,
    response=result['answer'],
    retrieval_scores=[0.85, 0.72, 0.68],
    latency=latency,
    cache_hit=False
)
```

## Troubleshooting Common Issues

### Issue 1: Irrelevant Results

**Symptoms:** Retrieved documents don't match query intent.

**Diagnosis:**
```python
def diagnose_retrieval(query: str, results: List[Dict]) -> str:
    """Diagnose retrieval issues"""
    
    if not results:
        return "No results - check embedding quality or index"
    
    avg_score = np.mean([r['score'] for r in results])
    
    if avg_score < 0.5:
        return "Low similarity scores - try different embedding model"
    
    if len(results) > 10:
        return "Too many results - reduce top_k or increase threshold"
    
    return "Retrieval looks OK - check generation step"
```

**Solutions:**
1. Try different embedding model
2. Adjust chunk size
3. Use query expansion
4. Implement hybrid search
5. Add reranking

### Issue 2: Slow Response Times

**Symptoms:** Queries take > 2 seconds.

**Diagnosis:**
```python
def profile_latency(rag_system, test_queries: List[str]) -> Dict:
    """Profile latency by component"""
    latencies = {
        'embedding': [],
        'retrieval': [],
        'generation': []
    }
    
    for query in test_queries:
        start = time.time()
        embedding = embedder.generate(query)
        latencies['embedding'].append(time.time() - start)
        
        start = time.time()
        results = vector_store.search(embedding, top_k=5)
        latencies['retrieval'].append(time.time() - start)
        
        start = time.time()
        response = generator.generate(query, results)
        latencies['generation'].append(time.time() - start)
    
    return {k: np.mean(v) * 1000 for k, v in latencies.items()}  # ms
```

**Solutions:**
1. Cache embeddings
2. Use smaller embedding model
3. Reduce top_k
4. Use approximate nearest neighbors (ANN)
5. Cache frequent responses
6. Use streaming for generation

### Issue 3: Inconsistent Answers

**Symptoms:** Same query gets different answers.

**Solutions:**
1. Set temperature = 0 for deterministic output
2. Use same system prompt consistently
3. Implement response validation
4. Cache responses for identical queries
5. Use majority voting for critical queries

```python
def consistent_query(rag_system, query: str, n: int = 3) -> str:
    """Get consistent answer via majority voting"""
    responses = []
    
    for _ in range(n):
        result = rag_system.query(query)
        responses.append(result['answer'])
    
    # For critical queries, use LLM to find consensus
    if n > 1:
        prompt = f"""
        Here are {n} answers to the same question:
        
        Question: {query}
        
        Answers:
        1. {responses[0]}
        2. {responses[1]}
        {'3. ' + responses[2] if n > 2 else ''}
        
        Find the common information and provide a consolidated answer.
        """
        return llm.generate(prompt)
    
    return responses[0]
```

### Issue 4: Missing Information

**Symptoms:** "I don't have information about that" for queries that should be answerable.

**Solutions:**
1. Check document coverage
2. Improve chunking (smaller chunks)
3. Use query expansion
4. Increase top_k
5. Lower similarity threshold
6. Add more relevant documents

## Code Example: Production RAG System

```python
from typing import Dict, List, Optional
import time
from dataclasses import dataclass

@dataclass
class RAGConfig:
    chunk_size: int = 400
    chunk_overlap: int = 50
    top_k: int = 5
    similarity_threshold: float = 0.5
    use_cache: bool = True
    use_reranking: bool = True
    temperature: float = 0.0

class ProductionRAG:
    """Production-ready RAG system"""
    
    def __init__(self, config: RAGConfig, api_key: str):
        self.config = config
        self.cache = RAGCache() if config.use_cache else None
        self.monitor = RAGMonitor()
        
        # Initialize components
        self.embedder = EmbeddingGenerator(api_key)
        self.vector_store = FAISSVectorStore()
        self.reranker = CrossEncoderReranker() if config.use_reranking else None
        self.generator = RAGGenerator(temperature=config.temperature)
    
    def index(self, documents: List[Dict]):
        """Index documents"""
        chunker = TextChunker(self.config.chunk_size, self.config.chunk_overlap)
        
        all_chunks = []
        all_metadata = []
        
        for doc in documents:
            chunks = chunker.chunk_recursive(doc['content'])
            all_chunks.extend(chunks)
            all_metadata.extend([
                {**doc.get('metadata', {}), 'chunk_id': i}
                for i in range(len(chunks))
            ])
        
        embeddings = self.embedder.generate_batch(all_chunks)
        self.vector_store.add(embeddings, [
            {'content': c, 'metadata': m} for c, m in zip(all_chunks, all_metadata)
        ])
    
    def query(self, question: str, filters: Dict = None) -> Dict:
        """Query with full production features"""
        start_time = time.time()
        
        # Check cache
        if self.cache:
            cached = self.cache.get(question)
            if cached:
                return {'answer': cached, 'cache_hit': True}
        
        # Preprocess query
        processed_query = preprocess_query(question)
        
        # Generate embedding
        query_embedding = self.embedder.generate(processed_query)
        
        # Retrieve
        raw_results = self.vector_store.search(
            query_embedding, 
            top_k=self.config.top_k * 2 if self.reranker else self.config.top_k,
            filters=filters
        )
        
        # Filter by threshold
        filtered_results = [
            (doc, score) for doc, score in raw_results
            if score >= self.config.similarity_threshold
        ]
        
        # Rerank if enabled
        if self.reranker and filtered_results:
            doc_texts = [doc['content'] for doc, _ in filtered_results]
            top_indices = self.reranker.rerank(
                processed_query, doc_texts, top_k=self.config.top_k
            )
            filtered_results = [filtered_results[i] for i in top_indices]
        
        # Generate response
        documents = [doc for doc, _ in filtered_results]
        scores = [score for _, score in filtered_results]
        
        response = self.generator.generate(processed_query, documents)
        
        # Validate
        validation = validate_response(response, question, documents)
        
        # Log
        latency = time.time() - start_time
        self.monitor.log_query(
            query=question,
            response=response,
            retrieval_scores=scores,
            latency=latency,
            cache_hit=False
        )
        
        # Cache
        if self.cache and validation['valid']:
            self.cache.set(question, response)
        
        return {
            'answer': response,
            'sources': [doc.get('metadata', {}).get('source') for doc in documents],
            'scores': scores,
            'validation': validation,
            'latency_ms': latency * 1000,
            'cache_hit': False
        }

# Usage
config = RAGConfig(
    chunk_size=400,
    top_k=5,
    use_cache=True,
    use_reranking=True,
    temperature=0.0
)

rag = ProductionRAG(config, api_key="your-key")

# Index documents
rag.index(documents)

# Query
result = rag.query("What is our PTO policy?")
print(f"Answer: {result['answer']}")
print(f"Latency: {result['latency_ms']:.2f}ms")
print(f"Validation: {result['validation']['score']:.2f}")
```

## Key Takeaways

- **Optimize chunk size** for your content type (200-500 tokens typical)
- **Use reranking** for better relevance
- **Cache frequently** to reduce latency and costs
- **Preprocess queries** for better retrieval
- **Monitor everything** - latency, quality, usage patterns
- **Validate responses** before returning
- **Troubleshoot systematically** - identify the failing component

## Glossary

- **Reranking:** Re-ordering retrieved results by relevance
- **Cross-Encoder:** Neural model for scoring query-document pairs
- **Cache Hit:** Request served from cache
- **Query Preprocessing:** Cleaning/normalizing queries
- **ANN (Approximate Nearest Neighbors):** Fast approximate search

## Quiz Questions

**1. What is the typical optimal chunk size for RAG?**

A) 50-100 tokens
B) 200-500 tokens
C) 1000-2000 tokens
D) 5000+ tokens

**Correct Answer:** B

**Explanation:** 200-500 tokens balances context preservation with retrieval efficiency.

---

**2. Why use reranking in RAG?**

A) To make responses longer
B) To improve relevance ordering of retrieved documents
C) To reduce costs
D) To speed up retrieval

**Correct Answer:** B

**Explanation:** Reranking uses more sophisticated scoring to ensure the most relevant documents are used for generation.

---

**3. What is the benefit of caching in RAG?**

A) Better accuracy
B) Reduced latency and costs for repeated queries
C) More comprehensive answers
D) Better citations

**Correct Answer:** B

**Explanation:** Caching serves repeated queries instantly without embedding, retrieval, or generation costs.

---

**4. What should you do if retrieval returns irrelevant documents?**

A) Increase chunk size
B) Try a different embedding model or use query expansion
C) Decrease top_k
D) Use a larger LLM

**Correct Answer:** B

**Explanation:** Irrelevant retrieval often indicates embedding-model mismatch or poor query formulation.

---

**5. What temperature setting is best for consistent RAG responses?**

A) 0.0 (deterministic)
B) 0.5 (balanced)
C) 0.7 (creative)
D) 1.0 (maximum creativity)

**Correct Answer:** A

**Explanation:** Temperature 0.0 produces deterministic outputs, ensuring consistent answers for the same query.

---

## Further Reading

- **RAG Optimization Guide** - LangChain: https://blog.langchain.dev/rag-optimization/
- **Advanced RAG Techniques** - LlamaIndex: https://www.llamaindex.ai/blog/advanced-rag
- **Production RAG Systems** - Pinecone: https://www.pinecone.io/learn/production-rag/

---

**🎉 Module 4 Complete!** You've mastered RAG systems. Continue to Module 5 for fine-tuning!
