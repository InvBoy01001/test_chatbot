import asyncio
import sys
from fastmcp import Client

# Windows asyncio fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_simple():
    """Simple test to debug tool calling."""
    
    print("🔍 Testing Simple Tool Calls...")
    
    try:
        async with Client("http://127.0.0.1:8000/sse") as client:
            print("✅ Connected to Intent Agent")
            
            # Test 1: Simple intent classification
            print("\n🎯 Testing intent classification...")
            try:
                result = await client.call_tool("classify_user_intent", {"user_message": "My app is crashing"})
                print(f"   ✅ Intent classification successful")
                print(f"   Response type: {type(result)}")
                print(f"   Response: {result}")
                
                # Try to access the data
                if hasattr(result, 'structured_content'):
                    print(f"   Structured content: {result.structured_content}")
                if hasattr(result, 'data'):
                    print(f"   Data: {result.data}")
                    
            except Exception as e:
                print(f"   ❌ Intent classification failed: {e}")
                print(f"   Error type: {type(e)}")
            
            # Test 2: Try routing
            print("\n🔄 Testing conversation routing...")
            try:
                result = await client.call_tool("route_conversation", {"user_message": "My app is crashing"})
                print(f"   ✅ Routing successful")
                print(f"   Response type: {type(result)}")
                print(f"   Response: {result}")
            except Exception as e:
                print(f"   ❌ Routing failed: {e}")
                print(f"   Error type: {type(e)}")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    print("Starting test...")
    asyncio.run(test_simple())
    print("Test completed.")
