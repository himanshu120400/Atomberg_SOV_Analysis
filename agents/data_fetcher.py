import os
import re
import requests

def parse_views(view_text: str) -> int:
    if not isinstance(view_text, str): return 0
    view_text = view_text.lower().replace(' views', '').strip()
    if 'k' in view_text: return int(float(view_text.replace('k', '')) * 1_000)
    if 'm' in view_text: return int(float(view_text.replace('m', '')) * 1_000_000)
    if 'b' in view_text: return int(float(view_text.replace('b', '')) * 1_000_000_000)
    try:
        return int(re.sub(r'\D', '', view_text))
    except (ValueError, TypeError):
        return 0

def fetch_Google_Search_results(keyword: str, num_results: int = 10) -> list:
    print(f"Fetching Google Search results for '{keyword}'...")
    params = {"engine": "google", "q": keyword, "api_key": os.getenv("SERPAPI_API_KEY"), "num": num_results}
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json().get("organic_results", [])
        return [{"title": r.get("title", ""), "link": r.get("link", ""), "snippet": r.get("snippet", "")} for r in data]
    except Exception as e:
        print(f"Error fetching Google Search results: {e}")
        return []

def fetch_youtube_results(keyword: str, num_results: int = 10) -> list:
    print(f"Fetching YouTube results for '{keyword}'...")
    params = {"engine": "youtube", "search_query": keyword, "api_key": os.getenv("SERPAPI_API_KEY")}
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json().get("video_results", [])
        return [{"title": r.get("title", ""), "views": parse_views(r.get("view_count_text", "0")), "snippet": r.get("description", "")} for r in data[:num_results]]
    except Exception as e:
        print(f"Error fetching YouTube results: {e}")
        return []