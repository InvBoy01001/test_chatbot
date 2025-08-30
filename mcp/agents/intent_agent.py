from fastmcp import FastMCP, Client
from typing import Dict, Any
import json
import subprocess
import sys, asyncio

mcp = FastMCP("intent_agent")

# ------------------------------------------------------------
# Local LLM helper (Ollama CLI)
# ------------------------------------------------------------
def query_local_llm(prompt: str, model: str = "gemma:2b") -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True
        )
        return result.stdout.decode("utf-8").strip()
    except Exception as e:
        return f"Error calling local model: {e}"

# ------------------------------------------------------------
# Intent classification with local LLM
# ------------------------------------------------------------
def classify_intent(user_message: str) -> Dict[str, Any]:
    """Classify user intent using a local LLM model."""
    prompt = f"""
    You are an intent classifier. 
    Analyze the following message and decide the intent.
    Possible intents: Support, Billing, General Inquiry, Human Transfer.
    Return JSON strictly in this format:
    {{
        "intent": "...",
        "confidence": 0.xx,
        "reasoning": "short explanation"
    }}

    Message: "{user_message}"
    """

    response = query_local_llm(prompt)

    # print('\n\n\n')
    # print('response')
    # print(response)
    # print('\n\n\n')

    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        parsed = {
            "intent": "Human Transfer",
            "confidence": 0.5,
            "reasoning": f"Fallback: could not parse model output. Raw response: {response}"
        }

    return parsed

# ------------------------------------------------------------
# FastMCP Tools
# ------------------------------------------------------------
@mcp.tool()
def classify_user_intent(user_message: str) -> Dict[str, Any]:
    """Classify user intent using local LLM."""
    result = classify_intent(user_message)

    # Add routing
    intent = result.get("intent", "Human Transfer")
    if intent == "Support":
        result["route_to"] = "support_agent"
        result["next_action"] = "Route to SupportAgent for technical assistance"
    elif intent == "Billing":
        result["route_to"] = "billing_agent"
        result["next_action"] = "Route to BillingAgent for payment and account issues"
    elif intent == "General Inquiry":
        result["route_to"] = "general_agent"
        result["next_action"] = "Route to GeneralInfoAgent for general questions"
    else:
        result["route_to"] = "human_agent"
        result["next_action"] = "Route to HumanAgent for escalation"

    return result


@mcp.tool()
async def route_conversation(user_message: str) -> Dict[str, Any]:
    """Route conversation to appropriate specialized agent."""
    classification = classify_intent(user_message)
    route_to = classification.get("intent", "Human Transfer")

    # Map intent to agents
    if route_to == "Support":
        agent_key = "support_agent"
    elif route_to == "Billing":
        agent_key = "billing_agent"
    elif route_to == "General Inquiry":
        agent_key = "general_agent"
    else:
        agent_key = "human_agent"

    agent_endpoints = {
        "support_agent": "http://127.0.0.1:8001/sse",
        "billing_agent": "http://127.0.0.1:8002/sse",
        "general_agent": "http://127.0.0.1:8003/sse",
        "human_agent": "http://127.0.0.1:8004/sse"
    }

    if agent_key not in agent_endpoints:
        return {"error": f"Unknown agent: {agent_key}"}

    agent_url = agent_endpoints[agent_key]

    try:
        async with Client(agent_url) as client:
            response = await client.call_tool("handle_request", {"user_message": user_message})

            if hasattr(response, 'structured_content'):
                agent_response = response.structured_content
            elif hasattr(response, 'data'):
                agent_response = response.data
            else:
                agent_response = response

            return {
                "routed_to": agent_key,
                "agent_response": agent_response,
                "status": "success"
            }
    except Exception as e:
        return {
            "routed_to": agent_key,
            "error": str(e),
            "status": "failed",
            "message": f"Failed to communicate with {agent_key}: {str(e)}"
        }

# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    mcp.run(transport="sse", host="127.0.0.1", port=8000)