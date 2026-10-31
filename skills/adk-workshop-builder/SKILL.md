---
name: adk-workshop-builder
description: Builds multi-language (Python, TypeScript, Go, Java/Kotlin) autonomous agent and multi-agent system workshops using Google Agent Development Kit (ADK) and the ADK CLI (adk web, adk run, adk api_server, adk eval, adk deploy). Generates root_agent LlmAgent hierarchies, MCP tool bindings, Human-in-the-Loop tool confirmations, and trajectory evaluation labs.
---

# Google ADK Workshop Builder Skill

## Purpose

Automates the end-to-end creation of technical hands-on workshops focused on **Google Agent Development Kit (ADK)** (`adk.dev` / `google/adk-python`) and autonomous multi-agent systems. It provides standardized, production-ready curriculum, CLI workflows (`adk create`, `adk web`, `adk run`, `adk api_server`, `adk eval`, `adk deploy`), and code skeletons across four major language tracks (**Python, TypeScript/JavaScript, Go, Java/Kotlin**), enforcing best practices for `root_agent` orchestration, sub-agent task delegation, Model Context Protocol (MCP) tool integration, and state persistence.

> Pre-Flight Web Research Protocol:
> Before generating workshop materials, execute live web searches to verify current ADK SDK package versions (`google-adk`, `@google/adk`, `google.golang.org/adk/v2`, `com.google.adk`), CLI flags, and Gemini model tags (`gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.5-flash-lite`).

---

## Supported Language & SDK Import Matrix

| Language Track | Official Repository / Package | Dependency Installation | Required Entry Point | Harness CLI Command |
|---|---|---|---|---|
| **Python** | `google/adk-python` (`google-adk`) | `uv add google-adk google-genai pydantic` | `agent.py` exposing `root_agent` | `python3 harness_cli.py init --name "..." --stack "python,adk"` |
| **Go (Golang)** | `google/adk-go` (`google.golang.org/adk/v2`) | `go get google.golang.org/adk/v2@latest` | `main.go` | `python3 harness_cli.py init --name "..." --stack "go,adk"` |
| **Java 21+** | `google/adk-java` (`com.google.adk:google-adk`) | `implementation 'com.google.adk:google-adk:0.5.0'` | `src/main/java/com/example/adk/AdkWorkshopApp.java` | `python3 harness_cli.py init --name "..." --stack "java,adk"` |
| **Kotlin** | `google/adk-java` (`com.google.adk:google-adk-kotlin-core`) | `implementation("com.google.adk:google-adk-kotlin-core:0.5.0")` | `src/main/kotlin/com/example/adk/AdkWorkshopApp.kt` | `python3 harness_cli.py init --name "..." --stack "kotlin,adk"` |
| **TypeScript / Node.js** | `google/adk-js` (`@google/adk`) | `npm install @google/adk @google/genai zod` | `src/agent.ts` exposing `rootAgent` | `python3 harness_cli.py init --name "..." --stack "typescript,adk"` |
| **Polyglot (All 5 Tracks)** | All Official ADK SDKs | Multi-language workspace (`polyglot/`) | `agent.py` + `polyglot/{go,java,kotlin,typescript}` | `python3 harness_cli.py init --name "..." --stack "adk,polyglot"` |

---

## Official ADK CLI Workflow (`adk`)

Every Python and TypeScript ADK workshop must teach attendees the core `adk` CLI lifecycle commands:

| Command | Default Endpoint / Target | Workshop Usage Purpose |
|---|---|---|
| `adk create <agent_name>` | `./<agent_name>/agent.py` | Scaffolds standard ADK directory (`__init__.py`, `agent.py`, `.env`) |
| `adk run <agent_name>` | Interactive Terminal Loop | Fast CLI sanity check for single/multi-turn prompts and tool traces |
| `adk web` | `http://127.0.0.1:8000` | Launches built-in FastAPI Dev UI to inspect events, state, and agent routing visually |
| `adk api_server` | `http://127.0.0.1:8000/run` | Starts production FastAPI REST server managing users, sessions, and event streams |
| `adk eval <agent_dir> <eval_set.json>` | Local / CI Evaluation | Verifies tool call trajectories (`tool_trajectory_avg_score`) and final response quality |
| `adk deploy` | Vertex AI Agent Runtime / Cloud Run | Containerizes and deploys the verified agent to managed Google Cloud infrastructure |

