# ELI5 (Explain Like I'm 5) AI Concept Cheat Sheet

> Workshop Topic: **Multi-Language Agent Systems with Google ADK (Python, Go, Java, Kotlin, TypeScript)**
> Primary Cloud Model: `gemini-3.8-flash` | Flagship Reasoning: `gemini-4-argon` | Local Model: `gemma4:e4b`

This cheat sheet translates core AI engineering concepts into intuitive everyday analogies across a 3-tier framework (Analogy -> Technical Mechanism -> Hands-on Action).

---

## Core Concepts At a Glance

| Concept | Everyday Analogy (Tier 1) | Technical Mechanism (Tier 2) | Hands-on Lab Action (Tier 3) |
| :--- | :--- | :--- | :--- |
| **Local LLM (`gemma4:e4b`)** | Having a personal librarian inside your laptop who works even with Wi-Fi turned off | Quantized model weights executing on local GPU/CPU and serving HTTP on `localhost:11434` | Run `ollama serve` and query local endpoints without cloud latency |
| **Model Quantization (4-bit)** | Packing a winter jacket into a vacuum-sealed travel bag so it fits in a carry-on | Compressing 16-bit floating-point weights into 4-bit integers to reduce RAM usage by ~70% | Use `gemma4:e2b` on 8GB RAM laptops to prevent Out-Of-Memory (OOM) errors |
| **Structured Outputs (JSON Schema)** | Handing someone a tax form with strict boxes instead of a blank sheet of paper | Constraining token sampling to match a typed schema (Pydantic / Zod / Data Class) | Parse LLM responses deterministically in `Lab 02` without regex |
| **RAG (Retrieval-Augmented Generation)** | Taking an open-book exam where you look up the exact page before answering | Retrieving relevant document chunks via embeddings (`gemini-embedding-2`) and injecting them into the prompt | Ground model answers on verified workshop data |
| **Multi-Agent Orchestration (ADK)** | A head chef (`gemini-4-argon`) delegating prep and plating to line cooks (`gemini-3.8-flash`) | `root_agent` routing tasks to specialized `sub_agents` and FunctionTools | Inspect sub-agent delegation and trajectory evaluation in `Lab 02 & Lab 03` |

## References
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Google Agent Development Kit (ADK)](https://adk.dev)
