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
    If,
    Else,
)
from prefab_ui.actions.mcp import CallTool
from prefab_ui.actions.ui import ShowToast
from prefab_ui.actions.state import SetState

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
        
        # Header Section
        with Card(css_class="border-0 bg-gradient-to-r from-purple-700 to-fuchsia-700 shadow-2xl mb-8"):
            with CardContent(css_class="pt-8 pb-8"):
                Heading(
                    "Companies Summary Hub",
                    level=1,
                    css_class="text-white text-4xl font-bold mb-2"
                )
                Text(
                    "Enter a company keyword to fetch a fresh summary and save it to the dashboard.",
                    css_class="text-purple-100 text-lg"
                )
        
        with Card(css_class="border-0 bg-slate-800 shadow-xl mb-8"):
            with CardContent(css_class="pt-6 pb-6"):
                Heading(
                    "Search company summary",
                    level=2,
                    css_class="text-white text-2xl font-semibold mb-3"
                )
                Text(
                    "Type a company name like JP Morgan, Tesla, or Samsung, then submit to fetch and store a fresh summary.",
                    css_class="text-slate-300 text-sm mb-4"
                )
                with Form(
                    onSubmit=[
                        CallTool(
                            "search_internet",
                            arguments={"query": "{{ query }}"},
                            onSuccess=[
                                SetState("search_data", "{{ $result }}"),
                                ShowToast("Summary fetched and saved successfully!", variant="success"),
                            ],
                        ),
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

        with If("{{ search_data }}"):
            with Card(css_class="border-0 bg-slate-700 shadow-xl overflow-hidden"):
                with CardContent(css_class="pt-6 pb-6"):
                    Heading(
                        "Search Result",
                        level=2,
                        css_class="text-white text-2xl font-semibold mb-3"
                    )
                    Text(
                        "This result was fetched on demand and saved to the local data vault.",
                        css_class="text-slate-300 text-sm mb-4"
                    )
                    Text(
                        "Query:",
                        css_class="text-slate-200 text-sm font-semibold"
                    )
                    Text(
                        "{{ search_data.query }}",
                        css_class="text-slate-100 text-base mb-4"
                    )
                    Text(
                        "Source:",
                        css_class="text-slate-200 text-sm font-semibold"
                    )
                    Text(
                        "{{ search_data.source }}",
                        css_class="text-slate-100 text-base mb-4"
                    )
                    Text(
                        "Saved message:",
                        css_class="text-slate-200 text-sm font-semibold"
                    )
                    Text(
                        "{{ search_data.save_message }}",
                        css_class="text-slate-100 text-base mb-6"
                    )
                    with Card(css_class="bg-slate-800 border border-slate-600 rounded p-4"):
                        Text(
                            "{{ search_data.content }}",
                            css_class="text-slate-100 text-sm leading-relaxed whitespace-pre-wrap"
                        )
        
        with Else():
            with Card(css_class="border-0 bg-slate-700 shadow-xl"):
                with CardContent(css_class="py-16 text-center"):
                    Heading(
                        "No Data Loaded Yet",
                        level=2,
                        css_class="text-white text-2xl font-bold mb-4"
                    )
                    Text(
                        "No results will be loaded until you search. Enter a company and click Search.",
                        css_class="text-slate-300 text-lg mb-6 max-w-lg mx-auto"
                    )
                    Text(
                        "Once the search completes, the result will appear immediately in the dashboard.",
                        css_class="text-slate-400 text-sm"
                    )
    return app