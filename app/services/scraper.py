import requests
from bs4 import BeautifulSoup

from app.config import Settings

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
)


class WebsiteFetchError(Exception):
    """Raised when the target URL cannot be fetched or parsed."""


class WebsiteScraperService:
    """Fetches and extracts readable text from a public URL."""

    def __init__(self, settings: Settings) -> None:
        self._timeout = settings.scrape_timeout_seconds
        self._max_chars = settings.scrape_max_chars

    def fetch(self, url: str) -> str:
        try:
            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
                timeout=self._timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise WebsiteFetchError(f"Failed to fetch website: {exc}") from exc

        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""

        return (title + "\n\n" + text)[: self._max_chars]
