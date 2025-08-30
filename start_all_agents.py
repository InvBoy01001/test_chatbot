import subprocess
import sys
import time
import os
from pathlib import Path

def start_agent(script_name, port, description):
    try:
        if sys.platform.startswith("win"):
            cmd = f'start "Agent: {description}" python {script_name}'
            subprocess.run(cmd, shell=True, check=True)
        else:
            cmd = f'nohup python {script_name} > {script_name}.log 2>&1 &'
            subprocess.run(cmd, shell=True, check=True)
        
        print(f"✅ Started {description} on port {port}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start {description}: {e}")
        return False

def main():
    """Main startup function."""
    print("🚀 Starting LLM-Based Agentic Chatbot System")
    print("=" * 50)
    
    # Define all agents
    agents = [
        ("mcp/agents/intent_agent.py", 8000, "Intent Agent (Main Router)"),
        ("mcp/agents/working_support_agent.py", 8001, "Support Agent"),
        ("mcp/agents/working_billing_agent.py", 8002, "Billing Agent"),
        ("mcp/agents/working_general_agent.py", 8003, "General Info Agent"),
        ("mcp/agents/working_human_agent.py", 8004, "Human Agent"),
    ]
    
    # Check if all agent files exist
    missing_files = []
    for script_name, _, _ in agents:
        if not Path(script_name).exists():
            missing_files.append(script_name)
    
    if missing_files:
        print(f"❌ Missing agent files: {', '.join(missing_files)}")
        print("Please make sure all agent files are in the current directory.")
        return
    
    print("📁 All agent files found. Starting agents...\n")
    
    # Start all agents
    started_count = 0
    for script_name, port, description in agents:
        if start_agent(script_name, port, description):
            started_count += 1
        time.sleep(1)  # Small delay between starts
    
    print(f"\n🎯 Started {started_count}/{len(agents)} agents successfully!")
    
    if started_count == len(agents):
        print("\n🚀 All agents are now running!")
        print("\n📋 Next steps:")
        print("1. Wait a few seconds for all agents to fully start")
        print("2. Test the system:")
        print("   • Run: python test_llm_system.py")
        print("   • Or run: python demo_client.py")
        print("\n🔧 To stop all agents, close their terminal windows")
        print("   or use: taskkill /f /im python.exe (Windows)")
    else:
        print(f"\n⚠️  {len(agents) - started_count} agents failed to start.")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main()
