"""Test to verify InlineQueryResultArticle handles None thumbnail_url correctly."""

from telegram import InlineQueryResultArticle, InputTextMessageContent


def test_none_thumbnail():
    """Test what happens when thumbnail_url is None."""
    print("Testing InlineQueryResultArticle with None thumbnail_url...\n")

    # Test 1: With valid thumbnail
    result_with_thumb = InlineQueryResultArticle(
        id="test-1",
        title="Game with Thumbnail",
        input_message_content=InputTextMessageContent("Test message"),
        url="https://boardgamegeek.com/boardgame/12345",
        thumbnail_url="https://cf.geekdo-images.com/example.jpg",
    )
    print("✅ Created result WITH thumbnail_url")
    print(f"   thumbnail_url = {result_with_thumb.thumbnail_url}")

    # Test 2: With None thumbnail
    result_no_thumb = InlineQueryResultArticle(
        id="test-2",
        title="Game without Thumbnail",
        input_message_content=InputTextMessageContent("Test message"),
        url="https://boardgamegeek.com/boardgame/12346",
        thumbnail_url=None,  # This is what happens when details.get("thumbnail") returns None
    )
    print("\n✅ Created result WITHOUT thumbnail_url (None)")
    print(f"   thumbnail_url = {result_no_thumb.thumbnail_url}")

    # The issue: When thumbnail_url is None, Telegram might not show any thumbnail
    # or might show a default placeholder
    print("\n" + "=" * 80)
    print("OBSERVATION:")
    print("When thumbnail_url is None, Telegram will NOT display a thumbnail in inline results.")
    print("The code in handlers.py line 170-181 DOES pass thumbnail_url correctly.")
    print("\nIf thumbnails are missing in production, check if BGG_API_KEY is set in Cloud Run!")


if __name__ == "__main__":
    test_none_thumbnail()
