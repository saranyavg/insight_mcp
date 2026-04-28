import asyncio
from dotenv import load_dotenv
from fastmcp import FastMCP
from src.logic import fetch_data, perform_crud_save, verify_data_quality
from src.ui import create_research_dashboard

load_dotenv()

mcp = FastMCP("InsightsServer")

@mcp.tool()
async def search_internet(query: str = "Tata Sons") -> str:
    """Fetches a company summary from the web for the given query and saves it to the local file."""
    try:
        print(f"[TOOL] search_internet called with query: {query}")
        data = await fetch_data(query)
        print(f"[TOOL] Fetched data: {len(data)} characters")
        
        if data.startswith("Failed") or data.startswith("Fetch error"):
            return f"Error during fetch: {data}"
        
        # Automatically save the fetched data with query metadata
        save_result = perform_crud_save(data, query=query)
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

@mcp.tool()
def verify_data() -> str:
    """Verifies the quality and integrity of saved research data."""
    try:
        print("[TOOL] verify_data called")
        report = verify_data_quality()
        print(f"[TOOL] Verification complete - Status: {report['status']}")
        
        # Format report for display
        result = f"""
📊 Data Quality Verification Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: {report['status']}
Total Records: {report['total_records']}
Valid Records: {report['valid_records']}
Invalid Records: {report['invalid_records']}
File Size: {report['file_size_kb']} KB
Avg Content Length: {int(report['avg_content_length'])} characters

File Exists: {'✓ Yes' if report['file_exists'] else '✗ No'}
        """
        
        if report['issues']:
            result += "\n⚠️  Issues Found:\n"
            for issue in report['issues']:
                result += f"  • {issue}\n"
        else:
            result += "\n✓ No issues detected!\n"
        
        return result
    except Exception as e:
        error_msg = f"Error in verify_data: {str(e)}"
        print(f"[TOOL] {error_msg}")
        return error_msg

@mcp.tool(app=True) # Crucial: app=True signals this returns a Prefab UI
async def show_dashboard() -> any:
    """Displays the interactive research dashboard UI."""
    return await create_research_dashboard()

if __name__ == "__main__":
    mcp.run()