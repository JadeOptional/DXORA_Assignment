from datetime import datetime, timezone
import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformResult

class BlueskyPlatform(BasePlatform):
    name = "Bluesky"

    async def publish(self, message: str) -> PlatformResult:
        if not settings.bluesky_handle or not settings.bluesky_app_password:
            return self.failure("Missing BLUESKY_HANDLE or BLUESKY_APP_PASSWORD")

        service = settings.bluesky_service.rstrip("/")
        async with httpx.AsyncClient(timeout=20) as client:
            session_response = await client.post(
                f"{service}/xrpc/com.atproto.server.createSession",
                json={"identifier": settings.bluesky_handle,
                      "password": settings.bluesky_app_password},
            )
            session_response.raise_for_status()
            session = session_response.json()

            post_response = await client.post(
                f"{service}/xrpc/com.atproto.repo.createRecord",
                headers={"Authorization": f"Bearer {session['accessJwt']}"},
                json={
                    "repo": session["did"],
                    "collection": "app.bsky.feed.post",
                    "record": {
                        "$type": "app.bsky.feed.post",
                        "text": message,
                        "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    },
                },
            )
            post_response.raise_for_status()
            uri = post_response.json()["uri"]
            rkey = uri.rsplit("/", 1)[-1]
            url = f"https://bsky.app/profile/{settings.bluesky_handle}/post/{rkey}"
            return self.success(url, True)

    async def safe_publish(self, message: str) -> PlatformResult:
        try:
            return await self.publish(message)
        except (httpx.HTTPError, KeyError, ValueError) as exc:
            return self.failure(f"Bluesky API error: {exc}")
