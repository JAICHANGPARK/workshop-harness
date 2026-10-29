---
marp: true
theme: default
paginate: true
header: "**adk-polyglot-workshop** | Hands-on Workshop"
footer: "Build with AI / DevFest Technical Workshop"
style: |
  section {
    font-family: 'Inter', -apple-system, sans-serif;
    font-size: 26px;
    padding: 40px 60px;
    background-color: #0f172a;
    color: #f8fafc;
  }
  h1 {
    color: #38bdf8;
    font-size: 44px;
  }
  h2 {
    color: #818cf8;
    font-size: 34px;
    border-bottom: 2px solid #334155;
    padding-bottom: 10px;
  }
  code {
    background: #1e293b;
    color: #38bdf8;
  }
  pre {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
  }
  .badge {
    background: #4f46e5;
    color: white;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 16px;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->
# adk-polyglot-workshop

### Multi-Language Agent Systems with Google ADK (Python, Go, Java, Kotlin, TypeScript)

<span class="badge">Hands-on Technical Lab</span>

**Facilitator**: Workshop Team  
**Event**: Build with AI / Community Coding Session

---

## 📋 Session Agenda & Timeline

* **00:00 - 00:10** (10m) ➔ Welcome & Architecture Overview
* **00:10 - 00:20** (10m) ➔ Environment & Hardware Verification
* **00:20 - 00:45** (25m) ➔ **Lab 01 & Lab 02 Hands-on**
* **00:45 - 01:10** (25m) ➔ **Lab 03 Pipeline & Challenge**
* **01:10 - 01:20** (10m) ➔ Wrap-up, Q&A & Community Resources

<!-- Speaker Notes: Greet attendees, check that everyone is seated and on the workshop Wi-Fi. -->

---

## ⚡ Prerequisites & Environment Check

* **Local Environment Setup**:
  * Run: `./scripts/check_env.sh` (Windows: `.\scripts\check_env.ps1`)
* **Google Colab Fallback (Zero Setup)**:
  * For low-spec laptops or GPU constraints, open the Colab notebook directly:
  * `output/colab/workshop_starter.ipynb`
* **API Keys & Credentials**:
  * Set `GEMINI_API_KEY` or local model server (`localhost:11434`)

<!-- Speaker Notes: Instruct TAs to roam and help attendees whose check_env script reports missing dependencies. -->

---

## 🏗️ Architecture & Core Concepts

```text
+-----------------------+      +-----------------------+      +-----------------------+
|   Attendee Input      | ---> |  Local LLM / Gemini   | ---> |  Structured Result    |
|  (Natural Language)   |      |  (Gemma 4 / Ollama)   |      |  (Pydantic / JSON)    |
+-----------------------+      +-----------------------+      +-----------------------+
                                           |
                                           v
                               +-----------------------+
                               |   Evaluation & Test   |
                               +-----------------------+
```

---

## 🚀 Lab 01: Environment Verification, ADK Scaffolding & Custom Tools

## Objective
Verify your local environment using `./scripts/check_env.sh` and initialize your ADK agent using Google Agent Development Kit (`google-adk` / `google.golang.org/adk/v2` / `com.google.adk:google-adk` / `@google/adk`) with `gemini-3.8-flash`.
## Official Multi-Language ADK Entry Points
- **Python (`google-adk`)**: `workshop/01_starter/sre_agent/agent.py` exposing `root_agent = LlmAgent(...)`
- **Go (`google.golang.org/adk/v2`)**: `llmagent.New`, `functiontool.New`, and `gemini.NewModel`
- **Java (`com.google.adk:google-adk`)**: `LlmAgent.builder()`, `SequentialAgent.builder()`, and `FunctionTool.create()`

```bash
# Run and verify your Lab 01 implementation:
python3 workshop/01_starter/main.py
```

* 💡 **Tip**: Refer to `workshop/02_final/main.py` if you get stuck!
* ☁️ **Colab Badge**: Open in Google Colab for instant GPU execution.

---

## 🚀 Lab 02: Multi-Agent Hierarchy, Sub-Agent Delegation & Structured Outputs

## Objective
Wire specialized sub-agents (`slo_specialist`, `report_specialist`) under a root coordinator (`root_agent` running `gemini-4-argon`) and enforce deterministic JSON schema outputs.
## Instructions
1. Review `prompt-pack/README.md` for the target JSON Schema.
2. In Python (`workshop/01_starter/agent.py`), attach `sub_agents=[slo_specialist, report_specialist]` to `root_agent`.
3. If exploring the Go, Java, Kotlin, or TypeScript tracks under `workshop/02_final/polyglot/`, compare how `SubAgents` / `subAgents` and `SequentialAgent` delegate tasks across languages.

```bash
# Run and verify your Lab 02 implementation:
python3 workshop/01_starter/main.py
```

* 💡 **Tip**: Refer to `workshop/02_final/main.py` if you get stuck!
* ☁️ **Colab Badge**: Open in Google Colab for instant GPU execution.

---

## 🚀 Lab 03: Trajectory Evaluation (adk eval), ADLC Optimization & Deployment

## Objective
Evaluate multi-agent tool trajectories against `evalset.json` (`adk eval` / `agents-cli eval`), run `InMemoryRunner` tests, and prepare for Cloud Run / Vertex AI Agent Engine deployment.
## Instructions
1. Run the reference solution:
   python3 workshop/02_final/main.py
2. Evaluate the ADK agent trajectory against `workshop/02_final/evalset.json`:

```bash
# Run and verify your Lab 03 implementation:
python3 workshop/01_starter/main.py
```

* 💡 **Tip**: Refer to `workshop/02_final/main.py` if you get stuck!
* ☁️ **Colab Badge**: Open in Google Colab for instant GPU execution.

---

## 🚨 Live Troubleshooting & Emergency Fallbacks

| Symptom / Error | Quick 10s Hotfix Command |
| :--- | :--- |
| **Port 11434 Busy** | `pkill ollama && ollama serve &` |
| **OOM / Low RAM** | Fallback to Google Colab Starter Notebook |
| **API Key Missing** | `export GEMINI_API_KEY="YOUR_KEY"` |

👉 Ask roaming TAs for immediate live assistance!

---

<!-- _class: lead -->
# 🎉 Congratulations & Wrap-up!

### You've successfully built and verified the workshop pipeline!

* 📂 **GitHub Repo**: [https://github.com/JAICHANGPARK/adk-polyglot-workshop](https://github.com/JAICHANGPARK/adk-polyglot-workshop)
* 📄 **PDF Handout**: `output/pdf/`
* ☁️ **Colab Notebooks**: `output/colab/`
* 💬 **Feedback & Q&A**: Please take 1 minute to fill out the session survey!
