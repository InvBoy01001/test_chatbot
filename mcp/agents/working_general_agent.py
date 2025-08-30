from fastmcp import FastMCP

mcp = FastMCP("working_general_agent")

@mcp.tool()
def handle_request(user_message: str) -> str:
    """Handle general information requests."""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['hours', 'business']):
        return "General Agent: Our support team is available 24/7 for urgent technical issues. General inquiries are handled Monday-Friday, 9 AM - 6 PM EST."
    elif any(word in message_lower for word in ['what', 'how', 'when', 'where']):
        return "General Agent: I'd be happy to help with your question. Please provide more specific details so I can assist you better."
    else:
        return "General Agent: Thank you for your inquiry. I'm here to help with general information and questions about our services."

if __name__ == "__main__":
    import sys, asyncio
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    mcp.run(transport="sse", host="127.0.0.1", port=8003)
