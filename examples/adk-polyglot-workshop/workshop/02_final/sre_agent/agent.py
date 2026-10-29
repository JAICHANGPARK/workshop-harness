"""
ADK & Google Agents CLI (google-agents-cli) Reference Solution (`agent.py`)
Compatible with:
  - `adk web` / `adk run` / `adk api_server` / `adk eval`
  - `agents-cli eval dataset synthesize` -> `eval run` -> `eval grade` -> `eval optimize`
  - `agents-cli deploy --target agent-runtime` / `agents-cli publish`
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


def verify_release_gate(service_name: str, current_p99_ms: int) -> dict:
    """Evaluates whether a staging deployment satisfies its production SLO gate.

    Args:
        service_name: Target microservice name.
        current_p99_ms: Measured staging P99 latency in milliseconds.
    """
    slo = lookup_service_slo(service_name)
    passed = current_p99_ms <= slo["target_p99_ms"] and slo["error_budget_remaining_pct"] > 10.0
    return {
        "service_name": service_name,
        "current_p99_ms": current_p99_ms,
        "target_p99_ms": slo["target_p99_ms"],
        "gate_decision": "APPROVE_DEPLOY" if passed else "BLOCK_AND_ROLLBACK",
    }


slo_specialist = LlmAgent(
    name="slo_specialist",
    model="gemini-3.8-flash",
    description="Audits microservice SLO metrics and evaluates release readiness gates.",
    instruction="Call lookup_service_slo and verify_release_gate to inspect staging telemetry.",
    tools=[lookup_service_slo, verify_release_gate],
)

report_specialist = LlmAgent(
    name="report_specialist",
    model="gemini-3.8-flash",
    description="Drafts structured SRE deployment gate reports for Gemini Enterprise.",
    instruction="Summarize the release gate decision from slo_specialist into an executive checklist.",
)

root_agent = LlmAgent(
    name="adlc_root_coordinator",
    model="gemini-4-argon",
    description="Root ADK & agents-cli orchestrator that delegates SLO checks and release reporting.",
    instruction="Delegate telemetry checks to slo_specialist and final reporting to report_specialist.",
    sub_agents=[slo_specialist, report_specialist],
)
