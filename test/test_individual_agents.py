import asyncio
import sys
from fastmcp import Client

# Windows asyncio fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_individual_agents():
    """Test individual agents to debug tool issues."""
    
    print("🔍 Testing Individual Agents for Tool Issues...\n")
    
    agents = [
        ("Support Agent", "http://127.0.0.1:8001/sse"),
        ("Billing Agent", "http://127.0.0.1:8002/sse"),
        ("General Agent", "http://127.0.0.1:8003/sse"),
        ("Human Agent", "http://127.0.0.1:8004/sse")
    ]
    
    for name, url in agents:
        print(f"--- Testing {name} ---")
        try:
            async with Client(url) as client:
                print(f"   ✅ Connected to {name}")
                
                # Try to call the handle_request tool
                try:
                    response = await client.call_tool("handle_request", {"user_message": "test message"})
                    print(f"   ✅ Tool call successful")
                    print(f"   Response: {response}")
                except Exception as e:
                    print(f"   ❌ Tool call failed: {e}")
                    print(f"   Error type: {type(e)}")
                    
                    # Try to list available tools
                    try:
                        print(f"   🔍 Attempting to discover tools...")
                        # This might not work, but let's try
                    except Exception as e2:
                        print(f"   ❌ Tool discovery failed: {e2}")
                        
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_individual_agents())
