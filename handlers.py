import logging
import uuid

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ContextTypes

from bgg_client import BGGClient

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    if update.message is None:
        return
    await update.message.reply_text(
        "Hi! I'm a BGG Search Bot. Try searching for a game in any chat "
        "by typing my username followed by the game name!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    if update.message is None:
        return
    await update.message.reply_text("Usage: Type @[bot_username] [game name] to search BGG.")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is called when you type @bot_name [query]"""
    if update.inline_query is None:
        return
    query = update.inline_query.query

    if not query:
        return

    logger.info(f"Inline search for: {query}")

    try:
        results = BGGClient.search_game(query)
        # Limit to top 10 results for better performance
        results = results[:10]

        # Batch fetch details (thumbnails) for all results
        game_ids = [g["id"] for g in results]
        details_map = BGGClient.get_games_details(game_ids) if game_ids else {}

        articles = []
        for game in results:
            game_details = details_map.get(game["id"], {})
            thumbnail_url = game_details.get("thumbnail")

            articles.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=f"{game['name']} ({game['year']})",
                    input_message_content=InputTextMessageContent(
                        f"<b>{game['name']} ({game['year']})</b>\n"
                        f"<a href='{game['url']}'>View on BoardGameGeek</a>",
                        parse_mode="HTML",
                    ),
                    url=game["url"],
                    thumbnail_url=thumbnail_url,
                    description="Tap to share this game",
                )
            )

        await update.inline_query.answer(articles, cache_time=300)
    except Exception as e:
        logger.error(f"Error during inline query: {e}")
