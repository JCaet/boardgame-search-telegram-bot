"""Test to verify thumbnail URLs are valid and accessible."""

import asyncio

import httpx

from bgg_client import BGGClient


async def test_thumbnail_accessibility():
    """Check if thumbnail URLs are actually accessible via HTTP."""
    print("🔍 Testing thumbnail URL accessibility...\n")

    # Search for Nemesis
    results = await BGGClient.search_game("Nemesis")
    game_ids = [g["id"] for g in results[:5]]
    details_map = await BGGClient.get_games_details(game_ids)

    async with httpx.AsyncClient(timeout=10.0) as client:
        for game in results[:5]:
            game_details = details_map.get(game["id"], {})
            thumbnail_url = game_details.get("thumbnail")

            print(f"Game: {game['name']}")
            print(f"Thumbnail URL: {thumbnail_url}")

            if thumbnail_url:
                try:
                    response = await client.head(thumbnail_url)
                    print(f"Status: {response.status_code}")
                    print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")

                    if response.status_code == 200:
                        print("✅ Thumbnail is accessible")
                    else:
                        print(f"❌ Thumbnail returned status {response.status_code}")
                except Exception as e:
                    print(f"❌ Error accessing thumbnail: {e}")
            else:
                print("❌ No thumbnail URL")

            print("-" * 80)


if __name__ == "__main__":
    asyncio.run(test_thumbnail_accessibility())
