# insight_mcp

## Quick Start

1. Open a terminal in the project folder: `C:\Users\Saranya\Downloads\insight_mcp`
2. Activate the conda environment: `conda activate prefab_env`
3. Start the app: `fastmcp dev apps main.py`
4. Open the browser URL shown (typically `http://localhost:8080`)

## Using the App

The app has four tools:

### 1. **search_internet**
- Fetches comprehensive Company ownership data from OpenRouter API (Claude) with Wikipedia fallback
- Automatically saves it to `data/company_research.json`
- Can be called manually to refresh data with the latest information

### 2. **save_to_file**
- Manually save any custom text or findings to the vault
- Useful for adding supplementary research data

### 3. **verify_data** ⭐ (NEW)
- Audits the quality and integrity of saved research data
- Checks for:
  - Valid JSON structure
  - Complete records with required fields
  - Minimum content length
  - Source information
- Returns a detailed verification report with statistics

### 4. **show_dashboard** 
- Displays a beautiful, enhanced research dashboard with real-time data
- Shows key statistics (total records, valid records, total words, verification status)
- **NEW**: Includes a company search bar to request fresh summaries for any keyword
- **NEW**: Shows complete full content in a detailed section below
- Auto-fetches data if none exists
- Features:
  - Modern gradient design with dark theme
  - Live data quality badges
  - Word count tracking
  - Responsive grid layout
  - Scrollable full content viewer
  - Hover effects and smooth transitions

## Workflow

### Quick Start:
Simply call `show_dashboard` - it will automatically fetch and display everything!

### Advanced Workflow:
1. Call `search_internet` → fetches fresh data from OpenRouter
2. Call `verify_data` → audits the saved data quality
3. Call `show_dashboard` → displays the dashboard with statistics

## Key Features

✨ **Enhanced UI**
- Gradient backgrounds with modern color scheme
- Responsive grid layout for statistics
- Hover effects and smooth transitions
- Professional typography and spacing
- Dark theme optimized for readability

🔐 **Data Verification**
- Automatic quality checks
- Comprehensive validation reports
- Issue detection and logging
- Data integrity confirmation

🔍 **Search & Filter Guidance**
- Tips for using MCP tools effectively
- Filter options and data organization
- Quality verification integration
- Real-time statistics dashboard

## Testing Locally (without FastMCP UI)

Run: `python test_workflow.py`

This will test all functionality locally and show you what the complete workflow looks like.

## Testing Locally (without FastMCP UI)

Run: `python test_workflow.py`

This will test all functionality locally and show you what the complete workflow looks like.

## Troubleshooting

- **"The vault is empty"**: Call the `search_internet` tool first
- **No output after calling tools**: Check terminal for [FETCH] or [SAVE] logs - they show what's happening
- **File not found**: The data is saved to `data/company_research.json` relative to the project root
- **Need to reset**: Delete the `data/` folder to start fresh

## Notes

- All paths use absolute paths internally, so location doesn't matter
- Data is stored in `data/company_research.json` as JSON
- Each call to `search_internet` appends a new record (doesn't replace old ones)
- The UI updates when `show_dashboard` is called
