---
name: adk-workshop-builder
description: Builds multi-language (Python, TypeScript, Go, Kotlin) autonomous agent and multi-agent system workshops using Google Agent Development Kit (ADK). Generates Coordinator-Worker agent architectures, tool bindings, Human-in-the-Loop (HITL) checkpoints, and trajectory evaluation labs.
---

# Google ADK Workshop Builder Skill

## Purpose

Automates the end-to-end creation of technical hands-on workshops focused on **Google Agent Development Kit (ADK)** and autonomous multi-agent systems. It provides standardized, production-ready curriculum and code skeletons across four major programming language tracks (**Python, TypeScript/JavaScript, Go, Kotlin**), enforcing best practices for agent planning, sub-agent delegation, tool bindings, and state persistence.

> Pre-Flight Web Research Protocol:
> Before generating workshop materials, execute live web searches to verify current ADK SDK package versions and Gemini model tags (`gemini-3.7-flash`, `gemini-3.5-flash`).

---

## Supported Language & SDK Import Matrix

| Language Track | Official SDK Package | Dependency Declaration | Entry Point File |
|---|---|---|---|
| **Python** | `google-genai-adk` / `google-adk` | `uv add google-genai-adk pydantic` | `main.py` |
| **TypeScript / Node.js** | `@google/adk` / `@google/genai-adk` | `npm install @google/adk @google/genai` | `src/index.ts` |
| **Go (Golang)** | `google.golang.org/adk` | `go get google.golang.org/adk@latest` | `main.go` |
| **Kotlin (JVM / Android)** | `com.google.adk:adk-core` | `implementation("com.google.adk:adk-core:1.0.0")` | `src/main/kotlin/Main.kt` |

---

## Core Agentic Architecture Patterns

When generating an ADK workshop, enforce the following three foundational architectural patterns:

### 1. Coordinator-Worker Multi-Agent Delegation Pattern
- **Coordinator (Root Agent)**: Receives user queries, decomposes complex objectives into sub-tasks, and delegates to specialized sub-agents.
- **Specialist Sub-Agents**: Dedicated agents with narrow scopes and custom tools (e.g. `ResearchAgent`, `CodeExecutionAgent`, `ReviewerAgent`).

```text
               +-----------------------------+
               |   User Natural Language     |
               +-----------------------------+
                              |
                              v
               +-----------------------------+
               |  Coordinator Agent (Root)   |
               |  (Gemini 3.7 Flash)         |
               +-----------------------------+
                 /            |            \
                /             |             \
               v              v              v
    +---------------+ +---------------+ +---------------+
    |  Search Agent | |  Coder Agent  | | Review Agent  |
    |  (Tool: Web)  | | (Tool: Exec)  | |(Tool: Linter) |
    +---------------+ +---------------+ +---------------+
```

### 2. Custom Tool Definition & Structured Output Binding
- Define type-safe tools with explicit schema descriptions and parameter validations.
- Use native language constructs: Pydantic V2 (Python), Zod / JSON Schema (TypeScript), Struct tags (Go), Data classes (Kotlin).

### 3. Human-in-the-Loop (HITL) Checkpoint & Interruption
- For state-mutating or sensitive actions (e.g., executing shell commands, database updates, cloud deployments), inject interactive approval breakpoints that pause agent execution until user confirmation.

### 4. Agent Trajectory Evaluation
- Verify agent reasoning paths by recording intermediate tool calls, arguments, and return states against benchmark test suites.

---

## 3-Stage Hands-on Lab Curriculum

```text
+-------------------------------------------------------------------------+
| Lab 01: ADK Single Agent & Custom Tool Binding (20-25 min)              |
| -> Initialize ADK Agent, register custom tools, test structured outputs |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Lab 02: Multi-Agent Orchestration & Sub-Agent Delegation (35-40 min)    |
| -> Build Coordinator Agent and delegate tasks to specialized workers    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
| Lab 03: Human-in-the-Loop Interruption & Trajectory Eval (25-30 min)    |
| -> Implement approval checkpoints and benchmark agent decision paths    |
+-------------------------------------------------------------------------+
```

---

## Multi-Language Implementation Snippets

### 1. Python (`google-genai-adk`)

```python
import os
from google_adk import Agent, Coordinator, tool
from pydantic import BaseModel, Field

# 1. Define custom tool
@tool
def fetch_system_metrics(host: str) -> dict:
    """Fetches real-time CPU and memory metrics for a given host."""
    return {"host": host, "cpu": "24%", "memory_free_gb": 14.2, "status": "healthy"}

# 2. Initialize specialized agent
ops_agent = Agent(
    name="OpsSpecialist",
    model="gemini-3.7-flash",
    instruction="Analyze system metrics and recommend scaling actions.",
    tools=[fetch_system_metrics]
)

# 3. Initialize Coordinator
coordinator = Coordinator(
    name="RootCoordinator",
    model="gemini-3.7-flash",
    instruction="Coordinate infrastructure tasks and delegate to OpsSpecialist.",
    subagents=[ops_agent]
)

# 4. Execute agent loop
response = coordinator.run("Check prod-web-01 server status and summarize findings.")
print(response.output)
```

