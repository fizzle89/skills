---
name: grounded-retrieval-eval
description: Tiny eval harness for any retrieval step. Fixed question to expected-source pairs, run on every change, report hit@1 and hit@3. Use before trusting a Security Desk or RAG source library.
---

# Grounded retrieval eval
Born from a real miss in offline-protocol-rag (see that skill).

1. Write 5+ pairs: `question -> expected source file`. Include at least one hard pair that shares vocabulary with another document (e.g. malaria test vs fever).
2. Run retrieval with limit 3. Record hit@1, hit@3, and the score of the first hit.
3. Print misses with the top 3 actual sources. Do not average away a miss.
4. Fail the change if hit@3 drops below 100% on the pairs, or a hard pair slips from hit@3.
5. Keep the pairs file beside the library so it grows when a customer question is answered wrong.
