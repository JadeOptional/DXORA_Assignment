import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult

class WordPressPlatform(BasePlatform):
    name = "WordPress"

    async def publish(self, message: str) -> PlatformResult:
        required = [settings.wordpress_site_url, settings.wordpress_username,
                    settings.wordpress_app_password]
        if not all(required):
            return self.failure(
                "Missing WORDPRESS_SITE_URL, WORDPRESS_USERNAME or WORDPRESS_APP_PASSWORD"
            )

        base_url = settings.wordpress_site_url.rstrip("/")
        async with httpx.AsyncClient(timeout=25) as client:
            response = await client.post(
                f"{base_url}/wp-json/wp/v2/posts",
                auth=(settings.wordpress_username, settings.wordpress_app_password),
                json={"title": "Quick update", "content": message, "status": "publish"},
            )
            response.raise_for_status()
            data = response.json()
            return self.success(data.get("link"), data.get("status") == "publish")

    async def safe_publish(self, message: str) -> PlatformResult:
        try:
            return await self.publish(message)
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            return self.failure(f"WordPress API error: {exc}")