---

## Core Agentic Architecture Patterns

When generating an ADK workshop, enforce the following four foundational architectural patterns:

### 1. Root Agent & Sub-Agent Delegation Pattern (`root_agent` + `sub_agents`)
- **Mandatory `root_agent` Variable**: In `google-adk`, the top-level orchestrator in `agent.py` must be assigned to the variable name `root_agent` so `adk web`, `adk run`, and `adk api_server` can discover it automatically.
- **Routing via `description`**: The root `LlmAgent` (or `SequentialAgent` / `ParallelAgent`) inspects each child agent's `description` field in `sub_agents=[...]` to dynamically delegate tasks.

```mermaid
flowchart TD
    User["Attendee Prompt (adk web / adk run)"] --> RootAgent["root_agent: LlmAgent<br>(Model: gemini-4-argon)"]
    RootAgent -->|"Delegates via description"| ResearchAgent["researcher: LlmAgent<br>(Model: gemini-3.8-flash)"]
    RootAgent -->|"Delegates via description"| OpsAgent["ops_specialist: LlmAgent<br>(Model: gemini-3.8-flash)"]
    OpsAgent -->|"Tool Confirmation (HITL)"| ToolExec["Custom Function / MCP Tool"]
```

### 2. Custom Function Tools & MCP Toolset Integration
- **Python Function Tools**: Plain Python functions with clear type annotations and docstrings (parsed automatically by ADK to construct the JSON schema for Gemini).
- **MCP Integration (`MCPToolset`)**: Connect external Model Context Protocol servers directly into ADK agents for standardized tool discovery.

### 3. Human-in-the-Loop (HITL) Tool Confirmation
- For state-mutating or sensitive operations (e.g., cloud scaling, database writes, external API mutations), configure ADK Tool Confirmation or `before_tool_callback` hooks to require explicit human approval in `adk web` before tool execution proceeds.

### 4. Agent Trajectory & Response Evaluation (`adk eval`)
- Author `evalset.json` and `test_config.json` files to assert both **Trajectory Accuracy** (exact sequence of delegated sub-agents and tool calls) and **Response Match Score**.

---

## 3-Stage Hands-on Lab Curriculum

```mermaid
flowchart TD
    Lab1["Lab 01: ADK Scaffolding, Custom Tools & Dev UI (20-25 min)<br>Run adk create, define root_agent with Python tools, inspect events in adk web"]
    Lab2["Lab 02: Multi-Agent Hierarchy & Workflow Agents (35-40 min)<br>Combine LlmAgent sub_agents, SequentialAgent, ParallelAgent, and Session State"]
    Lab3["Lab 03: HITL Tool Callbacks, adk eval & API Serving (25-30 min)<br>Add before_tool_callback guardrails, run adk eval on trajectories, serve via adk api_server"]

    Lab1 --> Lab2 --> Lab3
```

---

## Multi-Language Implementation Snippets

### 1. Python (`google-adk` - `agent.py`)

