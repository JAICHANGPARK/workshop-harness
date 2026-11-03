# Intel Mac (x86_64) Dedicated Preparation & Fallback Guide

> Workshop Topic: **Flutter and Gemma 4 AI Agent**

LM Studio lacks Metal GPU acceleration on Intel CPU-based Macs (`x86_64`) and can freeze during model loading. If you are using an Intel Mac, follow the **Ollama CLI** or **Google Colab Cloud GPU** workflow below.

---

## Option A: Ollama CLI Local Server (Recommended for Local Runs)

1. **Install Ollama**: Download from [https://ollama.com/download/Ollama-darwin.zip](https://ollama.com/download/Ollama-darwin.zip)
2. **Start the Local Server**:
   ```bash
   ollama serve
   ```
3. **Pull a Lightweight Quantized Model** (in a second terminal tab):
   - **8GB RAM Intel Mac**:
     ```bash
     ollama pull gemma4:e2b
     ```
   - **16GB+ RAM Intel Mac**:
     ```bash
     ollama pull gemma4:e4b
     ```
4. **Verify Local API Endpoint**:
   ```bash
   curl http://localhost:11434/api/version
   ```

---

## Option B: Zero-Setup Google Colab Cloud GPU Fallback

If your Intel Mac experiences thermal throttling or high CPU load:
1. Open `output/colab/workshop_starter.ipynb` in **Google Colab**.
2. Add your `GEMINI_API_KEY` (`gemini-3.8-flash`) in Colab Secrets (left sidebar key icon).
3. Run all lab exercises on cloud GPUs with zero local CPU/RAM overhead.

## References
- [Ollama Official Documentation](https://ollama.com)
- [Google AI Studio API Key Setup](https://aistudio.google.com)
