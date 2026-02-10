import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

BASE_URL = os.getenv("NOWCERTS_BASE_URL")
API_KEY = os.getenv("NOWCERTS_API_KEY")

# If those specific names aren't in .env, check the alternates found in the global .env
if not BASE_URL:
    # Based on the view_file of .env, we have these:
    # INSURED_DETAIL_LIST_URL=https://test-null-ref-express.nowcerts.com/api/odata/InsuredDetailList
    # We can derive the BASE_URL or just use the specific variables if needed.
    # But let's look at the .env content again.
    # 7: INSURED_DETAIL_LIST_URL=https://test-null-ref-express.nowcerts.com/api/odata/InsuredDetailList
    # 2: API_KEY=amp_ai_mLz0esF0pqsVAZgGWF2Y2oMAwqebSt1qudYB48pqo7RC7ZrH0ON80CJo5O5UngG6J1x0LFxhr5WYvwM67w
    
    # Let's use what's in the root .env
    API_KEY = os.getenv("API_KEY")
    BASE_URL = "https://test-null-ref-express.nowcerts.com"

from tools.insured_details import get_insured_details
from tools.insured_only_insert import insert_insured_no_override as insert_insured_only
from tools.insured_tasks import get_insured_tasks

# Initialize FastMCP server
mcp = FastMCP("Insurance Tools")

@mcp.tool()
def get_insured_details_tool():
    """Get insured detail list from NowCerts. Returns the most recent 30 items."""
    return get_insured_details()

@mcp.tool()
def insert_insured_only_tool(payload: dict):
    """
    Insert insured without override. 
    Expects a payload dictionary with insured details.
    """
    return insert_insured_only(payload)

@mcp.tool()
def get_insured_tasks_tool(insured_database_ids: list[str]):
    """
    Get tasks for specific insured database IDs.
    Expects a list of IDs.
    """
    return get_insured_tasks(insured_database_ids)

if __name__ == "__main__":
    mcp.run()