```python
from google.adk.agents import LlmAgent, SequentialAgent

# 1. Define a type-annotated tool function (docstring is required for ADK schema generation)
def fetch_system_metrics(host: str) -> dict:
    """Fetches real-time CPU and memory metrics for a given server hostname.

    Args:
        host: Target server hostname (e.g., 'prod-web-01').
    """
    return {
        "host": host,
        "cpu_usage_percent": 24.5,
        "memory_free_gb": 14.2,
        "status": "healthy",
    }

# 2. Define specialized Sub-Agents
ops_specialist = LlmAgent(
    name="ops_specialist",
    model="gemini-3.8-flash",
    description="Monitors infrastructure hosts, fetches system metrics, and diagnoses server health.",
    instruction="Use fetch_system_metrics to inspect the requested host and report anomalies.",
    tools=[fetch_system_metrics],
)

report_writer = LlmAgent(
    name="report_writer",
    model="gemini-3.8-flash",
    description="Drafts concise SRE incident summaries and scaling recommendations.",
    instruction="Summarize telemetry findings from ops_specialist into an actionable SRE checklist.",
)

# 3. Define mandatory root_agent entry point for `adk web` and `adk run`
root_agent = LlmAgent(
    name="sre_coordinator",
    model="gemini-4-argon",
    description="Root SRE orchestrator that delegates monitoring and reporting across sub-agents.",
    instruction=(
        "You are the lead SRE Coordinator. "
        "Delegate host health checks to 'ops_specialist' and summary drafting to 'report_writer'."
    ),
    sub_agents=[ops_specialist, report_writer],
)
```

---

### 2. TypeScript / Node.js (`@google/adk`)

```typescript
import { LlmAgent, FunctionTool } from '@google/adk';
import { z } from 'zod';

const fetchMetricsTool = new FunctionTool({
  name: 'fetch_system_metrics',
  description: 'Fetches real-time CPU and memory metrics for a given server hostname.',
  parameters: z.object({
    host: z.string().describe('Target server hostname, e.g. prod-web-01'),
  }),
  execute: async ({ host }) => ({
    host,
    cpu_usage_percent: 24.5,
    memory_free_gb: 14.2,
    status: 'healthy',
  }),
});

const opsSpecialist = new LlmAgent({
  name: 'ops_specialist',
  model: 'gemini-3.8-flash',
  description: 'Monitors infrastructure hosts and diagnoses server health.',
  instruction: 'Call fetch_system_metrics for the requested host and return the status.',
  tools: [fetchMetricsTool],
});

export const rootAgent = new LlmAgent({
  name: 'sre_coordinator',
  model: 'gemini-4-argon',
  description: 'Root SRE orchestrator that coordinates sub-agents.',
  instruction: 'Delegate telemetry checks to ops_specialist and synthesize the final answer.',
  subAgents: [opsSpecialist],
});
```

---

### 3. Go (`google.golang.org/adk/v2`)

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"google.golang.org/adk/v2/agent/llmagent"
	"google.golang.org/adk/v2/model/gemini"
	"google.golang.org/adk/v2/runner"
	"google.golang.org/adk/v2/session"
	"google.golang.org/adk/v2/tool"
	"google.golang.org/adk/v2/tool/functiontool"
	"google.golang.org/genai"
)

type ServerMetricsArgs struct {
	Host string `json:"host" jsonschema:"Target server hostname (e.g. prod-web-01)."`
}

type ServerMetricsResult struct {
	Host         string  `json:"host"`
	CPU          string  `json:"cpu"`
	MemoryFreeGB float64 `json:"memory_free_gb"`
	Status       string  `json:"status"`
}

func FetchSystemMetrics(_ tool.Context, args ServerMetricsArgs) (ServerMetricsResult, error) {
	return ServerMetricsResult{
		Host:         args.Host,
		CPU:          "24.5%",
		MemoryFreeGB: 14.2,
		Status:       "healthy",
	}, nil
}

