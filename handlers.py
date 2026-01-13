import asyncio
import logging
import time
import traceback
import uuid

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ContextTypes

from bgg_client import BGGClient

logger = logging.getLogger(__name__)

# Throttle: track last query time per user to debounce rapid typing
_user_last_query: dict[int, float] = {}
_throttle_lock = asyncio.Lock()  # Lock to protect shared throttle state
THROTTLE_SECONDS = 0.5  # Minimum time between queries per user
_last_cleanup_time: float = 0
CLEANUP_INTERVAL = 60  # Cleanup stale entries every 60 seconds
STALE_ENTRY_AGE = 60  # Remove entries older than 60 seconds
MIN_QUERY_LENGTH = 2  # Minimum characters required for search
CANDIDATE_LIMIT = 40  # Max candidates for rating lookup (BGG allows 20 IDs/request)


async def _cleanup_throttle_dict() -> None:
    """Remove stale entries from the throttle dictionary to prevent memory growth."""
    global _last_cleanup_time
    current_time = time.time()
    if current_time - _last_cleanup_time < CLEANUP_INTERVAL:
        return
    _last_cleanup_time = current_time
    cutoff = current_time - STALE_ENTRY_AGE
    async with _throttle_lock:
        stale_users = [uid for uid, ts in _user_last_query.items() if ts < cutoff]
        for uid in stale_users:
            del _user_last_query[uid]
    if stale_users:
        logger.debug(f"Cleaned up {len(stale_users)} stale throttle entries")


async def _search_games(query: str, limit: int = 10) -> tuple[list[dict], dict[str, dict], int]:
    """
    Search for games and fetch details, sorted by Geek Rating.

    Returns:
        Tuple of (sorted results list, details map, total results count)
    """
    results = await BGGClient.search_game(query)
    if not results:
        return [], {}, 0

    total_count = len(results)

    # Fetch ratings for candidates to ensure proper sorting
    # (the API doesn't return results in rating order)
    candidates = results[:CANDIDATE_LIMIT]

    # Fetch details for thumbnails and ratings
    game_ids = [g["id"] for g in candidates]
    details_map = await BGGClient.get_games_details(game_ids) if game_ids else {}

    # Sort by Geek Rating (bayesaverage) in descending order
    candidates.sort(
        key=lambda g: float(details_map.get(g["id"], {}).get("bayesaverage") or 0),
        reverse=True,
    )

    # Return only the requested limit
    return candidates[:limit], details_map, total_count


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    if update.message is None:
        return
    await update.message.reply_text(
        "Hi! I'm a Board Game Search Bot. Try searching for a game in any chat "
        "by typing my username followed by the game name!\n\n"
        "Powered by BoardGameGeek\n"
        "<i>Version: v1.1.2-debug</i>",
        parse_mode="HTML",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    if update.message is None:
        return
    await update.message.reply_text(
        "Usage:\n"
        "• Inline: Type @[bot_username] [game name] in any chat\n"
        "• Direct: Just send me a game name to search\n\n"
        "Powered by BoardGameGeek"
    )


async def search_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle direct message search. User sends a game name, bot replies with results."""
    if update.message is None or update.message.text is None:
        return

    query = update.message.text.strip()

    if len(query) < MIN_QUERY_LENGTH:
        await update.message.reply_text(
            f"Please enter at least {MIN_QUERY_LENGTH} characters to search."
        )
        return

    logger.info(f"Direct message search for: {query}")

    try:
        results, details_map, total_count = await _search_games(query, limit=10)

        if not results:
            await update.message.reply_text(f"No games found for '{query}'.")
            return

        # Format response (show top 10)
        response_lines = [f"🎲 <b>Search results for '{query}':</b>\n"]
        for i, game in enumerate(results[:10], 1):
            response_lines.append(
                f"{i}. <a href='{game['url']}'>{game['name']}</a> ({game['year']})"
            )

        # Add attribution
        response_lines.append("\nPowered by BoardGameGeek")

        # DEBUG: Add thumbnail info to response
        debug_lines = ["\n🔍 <b>Debug Info:</b>"]
        for i, game in enumerate(results[:10]):
            details = details_map.get(game["id"], {})
            thumb = details.get("thumbnail")
            debug_lines.append(f"{i + 1}. Thumb: {thumb if thumb else '❌ MISSING'}")

        await update.message.reply_text(
            "\n".join(response_lines + debug_lines),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    except Exception as e:
        logger.error(f"Error during direct message search: {e}")
        await update.message.reply_text("Something went wrong. Please try again.")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is called when you type @bot_name [query]"""
    await _cleanup_throttle_dict()  # Periodic cleanup to prevent memory growth
    logger.debug("inline_query handler triggered")
    if update.inline_query is None:
        logger.warning("update.inline_query is None")
        return
    query = update.inline_query.query
    logger.debug(f"Received query: '{query}'")

    if not query or len(query) < MIN_QUERY_LENGTH:
        logger.debug(f"Query too short or empty: '{query}'")
        return

    # Throttle: skip if user queried recently (debounce effect)
    user_id = update.inline_query.from_user.id
    current_time = time.time()
    async with _throttle_lock:
        last_query_time = _user_last_query.get(user_id, 0)
        if current_time - last_query_time < THROTTLE_SECONDS:
            logger.debug(f"Throttled query from user {user_id}")
            return
        _user_last_query[user_id] = current_time

    logger.info(f"Inline search for: {query}")

    try:
        results, details_map, _ = await _search_games(query, limit=10)
        logger.debug(f"Search returned {len(results)} results")

        articles = []
        for game in results:
            game_details = details_map.get(game["id"], {})
            # Prefer high-res image for Telegram thumbnail, fallback to small thumbnail
            thumbnail_url = game_details.get("image") or game_details.get("thumbnail")

            # Build article parameters
            article_params = {
                "id": str(uuid.uuid4()),
                "title": f"{game['name']} ({game['year']})",
                "input_message_content": InputTextMessageContent(
                    f"<a href='{game['url']}'><b>{game['name']} ({game['year']})</b></a>\n"
                    "Powered by BoardGameGeek",
                    parse_mode="HTML",
                ),
                "description": f"Rating: {game_details.get('bayesaverage', 'N/A')} - Tap to share",
            }

            # Only include thumbnail_url if it exists
            if thumbnail_url:
                article_params["thumbnail_url"] = thumbnail_url

            articles.append(InlineQueryResultArticle(**article_params))

        await update.inline_query.answer(articles, cache_time=300)
    except Exception as e:
        logger.error(f"Error during inline query: {e}")
        logger.error(traceback.format_exc())
