"""Test script to verify thumbnail fetching for Nemesis game."""

import asyncio
import sys

from bgg_client import BGGClient


async def test_nemesis_thumbnail():
    """Fetch Nemesis from BGG and verify thumbnail is present."""
    print("🔍 Searching for 'Nemesis' on BGG...")

    # Search for Nemesis
    results = await BGGClient.search_game("Nemesis")

    if not results:
        print("❌ No results found for 'Nemesis'")
        return False

    print(f"\n✅ Found {len(results)} results")
    print("\n📋 Top 5 search results:")
    for i, game in enumerate(results[:5], 1):
        print(f"  {i}. {game['name']} ({game['year']}) - ID: {game['id']}")

    # Get the first result (most likely the main Nemesis game)
    nemesis = results[0]
    print(f"\n🎯 Testing with: {nemesis['name']} ({nemesis['year']}) - ID: {nemesis['id']}")

    # Fetch detailed information including thumbnail
    print(f"\n🔄 Fetching game details for ID {nemesis['id']}...")
    details = await BGGClient.get_game_details(nemesis["id"])

    if not details:
        print("❌ Failed to fetch game details")
        return False

    print("\n📊 Game Details:")
    print(f"  • Thumbnail: {details.get('thumbnail', 'MISSING')}")
    print(f"  • Image: {details.get('image', 'MISSING')}")
    print(f"  • Rating: {details.get('bayesaverage', 'N/A')}")
    print(f"  • Description: {details.get('description', 'N/A')[:100]}...")

    # Verify thumbnail exists
    if details.get("thumbnail"):
        print(f"\n✅ SUCCESS: Thumbnail URL found: {details['thumbnail']}")
        return True
    else:
        print("\n❌ FAILURE: Thumbnail is missing!")
        return False


async def main():
    """Main test runner."""
    try:
        success = await test_nemesis_thumbnail()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
