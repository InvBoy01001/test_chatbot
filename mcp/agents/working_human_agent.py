from fastmcp import FastMCP

mcp = FastMCP("working_human_agent")

@mcp.tool()
def handle_request(user_message: str) -> str:
    """Handle human transfer requests."""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['legal', 'lawyer', 'terms of service']):
        return "Human Agent: I understand you have a legal question. I'm Sarah Johnson, Senior Support Specialist. I'll be happy to assist you with your legal inquiry. How can I help you today?"
    elif any(word in message_lower for word in ['complaint', 'escalate', 'manager']):
        return "Human Agent: I understand you'd like to escalate this matter. I'm David Thompson, Customer Success Manager. I'm here to help resolve your concern. Please tell me more about the situation."
    else:
        return "Human Agent: Hello! I'm a human agent here to assist you. I understand you need specialized help. How can I assist you today?"

if __name__ == "__main__":
    import sys, asyncio
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    mcp.run(transport="sse", host="127.0.0.1", port=8004)
