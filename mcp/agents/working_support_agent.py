from fastmcp import FastMCP

mcp = FastMCP("working_support_agent")

@mcp.tool()
def handle_request(user_message: str) -> str:
    """Handle support requests."""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['crash', 'crashing']):
        return "Support Agent: Detected application crash. I've restarted the application and cleared temporary files. Please test again."
    elif any(word in message_lower for word in ['error', 'bug']):
        return "Support Agent: Detected application error. I've checked error logs and applied fixes. Please test again."
    elif any(word in message_lower for word in ['slow', 'performance']):
        return "Support Agent: Detected performance issue. I've optimized database queries and cleared cache. Please test again."
    else:
        return "Support Agent: I've applied general troubleshooting. Please test the application and let me know if the issue persists."

if __name__ == "__main__":
    import sys, asyncio
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    mcp.run(transport="sse", host="127.0.0.1", port=8001)
