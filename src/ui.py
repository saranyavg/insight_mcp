import json
import os
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
)
from .logic import fetch_tata_data, perform_crud_save

async def create_research_dashboard():
    """Requirement 3: UI Dashboard using Prefab."""
    findings = []
    
    # Get absolute path to data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, "data")
    abs_data_file = os.path.join(data_dir, "tata_research.json")
    
    print(f"[UI] Looking for data at: {abs_data_file}")
    
    if os.path.exists(abs_data_file):
        try:
            with open(abs_data_file, "r") as f:
                data = json.load(f)
                print(f"[UI] Loaded {len(data)} records from file")
                # Formatting data for a Table component
                findings = [
                    {
                        "id": str(i + 1),
                        "summary": item.get("content", "")[:150] + "...",
                    }
                    for i, item in enumerate(data)
                    if isinstance(item, dict)
                ]
        except Exception as e:
            print(f"[UI] Error reading file: {str(e)}")
    else:
        print(f"[UI] Data file does not exist, fetching data automatically...")
        # Automatically fetch and save data
        fetched_data = await fetch_tata_data()
        if not (fetched_data.startswith("Failed") or fetched_data.startswith("Fetch error")):
            save_result = perform_crud_save(fetched_data)
            print(f"[UI] Auto-save result: {save_result}")
            # Reload data
            if os.path.exists(abs_data_file):
                try:
                    with open(abs_data_file, "r") as f:
                        data = json.load(f)
                        findings = [
                            {
                                "id": str(i + 1),
                                "summary": item.get("content", "")[:150] + "...",
                            }
                            for i, item in enumerate(data)
                            if isinstance(item, dict)
                        ]
                except Exception as e:
                    print(f"[UI] Error reading after auto-fetch: {str(e)}")
        else:
            print(f"[UI] Auto-fetch failed: {fetched_data}")

    with PrefabApp(css_class="max-w-3xl mx-auto p-6") as app:
        with Card():
            with CardHeader():
                CardTitle("Ownership Research Dashboard")
            with CardContent():
                if not findings:
                    Text(
                        "The vault is empty. Run the search_internet tool first, then refresh the dashboard.",
                        bold=True,
                        align="center",
                    )
                else:
                    with Table():
                        with TableHeader():
                            with TableRow():
                                TableHead("ID")
                                TableHead("Finding Summary")
                        with TableBody():
                            for item in findings:
                                with TableRow():
                                    TableCell(item["id"])
                                    TableCell(item["summary"])
    return app