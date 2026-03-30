# Chapter 14: Building a RAG System

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand RAG system architecture components
- Build document processing pipelines
- Implement retrieval mechanisms
- Create end-to-end RAG applications

## RAG System Architecture

A complete RAG system has two phases: **Indexing** and **Querying**.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PHASE 1: INDEXING (Offline)                                    │
│  ───────────────────────                                        │
│                                                                 │
│  Documents → [Parse] → [Chunk] → [Embed] → [Store]              │
│                                                                 │
│  ─────────────────────────────────────────────────────────      │
│                                                                 │
│  PHASE 2: QUERYING (Online)                                     │
│  ────────────────────────                                       │
│                                                                 │
│  Query → [Embed] → [Search] → [Retrieve] → [Generate] → Answer  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

```
1. Document Parser
   - Extract text from various formats (PDF, DOCX, HTML, etc.)
   - Clean and normalize text

2. Chunking Strategy
   - Split documents into retrievable units
   - Balance context vs. precision

3. Embedding Model
   - Convert text to vector representations
   - Enable semantic similarity search

4. Vector Store
   - Store embeddings for efficient retrieval
   - Support similarity search

5. Retriever
   - Find relevant chunks for queries
   - Rank by relevance

6. Generator (LLM)
   - Synthesize answer from retrieved content
   - Provide citations
```

## Phase 1: Document Processing Pipeline

### Step 1: Document Ingestion

**Supported Formats:**
```
- Plain text (.txt)
- Markdown (.md)
- PDF (.pdf)
- Word documents (.docx)
- HTML (.html)
- JSON (.json)
```

**Code Example: Document Loader**
```python
from pathlib import Path
from typing import List, Dict
import json

class DocumentLoader:
    """Load documents from various formats"""
    
    @staticmethod
    def load_txt(filepath: str) -> str:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def load_json(filepath: str) -> Dict:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def load_directory(dir_path: str, extension: str = '.txt') -> List[Dict]:
        """Load all files with extension from directory"""
        documents = []
        for filepath in Path(dir_path).glob(f'*{extension}'):
            documents.append({
                'content': DocumentLoader.load_txt(str(filepath)),
                'metadata': {
                    'source': str(filepath),
                    'filename': filepath.name
                }
            })
        return documents

# Usage
docs = DocumentLoader.load_directory('./knowledge_base', '.md')
print(f"Loaded {len(docs)} documents")
```

### Step 2: Text Chunking

Split documents into retrievable chunks.

**Chunking Strategies:**

| Strategy | Description | Best For |
|----------|-------------|----------|
| **Fixed-size** | Split by token/character count | Uniform documents |
| **Sentence-based** | Split at sentence boundaries | Preserving meaning |
| **Paragraph-based** | Split at paragraph breaks | Natural sections |
| **Semantic** | Split by topic shifts | Long, diverse documents |
| **Recursive** | Try multiple strategies | General purpose |

**Code Example: Chunking**
```python
from typing import List, Dict

class TextChunker:
    """Split text into retrievable chunks"""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_by_sentences(self, text: str) -> List[str]:
        """Split text into sentence-based chunks"""
        import re
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            current_chunk.append(sentence)
            current_length += len(sentence.split())
            
            if current_length >= self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = current_chunk[-2:]  # Keep overlap
                current_length = sum(len(s.split()) for s in current_chunk)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def chunk_recursive(self, text: str, separators: List[str] = None) -> List[str]:
        """Recursive chunking with multiple separators"""
        if separators is None:
            separators = ['\n\n', '\n', '. ', ' ']
        
        if not separators:
            return [text]
        
        separator = separators[0]
        parts = text.split(separator)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for part in parts:
            part_length = len(part.split())
            
            if current_length + part_length > self.chunk_size:
                if current_chunk:
                    chunks.append(separator.join(current_chunk))
                current_chunk = [part]
                current_length = part_length
            else:
                current_chunk.append(part)
                current_length += part_length
        
        if current_chunk:
            chunks.append(separator.join(current_chunk))
        
        # Recursively chunk if still too large
        if len(separators) > 1:
            final_chunks = []
            for chunk in chunks:
                if len(chunk.split()) > self.chunk_size * 1.2:
                    final_chunks.extend(
                        self.chunk_recursive(chunk, separators[1:])
                    )
                else:
                    final_chunks.append(chunk)
            return final_chunks
        
        return chunks

# Usage
chunker = TextChunker(chunk_size=200, overlap=20)
chunks = chunker.chunk_recursive(long_document)
print(f"Created {len(chunks)} chunks")
```

