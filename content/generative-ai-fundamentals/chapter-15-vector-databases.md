# Chapter 15: Vector Databases and Embeddings

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand how vector embeddings capture meaning
- Compare different vector database options
- Select appropriate embedding models for your use case
- Implement semantic search with vector similarity

## Understanding Vector Embeddings

### What Are Embeddings?

**Embedding:** A numerical representation of data (text, images, etc.) as vectors in high-dimensional space.

**Key Insight:** Similar items have similar vectors (close in vector space).

### Visualizing Embeddings

```
Text → Vector (simplified to 3D for visualization):

"King"   → [0.9, 0.1, 0.8]
"Queen"  → [0.8, 0.2, 0.9]
"Man"    → [0.7, 0.3, 0.2]
"Woman"  → [0.6, 0.4, 0.3]
"Cat"    → [0.2, 0.8, 0.1]
"Dog"    → [0.3, 0.7, 0.2]

In vector space:
- King and Queen are close (related concepts)
- Man and Woman are close (related concepts)
- Cat and Dog are close (both animals)
- King/Queen are far from Cat/Dog (different domains)
```

### Why Embeddings Work

**Semantic Relationships:**
```
Vector arithmetic captures relationships:

King - Man + Woman ≈ Queen

[0.9, 0.1, 0.8] - [0.7, 0.3, 0.2] + [0.6, 0.4, 0.3]
= [0.8, 0.2, 0.9] ≈ Queen's vector
```

**Analogy:** Think of embeddings as a multi-dimensional map where:
- Each dimension represents a concept/feature
- Similar items cluster together
- Relationships can be captured mathematically

### Embedding Dimensions

**Common Dimensions:**
```
- text-embedding-3-small: 1536 dimensions
- text-embedding-3-large: 3072 dimensions
- all-MiniLM-L6-v2: 384 dimensions
- all-mpnet-base-v2: 768 dimensions
```

**Trade-offs:**
| Dimension | Pros | Cons |
|-----------|------|------|
| **Low (100-400)** | Faster, less storage | Less nuanced |
| **Medium (500-1000)** | Good balance | Moderate cost |
| **High (1000+)** | More nuanced representations | Slower, more storage |

## Distance Metrics

How do we measure similarity between vectors?

### 1. Cosine Similarity

**Most common for text embeddings**

```
Measures the angle between vectors (ignores magnitude)

Formula:
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)

Range: -1 to 1
- 1 = identical direction (very similar)
- 0 = orthogonal (unrelated)
- -1 = opposite direction (very different)

Example:
A = [0.5, 0.5, 0.5]
B = [0.4, 0.6, 0.5]

cosine_similarity = 0.99 (very similar)
```

### 2. Euclidean Distance (L2)

```
Straight-line distance between points

Formula:
distance = √(Σ(ai - bi)²)

Range: 0 to ∞
- 0 = identical
- Larger = more different

Example:
A = [1, 2, 3]
B = [2, 3, 4]

euclidean_distance = √3 ≈ 1.73
```

### 3. Dot Product

```
Simple multiplication and sum

Formula:
dot_product = Σ(ai × bi)

Range: -∞ to ∞
- Larger positive = more similar
- Affected by vector magnitude

Example:
A = [0.5, 0.5, 0.5]
B = [0.4, 0.6, 0.5]

dot_product = 0.75
```

### Metric Comparison

| Metric | Best For | Normalization |
|--------|----------|---------------|
| **Cosine** | Text similarity, direction | Yes (magnitude ignored) |
| **Euclidean** | Absolute distance | No |
| **Dot Product** | When magnitude matters | No |

**Recommendation:** Use **cosine similarity** for most text applications.

## Embedding Models

### OpenAI Embeddings

**Models:**
```
text-embedding-3-small:
- Dimensions: 1536
- Performance: Good
- Cost: $0.02 / 1M tokens
- Best for: General purpose

text-embedding-3-large:
- Dimensions: 3072
- Performance: Excellent
- Cost: $0.13 / 1M tokens
- Best for: High-accuracy needs

text-embedding-ada-002:
- Dimensions: 1536
- Performance: Good (older model)
- Cost: $0.10 / 1M tokens
- Best for: Legacy compatibility
```

**Usage:**
```python
from openai import OpenAI

client = OpenAI(api_key="your-key")

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Your text here"
)

embedding = response.data[0].embedding
```

### Sentence Transformers (Hugging Face)

