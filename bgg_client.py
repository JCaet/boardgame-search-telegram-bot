import os

import requests
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
    def search_game(query: str) -> list[dict]:
        """Search for games by name."""
        params = {"query": query, "type": "boardgame"}
        response = requests.get(
            f"{BGGClient.BASE_URL}/search", params=params, headers=BGGClient._get_headers()
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
    def get_game_details(game_id: str) -> dict | None:
        """Fetch thumbnail and other details for a specific game."""
        details = BGGClient.get_games_details([game_id])
        return details.get(game_id)

    @staticmethod
    def get_games_details(game_ids: list[str]) -> dict[str, dict[str, str | None]]:
        """Fetch thumbnail and other details for multiple games at once."""
        if not game_ids:
            return {}

        params: dict[str, str | int] = {"id": ",".join(game_ids), "stats": 1}
        response = requests.get(
            f"{BGGClient.BASE_URL}/thing", params=params, headers=BGGClient._get_headers()
        )
        response.raise_for_status()

        root = etree.fromstring(response.content)
        results: dict[str, dict[str, str | None]] = {}

        for item in root.xpath("//item"):
            game_id: str = item.get("id", "")
            thumbnail = item.xpath("thumbnail/text()")
            image = item.xpath("image/text()")
            description = item.xpath("description/text()")

            results[game_id] = {
                "thumbnail": str(thumbnail[0]) if thumbnail else None,
                "image": str(image[0]) if image else None,
                "description": str(description[0]) if description else "",
            }

        return results
