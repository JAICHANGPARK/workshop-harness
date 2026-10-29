"""
ADK & Google Agents CLI (google-agents-cli) Starter Agent (`agent.py`)
Compatible with:
  - `adk web` / `adk run` / `adk eval`
  - `uvx google-agents-cli setup`
  - `agents-cli eval dataset synthesize` / `agents-cli deploy`
"""
try:
    from google.adk.agents import LlmAgent
except ImportError:
    class LlmAgent:  # Offline fallback stub when google-adk is not yet installed
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)


def lookup_service_slo(service_name: str) -> dict:
    """Returns target SLO latency and remaining error budget for a production microservice.

    Args:
        service_name: Target microservice name (e.g. 'checkout-api', 'auth-service').
    """
    catalog = {
        "checkout-api": {"target_p99_ms": 250, "error_budget_remaining_pct": 42.0, "tier": "critical"},
        "auth-service": {"target_p99_ms": 120, "error_budget_remaining_pct": 88.5, "tier": "critical"},
    }
    return catalog.get(service_name, {"target_p99_ms": 500, "error_budget_remaining_pct": 100.0, "tier": "standard"})


# TODO [Lab 01]: Define specialist sub-agents and register them under `sub_agents=[...]` on `root_agent`
root_agent = LlmAgent(
    name="adk_starter_coordinator",
    model="gemini-3.8-flash",
    description="Starter ADK root_agent entry point for Multi-Language Agent Systems with Google ADK (Python, Go, Java, Kotlin, TypeScript).",
    instruction="Use lookup_service_slo to answer questions about microservice SLOs.",
    tools=[lookup_service_slo],
)
