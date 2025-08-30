import asyncio
import sys
from fastmcp import Client

# Windows asyncio fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def get_response_data(response):
    """Helper function to extract data from FastMCP response."""
    if hasattr(response, 'structured_content'):
        return response.structured_content
    elif hasattr(response, 'data'):
        return response.data
    else:
        return response

async def interactive_demo():
    """Interactive demo of the LLM-based agentic chatbot system."""
    
    print("🤖 LLM-Based Agentic Chatbot System Demo")
    print("=" * 50)
    print("This demo simulates the system described in project_info.txt")
    print("Type 'quit' to exit, 'help' for examples\n")
    
    try:
        async with Client("http://127.0.0.1:8000/sse") as client:
            while True:
                # Get user input
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() == 'quit':
                    print("👋 Goodbye!")
                    break
                    
                if user_input.lower() == 'help':
                    print("\n📚 Example messages to test:")
                    print("• 'My app keeps crashing when I open it' (Support)")
                    print("• 'Why was I charged for a subscription I canceled?' (Billing)")
                    print("• 'What are your business hours?' (General Inquiry)")
                    print("• 'I have a legal question about your terms of service' (Human Transfer)")
                    print("• 'The system is very slow and keeps giving me database errors' (Support)")
                    print("• 'I need a refund for the charge that was made yesterday' (Billing)")
                    continue
                
                if not user_input:
                    continue
                
                print("\n🔍 Analyzing your message...")
                
                # Step 1: Intent Classification
                try:
                    print("1️⃣ Classifying intent...")
                    classification = await client.call_tool("classify_user_intent", {"user_message": user_input})
                    
                    intent_info = get_response_data(classification)
                    print(f"   🎯 Intent: {intent_info.get('intent', 'Unknown')}")
                    print(f"   📊 Confidence: {intent_info.get('confidence', 'Unknown')}")
                    print(f"   🚀 Route To: {intent_info.get('route_to', 'Unknown')}")
                    print(f"   📋 Next Action: {intent_info.get('next_action', 'Unknown')}")
                    
                    # Show confidence scores for all intents
                    if 'all_scores' in intent_info:
                        print("   📈 All Intent Scores:")
                        for intent, score in intent_info['all_scores'].items():
                            print(f"      {intent}: {score:.2f}")
                    
                except Exception as e:
                    print(f"   ❌ Intent classification failed: {e}")
                    continue
                
                # Step 2: Conversation Routing
                try:
                    print("\n2️⃣ Routing conversation...")
                    routing = await client.call_tool("route_conversation", {"user_message": user_input})
                    
                    routing_info = get_response_data(routing)
                    print(f"   📍 Routed To: {routing_info.get('routed_to', 'Unknown')}")
                    print(f"   ✅ Status: {routing_info.get('status', 'Unknown')}")
                    
                    if routing_info.get('status') == 'success':
                        # Show agent response
                        agent_response = routing_info.get('agent_response', {})
                        print(f"\n🤖 {agent_response.get('agent', 'Unknown Agent')} Response:")
                        print(f"   📝 Summary: {agent_response.get('summary', 'No summary available')}")
                        
                        # Show detailed response based on agent type
                        if agent_response.get('agent') == 'SupportAgent':
                            if 'diagnosis' in agent_response:
                                diag = agent_response['diagnosis']
                                print(f"   🔍 Issue Type: {diag.get('issue_type', 'Unknown')}")
                                print(f"   ⚠️  Severity: {diag.get('severity', 'Unknown')}")
                                print(f"   📋 Diagnosis: {diag.get('diagnosis', 'No diagnosis')}")
                            
                            if 'troubleshooting' in agent_response:
                                ts = agent_response['troubleshooting']
                                print(f"   🛠️  Status: {ts.get('current_status', 'Unknown')}")
                                print(f"   ⏱️  Resolution Time: {ts.get('estimated_resolution_time', 'Unknown')}")
                                
                        elif agent_response.get('agent') == 'BillingAgent':
                            if 'account_verification' in agent_response:
                                ver = agent_response['account_verification']
                                print(f"   🔐 Account Status: {ver.get('account_status', 'Unknown')}")
                                print(f"   📋 Verification Steps: {len(ver.get('verification_steps', []))} completed")
                                
                            if 'payment_processing' in agent_response:
                                proc = agent_response['payment_processing']
                                print(f"   💳 Transaction: {proc.get('transaction_type', 'Unknown')}")
                                print(f"   💰 Amount: {proc.get('amount', 'Unknown')}")
                                print(f"   📊 Status: {proc.get('status', 'Unknown')}")
                                
                        elif agent_response.get('agent') == 'GeneralInfoAgent':
                            if 'answer' in agent_response:
                                ans = agent_response['answer']
                                print(f"   📚 Category: {ans.get('category', 'Unknown')}")
                                print(f"   🎯 Confidence: {ans.get('confidence', 'Unknown')}")
                                print(f"   💡 Answer: {ans.get('answer', 'No answer available')}")
                                
                        elif agent_response.get('agent') == 'HumanAgent':
                            if 'transfer_details' in agent_response:
                                trans = agent_response['transfer_details']
                                print(f"   👤 Agent Assigned: {trans.get('agent_assigned', 'Unknown')}")
                                print(f"   ⏰ Wait Time: {trans.get('estimated_wait_time', 'Unknown')}")
                                print(f"   🎯 Priority: {trans.get('priority_level', 'Unknown')}")
                            
                            if 'human_agent_message' in agent_response:
                                print(f"   💬 Human Agent: {agent_response['human_agent_message']}")
                        
                        print(f"\n   📋 Next Steps: {agent_response.get('next_steps', 'No next steps')}")
                        
                    else:
                        print(f"   ❌ Routing failed: {routing_info.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    print(f"   ❌ Routing failed: {e}")
                
                print("\n" + "─" * 50)
                
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure all agents are running on their respective ports.")

if __name__ == "__main__":
    print("🚀 Starting Interactive Demo...")
    print("Make sure you have started all agents:")
    print("• Intent Agent: python intent_agent.py (port 8000)")
    print("• Support Agent: python support_agent.py (port 8001)")
    print("• Billing Agent: python billing_agent.py (port 8002)")
    print("• General Agent: python general_agent.py (port 8003)")
    print("• Human Agent: python human_agent.py (port 8004)")
    print()
    
    asyncio.run(interactive_demo())
