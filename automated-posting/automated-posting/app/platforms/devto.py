import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult

class DevToPlatform(BasePlatform):
    name = "DEV.to"

    async def publish(self, message: str) -> PlatformResult:
        if not settings.devto_api_key:
            return self.failure("Missing DEVTO_API_KEY")

        # DEV.to requires an article title and body. Keep the submitted message as the body.
        title = "Quick update"
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.post(
                "https://dev.to/api/articles",
                headers={"api-key": settings.devto_api_key,
                         "Accept": "application/vnd.forem.api-v1+json",
                         "User-Agent": "AutomatedPostingSystem/1.0"},
                json={"article": {
                    "title": title,
                    "body_markdown": message,
                    "published": True,
                }},
            )
            response.raise_for_status()
            data = response.json()
            return self.success(data.get("url"), bool(data.get("url")))

    async def safe_publish(self, message: str) -> PlatformResult:
        try:
            return await self.publish(message)
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            return self.failure(f"DEV.to API error: {exc}")
