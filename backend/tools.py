import os
import requests
from dotenv import load_dotenv
load_dotenv()

def web_search(query: str, max_results: int = 10):
    headers = {"X-API-KEY": os.getenv("SERPER_API_KEY"), "Content-Type": "application/json"}
    payload = {"q": query, "num": max_results, "gl": "in", "location": "India"}
    res = requests.post("https://google.serper.dev/shopping", headers=headers, json=payload)
    data = res.json()

    results = []
    for r in data.get("shopping", []):
        results.append({
            "title": r.get("title", ""),
            "snippet": f"Price: {r.get('price', 'N/A')}, Source: {r.get('source', '')}, Rating: {r.get('rating', 'N/A')}",
            "url": r.get("link", "")
        })
    return results

def format_results_for_llm(results: list):
    """Format raw search results into text for the LLM to extract/compare."""
    text = ""
    for i, r in enumerate(results, 1):
        text += f"{i}. {r['title']}\n   {r['snippet']}\n   Link: {r['url']}\n\n"
    return text