import asyncio
import sys
from fastmcp import Client

# Windows asyncio fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_minimal_agent():
    """Test the minimal agent."""
    
    print("🔍 Testing Minimal Agent...")
    
    try:
        async with Client("http://127.0.0.1:8005/sse") as client:
            print("✅ Connected to Minimal Agent")
            
            # Test the simple tool
            try:
                response = await client.call_tool("simple_test", {"message": "hello world"})
                print(f"✅ Tool call successful")
                print(f"Response: {response}")
            except Exception as e:
                print(f"❌ Tool call failed: {e}")
                print(f"Error type: {type(e)}")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_minimal_agent())