func main() {
	ctx := context.Background()

	model, err := gemini.NewModel(ctx, "gemini-3.8-flash", &genai.ClientConfig{
		APIKey: os.Getenv("GEMINI_API_KEY"),
	})
	if err != nil {
		log.Fatal(err)
	}

	metricsTool, err := functiontool.New(
		functiontool.Config{
			Name:        "fetch_system_metrics",
			Description: "Fetches real-time CPU and memory metrics for a server host.",
		},
		FetchSystemMetrics,
	)
	if err != nil {
		log.Fatal(err)
	}

	opsAgent, err := llmagent.New(llmagent.Config{
		Name:        "ops_specialist",
		Model:       model,
		Description: "Monitors infrastructure hosts and fetches system metrics.",
		Instruction: "Analyze system metrics and recommend scaling actions.",
		Tools:       []tool.Tool{metricsTool},
	})
	if err != nil {
		log.Fatal(err)
	}

	rootAgent, err := llmagent.New(llmagent.Config{
		Name:        "sre_coordinator",
		Model:       model,
		Description: "Root SRE coordinator agent.",
		Instruction: "Coordinate infrastructure tasks and delegate to ops_specialist.",
		SubAgents:   []llmagent.Agent{opsAgent},
	})
	if err != nil {
		log.Fatal(err)
	}

	sessionService := session.InMemoryService()
	r, err := runner.New(runner.Config{
		AppName:        "sre_adk_go_app",
		Agent:          rootAgent,
		SessionService: sessionService,
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Initialized Go ADK Runner: %v\n", r)
}
```

---

### 4. Java 21+ (`com.google.adk:google-adk`)

```java
package com.example.adk;

import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.run.InMemoryRunner;
import com.google.adk.sessions.Session;
import com.google.adk.tools.FunctionTool;
import java.util.Map;

public final class SreAdkJavaApp {

    public static Map<String, Object> fetchSystemMetrics(String host) {
        return Map.of(
            "host", host,
            "cpu", "24.5%",
            "memoryFreeGb", 14.2,
            "status", "healthy"
        );
    }

    public static final BaseAgent opsAgent = LlmAgent.builder()
            .name("ops_specialist")
            .model("gemini-3.8-flash")
            .description("Monitors infrastructure hosts and fetches system metrics.")
            .instruction("Call fetchSystemMetrics for the target host and store output.")
            .tools(FunctionTool.create(SreAdkJavaApp.class, "fetchSystemMetrics"))
            .outputKey("telemetry_result")
            .build();

    public static final BaseAgent reportAgent = LlmAgent.builder()
            .name("report_writer")
            .model("gemini-3.8-flash")
            .description("Drafts SRE deployment gate reports.")
            .instruction("Summarize {telemetry_result} into an executive checklist.")
            .build();

    public static final BaseAgent rootAgent = SequentialAgent.builder()
            .name("sre_coordinator_pipeline")
            .description("Sequential Java ADK pipeline for telemetry and reporting.")
            .subAgents(opsAgent, reportAgent)
            .build();

    public static void main(String[] args) {
        InMemoryRunner runner = new InMemoryRunner(rootAgent, "SreAdkJavaApp");
        Session session = runner.sessionService().createSession("SreAdkJavaApp", "user-01").blockingGet();
        System.out.println("Created Java ADK session: " + session.id());
    }
}
```

---

### 5. Kotlin (`com.google.adk:google-adk-kotlin-core` / `com.google.adk:google-adk`)

```kotlin
package com.example.adk

import com.google.adk.kt.agents.Instruction
import com.google.adk.kt.agents.LlmAgent
import com.google.adk.kt.models.Gemini
import com.google.adk.tools.FunctionTool

data class ServerMetrics(val host: String, val cpu: String, val memoryFreeGb: Double, val status: String)

fun fetchSystemMetrics(host: String): ServerMetrics {
    return ServerMetrics(host = host, cpu = "24.5%", memoryFreeGb = 14.2, status = "healthy")
}

fun main() {
    val opsAgent = LlmAgent(
        name = "ops_specialist",
        model = Gemini("gemini-3.8-flash"),
        description = "Monitors infrastructure hosts and fetches system metrics.",
        instruction = Instruction("Analyze system metrics and recommend scaling actions."),
        tools = listOf(FunctionTool.create(::fetchSystemMetrics)),
    )

    val rootAgent = LlmAgent.builder()
        .name("sre_coordinator")
        .model("gemini-4-argon")
        .description("Root SRE coordinator agent.")
        .instruction("Coordinate infrastructure tasks and delegate to ops_specialist.")
        .subAgents(listOf(opsAgent))
        .build()

    println("Initialized Kotlin ADK rootAgent: ${rootAgent.name()}")
}
```

---

## ADK Troubleshooting & Hotfix Matrix

| Error Signature | Root Cause | Instant Hotfix / Action |
|---|---|---|
| `ValueError: No root_agent found in agent.py` | Missing `root_agent` variable name | Ensure top-level agent instance in `agent.py` is named exactly `root_agent` |
| `ValueError: Tool function must have a docstring` | Python function passed to `tools=[]` lacks docstring | Add a descriptive docstring and parameter type annotations to the tool function |
| `Address already in use: 127.0.0.1:8000` | Previous `adk web` or `adk api_server` process active | Run `adk web --port 8080` or terminate old process on port 8000 |
| `MissingDependency: google-adk` | Virtualenv missing ADK library | Run `uv add google-adk` or `pip install google-adk` |

---

## Typography, Developer Terminology & Bilingual Notation Rules

- **Developer-Friendly Terminology & English Original Notation (영어 원문 병기 & 직역 금지)**:
  - Never use awkward literal translations (e.g., never write "손으로 하는 실험실", "달리는 책", "발판 설치", "생각 예산", "도구 부르기").
  - Always use developer-friendly terminology commonly used by real-world software engineers AND include the original English technical term in parentheses (`개발자 친화적 용어 (English Original)`), such as:
    - **핸즈온 랩 (Hands-on Lab)**, **스캐폴딩 (Scaffolding)**, **런북 (Runbook)**, **프롬프트 엔지니어링 (Prompt Engineering)**, **구조화 출력 (Structured Outputs / JSON Schema)**, **툴 콜링 / 함수 호출 (Tool Calling / Function Calling)**, **검색 증강 생성 (RAG, Retrieval-Augmented Generation)**, **임베딩 (Embedding)**, **양자화 (Quantization)**, **추론 예산 (Thinking Budget)**, **멀티 에이전트 오케스트레이션 (Multi-Agent Orchestration)**, **서브 에이전트 위임 (Sub-Agent Delegation)**, **궤적 평가 (Trajectory Evaluation)**, **의존성 주입 (Dependency Injection)**, **폴백 (Fallback)**, **스모크 테스트 (Smoke Test)**, **보일러플레이트 코드 (Boilerplate Code)**.
  - In **code comments and docstrings**, keep SDK identifiers (`root_agent`, `LlmAgent`, `FunctionTool`, `thinking_budget`, `response_schema`) in exact English and pair localized explanations with the original English technical term in parentheses.
- **No Em Dash (`\u2014`)**: Never generate em dash characters (`\u2014`) in any generated documentation, markdown (`.md`) files, slide decks, setup guides, code comments, or runbooks. Always use standard hyphens (`-`), colons (`:`), or parentheses `()` instead.
- **Automated Verification**: Run `python3 harness_cli.py audit-typography --target <dir> --fix` or `python3 harness_cli.py test --target <dir>` to verify zero em dashes and zero awkward literal translations across all generated files.

---

## References

- **Official ADK Documentation**: [https://adk.dev](https://adk.dev)
- **Google ADK Python Repository**: [https://github.com/google/adk-python](https://github.com/google/adk-python)
- **Google Cloud Agent Development Kit**: [https://cloud.google.com/vertex-ai/docs/agent-development-kit](https://cloud.google.com/vertex-ai/docs/agent-development-kit)
- **Google Agents CLI (`google/agents-cli`)**: [https://github.com/google/agents-cli](https://github.com/google/agents-cli)
- **Workshop Harness Repository**: [https://github.com/JAICHANGPARK/workshop-harness](https://github.com/JAICHANGPARK/workshop-harness)
