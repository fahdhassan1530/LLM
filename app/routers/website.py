from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import HttpUrl

from app.dependencies import get_scraper_service, get_summarizer_service
from app.schemas import WebsiteSummaryResponse
from app.services import (
    SummarizationError,
    WebsiteFetchError,
    WebsiteScraperService,
    WebsiteSummarizerService,
)

router = APIRouter(prefix="/api", tags=["website"])


@router.get(
    "/website-scraper",
    response_model=WebsiteSummaryResponse,
    summary="Summarize a website",
    response_description="Markdown summary of the page content",
)
def summarize_website(
    url: Annotated[HttpUrl, Query(description="Public URL to fetch and summarize")],
    scraper: Annotated[WebsiteScraperService, Depends(get_scraper_service)],
    summarizer: Annotated[WebsiteSummarizerService, Depends(get_summarizer_service)],
) -> WebsiteSummaryResponse:
    """
    Fetch a website, extract readable text, and return a snarky markdown summary.

    Uses a sync `def` route so blocking HTTP and OpenAI calls run in FastAPI's
    thread pool instead of blocking the async event loop.
    """
    url_str = str(url)
    try:
        content = scraper.fetch(url_str)
    except WebsiteFetchError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    try:
        summary = summarizer.summarize(content)
    except SummarizationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return WebsiteSummaryResponse(url=url, summary=summary)