---

### 2. TypeScript / Node.js (`@google/adk`)

```typescript
import { Agent, Coordinator, defineTool } from '@google/adk';
import { z } from 'zod';

// 1. Define custom tool
const fetchMetricsTool = defineTool({
  name: 'fetchSystemMetrics',
  description: 'Fetches real-time CPU and memory metrics for a given host.',
  parameters: z.object({ host: z.string() }),
  execute: async ({ host }) => ({ host, cpu: '24%', memory_free_gb: 14.2, status: 'healthy' })
});

// 2. Initialize Specialist Agent
const opsAgent = new Agent({
  name: 'OpsSpecialist',
  model: 'gemini-3.7-flash',
  instruction: 'Analyze system metrics and recommend scaling actions.',
  tools: [fetchMetricsTool]
});

// 3. Initialize Coordinator
const coordinator = new Coordinator({
  name: 'RootCoordinator',
  model: 'gemini-3.7-flash',
  instruction: 'Coordinate infrastructure tasks and delegate to OpsSpecialist.',
  subagents: [opsAgent]
});

const result = await coordinator.run('Check prod-web-01 server status and summarize findings.');
console.log(result.output);
```

---

### 3. Go (`google.golang.org/adk`)

```go
package main

import (
	"context"
	"fmt"
	"log"

	"google.golang.org/adk"
)

type ServerMetrics struct {
	Host         string `json:"host"`
	CPU          string `json:"cpu"`
	MemoryFreeGB float64 `json:"memory_free_gb"`
	Status       string `json:"status"`
}

func fetchSystemMetrics(ctx context.Context, host string) (*ServerMetrics, error) {
	return &ServerMetrics{Host: host, CPU: "24%", MemoryFreeGB: 14.2, Status: "healthy"}, nil
}

func main() {
	ctx := context.Background()

	opsAgent, err := adk.NewAgent(&adk.AgentConfig{
		Name:        "OpsSpecialist",
		Model:       "gemini-3.7-flash",
		Instruction: "Analyze system metrics and recommend scaling actions.",
		Tools:       []adk.Tool{adk.NewTool("fetchSystemMetrics", fetchSystemMetrics)},
	})
	if err != nil {
		log.Fatal(err)
	}

	coordinator, err := adk.NewCoordinator(&adk.CoordinatorConfig{
		Name:        "RootCoordinator",
		Model:       "gemini-3.7-flash",
		Instruction: "Coordinate infrastructure tasks and delegate to OpsSpecialist.",
		SubAgents:   []*adk.Agent{opsAgent},
	})
	if err != nil {
		log.Fatal(err)
	}

	res, err := coordinator.Run(ctx, "Check prod-web-01 server status and summarize findings.")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(res.Output)
}
```

---

### 4. Kotlin (`com.google.adk`)

```kotlin
package com.example.adk

import com.google.adk.Agent
import com.google.adk.Coordinator
import com.google.adk.tool

data class ServerMetrics(val host: String, val cpu: String, val memoryFreeGb: Double, val status: String)

val fetchMetricsTool = tool("fetchSystemMetrics", "Fetches real-time server metrics") { host: String ->
    ServerMetrics(host = host, cpu = "24%", memoryFreeGb = 14.2, status = "healthy")
}

fun main() {
    val opsAgent = Agent(
        name = "OpsSpecialist",
        model = "gemini-3.7-flash",
        instruction = "Analyze system metrics and recommend scaling actions.",
        tools = listOf(fetchMetricsTool)
    )

    val coordinator = Coordinator(
        name = "RootCoordinator",
        model = "gemini-3.7-flash",
        instruction = "Coordinate infrastructure tasks and delegate to OpsSpecialist.",
        subagents = listOf(opsAgent)
    )

    val response = coordinator.run("Check prod-web-01 server status and summarize findings.")
    println(response.output)
}
```

---

## ADK Troubleshooting & Hotfix Matrix

| Error Signature | Root Cause | Instant Hotfix / Action |
|---|---|---|
| `RecursionLimitExceeded: Max turns (25) reached` | Circular delegation between sub-agents | Set `max_turns=10` and add strict completion criteria in prompt |
| `ToolSchemaValidationError: Invalid parameter type` | Tool parameter type mismatch | Verify Pydantic V2 / Zod schema types match runtime argument |
| `HumanApprovalTimeoutError` | HITL approval prompt timed out | Extend `approval_timeout_seconds=120` in coordinator configuration |
| `MissingDependency: google-genai-adk` | Virtualenv missing ADK library | Run `uv add google-genai-adk` or `npm install @google/adk` |

---

## References

- **Google Agent Development Kit (ADK)**: [https://cloud.google.com/vertex-ai/docs/agent-development-kit](https://cloud.google.com/vertex-ai/docs/agent-development-kit)
- **Google GenAI SDK Documentation**: [https://ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs)
- **Workshop Harness Repository**: [https://github.com/JAICHANGPARK/workshop-harness](https://github.com/JAICHANGPARK/workshop-harness)
