# FastAPI + OpenAI Website Scraper

Summarizes any public URL using OpenAI (`gpt-4o-mini`).

## Project layout (FastAPI conventions)

```
app/
├── main.py              # App factory, lifespan, router registration
├── config.py            # Settings (pydantic-settings + .env)
├── dependencies.py      # FastAPI Depends() providers
├── prompts.py           # LLM prompt constants
├── routers/             # HTTP routes only (thin handlers)
│   ├── health.py
│   └── website.py
├── schemas/             # Pydantic request/response models
│   └── website.py
└── services/            # Business logic (no FastAPI imports)
    ├── scraper.py
    └── summarizer.py
```

## Setup

From the project root (`fast_api_llm`):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp app/.env.example app/.env
# Edit app/.env and set OPENAI_API_KEY
```

## Run

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Server: http://127.0.0.1:8000  
API docs: http://127.0.0.1:8000/docs

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/api/website-scraper?url=...` | Fetch and summarize a website |

Example:

```bash
curl "http://127.0.0.1:8000/api/website-scraper?url=https://example.com"
```

Response (JSON):

```json
{
  "url": "https://example.com/",
  "summary": "# Example Domain\n\n..."
}
```
