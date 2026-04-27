import asyncio
from dotenv import load_dotenv
from fastmcp import FastMCP
from src.logic import fetch_tata_data, perform_crud_save
from src.ui import create_research_dashboard

load_dotenv()

mcp = FastMCP("TataInsightsServer")

@mcp.tool()
async def search_internet() -> str:
    """Fetches ownership snippets about Tata Sons from the web and saves to file automatically."""
    try:
        print("[TOOL] search_internet called")
        data = await fetch_tata_data()
        print(f"[TOOL] Fetched data: {len(data)} characters")
        
        if data.startswith("Failed") or data.startswith("Fetch error"):
            return f"Error during fetch: {data}"
        
        # Automatically save the fetched data
        save_result = perform_crud_save(data)
        print(f"[TOOL] Save result: {save_result}")
        return save_result
    except Exception as e:
        error_msg = f"Error in search_internet: {str(e)}"
        print(f"[TOOL] {error_msg}")
        return error_msg

@mcp.tool()
def save_to_file(details: str) -> str:
    """Saves the provided details to the local findings file."""
    return perform_crud_save(details)

@mcp.tool(app=True) # Crucial: app=True signals this returns a Prefab UI
async def show_dashboard() -> any:
    """Displays the interactive research dashboard UI."""
    return await create_research_dashboard()

if __name__ == "__main__":
    mcp.run()