**Popular Models:**
```
all-MiniLM-L6-v2:
- Dimensions: 384
- Speed: Very fast
- Performance: Good for general use
- Local execution (free)

all-mpnet-base-v2:
- Dimensions: 768
- Speed: Moderate
- Performance: Better quality
- Local execution (free)

multi-qa-MiniLM-L6-cos-v1:
- Dimensions: 384
- Optimized for: Question-answer retrieval
```

**Usage:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Single sentence
embedding = model.encode("Hello world")

# Multiple sentences
embeddings = model.encode(["Sentence 1", "Sentence 2"])

# Similarity
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity([embedding1], [embedding2])
```

### Cohere Embeddings

**Models:**
```
embed-english-v3.0:
- Dimensions: 1024
- Languages: English optimized
- Use cases: Search, RAG

embed-multilingual-v3.0:
- Dimensions: 1024
- Languages: 100+ languages
- Use cases: Multilingual applications
```

### Model Comparison

| Model | Dimensions | Speed | Quality | Cost |
|-------|------------|-------|---------|------|
| **OpenAI 3-small** | 1536 | Fast (API) | Good | $ |
| **OpenAI 3-large** | 3072 | Fast (API) | Excellent | $$ |
| **MiniLM-L6-v2** | 384 | Very Fast (local) | Good | Free |
| **mpnet-base-v2** | 768 | Moderate (local) | Better | Free |
| **Cohere v3** | 1024 | Fast (API) | Good | $ |

## Vector Databases

### Why Specialized Databases?

**Problem:** Standard databases are slow at similarity search.

```
Naive approach (SQL):
SELECT * FROM documents
ORDER BY cosine_similarity(embedding, query_vector)
-- O(n) - scans all rows, very slow for large datasets

Vector database:
-- O(log n) using specialized indexes (HNSW, IVF)
-- 1000x faster for million-scale datasets
```

### Vector Database Options

#### 1. Pinecone (Managed)

**Pros:**
- ✅ Fully managed (no infrastructure)
- ✅ Easy setup (minutes)
- ✅ High performance
- ✅ Built-in filtering

**Cons:**
- ❌ Cost at scale
- ❌ Vendor lock-in

**Best For:** Production applications, teams without ML infrastructure expertise

**Pricing:** Free tier available, then usage-based

#### 2. Weaviate (Open Source)

**Pros:**
- ✅ Open source (self-host or managed)
- ✅ GraphQL API
- ✅ Built-in ML models
- ✅ Hybrid search (vector + keyword)

**Cons:**
- ❌ More complex setup
- ❌ Higher resource requirements

**Best For:** Teams wanting flexibility and control

#### 3. Qdrant (Open Source)

**Pros:**
- ✅ Rust-based (fast)
- ✅ Rich filtering
- ✅ Easy deployment
- ✅ Good documentation

**Cons:**
- ❌ Smaller community than some alternatives

**Best For:** Performance-critical applications

#### 4. Milvus (Open Source)

**Pros:**
- ✅ Highly scalable
- ✅ Production-proven
- ✅ Multiple index types
- ✅ Cloud-native

**Cons:**
- ❌ Complex setup
- ❌ Heavy resource requirements

**Best For:** Large-scale enterprise deployments

#### 5. Chroma (Lightweight)

**Pros:**
- ✅ Simple API
- ✅ Easy setup
- ✅ Good for prototyping
- ✅ Python-native

**Cons:**
- ❌ Not designed for large scale
- ❌ Limited production features

**Best For:** Prototyping, small projects

#### 6. FAISS (Library)

**Pros:**
- ✅ Very fast
- ✅ From Facebook Research
- ✅ Multiple index types
- ✅ Free and open source

**Cons:**
- ❌ Not a database (just a library)
- ❌ No persistence built-in
- ❌ Requires custom infrastructure

**Best For:** Building custom solutions, research

### Database Comparison Table

| Database | Type | Setup | Scale | Cost |
|----------|------|-------|-------|------|
| **Pinecone** | Managed | Easy | High | $$ |
| **Weaviate** | OSS/Managed | Medium | High | $ |
| **Qdrant** | OSS/Managed | Medium | High | $ |
| **Milvus** | OSS | Hard | Very High | $ |
| **Chroma** | OSS | Easy | Low-Medium | Free |
| **FAISS** | Library | Medium | High | Free |

## Implementing Semantic Search

### Basic Similarity Search

```python
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SemanticSearch:
    """Basic semantic search implementation"""
    
    def __init__(self, embeddings: List[List[float]], documents: List[str]):
        self.embeddings = np.array(embeddings)
        self.documents = documents
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[tuple]:
        """Find most similar documents"""
        # Calculate cosine similarity
        similarities = cosine_similarity(
            [query_embedding],
            self.embeddings
        )[0]
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Return documents with scores
        results = [
            (self.documents[i], float(similarities[i]))
            for i in top_indices
        ]
        
        return results

