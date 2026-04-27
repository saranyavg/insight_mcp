import json
import os
import httpx
import asyncio

DATA_FILE = "data/tata_research.json"

async def fetch_tata_data():
    """Requirement 1: Fetch data from the internet using OpenRouter/Gemini API."""
    # Check for API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if api_key:
        return await fetch_from_openrouter(api_key)
    else:
        print("[FETCH] No OpenRouter API key found, falling back to Wikipedia API")
        return await fetch_from_wikipedia()

async def fetch_from_openrouter(api_key: str):
    """Fetch data using OpenRouter with Gemini model."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "anthropic/claude-3-haiku",
        "messages": [
            {
                "role": "user",
                "content": "Provide a comprehensive summary of Tata Sons, its ownership structure, history, and significance in India. Include key facts about its role in the Tata Group and its business operations."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    print(f"[FETCH] Starting fetch from OpenRouter (Claude)")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=30.0)
            print(f"[FETCH] OpenRouter Response status: {response.status_code}")
            
            if response.status_code != 200:
                error_msg = f"OpenRouter API failed. Status: {response.status_code}"
                print(f"[FETCH] {error_msg}")
                return await fetch_from_wikipedia()
            
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', 'No data found.')
            print(f"[FETCH] Successfully retrieved {len(content)} characters from OpenRouter")
            return content
    except Exception as e:
        error_msg = f"OpenRouter fetch error: {str(e)}, falling back to Wikipedia"
        print(f"[FETCH] {error_msg}")
        return await fetch_from_wikipedia()

async def fetch_from_wikipedia():
    """Fetch data from Wikipedia API (fallback)."""
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/Tata_Sons"
    headers = {"User-Agent": "TataInsightsApp/1.0"}
    print(f"[FETCH] Starting fetch from Wikipedia")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=30.0)
            print(f"[FETCH] Wikipedia Response status: {response.status_code}")
            if response.status_code != 200:
                error_msg = f"Failed to fetch data. Status: {response.status_code}"
                print(f"[FETCH] {error_msg}")
                return error_msg
            data = response.json()
            extract = data.get('extract', 'No data found.')
            print(f"[FETCH] Successfully retrieved {len(extract)} characters from Wikipedia")
            return extract
    except Exception as e:
        error_msg = f"Fetch error: {str(e)}"
        print(f"[FETCH] {error_msg}")
        return error_msg

def perform_crud_save(content: str):
    """Requirement 2: Perform CRUD (Create/Update) on a local file."""
    try:
        # Get absolute path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        data_dir = os.path.join(project_root, "data")
        abs_data_file = os.path.join(data_dir, "tata_research.json")
        
        print(f"[SAVE] Project root: {project_root}")
        print(f"[SAVE] Data directory: {data_dir}")
        print(f"[SAVE] Target file: {abs_data_file}")
        
        os.makedirs(data_dir, exist_ok=True)
        print(f"[SAVE] Data directory ensured at {data_dir}")
        
        # Load existing or start new list
        records = []
        if os.path.exists(abs_data_file):
            with open(abs_data_file, "r") as f:
                records = json.load(f)
            print(f"[SAVE] Loaded {len(records)} existing records")
        else:
            print(f"[SAVE] No existing file, starting fresh")
            
        # Append new finding
        records.append({"content": content, "source": "Web Search"})
        print(f"[SAVE] Total records to save: {len(records)}")
        
        with open(abs_data_file, "w") as f:
            json.dump(records, f, indent=2)
        
        # Verify file was written
        if os.path.exists(abs_data_file):
            file_size = os.path.getsize(abs_data_file)
            print(f"[SAVE] File successfully written at {abs_data_file} ({file_size} bytes)")
            return f"Successfully saved to {abs_data_file}"
        else:
            error_msg = f"File write failed - file not found at {abs_data_file}"
            print(f"[SAVE] {error_msg}")
            return error_msg
    except Exception as e:
        error_msg = f"Save error: {str(e)}"
        print(f"[SAVE] {error_msg}")
        return error_msg