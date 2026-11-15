# Automated Multi-Platform Posting System

A FastAPI application that accepts one message containing exactly one HTTP(S) CTA URL and attempts to publish it to Bluesky, Mastodon, DEV.to, WordPress, and Telegram.

## Requirements

- Python 3.11+
- An account and API credentials for each platform you want to connect
- Publishing permissions on the target Mastodon instance, WordPress site, and Telegram channel

## Setup

```bash
git clone <your-public-repository-url>
cd automated-posting
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies and configure credentials:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the credentials. Never commit `.env`.

## Platform setup notes

- **Bluesky:** create an app password and use your handle plus app password.
- **Mastodon:** create an OAuth access token with `write:statuses`; use your own instance URL.
- **DEV.to:** create an API key in your DEV.to account settings. The integration publishes a short article titled `Quick update` with the submitted message as its body.
- **WordPress:** enable Application Passwords and create one for your user. The user must have permission to publish posts.
- **Telegram:** create a bot with BotFather, add it as an administrator of your channel, and set the channel ID. For a public permalink, set `TELEGRAM_CHANNEL_USERNAME` to the public channel username without `@`.

Platform policies, account permissions, rate limits, and API access may vary. Test with accounts/channels you control.

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

Open API documentation at http://localhost:4000/docs.

## Request

```bash
curl -X POST "http://localhost:4000/posting" \
  -H "Content-Type: application/json" \
  -d '{"message":"Check out our latest business platform: https://example.com"}'
```

## Response behavior

Each platform returns its own status. A failed or unconfigured platform does not stop the remaining integrations. The top-level `success` value is `true` when at least one platform successfully accepts the post. A platform's public URL is returned when the API provides one or it can be constructed from the public channel/account information.

The `date` and `time` fields are UTC timestamps recorded after the API confirms the publish operation. `public_access` is based on the platform's response and configured public destination; it is not an independent anonymous-browser verification.

## Tests

```bash
python -m pytest -q
```

The included tests cover request validation. They do not publish live posts.

## Security

- Keep API keys and passwords in `.env`.
- `.env` is excluded through `.gitignore`.
- Use app passwords/tokens with the minimum required permissions.
- Do not upload real credentials, access tokens, or private account data to GitHub.