# Usage
embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], ...]
documents = ["Doc 1", "Doc 2", ...]

searcher = SemanticSearch(embeddings, documents)
query_embedding = [0.15, 0.25, 0.35]

results = searcher.search(query_embedding, top_k=3)
for doc, score in results:
    print(f"Score: {score:.4f} - {doc}")
```

### Hybrid Search (Vector + Keyword)

```python
from typing import List, Dict, Tuple
from collections import defaultdict

class HybridSearch:
    """Combine vector and keyword search"""
    
    def __init__(self, vector_store, text_index):
        self.vector_store = vector_store
        self.text_index = text_index  # BM25 or similar
    
    def search(self, query: str, query_embedding: List[float], 
               top_k: int = 5, alpha: float = 0.5) -> List[Dict]:
        """
        Hybrid search with weighted combination
        
        alpha: 0 = pure keyword, 1 = pure vector
        """
        # Vector search
        vector_results = self.vector_store.search(
            query_embedding, top_k * 2
        )
        
        # Keyword search
        keyword_results = self.text_index.search(query, top_k * 2)
        
        # Combine scores (reciprocal rank fusion)
        combined_scores = defaultdict(float)
        
        for rank, (doc_id, score) in enumerate(vector_results):
            combined_scores[doc_id] += (1 / (rank + 1)) * (1 - alpha)
        
        for rank, (doc_id, score) in enumerate(keyword_results):
            combined_scores[doc_id] += (1 / (rank + 1)) * alpha
        
        # Sort by combined score
        ranked = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        return ranked[:top_k]

# Usage
hybrid = HybridSearch(vector_store=vs, text_index=bm25)

results = hybrid.search(
    query="machine learning",
    query_embedding=embedding,
    top_k=5,
    alpha=0.7  # 70% vector, 30% keyword
)
```

### Query Optimization Techniques

**1. Query Expansion**
```python
def expand_query(llm, query: str) -> List[str]:
    """Generate query variations"""
    prompt = f"""
    Generate 5 different ways to ask about: "{query}"
    
    Include:
    - Synonyms
    - Related concepts
    - Different phrasings
    """
    response = llm.generate(prompt)
    return response.split('\n')

# Use all variations for retrieval
expanded_queries = expand_query(llm, "Python tutorials")
all_results = []
for q in expanded_queries:
    embedding = embedder.generate(q)
    results = vector_store.search(embedding, top_k=3)
    all_results.extend(results)

# Deduplicate and rerank
final_results = deduplicate_and_rerank(all_results)
```

**2. Metadata Filtering**
```python
# Filter before or after vector search
filtered_results = vector_store.search(
    query_embedding,
    top_k=10,
    filters={
        "date": {"$gte": "2025-01-01"},
        "category": {"$in": ["tutorial", "guide"]},
        "language": "en"
    }
)
```

## Code Example: Complete Vector Search System

```python
import numpy as np
from typing import List, Dict, Tuple
import json

