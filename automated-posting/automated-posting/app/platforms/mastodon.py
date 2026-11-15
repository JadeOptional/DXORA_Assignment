import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult

class MastodonPlatform(BasePlatform):
    name = "Mastodon"

    async def publish(self, message: str) -> PlatformResult:
        if not settings.mastodon_instance_url or not settings.mastodon_access_token:
            return self.failure("Missing MASTODON_INSTANCE_URL or MASTODON_ACCESS_TOKEN")

        base_url = settings.mastodon_instance_url.rstrip("/")
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                f"{base_url}/api/v1/statuses",
                headers={"Authorization": f"Bearer {settings.mastodon_access_token}"},
                data={"status": message, "visibility": "public"},
            )
            response.raise_for_status()
            data = response.json()
            return self.success(data.get("url"), data.get("visibility") == "public")

    async def safe_publish(self, message: str) -> PlatformResult:
        try:
            return await self.publish(message)
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            return self.failure(f"Mastodon API error: {exc}")