### Step 3: Embedding Generation

Convert text chunks to vectors.

**Popular Embedding Models:**
```
- OpenAI embeddings (text-embedding-3-small, ada-002)
- Sentence Transformers (all-MiniLM-L6-v2)
- Cohere embeddings
- Hugging Face models
```

**Code Example: Creating Embeddings**
```python
from openai import OpenAI
from typing import List
import numpy as np

class EmbeddingGenerator:
    """Generate embeddings for text"""
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate(self, text: str) -> List[float]:
        """Generate embedding for single text"""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]

# Usage
embedder = EmbeddingGenerator(api_key="your-key")

chunks = ["Chunk 1 text...", "Chunk 2 text...", "Chunk 3 text..."]
embeddings = embedder.generate_batch(chunks)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding dimension: {len(embeddings[0])}")
```

### Step 4: Vector Storage

Store embeddings for efficient retrieval.

**Vector Database Options:**
```
- Pinecone (managed, easy setup)
- Weaviate (open source, feature-rich)
- Milvus (open source, scalable)
- Qdrant (open source, Rust-based)
- FAISS (Facebook library, local)
- Chroma (lightweight, easy)
```

**Code Example: FAISS Vector Store**
```python
import faiss
import numpy as np
from typing import List, Dict, Tuple

class FAISSVectorStore:
    """Simple FAISS-based vector store"""
    
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance
        self.documents: List[Dict] = []
    
    def add(self, embeddings: List[List[float]], documents: List[Dict]):
        """Add embeddings and associated documents"""
        # Convert to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Add to index
        self.index.add(embeddings_array)
        
        # Store documents
        self.documents.extend(documents)
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar embeddings"""
        query_array = np.array([query_embedding]).astype('float32')
        
        # Search
        distances, indices = self.index.search(query_array, top_k)
        
        # Return documents with scores
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                results.append((
                    self.documents[idx],
                    float(distances[0][i])
                ))
        
        return results
    
    def save(self, filepath: str):
        """Save index to disk"""
        faiss.write_index(self.index, filepath)
    
    def load(self, filepath: str):
        """Load index from disk"""
        self.index = faiss.read_index(filepath)

# Usage
vector_store = FAISSVectorStore(dimension=1536)

# Add documents
embeddings = [[0.1] * 1536, [0.2] * 1536, [0.3] * 1536]
documents = [
    {'content': 'Document 1', 'source': 'file1.txt'},
    {'content': 'Document 2', 'source': 'file2.txt'},
    {'content': 'Document 3', 'source': 'file3.txt'}
]

vector_store.add(embeddings, documents)

# Search
query_embedding = [0.15] * 1536
results = vector_store.search(query_embedding, top_k=2)

for doc, score in results:
    print(f"Score: {score:.4f}, Content: {doc['content'][:50]}...")
```

## Phase 2: Querying and Retrieval

### Step 1: Query Processing

```python
class QueryProcessor:
    """Process user queries"""
    
    def __init__(self, embedder):
        self.embedder = embedder
    
    def process(self, query: str) -> List[float]:
        """Convert query to embedding"""
        return self.embedder.generate(query)
    
    def expand_query(self, query: str) -> List[str]:
        """Generate query variations for better retrieval"""
        # Simple expansion: add synonyms
        expansions = [query]
        
        # Add wh-questions
        if not query.startswith(('what', 'how', 'why', 'when', 'where')):
            expansions.append(f"What is {query}?")
            expansions.append(f"How does {query} work?")
        
        return expansions
```

