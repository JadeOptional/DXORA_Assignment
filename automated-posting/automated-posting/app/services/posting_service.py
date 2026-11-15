import asyncio
from app.platforms.bluesky import BlueskyPlatform
from app.platforms.mastodon import MastodonPlatform
from app.platforms.devto import DevToPlatform
from app.platforms.wordpress import WordPressPlatform
from app.platforms.telegram import TelegramPlatform
from app.schemas import PlatformResult

PLATFORMS = [
    BlueskyPlatform(),
    MastodonPlatform(),
    DevToPlatform(),
    WordPressPlatform(),
    TelegramPlatform(),
]

async def post_to_all_platforms(message: str) -> list[PlatformResult]:
    # Each integration catches its own errors, so one failure does not stop the others.
    results = await asyncio.gather(
        *(platform.safe_publish(message) for platform in PLATFORMS),
        return_exceptions=True,
    )

    normalized: list[PlatformResult] = []
    for platform, result in zip(PLATFORMS, results):
        if isinstance(result, Exception):
            normalized.append(platform.failure(f"Unexpected integration error: {result}"))
        else:
            normalized.append(result)
    return normalized
