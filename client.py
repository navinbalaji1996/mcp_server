import asyncio
import os
from copilot import CopilotClient
from copilot.session import PermissionHandler

async def main():
    print("🔄 Initializing GitHub Copilot Client session...")
    
    # 1. Initialize the official Copilot client engine
    client = CopilotClient()
    await client.start()
    
    # 2. Spin up the agent workflow and bind your HTTP FastMCP server
    # Note: 'approve_all' allows the Copilot engine to execute tools autonomously
    session = await client.create_session(
        on_permission_request=PermissionHandler.approve_all,
        model="gpt-5-mini",  # Select any active Copilot infrastructure model
        mcp_servers={
            "CashGiftServer": {
                "type": "remote",
                "url": "http://localhost:8000/mcp"
            }
        }
    )
    
    print("✅ Session tied successfully to CashGiftServer.")
    print("-" * 60)
    
    # 3. Accept User Input
    user_query = input("Ask a query: ")
    print("\n🤖 Copilot is planning workflows and invoking local MCP tools...")
    
    # 4. Fire prompt. Copilot evaluates it, drafts a plan, POSTs to your 
    # FastAPI endpoint, fetches the math response, and creates the conclusion.
    result = await session.send_and_wait(user_query)
    
    print("\n--- Copilot Final Answer ---")
    print(result)

if __name__ == "__main__":
    # Ensure Copilot configuration keys exist if you aren't using the local interactive CLI login
    if "COPILOT_GITHUB_TOKEN" not in os.environ and "GITHUB_TOKEN" not in os.environ:
        print("💡 Note: Ensure you are logged into your GitHub CLI ('gh auth login') or have your tokens exported.")
        
    asyncio.run(main())