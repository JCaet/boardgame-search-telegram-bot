import os

import httpx
from dotenv import load_dotenv
from lxml import etree

load_dotenv()


class BGGClient:
    BASE_URL = "https://boardgamegeek.com/xmlapi2"
    API_KEY = os.getenv("BGG_API_KEY")

    @staticmethod
    def _get_headers() -> dict[str, str]:
        headers: dict[str, str] = {}
        if BGGClient.API_KEY:
            headers["Authorization"] = f"Bearer {BGGClient.API_KEY}"
        return headers

    @staticmethod
    async def search_game(query: str) -> list[dict]:
        """Search for games by name."""
        params = {"query": query, "type": "boardgame"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BGGClient.BASE_URL}/search",
                params=params,
                headers=BGGClient._get_headers(),
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
        return games

    @staticmethod
    async def get_game_details(game_id: str) -> dict | None:
        """Fetch thumbnail and other details for a specific game."""
        details = await BGGClient.get_games_details([game_id])
        return details.get(game_id)

    @staticmethod
    async def get_games_details(game_ids: list[str]) -> dict[str, dict[str, str | None]]:
        """Fetch thumbnail and other details for multiple games at once."""
        if not game_ids:
            return {}

        results: dict[str, dict[str, str | None]] = {}

        # BGG API has a limit on IDs per request, batch into chunks
        batch_size = 20
        async with httpx.AsyncClient() as client:
            for i in range(0, len(game_ids), batch_size):
                batch_ids = game_ids[i : i + batch_size]
                params: dict[str, str | int] = {"id": ",".join(batch_ids), "stats": 1}
                response = await client.get(
                    f"{BGGClient.BASE_URL}/thing",
                    params=params,
                    headers=BGGClient._get_headers(),
                )
                response.raise_for_status()

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
