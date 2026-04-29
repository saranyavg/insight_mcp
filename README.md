# insight_mcp

## Quick Start

1. Open a terminal in the project folder: `C:\Users\Saranya\Downloads\insight_mcp`
2. Activate the conda environment: `conda activate prefab_env`
3. Start the app: `fastmcp dev apps main.py`
4. Open the browser URL shown by FastMCP (for example `http://localhost:8080`)

## App Behavior

This project exposes an MCP server with a Prefab UI dashboard that is search-driven.
The UI does not preload saved results on open. Data is only fetched when you enter a company name and press `Search`.
Once the search completes, the result is saved to `data/company_research.json` and immediately displayed in the dashboard.

## Tools

### 1. **search_internet**
- Fetches company summary data from OpenRouter AI
- Falls back to Wikipedia if no API key is available or the OpenRouter request fails
- Saves the fetched result to `data/company_research.json`
- Returns structured data for the UI to render immediately after search

### 2. **save_to_file**
- Saves custom text or findings to the local vault
- Useful for persisting supplementary research notes

### 3. **verify_data**
- Verifies the saved JSON data for structure and content quality
- Checks:
  - File existence
  - JSON validity
  - Required fields
  - Minimum content length
  - Source metadata
- Returns a verification report with status and issue details

### 4. **show_dashboard**
- Opens the interactive dashboard UI
- Starts clean and waits for a manual search
- Displays the latest search result once the search tool writes it
- Includes:
  - search bar for custom company queries
  - saved result preview with query, source, and save message
  - full fetched content viewer

## Workflow

### Recommended Flow
1. Open the UI by calling `show_dashboard`
2. Enter a company name in the search box
3. Click `Search`
4. The app fetches fresh data, saves it, and displays it immediately

### Optional Verification
1. Call `verify_data` to audit the saved JSON data
2. Review the verification report for any warnings or issues

## Demo Video

Please find the demo video link here:

`https://youtu.be/-iehr7BhgdE`

## Troubleshooting

- **UI shows no data on open**: This is expected. Search must be performed before results appear.
- **Search returns an error**: Check terminal logs for `[FETCH]` and `[SAVE]` messages.
- **Saved file not found**: The app writes to `data/company_research.json` relative to the project root.
- **Need to reset data**: Delete the `data/company_research.json` file and restart.

## Notes

- The UI is intentionally search-driven and does not auto-fetch on load.
- Fetched data is saved as JSON and displayed after the search returns.
- The dashboard uses state binding so the result appears immediately after the search tool finishes.
