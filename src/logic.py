import json
import os
import httpx
import asyncio
from urllib.parse import quote_plus

DATA_FILE = "data/company_research.json"

async def fetch_data(query: str = "Tata Sons"):
    """Requirement 1: Fetch data from the internet using OpenRouter or Wikipedia API."""
    # Check for API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if api_key:
        return await fetch_from_openrouter(api_key, query)
    else:
        print("[FETCH] No OpenRouter API key found, falling back to Wikipedia API")
        return await fetch_from_wikipedia(query)

async def fetch_from_openrouter(api_key: str, query: str):
    """Fetch data using OpenRouter with a Claude model."""
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
                "content": (
                    f"Provide a comprehensive summary of {query}, its ownership structure, history, "
                    f"and market significance. Include key facts about its role, business operations, "
                    f"and high-level corporate overview."
                )
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    print(f"[FETCH] Starting fetch from OpenRouter for query: {query}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=30.0)
            print(f"[FETCH] OpenRouter Response status: {response.status_code}")
            
            if response.status_code != 200:
                error_msg = f"OpenRouter API failed. Status: {response.status_code}"
                print(f"[FETCH] {error_msg}")
                return await fetch_from_wikipedia(query)
            
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', 'No data found.')
            print(f"[FETCH] Successfully retrieved {len(content)} characters from OpenRouter")
            return content
    except Exception as e:
        error_msg = f"OpenRouter fetch error: {str(e)}, falling back to Wikipedia"
        print(f"[FETCH] {error_msg}")
        return await fetch_from_wikipedia()

async def fetch_from_wikipedia(query: str):
    """Fetch data from Wikipedia API (fallback) for a given search query."""
    query_text = query.strip()
    page_title = quote_plus(query_text.replace(' ', '_'))
    headers = {"User-Agent": "CompanyInsightsApp/1.0"}
    print(f"[FETCH] Starting fetch from Wikipedia for query: {query_text}")
    try:
        async with httpx.AsyncClient() as client:
            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title}"
            response = await client.get(summary_url, headers=headers, timeout=30.0)
            print(f"[FETCH] Wikipedia Summary Response status: {response.status_code}")
            if response.status_code == 404:
                search_url = "https://en.wikipedia.org/w/api.php"
                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": query_text,
                    "utf8": 1,
                    "format": "json",
                    "srlimit": 1,
                }
                search_response = await client.get(search_url, params=params, headers=headers, timeout=30.0)
                if search_response.status_code != 200:
                    error_msg = f"Failed Wikipedia search. Status: {search_response.status_code}"
                    print(f"[FETCH] {error_msg}")
                    return error_msg
                search_data = search_response.json()
                search_results = search_data.get("query", {}).get("search", [])
                if not search_results:
                    error_msg = f"No Wikipedia page found for '{query_text}'"
                    print(f"[FETCH] {error_msg}")
                    return error_msg
                page_title = quote_plus(search_results[0].get("title", query_text).replace(' ', '_'))
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title}"
                response = await client.get(summary_url, headers=headers, timeout=30.0)
                print(f"[FETCH] Wikipedia search summary status: {response.status_code}")
            
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

def perform_crud_save(content: str, query: str | None = None):
    """Requirement 2: Perform CRUD (Create/Update) on a local file."""
    try:
        # Get absolute path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        data_dir = os.path.join(project_root, "data")
        abs_data_file = os.path.join(data_dir, "company_research.json")
        
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
            
        # Append new finding with optional query metadata
        payload = {"content": content, "source": "Web Search"}
        if query:
            payload["query"] = query
        records.append(payload)
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

def verify_data_quality() -> dict:
    """Requirement 2.5: Verify the quality and integrity of saved data."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, "data")
    abs_data_file = os.path.join(data_dir, "company_research.json")
    
    verification_report = {
        "status": "UNKNOWN",
        "total_records": 0,
        "valid_records": 0,
        "invalid_records": 0,
        "total_content_length": 0,
        "avg_content_length": 0,
        "file_exists": False,
        "file_size_kb": 0,
        "issues": []
    }
    
    print(f"[VERIFY] Starting data quality verification...")
    
    # Check if file exists
    if not os.path.exists(abs_data_file):
        verification_report["status"] = "FAILED"
        verification_report["issues"].append("Data file does not exist")
        print(f"[VERIFY] File not found at {abs_data_file}")
        return verification_report
    
    verification_report["file_exists"] = True
    verification_report["file_size_kb"] = round(os.path.getsize(abs_data_file) / 1024, 2)
    
    try:
        with open(abs_data_file, "r") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            verification_report["status"] = "FAILED"
            verification_report["issues"].append("Data is not a list")
            return verification_report
        
        verification_report["total_records"] = len(data)
        
        for idx, record in enumerate(data):
            if not isinstance(record, dict):
                verification_report["invalid_records"] += 1
                verification_report["issues"].append(f"Record {idx} is not a dictionary")
                continue
            
            content = record.get("content", "")
            source = record.get("source", "")
            
            # Validation checks
            is_valid = True
            if not content or len(content.strip()) == 0:
                verification_report["issues"].append(f"Record {idx} has empty content")
                is_valid = False
            elif len(content) < 50:
                verification_report["issues"].append(f"Record {idx} content too short ({len(content)} chars)")
                is_valid = False
            
            if not source:
                verification_report["issues"].append(f"Record {idx} missing source")
                is_valid = False
            
            if is_valid:
                verification_report["valid_records"] += 1
                verification_report["total_content_length"] += len(content)
            else:
                verification_report["invalid_records"] += 1
        
        # Calculate average
        if verification_report["valid_records"] > 0:
            verification_report["avg_content_length"] = round(
                verification_report["total_content_length"] / verification_report["valid_records"], 0
            )
        
        # Determine overall status
        if verification_report["invalid_records"] == 0 and verification_report["valid_records"] > 0:
            verification_report["status"] = "PASSED"
            print(f"[VERIFY] ✓ All records validated successfully")
        elif verification_report["valid_records"] > 0:
            verification_report["status"] = "PASSED_WITH_WARNINGS"
            print(f"[VERIFY] ⚠ {verification_report['invalid_records']} invalid record(s) found")
        else:
            verification_report["status"] = "FAILED"
            print(f"[VERIFY] ✗ No valid records found")
        
    except json.JSONDecodeError as e:
        verification_report["status"] = "FAILED"
        verification_report["issues"].append(f"Invalid JSON format: {str(e)}")
        print(f"[VERIFY] JSON parsing error: {str(e)}")
    except Exception as e:
        verification_report["status"] = "FAILED"
        verification_report["issues"].append(f"Verification error: {str(e)}")
        print(f"[VERIFY] {str(e)}")
    
    return verification_report