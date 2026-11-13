from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from router import LLMRouterOptimizer

app = FastAPI(
    title="LLM Latency & Cost Optimizer Proxy",
    description="Production-grade proxy router for intelligent model selection, token cost minimization, and latency optimization.",
    version="1.0.0"
)

optimizer = LLMRouterOptimizer(cost_threshold_tokens=150)

class OptimizationRequest(BaseModel):
    prompt: str = Field(..., example="Explain quantum computing principles and provide a detailed architectural comparison with classical computing.")
    target_latency_ms: int = Field(1000, description="Maximum acceptable latency SLA in milliseconds")

@app.post("/v1/optimize/route", summary="Route and Optimize LLM Request")
def route_llm_request(payload: OptimizationRequest):
    try:
        result = optimizer.route_and_optimize(
            prompt=payload.prompt,
            target_latency_ms=payload.target_latency_ms
        )
        return {
            "status": "success",
            "routing_decision": result
        }
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
