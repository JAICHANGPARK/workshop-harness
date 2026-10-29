package com.example.adk;

import com.google.adk.agents.BaseAgent;
import com.google.adk.agents.LlmAgent;
import com.google.adk.agents.SequentialAgent;
import com.google.adk.run.InMemoryRunner;
import com.google.adk.tools.FunctionTool;
import java.util.Map;

public final class SreAdkJavaApp {

    public static Map<String, Object> lookupServiceSlo(String serviceName) {
        return Map.of("serviceName", serviceName, "targetP99Ms", 250, "gateDecision", "APPROVE_DEPLOY");
    }

    public static final BaseAgent opsAgent = LlmAgent.builder()
            .name("ops_specialist")
            .model("gemini-3.8-flash")
            .description("Audits microservice SLO metrics in Java.")
            .instruction("Use lookupServiceSlo and store output in telemetry_result.")
            .tools(FunctionTool.create(SreAdkJavaApp.class, "lookupServiceSlo"))
            .outputKey("telemetry_result")
            .build();

    public static final BaseAgent reportAgent = LlmAgent.builder()
            .name("report_writer")
            .model("gemini-3.8-flash")
            .description("Formats SRE deployment gate reports.")
            .instruction("Summarize {telemetry_result} into a release checklist.")
            .build();

    public static final BaseAgent rootAgent = SequentialAgent.builder()
            .name("sre_release_pipeline")
            .description("Java ADK SequentialAgent pipeline.")
            .subAgents(opsAgent, reportAgent)
            .build();

    public static void main(String[] args) {
        InMemoryRunner runner = new InMemoryRunner(rootAgent, "SreAdkJavaApp");
        System.out.println("Initialized Java ADK InMemoryRunner for: " + runner.toString());
    }
}
