# ELI5 (Explain Like I'm 5) AI Concept Cheat Sheet

> Workshop Topic: **Local RAG with Gemma 4**
> Primary Cloud Model: `gemma-4-26b-a4b-it` | Flagship Reasoning: `gemma-4-31b-it` | Local Model: `gemma4:e4b`

This cheat sheet translates core AI engineering concepts into intuitive everyday analogies across a 3-tier framework (Analogy -> Technical Mechanism -> Hands-on Action).

---

## Core Concepts At a Glance

| Concept | Everyday Analogy (Tier 1) | Technical Mechanism (Tier 2) | Hands-on Lab Action (Tier 3) |
| :--- | :--- | :--- | :--- |
| **Local LLM (`gemma4:e4b`)** | Having a personal librarian inside your laptop who works even with Wi-Fi turned off | Quantized model weights executing on local GPU/CPU and serving HTTP on `localhost:11434` | Run `ollama serve` and query local endpoints without cloud latency |
| **Model Quantization (4-bit)** | Packing a winter jacket into a vacuum-sealed travel bag so it fits in a carry-on | Compressing 16-bit floating-point weights into 4-bit integers to reduce RAM usage by ~70% | Use `gemma4:e2b` on 8GB RAM laptops to prevent Out-Of-Memory (OOM) errors |
| **Structured Outputs (JSON Schema)** | Handing someone a tax form with strict boxes instead of a blank sheet of paper | Constraining token sampling to match a typed schema (Pydantic / Zod / Data Class) | Parse LLM responses deterministically in `Lab 02` without regex |
| **RAG (Retrieval-Augmented Generation)** | Taking an open-book exam where you look up the exact page before answering | Retrieving relevant document chunks via multimodal embeddings (`gemini-embedding-2` cloud / `embeddinggemma-2` local 768d MRL) and injecting them into the prompt | Ground model answers on verified workshop data |
| **Multi-Agent Orchestration** | A head chef (`gemma-4-31b-it`) delegating prep and plating to line cooks (`gemma-4-26b-a4b-it`) | Coordinator routing tasks to specialized sub-agents and FunctionTools | Inspect sub-agent delegation and trajectory evaluation in `Lab 02 & Lab 03` |

## References
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [OpenAI Platform Documentation](https://platform.openai.com/docs)
- [Google Agent Development Kit (ADK)](https://adk.dev)
