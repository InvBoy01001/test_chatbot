import asyncio
import sys
from fastmcp import Client

# Windows asyncio fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def test_llm_system():
    """Test the LLM-based agentic chatbot system."""
    
    print("=== Testing LLM-Based Agentic Chatbot System ===\n")
    
    # Test cases based on project requirements
    test_cases = [
        {
            "category": "Billing Issue",
            "message": "Why was I charged for a subscription I canceled?",
            "expected_intent": "Billing",
            "description": "User has billing issue with canceled subscription"
        },
        {
            "category": "Technical Support", 
            "message": "My app keeps crashing when I open it.",
            "expected_intent": "Support",
            "description": "User has technical issue with app crashes"
        },
        {
            "category": "Human Transfer",
            "message": "I have a legal question about your terms of service.",
            "expected_intent": "Human Transfer",
            "description": "User has legal question requiring human agent"
        }
    ]
    
    try:
        async with Client("http://127.0.0.1:8000/sse") as client:
            for i, test_case in enumerate(test_cases, 1):
                print(f"--- Test Case {i}: {test_case['category']} ---")
                print(f"Message: '{test_case['message']}'")
                print(f"Expected Intent: {test_case['expected_intent']}")
                print(f"Description: {test_case['description']}")
                
                # Test intent classification
                print("\n1. Testing Intent Classification...")
                try:
                    classification = await client.call_tool("classify_user_intent", {"user_message": test_case['message']})
                    
                    # Access the response data correctly
                    if hasattr(classification, 'structured_content'):
                        intent_data = classification.structured_content
                    elif hasattr(classification, 'data'):
                        intent_data = classification.data
                    else:
                        intent_data = classification
                    
                    print(f"   Intent: {intent_data.get('intent', 'Unknown')}")
                    print(f"   Confidence: {intent_data.get('confidence', 'Unknown')}")
                    print(f"   Route To: {intent_data.get('route_to', 'Unknown')}")
                    
                    # Verify intent matches expectation
                    if intent_data.get('intent') == test_case['expected_intent']:
                        print("   ✅ Intent classification CORRECT")
                    else:
                        print(f"   ❌ Intent classification INCORRECT. Expected: {test_case['expected_intent']}")
                        
                except Exception as e:
                    print(f"   ❌ Intent classification failed: {e}")
                
                # Test conversation routing
                print("\n2. Testing Conversation Routing...")
                try:
                    routing = await client.call_tool("route_conversation", {"user_message": test_case['message']})
                    
                    # Access the response data correctly
                    if hasattr(routing, 'structured_content'):
                        routing_data = routing.structured_content
                    elif hasattr(routing, 'data'):
                        routing_data = routing.data
                    else:
                        routing_data = routing
                    
                    print(f"   Routed To: {routing_data.get('routed_to', 'Unknown')}")
                    print(f"   Status: {routing_data.get('status', 'Unknown')}")
                    
                    if routing_data.get('status') == 'success':
                        print("   ✅ Routing successful")
                        
                        # Show agent response summary
                        agent_response = routing_data.get('agent_response', {})
                        if 'agent' in agent_response:
                            print(f"   Agent: {agent_response['agent']}")
                        if 'summary' in agent_response:
                            print(f"   Summary: {agent_response['summary']}")
                    else:
                        print(f"   ❌ Routing failed: {routing_data.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    print(f"   ❌ Routing failed: {e}")
                
                print("\n" + "="*60 + "\n")
                
    except Exception as e:
        print(f"❌ System test failed: {e}")

async def test_individual_agents():
    """Test individual agents directly."""
    
    print("=== Testing Individual Agents ===\n")
    
    # Test Support Agent
    try:
        async with Client("http://127.0.0.1:8001/sse") as client:
            print("--- Testing Support Agent ---")
            response = await client.call_tool("handle_request", {"user_message": "My app keeps crashing"})
            
            # Access the response data correctly
            if hasattr(response, 'structured_content'):
                response_data = response.structured_content
            elif hasattr(response, 'data'):
                response_data = response.data
            else:
                response_data = response
                
            print(f"Support Agent Response: {response_data.get('summary', 'No summary available')}")
            print("✅ Support Agent working")
    except Exception as e:
        print(f"❌ Support Agent failed: {e}")
    
    # Test Billing Agent
    try:
        async with Client("http://127.0.0.1:8002/sse") as client:
            print("\n--- Testing Billing Agent ---")
            response = await client.call_tool("handle_request", {"user_message": "I need a refund"})
            
            # Access the response data correctly
            if hasattr(response, 'structured_content'):
                response_data = response.structured_content
            elif hasattr(response, 'data'):
                response_data = response.data
            else:
                response_data = response
                
            print(f"Billing Agent Response: {response_data.get('summary', 'No summary available')}")
            print("✅ Billing Agent working")
    except Exception as e:
        print(f"❌ Billing Agent failed: {e}")
    
    # Test General Agent
    try:
        async with Client("http://127.0.0.1:8003/sse") as client:
            print("\n--- Testing General Agent ---")
            response = await client.call_tool("handle_request", {"user_message": "What are your business hours?"})
            
            # Access the response data correctly
            if hasattr(response, 'structured_content'):
                response_data = response.structured_content
            elif hasattr(response, 'data'):
                response_data = response.data
            else:
                response_data = response
                
            print(f"General Agent Response: {response_data.get('summary', 'No summary available')}")
            print("✅ General Agent working")
    except Exception as e:
        print(f"❌ General Agent failed: {e}")
    
    # Test Human Agent
    try:
        async with Client("http://127.0.0.1:8004/sse") as client:
            print("\n--- Testing Human Agent ---")
            response = await client.call_tool("handle_request", {"user_message": "I have a legal question"})
            
            # Access the response data correctly
            if hasattr(response, 'structured_content'):
                response_data = response.structured_content
            elif hasattr(response, 'data'):
                response_data = response.data
            else:
                response_data = response
                
            print(f"Human Agent Response: {response_data.get('summary', 'No summary available')}")
            print("✅ Human Agent working")
    except Exception as e:
        print(f"❌ Human Agent failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting LLM-Based Agentic Chatbot System Tests...\n")
    
    # Test individual agents first
    # asyncio.run(test_individual_agents())
    
    # print("\n" + "="*60 + "\n")
    
    # Test the full system
    asyncio.run(test_llm_system())
    
    print("🎉 All tests completed!")
