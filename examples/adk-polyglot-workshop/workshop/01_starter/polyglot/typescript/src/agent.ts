import { LlmAgent, FunctionTool } from "@google/adk";
import { z } from "zod";

export const lookupServiceSloTool = new FunctionTool({
  name: "lookup_service_slo",
  description: "Returns target P99 SLO latency for a microservice.",
  parameters: z.object({ serviceName: z.string() }),
  execute: async ({ serviceName }) => ({ serviceName, targetP99Ms: 250, gateDecision: "APPROVE_DEPLOY" }),
});

export const opsSpecialist = new LlmAgent({
  name: "ops_specialist",
  model: "gemini-3.8-flash",
  description: "Audits microservice SLO metrics in TypeScript.",
  instruction: "Call lookup_service_slo and return gate decision.",
  tools: [lookupServiceSloTool],
});

export const rootAgent = new LlmAgent({
  name: "sre_coordinator",
  model: "gemini-4-argon",
  description: "Root TypeScript ADK coordinator.",
  instruction: "Delegate SLO inspection to ops_specialist.",
  subAgents: [opsSpecialist],
});
