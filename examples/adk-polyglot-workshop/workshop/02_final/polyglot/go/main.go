package main

import (
	"context"
	"fmt"
	"os"

	"google.golang.org/adk/v2/agent/llmagent"
	"google.golang.org/adk/v2/model/gemini"
	"google.golang.org/adk/v2/tool"
	"google.golang.org/adk/v2/tool/functiontool"
	"google.golang.org/genai"
)

type SLOArgs struct {
	ServiceName string `json:"service_name" jsonschema:"Target microservice name (e.g. checkout-api)."`
}

type SLOResult struct {
	ServiceName  string `json:"service_name"`
	TargetP99Ms  int    `json:"target_p99_ms"`
	GateDecision string `json:"gate_decision"`
}

func LookupSLO(_ tool.Context, args SLOArgs) (SLOResult, error) {
	return SLOResult{ServiceName: args.ServiceName, TargetP99Ms: 250, GateDecision: "APPROVE_DEPLOY"}, nil
}

func BuildRootAgent(ctx context.Context) (llmagent.Agent, error) {
	model, err := gemini.NewModel(ctx, "gemini-3.8-flash", &genai.ClientConfig{APIKey: os.Getenv("GEMINI_API_KEY")})
	if err != nil {
		return nil, err
	}
	sloTool, err := functiontool.New(functiontool.Config{Name: "lookup_service_slo", Description: "Fetches SLO target."}, LookupSLO)
	if err != nil {
		return nil, err
	}
	opsAgent, err := llmagent.New(llmagent.Config{
		Name:        "ops_specialist",
		Model:       model,
		Description: "Audits microservice SLO metrics.",
		Instruction: "Call lookup_service_slo and return gate decision.",
		Tools:       []tool.Tool{sloTool},
	})
	if err != nil {
		return nil, err
	}
	return llmagent.New(llmagent.Config{
		Name:        "sre_coordinator",
		Model:       model,
		Description: "Root Go ADK coordinator.",
		Instruction: "Delegate SLO inspection to ops_specialist.",
		SubAgents:   []llmagent.Agent{opsAgent},
	})
}

func main() {
	fmt.Println("Go ADK (google.golang.org/adk/v2) track ready (02_final).")
}
