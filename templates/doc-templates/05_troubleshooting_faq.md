# Troubleshooting & Frequently Asked Questions (FAQ)

## Troubleshooting Guide

### Q1. Ollama / LM Studio Connection Failure (`Connection refused`)
- **Cause**: Local server process is not running or the port number is incorrect.
- **Fix**:
  - Ollama: Verify `ollama serve` is running in terminal and `http://localhost:11434` is accessible
  - LM Studio: Check the `Developer` tab to confirm `Local Inference Server` status is `Started` (port: `1234`)

### Q2. Out of Memory (OOM) or Model Loading Failure
- **Cause**: Insufficient RAM capacity.
- **Fix**:
  - For 8GB RAM laptops, use a smaller quantized model such as `gemma4:e2b` or below.
  - Close other resource-heavy applications (browser tabs, additional IDEs).

### Q3. Windows PowerShell Security Error (`Execution_Policies`)
- **Cause**: PowerShell script execution policy restriction.
- **Fix**:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```

---

## Frequently Asked Questions (FAQ)

**Q: What if there is no internet connection on the day of the event?**
A: If you followed the pre-event setup guide and pre-installed models and packages, the workshop runs 100% offline in your local environment.

**Q: I'm an Intel Mac user and model generation is slow in LM Studio.**
A: On Intel Mac, Ollama CLI provides faster inference than LM Studio. Test with `ollama run gemma4:e4b`.
