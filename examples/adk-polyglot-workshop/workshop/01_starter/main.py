#!/usr/bin/env python3
"""
Starter Code for Multi-Language Agent Systems with Google ADK (Python, Go, Java, Kotlin, TypeScript)
Primary Cloud Model: gemini-3.8-flash | Local Ollama Model: gemma4:e4b
"""

import os
import json
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class WorkshopTaskResult:
    status: str
    model_used: str
    summary: str
    action_items: List[str]


# =========================================================================
# TODO: [Lab 01 - Exercise] Initialize AI Client & Run Sanity Check
# Hint: Connect to Google GenAI (gemini-3.8-flash) or Local Ollama (gemma4:e4b)
# =========================================================================
def lab1_sanity_check(prompt: str) -> str:
    return f"[Starter Lab 01 Placeholder] Received prompt: {prompt}"


# =========================================================================
# TODO: [Lab 02 - Exercise] Implement Structured Output Schema Parser
# Hint: Parse response into WorkshopTaskResult JSON schema
# =========================================================================
def lab2_structured_output(topic_name: str) -> WorkshopTaskResult:
    return WorkshopTaskResult(
        status="pending",
        model_used="gemini-3.8-flash",
        summary=f"Starter placeholder for {topic_name}",
        action_items=["Complete Lab 01", "Complete Lab 02", "Verify Lab 03 pipeline"],
    )


def main():
    print("Welcome to the Multi-Language Agent Systems with Google ADK (Python, Go, Java, Kotlin, TypeScript) Workshop! Open workshop/03_labs/README.md to begin.")
    msg = lab1_sanity_check("Hello from adk-polyglot-workshop")
    print(msg)
    result = lab2_structured_output("Multi-Language Agent Systems with Google ADK (Python, Go, Java, Kotlin, TypeScript)")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
