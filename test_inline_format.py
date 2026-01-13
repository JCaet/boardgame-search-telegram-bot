"""Test inline query format to verify thumbnail_url field."""

import asyncio

from telegram import InlineQueryResultArticle, InputTextMessageContent

from bgg_client import BGGClient


async def test_inline_query_format():
    """Simulate the inline query handler to see how thumbnails are formatted."""
    print("🔍 Simulating inline query for 'Nemesis'...")

    # Replicate the search logic from handlers.py
    query = "Nemesis"
    results = await BGGClient.search_game(query)

    if not results:
        print("❌ No results found")
        return

    # Fetch details (replicating _search_games logic)
    candidates = results[:40]
    game_ids = [g["id"] for g in candidates]
    details_map = await BGGClient.get_games_details(game_ids)

    # Sort by rating
    candidates.sort(
        key=lambda g: float(details_map.get(g["id"], {}).get("bayesaverage") or 0),
        reverse=True,
    )

    print(f"\n✅ Found {len(results)} total results\n")

    # Create inline query results (top 10)
    for i, game in enumerate(candidates[:10], 1):
        game_details = details_map.get(game["id"], {})
        thumbnail_url = game_details.get("thumbnail")

        print(f"{i}. {game['name']} ({game['year']})")
        print(f"   ID: {game['id']}")
        print(f"   URL: {game['url']}")
        print(f"   Thumbnail: {thumbnail_url if thumbnail_url else '❌ MISSING'}")
        print(f"   Rating: {game_details.get('bayesaverage', 'N/A')}")

        # Create the inline result object
        result = InlineQueryResultArticle(
            id=f"test-{game['id']}",
            title=f"{game['name']} ({game['year']})",
            input_message_content=InputTextMessageContent(
                f"<b>{game['name']} ({game['year']})</b>\nPowered by BoardGameGeek",
                parse_mode="HTML",
            ),
            url=game["url"],
            thumbnail_url=thumbnail_url,  # This is the critical field
            description=f"Rating: {game_details.get('bayesaverage', 'N/A')} - Tap to share",
        )

        # Check if thumbnail is set
        if hasattr(result, "thumbnail_url") and result.thumbnail_url:
            print(f"   ✅ InlineQueryResultArticle.thumbnail_url = {result.thumbnail_url}")
        else:
            print("   ❌ InlineQueryResultArticle.thumbnail_url is NOT SET!")

        print()

    print("\n" + "=" * 80)
    print("SUMMARY:")
    thumbnails_present = sum(
        1 for g in candidates[:10] if details_map.get(g["id"], {}).get("thumbnail")
    )
    print(f"Thumbnails present: {thumbnails_present}/10")
    if thumbnails_present == 10:
        print("✅ All thumbnails are present!")
    else:
        print(f"❌ {10 - thumbnails_present} thumbnails are missing!")


if __name__ == "__main__":
    asyncio.run(test_inline_query_format())
