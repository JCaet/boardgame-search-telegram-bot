import asyncio
import contextlib
import os
import time

import httpx
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# We need to add project root to path to import bgg_client
import sys  # noqa: E402

sys.path.append(os.getcwd())

from bgg_client import BGGClient  # noqa: E402  # type: ignore


async def test_concurrency(concurrency: int = 5) -> bool:
    print(f"Testing with concurrency: {concurrency}")

    # Pre-warm the client
    await BGGClient.get_client()

    queries = [
        "Catan",
        "Monopoly",
        "Risk",
        "Pandemic",
        "Ticket to Ride",
        "Gloomhaven",
        "Scythe",
        "Terraforming Mars",
        "Wingspan",
        "Azul",
    ]

    # Limit queries to concurrency count
    queries = queries[:concurrency]

    tasks = []
    start_time = time.time()

    for q in queries:
        tasks.append(BGGClient.search_game(q))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = time.time()

    success = 0
    errors = 0

    for res in results:
        if isinstance(res, Exception):
            errors += 1
            print(f"Error: {res}")
            if isinstance(res, httpx.HTTPStatusError):
                print(f"Status Code: {res.response.status_code}")
        else:
            success += 1

    print(f"Total time: {end_time - start_time:.2f}s")
    print(f"Success: {success}")
    print(f"Errors: {errors}")
    return errors == 0


async def main() -> None:
    print("WARNING: This script hits the real BGG API.")
    print("Do not run this too often.")

    # Test 3 concurrent requests (safe-ish)
    if await test_concurrency(3):
        print("PASS: 3 concurrent requests succeeded.")
    else:
        print("FAIL: 3 concurrent requests failed.")

    # Wait a bit
    await asyncio.sleep(5)

    # Test 5 concurrent requests
    if await test_concurrency(5):
        print("PASS: 5 concurrent requests succeeded.")
    else:
        print("FAIL: 5 concurrent requests failed.")


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