class VectorSearchSystem:
    """Complete vector search implementation"""
    
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.documents: List[Dict] = []
        self.embeddings: List[np.ndarray] = []
        self.metadata_index: Dict[str, List[int]] = defaultdict(list)
    
    def add_documents(self, documents: List[Dict], embeddings: List[List[float]]):
        """Add documents with embeddings"""
        start_idx = len(self.documents)
        
        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            self.documents.append(doc)
            self.embeddings.append(np.array(emb))
            
            # Index metadata for filtering
            for key, value in doc.get('metadata', {}).items():
                self.metadata_index[f"{key}:{value}"].append(start_idx + i)
    
    def search(self, query_embedding: List[float], top_k: int = 5,
               filters: Dict = None) -> List[Tuple[Dict, float]]:
        """Search with optional filtering"""
        query_vec = np.array(query_embedding)
        
        # Calculate similarities
        similarities = []
        for i, emb in enumerate(self.embeddings):
            # Skip if doesn't match filters
            if filters and not self._matches_filters(i, filters):
                continue
            
            sim = cosine_similarity(query_vec, emb)
            similarities.append((i, sim))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k results
        results = [
            (self.documents[i], float(sim))
            for i, sim in similarities[:top_k]
        ]
        
        return results
    
    def _matches_filters(self, doc_idx: int, filters: Dict) -> bool:
        """Check if document matches filter criteria"""
        doc = self.documents[doc_idx]
        metadata = doc.get('metadata', {})
        
        for key, condition in filters.items():
            if key not in metadata:
                return False
            
            if isinstance(condition, dict):
                # Handle operators like $gte, $in
                if '$gte' in condition:
                    if metadata[key] < condition['$gte']:
                        return False
                if '$in' in condition:
                    if metadata[key] not in condition['$in']:
                        return False
            else:
                # Exact match
                if metadata[key] != condition:
                    return False
        
        return True
    
    def save(self, filepath: str):
        """Save index to disk"""
        data = {
            'documents': self.documents,
            'embeddings': [emb.tolist() for emb in self.embeddings],
            'metadata_index': dict(self.metadata_index)
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)
    
    def load(self, filepath: str):
        """Load index from disk"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.documents = data['documents']
        self.embeddings = [np.array(e) for e in data['embeddings']]
        self.metadata_index = defaultdict(list, data['metadata_index'])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Usage
system = VectorSearchSystem(dimension=1536)

# Add documents
documents = [
    {'content': 'Python is a programming language', 'metadata': {'category': 'programming'}},
    {'content': 'Machine learning uses algorithms', 'metadata': {'category': 'ai'}},
    {'content': 'Deep learning is a subset of ML', 'metadata': {'category': 'ai'}}
]
embeddings = embedder.generate_batch([d['content'] for d in documents])

system.add_documents(documents, embeddings)

# Search
query_embedding = embedder.generate("artificial intelligence")
results = system.search(query_embedding, top_k=2)

for doc, score in results:
    print(f"Score: {score:.4f} - {doc['content']}")

# Search with filter
filtered_results = system.search(
    query_embedding,
    top_k=2,
    filters={'category': 'ai'}
)
```

## Key Takeaways

- **Embeddings** represent text as vectors in high-dimensional space
- **Similar vectors** represent similar meanings
- **Cosine similarity** is the most common distance metric for text
- **Vector databases** enable fast similarity search at scale
- **Choose databases** based on scale, budget, and infrastructure needs
- **Hybrid search** combines vector and keyword for better results
- **Query optimization** improves retrieval quality

## Glossary

- **Embedding:** Vector representation of data
- **Cosine Similarity:** Angle-based similarity metric
- **Euclidean Distance:** Straight-line distance
- **Vector Database:** Database optimized for similarity search
- **HNSW:** Hierarchical Navigable Small World (index type)
- **Hybrid Search:** Combining vector and keyword search
- **Query Expansion:** Generating query variations

## Quiz Questions

**1. What do vector embeddings represent?**

A) The length of text
B) The meaning of data in numerical form
C) The number of words
D) The document format

**Correct Answer:** B

**Explanation:** Embeddings capture semantic meaning as vectors in high-dimensional space.

---

**2. Which distance metric is MOST common for text embeddings?**

A) Euclidean distance
B) Manhattan distance
C) Cosine similarity
D) Hamming distance

**Correct Answer:** C

**Explanation:** Cosine similarity measures the angle between vectors, making it ideal for text where direction (meaning) matters more than magnitude.

---

**3. What is the main advantage of vector databases over traditional databases?**

A) They store more data
B) They're cheaper
C) They enable fast similarity search
D) They're easier to use

**Correct Answer:** C

**Explanation:** Vector databases use specialized indexes (HNSW, IVF) that make similarity search 1000x faster than scanning all rows.

---

**4. What does hybrid search combine?**

A) Multiple vector databases
B) Vector similarity and keyword search
C) Different embedding models
D) Multiple queries

**Correct Answer:** B

**Explanation:** Hybrid search combines semantic (vector) similarity with traditional keyword matching for better retrieval quality.

---

**5. Which embedding model is FREE and runs locally?**

A) OpenAI text-embedding-3-small
B) OpenAI text-embedding-3-large
C) Sentence Transformers all-MiniLM-L6-v2
D) Cohere embed-english-v3.0

**Correct Answer:** C

**Explanation:** Sentence Transformers models are open source and run locally without API costs.

---

## Further Reading

- **Sentence Transformers Documentation**: https://www.sbert.net/
- **Pinecone Learning Center**: https://www.pinecone.io/learn/
- **Vector Database Comparison**: https://www.db-engines.com/en/vector-db
- **Embedding Model Benchmark**: https://github.com/mteb/leaderboard

---

**Continue to Chapter 16** to learn RAG optimization and best practices!
