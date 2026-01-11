import logging
import os

from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    InlineQueryHandler,
    MessageHandler,
    filters,
)

import handlers

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        return

    application = ApplicationBuilder().token(token).build()

    # Handlers
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help_command))
    application.add_handler(InlineQueryHandler(handlers.inline_query))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.search_message)
    )

    if webhook_url := os.getenv("WEBHOOK_URL"):
        port = int(os.getenv("PORT", "8080"))
        webhook_secret = os.getenv("WEBHOOK_SECRET")
        if not webhook_secret:
            logger.warning("WEBHOOK_SECRET not set - webhook requests will not be verified!")
        logger.info(f"Starting webhook on port {port}...")
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=token,
            webhook_url=f"{webhook_url}/{token}",
            secret_token=webhook_secret,
        )
    else:
        logger.info("Bot started with polling...")
        application.run_polling()


if __name__ == "__main__":
    main()
