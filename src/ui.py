import json
import os
from datetime import datetime
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Table,
    TableHeader,
    TableBody,
    TableRow,
    TableHead,
    TableCell,
    Text,
    Heading,
    Badge,
    Form,
    Input,
    Button,
)
from prefab_ui.actions.mcp import CallTool
from prefab_ui.actions.ui import ShowToast
from prefab_ui.actions.state import PopState, SetState
from .logic import fetch_data, perform_crud_save, verify_data_quality

async def create_research_dashboard():
    """Requirement 3: Enhanced UI Dashboard with summaries and search capabilities."""
    findings = []
    verification_report = {}
    
    # Get absolute path to data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, "data")
    abs_data_file = os.path.join(data_dir, "company_research.json")
    
    print(f"[UI] Looking for data at: {abs_data_file}")
    
    with PrefabApp(css_class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8") as app:
        
        # ✅ VERY IMPORTANT: Hidden state binding (forces UI refresh)
        Text("{{ refresh_trigger }}", css_class="hidden")
        
        if os.path.exists(abs_data_file):
            try:
                print(f"[UI] File exists: {os.path.exists(abs_data_file)}")
                print(f"[UI] File size: {os.path.getsize(abs_data_file) if os.path.exists(abs_data_file) else 'N/A'}")

                with open(abs_data_file, "r") as f:
                    data = json.load(f)
                    print(f"[UI] Loaded {len(data)} records from file")
                    
                    # Process data with summaries and full content
                    findings = []
                    for i, item in enumerate(data):
                        if isinstance(item, dict):
                            full_content = item.get("content", "")
                            words = full_content.split()                        
                            
                            findings.append({
                                "id": str(i + 1),
                                "full_content": full_content,
                                "source": item.get("source", "Unknown"),
                                "word_count": len(words),
                                "char_count": len(full_content),
                            })
            
                # Verify data quality
                verification_report = verify_data_quality()
                print(f"[UI] Data quality status: {verification_report['status']}")
                
            except Exception as e:
                print(f"[UI] Error reading file: {str(e)}")
        else:
            print(f"[UI] Data file does not exist, fetching data automatically...")
            # Automatically fetch and save data
            fetched_data = await fetch_data()
            if not (fetched_data.startswith("Failed") or fetched_data.startswith("Fetch error")):
                save_result = perform_crud_save(fetched_data)
                print(f"[UI] Auto-save result: {save_result}")
                # Reload data
                if os.path.exists(abs_data_file):
                    try:
                        with open(abs_data_file, "r") as f:
                            data = json.load(f)
                            findings = []
                            for i, item in enumerate(data):
                                if isinstance(item, dict):
                                    full_content = item.get("content", "")
                                    words = full_content.split()
                                    
                                    findings.append({
                                        "id": str(i + 1),
                                        "full_content": full_content,
                                        "source": item.get("source", "Unknown"),
                                        "word_count": len(words),
                                        "char_count": len(full_content),
                                    })
                        verification_report = verify_data_quality()
                    except Exception as e:
                        print(f"[UI] Error reading after auto-fetch: {str(e)}")
            else:
                print(f"[UI] Auto-fetch failed: {fetched_data}")

        # Determine status color and icon
        status_color = "green" if verification_report.get("status") == "PASSED" else "blue" if verification_report.get("status") == "PASSED_WITH_WARNINGS" else "red"
        status_icon = "✓" if verification_report.get("status") == "PASSED" else "⚠" if verification_report.get("status") == "PASSED_WITH_WARNINGS" else "✗"

        # Header Section
        with Card(css_class="border-0 bg-gradient-to-r from-purple-700 to-fuchsia-700 shadow-2xl mb-8"):
            with CardContent(css_class="pt-8 pb-8"):
                Heading(
                    "🏢 Companies Summary Hub",
                      level=1,
                      css_class="text-white text-4xl font-bold mb-2"
                )
                Text(
                    "Enter a company keyword to fetch a fresh summary and save the result in the dashboard.",
                    css_class="text-purple-100 text-lg"
                )
        
        with Card(css_class="border-0 bg-slate-800 shadow-xl mb-8"):
            with CardContent(css_class="pt-6 pb-6"):
                Heading(
                    "🔎 Search company summary",
                    level=2,
                    css_class="text-white text-2xl font-semibold mb-3"
                )
                Text(
                    "Type a company name like JP Morgan, Tesla, or Samsung, then submit to generate a fresh summary.",
                    css_class="text-slate-300 text-sm mb-4"
                )
                with Form(
                    onSubmit=[
                        CallTool("search_internet", arguments={"query": "{{ query }}"}),
                        SetState("refresh_trigger", "{{ $now }}"),
                        ShowToast("✓ Summary updated! Dashboard refreshing...", variant="success"),
                    ],
                    css_class="grid gap-4",
                ):
                    Input(
                        name="query",
                        placeholder="Enter company name (e.g. JP Morgan)",
                        css_class="w-full bg-slate-900 text-white border border-slate-700 rounded px-4 py-3",
                        required=True,
                    )
                    Button(
                        "Search",
                        buttonType="submit",
                        variant="success",
                        css_class="w-full md:w-40",
                    )
        
        if findings:
            with CardContent(css_class="mb-8 grid grid-cols-2 md:grid-cols-4 gap-4"):
                
                # Card 1: Data Quality Status
                with Card(css_class="border-0 bg-slate-700 shadow-lg hover:shadow-xl transition-shadow"):
                    with CardContent(css_class="pt-4 pb-4 text-center"):
                        Text(
                            "🔐 Verification",
                            css_class="text-slate-300 text-xs font-semibold uppercase tracking-wider mb-1"
                        )
                        Heading(
                            f"{status_icon} {verification_report.get('status', 'UNKNOWN')}",
                            level=2,
                            css_class=f"text-{status_color}-400 text-lg font-bold"
                        )
            
            # Full Content Section
            with Card(css_class="border-0 bg-slate-800 shadow-xl overflow-hidden"):
                with CardHeader(css_class="bg-slate-700 border-b border-slate-600"):
                    Heading(
                        "📖 Complete Research Content",
                        level=2,
                        css_class="text-white text-2xl font-bold mb-4"
                    )
                    Text(
                        "Full detailed information from all research findings",
                        css_class="text-slate-300 text-sm"
                    )
                
                with CardContent(css_class="max-h-96 overflow-y-auto"):
                    for i, item in enumerate(findings):
                        with Card(css_class="border-0 bg-slate-700 mb-4 last:mb-0"):
                            with CardHeader(css_class="bg-slate-600 border-b border-slate-500 flex justify-between items-center py-3"):
                                Heading(
                                    f"Entry #{item['id']} - {item['source']}",
                                    level=3,
                                    css_class="text-white text-lg font-semibold"
                                )
                                Badge(
                                    f"{item['word_count']} words",
                                    css_class="bg-blue-600 text-white px-2 py-1 rounded text-xs"
                                )
                            
                            with CardContent(css_class="pt-4 pb-4"):
                                Text(
                                    item["full_content"],
                                    css_class="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap"
                                )
            
            # Footer with metadata
            with Card(css_class="border-0 bg-slate-700 shadow-lg mt-8"):
                with CardContent(css_class="pt-4 pb-4 flex justify-between items-center text-slate-400 text-sm"):
                    Text(
                        f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        css_class="text-slate-300"
                    )
                    Text(
                        f"📦 File Size: {verification_report.get('file_size_kb', 0)} KB",
                        css_class="text-slate-300"
                    )
        
        else:
            # Empty State
            with Card(css_class="border-0 bg-slate-700 shadow-xl"):
                with CardContent(css_class="py-16 text-center"):
                    Heading(
                        "🔍 No Data Found",
                        level=2,
                        css_class="text-white text-2xl font-bold mb-4"
                    )
                    Text(
                        "The research vault is empty. Call the search_internet tool first to fetch Company ownership data.",
                        css_class="text-slate-300 text-lg mb-6 max-w-lg mx-auto"
                    )
                    Text(
                        "Once data is fetched and saved, it will appear here in a beautiful, organized dashboard.",
                        css_class="text-slate-400 text-sm"
                    )
    
    return app