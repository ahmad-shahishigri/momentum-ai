import os
import sys
import json
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("NOWCERTS_BASE_URL")
API_KEY = os.getenv("NOWCERTS_API_KEY")

# Import your tools
from tools.insured_details import get_insured_details
from tools.insured_only_insert import insert_insured_no_override as insert_insured_only
from tools.insured_tasks import get_insured_tasks

# Import MCP server components
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio

# Create server
server = Server("insurance-tools")

@server.list_tools()
async def handle_list_tools():
    """List available tools"""
    return [
        {
            "name": "get_insured_details_tool",
            "description": "Get insured detail list from NowCerts. Returns the most recent 30 items.",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "insert_insured_only_tool",
            "description": "Insert insured without override. Expects a payload dictionary with insured details.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "payload": {
                        "type": "object",
                        "description": "Dictionary with insured details"
                    }
                },
                "required": ["payload"]
            }
        },
        {
            "name": "get_insured_tasks_tool",
            "description": "Get tasks for specific insured database IDs. Expects a list of IDs.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "insured_database_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of insured database IDs"
                    }
                },
                "required": ["insured_database_ids"]
            }
        }
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    """Handle tool execution"""
    try:
        if name == "get_insured_details_tool":
            result = get_insured_details()
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }]
            }
            
        elif name == "insert_insured_only_tool":
            payload = arguments.get("payload", {})
            result = insert_insured_only(payload)
            return {
                "content": [{
                    "type": "text", 
                    "text": json.dumps(result, indent=2)
                }]
            }
            
        elif name == "get_insured_tasks_tool":
            insured_ids = arguments.get("insured_database_ids", [])
            result = get_insured_tasks(insured_ids)
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }]
            }
            
        else:
            return {
                "content": [{
                    "type": "text",
                    "text": f"Unknown tool: {name}"
                }],
                "isError": True
            }
            
    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error: {str(e)}"
            }],
            "isError": True
        }

async def main():
    """Run the server"""
    print("Starting MCP Insurance Server...", file=sys.stderr)
    print(f"BASE_URL: {BASE_URL}", file=sys.stderr)
    print(f"API_KEY present: {'Yes' if API_KEY else 'No'}", file=sys.stderr)
    
    # Run with stdio transport
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="insurance-tools",
                server_version="0.1.0",
                capabilities=server.get_capabilities()
            )
        )

if __name__ == "__main__":
    asyncio.run(main())