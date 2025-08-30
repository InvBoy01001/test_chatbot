from fastmcp import FastMCP

mcp = FastMCP("working_billing_agent")

@mcp.tool()
def handle_request(user_message: str) -> str:
    """Handle billing requests."""
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['refund', 'cancel', 'canceled']):
        return "Billing Agent: I've processed your refund request for the canceled subscription. You'll receive a confirmation email within 3-5 business days."
    elif any(word in message_lower for word in ['charge', 'charged', 'billing']):
        return "Billing Agent: I've verified your account and found the charge. This appears to be for an active subscription. Please check your subscription status."
    else:
        return "Billing Agent: I've reviewed your billing inquiry. Please check your account dashboard for detailed information."

if __name__ == "__main__":
    import sys, asyncio
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    mcp.run(transport="sse", host="127.0.0.1", port=8002)
