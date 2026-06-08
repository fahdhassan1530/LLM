from openai import OpenAI

from app.config import Settings
from app.prompts import SYSTEM_PROMPT, USER_PROMPT_PREFIX


class SummarizationError(Exception):
    """Raised when the LLM request fails."""


class WebsiteSummarizerService:
    """Calls OpenAI to produce a markdown summary of website content."""

    def __init__(self, client: OpenAI, settings: Settings) -> None:
        self._client = client
        self._model = settings.openai_model

    def summarize(self, website_text: str) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=self._build_messages(website_text),
            )
        except Exception as exc:
            raise SummarizationError(f"OpenAI request failed: {exc}") from exc

        content = response.choices[0].message.content
        if not content:
            raise SummarizationError("OpenAI returned an empty response")
        return content

    @staticmethod
    def _build_messages(website_text: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_PREFIX + website_text},
        ]
