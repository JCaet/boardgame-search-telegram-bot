import asyncio
import os
import time

import httpx
from dotenv import load_dotenv
from lxml import etree

load_dotenv()


class BGGClient:
    BASE_URL = "https://boardgamegeek.com/xmlapi2"
    API_KEY = os.getenv("BGG_API_KEY")

    # Connection pooling: Shared client instance
    _client: httpx.AsyncClient | None = None

    # Caching: Simple in-memory cache {query: (results, timestamp)}
    _cache: dict[str, tuple[list[dict], float]] = {}
    CACHE_TTL = 3600  # 1 hour

    @classmethod
    async def get_client(cls) -> httpx.AsyncClient:
        """Get or create the shared HTTP client."""
        if cls._client is None or cls._client.is_closed:
            cls._client = httpx.AsyncClient(
                timeout=10.0, limits=httpx.Limits(max_keepalive_connections=20, max_connections=20)
            )
        return cls._client

    @staticmethod
    def _get_headers() -> dict[str, str]:
        headers: dict[str, str] = {}
        if BGGClient.API_KEY:
            headers["Authorization"] = f"Bearer {BGGClient.API_KEY}"
        return headers

    @classmethod
    async def search_game(cls, query: str) -> list[dict]:
        """Search for games by name (with caching)."""
        # Check cache
        if query in cls._cache:
            results, timestamp = cls._cache[query]
            if time.time() - timestamp < cls.CACHE_TTL:
                return results

        params = {"query": query, "type": "boardgame"}
        client = await cls.get_client()

        response = await client.get(
            f"{cls.BASE_URL}/search",
            params=params,
            headers=cls._get_headers(),
        )
        response.raise_for_status()

        root = etree.fromstring(response.content)
        games: list[dict[str, str | None]] = []
        for item in root.xpath("//item"):
            game_id: str = item.get("id", "")
            name_nodes = item.xpath("name[@type='primary']/@value")
            name: str = str(name_nodes[0]) if name_nodes else "Unknown"
            year_nodes = item.xpath("yearpublished/@value")
            year: str = str(year_nodes[0]) if year_nodes else "N/A"

            games.append(
                {
                    "id": game_id,
                    "name": name,
                    "year": year,
                    "url": f"https://boardgamegeek.com/boardgame/{game_id}",
                }
            )

        # Update cache
        cls._cache[query] = (games, time.time())
        return games

    @staticmethod
    async def get_game_details(game_id: str) -> dict | None:
        """Fetch thumbnail and other details for a specific game."""
        details = await BGGClient.get_games_details([game_id])
        return details.get(game_id)

    @classmethod
    async def get_games_details(
        cls, game_ids: list[str]
    ) -> dict[str, dict[str, str | float | None]]:
        """Fetch thumbnail and other details for multiple games at once."""
        if not game_ids:
            return {}

        results: dict[str, dict[str, str | float | None]] = {}
        client = await cls.get_client()

        # BGG API has a limit on IDs per request, batch into chunks
        batch_size = 20
        tasks = []
        for i in range(0, len(game_ids), batch_size):
            batch_ids = game_ids[i : i + batch_size]
            params: dict[str, str | int] = {"id": ",".join(batch_ids), "stats": 1}

            tasks.append(
                client.get(
                    f"{cls.BASE_URL}/thing",
                    params=params,
                    headers=cls._get_headers(),
                )
            )

        # Run requests in parallel
        # Note: BGG limits rate, but 2-3 parallel requests (40-60 items) is usually safe
        responses = await asyncio.gather(*tasks)

        for response in responses:
            response.raise_for_status()

            # FIX: Process response inside the loop to accumulate results from all batches
            root = etree.fromstring(response.content)

            for item in root.xpath("//item"):
                game_id: str = item.get("id", "")
                thumbnail = item.xpath("thumbnail/text()")
                image = item.xpath("image/text()")
                description = item.xpath("description/text()")
                # Extract Geek Rating (bayesaverage) for sorting
                bayesaverage_nodes = item.xpath("statistics/ratings/bayesaverage/@value")
                bayesaverage = float(bayesaverage_nodes[0]) if bayesaverage_nodes else 0.0

                results[game_id] = {
                    "thumbnail": str(thumbnail[0]) if thumbnail else None,
                    "image": str(image[0]) if image else None,
                    "description": str(description[0]) if description else "",
                    "bayesaverage": bayesaverage,
                }

        return results