### Step 2: Retrieval Strategies

**1. Similarity Search**
```python
def similarity_search(vector_store, query_embedding, top_k=5):
    """Find most similar documents"""
    return vector_store.search(query_embedding, top_k)
```

**2. Hybrid Search (Similarity + Keyword)**
```python
def hybrid_search(vector_store, text_store, query, query_embedding, top_k=5):
    """Combine semantic and keyword search"""
    # Semantic search
    semantic_results = vector_store.search(query_embedding, top_k * 2)
    
    # Keyword search
    keyword_results = text_store.keyword_search(query, top_k * 2)
    
    # Combine and rerank
    combined = merge_and_rerank(semantic_results, keyword_results)
    return combined[:top_k]
```

**3. Multi-Query Retrieval**
```python
def multi_query_retrieve(llm, vector_store, embedder, query, top_k=5):
    """Generate multiple query variations and retrieve"""
    # Generate variations
    prompt = f"Generate 3 different ways to ask: '{query}'"
    variations = llm.generate(prompt).split('\n')
    
    # Retrieve for each variation
    all_results = []
    for variation in variations:
        embedding = embedder.generate(variation)
        results = vector_store.search(embedding, top_k)
        all_results.extend(results)
    
    # Deduplicate and return top results
    return deduplicate_and_rank(all_results)[:top_k]
```

### Step 3: Response Generation

```python
class RAGGenerator:
    """Generate responses using retrieved context"""
    
    def __init__(self, llm):
        self.llm = llm
    
    def generate(self, query: str, documents: List[Dict]) -> str:
        """Generate response with retrieved context"""
        # Format context
        context = self._format_context(documents)
        
        # Create prompt
        prompt = f"""
Context information from multiple sources:
{context}

Question: {query}

Based on the context above, provide a comprehensive answer.
- Cite sources using [Source: filename]
- If the answer isn't in the context, say so
- Be specific and detailed

Answer:
"""
        
        # Generate response
        return self.llm.generate(prompt)
    
    def _format_context(self, documents: List[Dict]) -> str:
        """Format documents as context"""
        formatted = []
        for i, doc in enumerate(documents):
            source = doc.get('metadata', {}).get('source', 'Unknown')
            formatted.append(f"[Source {i+1}: {source}]\n{doc['content']}")
        return "\n\n".join(formatted)
```

## Complete RAG Implementation

```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class RAGConfig:
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5
    embedding_model: str = "text-embedding-3-small"

class RAGSystem:
    """Complete RAG implementation"""
    
    def __init__(self, config: RAGConfig, api_key: str):
        self.config = config
        
        # Initialize components
        self.chunker = TextChunker(config.chunk_size, config.chunk_overlap)
        self.embedder = EmbeddingGenerator(api_key, config.embedding_model)
        self.vector_store = FAISSVectorStore(dimension=1536)
        self.generator = RAGGenerator(llm=self._create_llm(api_key))
    
    def _create_llm(self, api_key: str):
        """Create LLM client"""
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    
    def index_documents(self, documents: List[Dict]):
        """Index a collection of documents"""
        all_chunks = []
        all_metadata = []
        
        # Chunk all documents
        for doc in documents:
            chunks = self.chunker.chunk_recursive(doc['content'])
            all_chunks.extend(chunks)
            all_metadata.extend([
                {**doc.get('metadata', {}), 'chunk_id': i}
                for i in range(len(chunks))
            ])
        
        # Generate embeddings
        embeddings = self.embedder.generate_batch(all_chunks)
        
        # Store in vector database
        self.vector_store.add(embeddings, [
            {'content': chunk, 'metadata': meta}
            for chunk, meta in zip(all_chunks, all_metadata)
        ])
        
        return len(all_chunks)
    
    def query(self, question: str) -> Dict:
        """Query the RAG system"""
        # Generate query embedding
        query_embedding = self.embedder.generate(question)
        
        # Retrieve relevant documents
        results = self.vector_store.search(query_embedding, self.config.top_k)
        documents = [doc for doc, score in results]
        
        # Generate response
        response = self.generator.generate(question, documents)
        
        return {
            'answer': response,
            'sources': [doc.get('metadata', {}).get('source', 'Unknown') for doc in documents],
            'relevant_chunks': documents
        }


# Usage Example
if __name__ == "__main__":
    # Initialize RAG system
    config = RAGConfig(chunk_size=300, top_k=3)
    rag = RAGSystem(config, api_key="your-openai-key")
    
    # Index documents
    documents = [
        {
            'content': "Our company offers 15 days PTO annually. PTO accrues monthly starting from your first day.",
            'metadata': {'source': 'Employee Handbook'}
        },
        {
            'content': "Health insurance coverage begins on the 1st of the month after 30 days of employment.",
            'metadata': {'source': 'Benefits Guide'}
        }
    ]
    
    num_chunks = rag.index_documents(documents)
    print(f"Indexed {num_chunks} chunks")
    
    # Query
    result = rag.query("When does health insurance start?")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {result['sources']}")
```

