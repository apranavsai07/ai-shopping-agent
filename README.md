# AI Shopping Agent

An AI-powered shopping assistant that understands natural language product requests, searches the web for real products, compares them, and recommends the best options with prices and links.

## Example
Input: "Find the best laptop for AI development under ₹70,000"
Output: Top matching products with price, specs, reasoning, and a source link to compare/buy.

## How it works (Agentic Flow)
1. **Understand** — Gemini extracts a clean search query + constraints from the user's natural language request
2. **Search (Tool)** — Calls Serper.dev's Google Shopping API (India locale) to fetch real products with live prices from Amazon, Flipkart, Croma, etc.
3. **Compare & Recommend** — Gemini analyzes the search results against the user's original need and picks the best 2-4 matches with reasoning
4. **Store** — Original query + full analysis saved to SQLite for search history
5. **Display** — Frontend renders results as cards; past searches viewable via History

## Stack
- **Backend:** FastAPI, SQLite
- **LLM:** Google Gemini
- **Search Tool:** Serper.dev (Google Shopping API)
- **Frontend:** Vanilla HTML/CSS/JS

## Setup

1. Clone the repo and navigate to `backend/`
2. Create virtual environment:

python -m venv venv
venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Create `.env` in `backend/`:

LLM_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key

5. Run backend:

uvicorn main:app --reload --port 8000

6. Serve frontend (from `frontend/` folder):

python -m http.server 5500

7. Open `http://localhost:5500/index.html`

## API Endpoints
- `POST /search` — takes `{query}`, returns AI-analyzed recommendations
- `GET /history` — returns all past searches

## Known Limitations
- Prices are LLM-estimated from search snippets, not live scraped — may vary slightly from actual retailer price
- Uses SQLite for simplicity; production would use Postgres
- No authentication (out of scope for MVP)