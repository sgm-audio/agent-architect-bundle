---
name: audio-embeddings-vector-database-architecture
description: >-
  Use this skill when the user is working on or asking about audio embeddings, vector similarity search for audio, FAISS, ChromaDB for sounds, or audio fingerprinting with embeddings.
version: 1.0.0
---

# Skill: Audio Embeddings & Vector Database Architecture
## 📖 1. Overview
Uses CLAP embeddings to index/search audio semantically ("warm analog bass") via local vector databases for sample libraries and AI-driven curation.
## ⚙️ 2. Core Functionality
- Embedding Extraction: CLAP model → 512-dim vector per audio clip
- Vector Index: FAISS/HNSWlib for fast nearest-neighbor search
- Metadata Tagging: Combine text/audio embeddings for hybrid search
- Local Caching: Pre-compute embeddings, incremental updates
## 📥📤 3. Input/Output Schema
| Inputs | WAV/MP3 files, CLAP model, query text/audio | Outputs | Ranked similarity list, vector DB entries, confidence scores |
## 🏗️ 4. Architecture
`faiss.IndexHNSWFlat` for local search. Pre-compute embeddings on file import. Query: `text_encoder → vector → FAISS.search(k)`.
## 🔗 5. Dependencies
`laion/CLAP`, `faiss-cpu`, `numpy`, `librosa`
## ⚠️ 6. Edge Cases
| Out-Of-Vocabulary Queries | Poor results | Fallback to text metadata matching |
| Embedding Drift | Model updates break index | Version index, recompute on update |
| High-Dim Search Slow | >100k samples latency | Quantize to PQ, reduce dim via PCA |
## 🛡️ 7. Constraints
- Search Latency: < 50ms for 10k samples
- Storage: ~2KB per sample vector
- Memory: FAISS index fits in RAM
## 🤖 8. Usage
- *Prompt:* "Generate a Python script to batch extract CLAP embeddings and build a FAISS HNSW index for a sample library."
## 🧪 9. Testing
- Recall@10 vs ground truth
- Query diversity benchmark
- Incremental add/delete validation
## 📝 10. Best Practices
- Normalize embeddings (`L2`) before indexing
- Store metadata alongside vectors
- Version CLAP model in DB schema
*Skill Version: 1.0.0 | Standards: CLAP, FAISS, HNSW | Domain: Audio AI & ML*