## Key Takeaways

- **RAG has two phases:** Indexing (offline) and Querying (online)
- **Document processing** includes parsing, chunking, embedding, and storage
- **Chunking strategy** affects retrieval quality
- **Vector databases** enable efficient similarity search
- **Retrieval strategies** include similarity, hybrid, and multi-query
- **Response generation** synthesizes retrieved context into answers
- **Complete RAG systems** integrate all components seamlessly

## Glossary

- **Indexing:** Preparing documents for retrieval
- **Chunking:** Splitting documents into retrievable units
- **Embedding:** Vector representation of text
- **Vector Store:** Database for storing and searching embeddings
- **Similarity Search:** Finding similar vectors
- **Hybrid Search:** Combining multiple retrieval methods
- **RAG Pipeline:** Complete flow from query to answer

## Quiz Questions

**1. What is the first step in the RAG indexing pipeline?**

A) Generate embeddings
B) Parse and load documents
C) Search for relevant content
D) Generate response

**Correct Answer:** B

**Explanation:** Document parsing/loading is the first step, followed by chunking, embedding, and storage.

---

**2. Why is chunking important in RAG systems?**

A) It makes documents shorter
B) It enables retrieval of relevant portions rather than entire documents
C) It reduces embedding costs
D) It's not important

**Correct Answer:** B

**Explanation:** Chunking allows retrieval of specific relevant sections rather than entire documents, improving precision.

---

**3. What does a vector store do?**

A) Stores raw text documents
B) Stores embeddings and enables similarity search
C) Generates embeddings
D) Creates document chunks

**Correct Answer:** B

**Explanation:** Vector stores store embeddings and provide efficient similarity search capabilities.

---

**4. What is hybrid search?**

A) Using multiple LLMs
B) Combining semantic similarity with keyword search
C) Searching multiple vector stores
D) Using both RAG and fine-tuning

**Correct Answer:** B

**Explanation:** Hybrid search combines semantic (vector) similarity with traditional keyword matching for better retrieval.

---

**5. In what order do RAG querying steps occur?**

A) Generate → Retrieve → Embed → Answer
B) Embed → Retrieve → Generate → Answer
C) Retrieve → Embed → Generate → Answer
D) Answer → Generate → Retrieve → Embed

**Correct Answer:** B

**Explanation:** Query is embedded, used to retrieve documents, then the LLM generates an answer from retrieved content.

---

## Further Reading

- **LangChain RAG Tutorial**: https://python.langchain.com/docs/tutorials/rag/
- **LlamaIndex Documentation**: https://docs.llamaindex.ai/
- **Vector Database Comparison**: https://www.pinecone.io/learn/vector-database/
- **RAG Implementation Guide**: https://www.llamaindex.ai/blog/ultimate-guide-implementing-rag

---

**Continue building!** Chapter 15 covers vector databases and embeddings in depth!
