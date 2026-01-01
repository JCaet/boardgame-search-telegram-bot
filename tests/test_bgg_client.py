"""Tests for the BGG client."""

from unittest.mock import Mock, patch

from bgg_client import BGGClient


class TestBGGClient:
    """Tests for BGGClient class."""

    @patch("bgg_client.requests.get")
    def test_search_game_returns_list(self, mock_get: Mock) -> None:
        """Test that search_game returns a list of games."""
        mock_response = Mock()
        mock_response.content = b"""<?xml version="1.0" encoding="utf-8"?>
        <items total="1">
            <item type="boardgame" id="13">
                <name type="primary" value="Catan"/>
                <yearpublished value="1995"/>
            </item>
        </items>"""
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        results = BGGClient.search_game("Catan")

        assert len(results) == 1
        assert results[0]["name"] == "Catan"
        assert results[0]["year"] == "1995"
        assert results[0]["id"] == "13"

    @patch("bgg_client.requests.get")
    def test_get_games_details_returns_thumbnails(self, mock_get: Mock) -> None:
        """Test that get_games_details returns thumbnails."""
        mock_response = Mock()
        mock_response.content = b"""<?xml version="1.0" encoding="utf-8"?>
        <items>
            <item type="boardgame" id="13">
                <thumbnail>https://example.com/thumb.jpg</thumbnail>
                <image>https://example.com/image.jpg</image>
                <description>A game</description>
            </item>
        </items>"""
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        results = BGGClient.get_games_details(["13"])

        assert "13" in results
        assert results["13"]["thumbnail"] == "https://example.com/thumb.jpg"
