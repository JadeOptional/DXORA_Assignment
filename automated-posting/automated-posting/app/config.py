import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    # Bluesky
    bluesky_handle: str = os.getenv("BLUESKY_HANDLE", "")
    bluesky_app_password: str = os.getenv("BLUESKY_APP_PASSWORD", "")
    bluesky_service: str = os.getenv("BLUESKY_SERVICE", "https://bsky.social")

    # Mastodon
    mastodon_instance_url: str = os.getenv("MASTODON_INSTANCE_URL", "")
    mastodon_access_token: str = os.getenv("MASTODON_ACCESS_TOKEN", "")

    # DEV.to
    devto_api_key: str = os.getenv("DEVTO_API_KEY", "")
    devto_username: str = os.getenv("DEVTO_USERNAME", "")

    # WordPress
    wordpress_site_url: str = os.getenv("WORDPRESS_SITE_URL", "")
    wordpress_username: str = os.getenv("WORDPRESS_USERNAME", "")
    wordpress_app_password: str = os.getenv("WORDPRESS_APP_PASSWORD", "")

    # Telegram
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_channel_id: str = os.getenv("TELEGRAM_CHANNEL_ID", "")
    telegram_channel_username: str = os.getenv("TELEGRAM_CHANNEL_USERNAME", "")

settings = Settings()
