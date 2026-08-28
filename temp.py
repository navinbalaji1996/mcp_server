import os
import asyncio
from copilot import CopilotClient
from fastmcp import Client as MCPClient

async def call_mcp_tool(name: str, arguments: dict):
    server_url = "http://127.0.0.1:8000/mcp"
    async with MCPClient(server_url) as client:
        return await client.call_tool(name=name, arguments=arguments)

async def main():
    github_token = os.environ["GITHUB_TOKEN"]  # or COPILOT_GITHUB_TOKEN
    copilot = CopilotClient(
        github_token=github_token,
        use_logged_in_user=False,
    )
    await copilot.start()

    session = await copilot.create_session(model="auto")

    prompt = """
You are an MCP tool agent.
Available tools:
- get_transactions(name: string): return a transaction summary for the given user.
- update_transactions(id: string, amount: number): update the transaction amount.

When the user asks a question, choose one tool and return:
tool: <tool_name>
arguments: <JSON object>
"""

    user_query = "Get the summary of ganesh"
    response = await session.send_and_wait(prompt + "\nUser: " + user_query)

    print("Copilot response:", response)

    # Example parse step:
    # tool = "get_transactions"
    # arguments = {"name": "ganesh"}
    tool = "get_transactions"
    arguments = {"name": "ganesh"}

    result = await call_mcp_tool(tool, arguments)
    print(result.data)

    await copilot.stop()

if __name__ == "__main__":
    asyncio.run(main())