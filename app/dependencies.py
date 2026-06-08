from typing import Annotated

from fastapi import Depends
from openai import OpenAI

from app.config import Settings, get_settings
from app.services.scraper import WebsiteScraperService
from app.services.summarizer import WebsiteSummarizerService


def get_openai_client(
    settings: Annotated[Settings, Depends(get_settings)],
) -> OpenAI:
    return OpenAI(api_key=settings.openai_api_key)


def get_scraper_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> WebsiteScraperService:
    return WebsiteScraperService(settings)


def get_summarizer_service(
    settings: Annotated[Settings, Depends(get_settings)],
    client: Annotated[OpenAI, Depends(get_openai_client)],
) -> WebsiteSummarizerService:
    return WebsiteSummarizerService(client=client, settings=settings)
