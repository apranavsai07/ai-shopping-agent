from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from database import init_db, save_search, get_all_searches
from agent import run_shopping_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
def search_products(req: SearchRequest):
    if not req.query or not req.query.strip():
        return {"error": "Query cannot be empty"}

    try:
        result = run_shopping_agent(req.query)
        save_search(req.query, json.dumps(result))
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/history")
def get_history():
    return get_all_searches()