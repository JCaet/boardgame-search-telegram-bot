# Board Game Search Telegram Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A Telegram bot that allows users to search for board games on [BoardGameGeek](https://boardgamegeek.com) and quickly share them in chats using inline queries.

## Features

- 🔍 **Inline Search**: Type `@botname <game>` in any chat to search BoardGameGeek
- 🖼️ **Thumbnails**: See game images in search results  
- 🔗 **Quick Share**: Tap a result to share a formatted link

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- BGG API Key (register at BoardGameGeek)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/boardgame-search-telegram-bot.git
cd boardgame-search-telegram-bot

# Install dependencies
uv sync

# Copy environment template and fill in your credentials
cp .env.example .env
```

## Configuration

Edit `.env` with your credentials:

```env
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
BGG_API_KEY=your_bgg_api_key_here

# For webhook mode (Cloud Run deployment)
WEBHOOK_URL=https://your-service.run.app
WEBHOOK_SECRET=your_generated_secret  # Recommended for security
```

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Bot token from [@BotFather](https://t.me/BotFather) |
| `BGG_API_KEY` | Yes | BoardGameGeek API key |
| `WEBHOOK_URL` | No* | Your Cloud Run service URL (*required for webhook mode) |
| `WEBHOOK_SECRET` | No | Secret token for webhook verification (recommended) |
| `PORT` | No | Webhook server port (default: 8080, auto-set by Cloud Run) |

Generate a webhook secret with:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Usage

```bash
# Run the bot (polling mode)
uv run main.py
```

Then in Telegram, type `@yourbotname Catan` in any chat to search for games.

## Cloud Run Deployment

The bot can be deployed to Google Cloud Run using the included GitHub Actions workflow.

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `GCP_PROJECT_ID` | Your Google Cloud project ID |
| `GCP_CREDENTIALS` | Service account JSON key with Cloud Run permissions |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token |
| `BGG_API_KEY` | Your BoardGameGeek API key |
| `WEBHOOK_URL` | Your Cloud Run service URL (e.g., `https://boardgame-search-bot-xxx-uc.a.run.app`) |
| `WEBHOOK_SECRET` | Generated secret for webhook verification |

The deployment is triggered automatically on successful releases or manually via workflow dispatch.


## Development

```bash
# Install dev dependencies
uv sync --group dev

# Run linter
uv run ruff check .

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov

# Install pre-commit hooks
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

## Docker

```bash
# Build
docker build -t boardgame-search-bot .

# Run
docker run -d --env-file .env boardgame-search-bot
```

## License

[MIT](LICENSE)
