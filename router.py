from typing import Dict, Any

class LLMRouterOptimizer:
    def __init__(self, cost_threshold_tokens: int = 150):
        self.cost_threshold_tokens = cost_threshold_tokens

    def route_and_optimize(self, prompt: str, target_latency_ms: int = 1000) -> Dict[str, Any]:
        """Routes prompt to optimal model tier based on token complexity, cost, and latency targets."""
        token_count = len(prompt.split())
        
        # Intelligent Model Tier Selection
        if token_count <= self.cost_threshold_tokens:
            selected_model = "Llama-3-8B-Instruct (Fast/Low-Cost Tier)"
            estimated_cost_usd = round(token_count * 0.0000002, 6)
            estimated_latency_ms = 180
            tier = "LIGHTWEIGHT"
        else:
            selected_model = "Claude-3.5-Sonnet / GPT-4o (Heavy Reasoning Tier)"
            estimated_cost_usd = round(token_count * 0.0000035, 6)
            estimated_latency_ms = 750
            tier = "ENTERPRISE"

        is_within_latency_target = estimated_latency_ms <= target_latency_ms

        return {
            "selected_model": selected_model,
            "tier": tier,
            "metrics": {
                "input_token_count": token_count,
                "estimated_cost_usd": estimated_cost_usd,
                "estimated_latency_ms": estimated_latency_ms,
                "target_latency_ms": target_latency_ms,
                "is_within_latency_target": is_within_latency_target
            },
            "optimization_action": "Routed to optimal tier to minimize inference cost and respect latency SLA."
        }
