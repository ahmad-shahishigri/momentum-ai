import os
import sys
from pathlib import Path
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Get the absolute path to your project directory
PROJECT_DIR = Path(__file__).parent.parent

# Path to your FIXED MCP server
MCP_SERVER_PATH = PROJECT_DIR / "mcp_server.py"

print(f"MCP Server location: {MCP_SERVER_PATH}")

# Create the agent
root_agent = Agent(
    name="insurance_agent",
    model="gemini-2.0-flash",
    description="An insurance agent with access to NowCerts API via MCP tools.",
    instruction="""
    You are a helpful insurance assistant with access to insurance data tools.
    
    You have access to these insurance-specific tools:
    
    1. get_insured_details_tool - Get a list of recent insured details (most recent 30 items)
    2. insert_insured_only_tool - Add a new insured record without override
    3. get_insured_tasks_tool - Get tasks for specific insured database IDs
    
    Always ask for clarification if information is missing.
    When you use a tool, summarize the results clearly for the user.
    """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=sys.executable,  # Use current Python interpreter
                    args=[
                        str(MCP_SERVER_PATH)
                    ],
                ),
            ),
        )
    ],
)