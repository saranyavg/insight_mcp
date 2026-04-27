# insight_mcp

## Quick Start

1. Open a terminal in the project folder: `C:\Users\Saranya\Downloads\insight_mcp`
2. Activate the conda environment: `conda activate prefab_env`
3. Start the app: `fastmcp dev apps main.py`
4. Open the browser URL shown (typically `http://localhost:8080`)

## Using the App

The app has three tools:

### 1. **search_internet**
- Fetches Tata Sons ownership data from Wikipedia or OpenRouter
- Automatically saves it to `data/tata_research.json`
- Can be called manually to refresh data

### 2. **show_dashboard** 
- Displays the research dashboard with the saved data
- Automatically fetches and saves data if none exists
- Shows all records in a table

### 3. **save_to_file**
- Manually save any text to the vault
- Useful for adding custom data

## Workflow

Simply call `show_dashboard` - it will automatically fetch data if needed and display the dashboard.

For manual control:
1. Call `search_internet` → fetches data and saves it
2. Call `show_dashboard` → displays the dashboard with the saved data

## Testing Locally (without FastMCP UI)

Run: `python test_workflow.py`

This will test all functionality locally and show you what the complete workflow looks like.

## Testing Locally (without FastMCP UI)

Run: `python test_workflow.py`

This will test all functionality locally and show you what the complete workflow looks like.

## Troubleshooting

- **"The vault is empty"**: Call the `search_internet` tool first
- **No output after calling tools**: Check terminal for [FETCH] or [SAVE] logs - they show what's happening
- **File not found**: The data is saved to `data/tata_research.json` relative to the project root
- **Need to reset**: Delete the `data/` folder to start fresh

## Notes

- All paths use absolute paths internally, so location doesn't matter
- Data is stored in `data/tata_research.json` as JSON
- Each call to `search_internet` appends a new record (doesn't replace old ones)
- The UI updates when `show_dashboard` is called
