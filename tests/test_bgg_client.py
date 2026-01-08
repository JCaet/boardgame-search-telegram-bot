"""Tests for the BGG client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from bgg_client import BGGClient


class TestBGGClient:
    """Tests for BGGClient class."""

    @pytest.mark.asyncio
    async def test_search_game_returns_list(self) -> None:
        """Test that search_game returns a list of games."""
        mock_response = MagicMock()
        mock_response.content = b"""<?xml version="1.0" encoding="utf-8"?>
        <items total="1">
            <item type="boardgame" id="13">
                <name type="primary" value="Catan"/>
                <yearpublished value="1995"/>
            </item>
        </items>"""
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            results = await BGGClient.search_game("Catan")

            assert len(results) == 1
            assert results[0]["name"] == "Catan"
            assert results[0]["year"] == "1995"
            assert results[0]["id"] == "13"

    @pytest.mark.asyncio
    async def test_get_games_details_returns_thumbnails(self) -> None:
        """Test that get_games_details returns thumbnails."""
        mock_response = MagicMock()
        mock_response.content = b"""<?xml version="1.0" encoding="utf-8"?>
        <items>
            <item type="boardgame" id="13">
                <thumbnail>https://example.com/thumb.jpg</thumbnail>
                <image>https://example.com/image.jpg</image>
                <description>A game</description>
                <statistics>
                    <ratings>
                        <bayesaverage value="7.5"/>
                    </ratings>
                </statistics>
            </item>
        </items>"""
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client_class.return_value = mock_client

            results = await BGGClient.get_games_details(["13"])

            assert "13" in results
            assert results["13"]["thumbnail"] == "https://example.com/thumb.jpg"
            assert results["13"]["bayesaverage"] == 7.5
