# BGG Search Telegram Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A Telegram bot that allows users to search for board games on [BoardGameGeek](https://boardgamegeek.com) and quickly share them in chats using inline queries.

## Features

- 🔍 **Inline Search**: Type `@botname <game>` in any chat to search BGG
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
git clone https://github.com/yourusername/bgg-search-telegram-bot.git
cd bgg-search-telegram-bot

# Install dependencies
uv sync

# Copy environment template and fill in your credentials
cp .env.example .env
```

## Configuration

Edit `.env` with your credentials:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
BGG_API_KEY=your_bgg_api_key_here
```

## Usage

```bash
# Run the bot
uv run main.py
```

Then in Telegram, type `@yourbotname Catan` in any chat to search for games.

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
docker build -t bgg-search-bot .

# Run
docker run -d --env-file .env bgg-search-bot
```

## License

[MIT](LICENSE)
