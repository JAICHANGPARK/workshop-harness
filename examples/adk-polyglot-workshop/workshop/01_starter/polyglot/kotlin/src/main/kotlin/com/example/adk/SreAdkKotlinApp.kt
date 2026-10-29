package com.example.adk

import com.google.adk.kt.agents.Instruction
import com.google.adk.kt.agents.LlmAgent
import com.google.adk.kt.models.Gemini
import com.google.adk.tools.FunctionTool

data class SloMetrics(val serviceName: String, val targetP99Ms: Int, val gateDecision: String)

fun lookupServiceSlo(serviceName: String): SloMetrics =
    SloMetrics(serviceName = serviceName, targetP99Ms = 250, gateDecision = "APPROVE_DEPLOY")

val opsSpecialist = LlmAgent(
    name = "ops_specialist",
    model = Gemini("gemini-3.8-flash"),
    description = "Monitors service SLO budgets in Kotlin.",
    instruction = Instruction("Use lookupServiceSlo to inspect service health."),
    tools = listOf(FunctionTool.create(::lookupServiceSlo)),
)

val rootAgent = LlmAgent.builder()
    .name("sre_coordinator")
    .model("gemini-4-argon")
    .description("Root Kotlin ADK coordinator.")
    .instruction("Delegate SLO checks to ops_specialist.")
    .subAgents(listOf(opsSpecialist))
    .build()

fun main() {
    println("Initialized Kotlin ADK rootAgent: ${rootAgent.name()}")
}
