---
name: offline-protocol-rag
description: Build a keyless, local retrieval layer over a folder of approved documents (policies, protocols, security answers) with MiniLM embeddings and an on-disk Qdrant store, returning the best source file plus score. Use for Security Desk source libraries or any cited-answer lookup where no paid API is allowed.
---

# Offline protocol RAG
Pattern from Sumanth077/Hands-On-AI-Engineering `ai_agents/offline_medical_agent` (MIT per its README). Own implementation, retrieval only. No LLM key needed.

1. `pip install sentence-transformers qdrant-client` (CPU torch is fine, runs in 2 GB RAM).
2. Embed each `.md`/`.txt` in the library with `all-MiniLM-L6-v2` (384 dims). One point per file, payload = title, content, source filename.
3. Store with `QdrantClient(path="./qdrant_data")`, cosine distance. No server process.
4. Query: embed the question, `query_points(limit=3)`. Return source filename and score for every hit.
5. Use top 3, not top 1. Single-file top-1 missed the malaria protocol on "positive rapid test fever chills" (went to pediatric fever, 0.41). Show the score and let the writer step cite the source.
6. Never answer outside retrieved text. If best score < 0.30, say "no approved source found" instead of drafting.
7. Do not import the project's package `__init__` if it pulls a local LLM (llama-cpp). Load the retriever module directly.
