import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from tools import web_search, format_results_for_llm

load_dotenv()
genai.configure(api_key=os.getenv("LLM_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

def understand_query(user_query: str):
    """Step 1: LLM extracts a clean search query + constraints from user request."""
    prompt = f"""Extract a concise web search query and constraints from this shopping request.

User request: "{user_query}"

Respond ONLY with valid JSON (no markdown):
{{
  "search_query": "short search terms for web search",
  "category": "product category",
  "budget": "budget if mentioned, else null",
  "requirements": "key requirements in 1 line"
}}"""
    response = model.generate_content(prompt)
    text = clean_json(response.text)
    return json.loads(text)

def compare_and_recommend(user_query: str, search_results_text: str):
    """Step 2: LLM compares products from search results and recommends best options."""
    prompt = f"""You are a shopping assistant. A user asked: "{user_query}"

Here are web search results about relevant products:
{search_results_text}

Analyze these and recommend the best 2-4 matching products. Respond ONLY with valid JSON (no markdown):
{{
  "recommendations": [
    {{
      "name": "product name",
      "price": "price if mentioned, else 'Not listed'",
      "key_details": "key specs relevant to the request",
      "why_recommended": "1-2 sentence reasoning",
      "source_link": "the URL from search results"
    }}
  ],
  "summary": "2-3 sentence overall summary of the recommendation"
}}"""
    response = model.generate_content(prompt)
    text = clean_json(response.text)
    return json.loads(text)

def clean_json(text: str):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()

def run_shopping_agent(user_query: str):
    """Full agentic pipeline: understand -> search -> compare -> recommend."""
    understanding = understand_query(user_query)
    search_results = web_search(understanding["search_query"])
    formatted = format_results_for_llm(search_results)
    analysis = compare_and_recommend(user_query, formatted)
    return {
        "understanding": understanding,
        "raw_results_count": len(search_results),
        "recommendations": analysis["recommendations"],
        "summary": analysis["summary"]
    }