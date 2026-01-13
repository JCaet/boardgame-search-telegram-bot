"""Tests for the BGG client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from bgg_client import BGGClient


class TestBGGClient:
    """Tests for BGGClient class."""
    
    @pytest.fixture(autouse=True)
    async def cleanup_client(self):
        """Reset the singleton client and cache before and after each test."""
        BGGClient._client = None
        BGGClient._cache = {}
        yield
        if BGGClient._client:
            await BGGClient._client.aclose()
        BGGClient._client = None
        BGGClient._cache = {}

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

        # Mock httpx.AsyncClient to return our mock client
        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.is_closed = False
            mock_client_class.return_value = mock_client

            results = await BGGClient.search_game("Catan")

            assert len(results) == 1
            assert results[0]["name"] == "Catan"
            assert results[0]["year"] == "1995"
            assert results[0]["id"] == "13"
            
            # Verify cache was populated
            assert "Catan" in BGGClient._cache

    @pytest.mark.asyncio
    async def test_search_game_uses_cache(self) -> None:
        """Test that search_game uses the cache."""
        # Pre-populate cache
        cached_results = [{"id": "99", "name": "Cached Game", "year": "2020", "url": "..."}]
        import time
        BGGClient._cache["Cached Game"] = (cached_results, time.time())
        
        with patch("httpx.AsyncClient") as mock_client_class:
            results = await BGGClient.search_game("Cached Game")
            
            assert results == cached_results
            # Ensure no HTTP request was made (mock class not instantiated or used)
            assert not mock_client_class.called

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
            mock_client.is_closed = False
            mock_client_class.return_value = mock_client

            results = await BGGClient.get_games_details(["13"])

            assert "13" in results
            assert results["13"]["thumbnail"] == "https://example.com/thumb.jpg"
            assert results["13"]["bayesaverage"] == 7.5

    @pytest.mark.asyncio
    async def test_get_games_details_accumulates_batches(self) -> None:
        """Test that get_games_details accumulates results from multiple batches."""
        # Create 25 IDs (batch size is 20, so 2 chunks)
        ids = [str(i) for i in range(25)]
        
        # We expect 2 calls. 
        # API returns XML with items corresponding to the requested IDs.
        # We can mock the response specific to the IDs or just return generic items.
        
        def side_effect(*args, **kwargs):
            # Parse 'id' param to see which IDs were requested
            params = kwargs.get('params', {})
            requested_ids = params.get('id', '').split(',')
            
            items_xml = ""
            for rid in requested_ids:
                 items_xml += f"""
                    <item type="boardgame" id="{rid}">
                        <thumbnail>thumb_{rid}.jpg</thumbnail>
                        <statistics><ratings><bayesaverage value="5.0"/></ratings></statistics>
                    </item>
                """
            
            content = f'<items>{items_xml}</items>'.encode('utf-8')
            resp = MagicMock()
            resp.content = content
            resp.raise_for_status = MagicMock()
            return resp

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=side_effect)
            mock_client.is_closed = False
            mock_client_class.return_value = mock_client

            results = await BGGClient.get_games_details(ids)

            # Verification
            assert len(results) == 25
            assert results["0"]["thumbnail"] == "thumb_0.jpg"
            assert results["24"]["thumbnail"] == "thumb_24.jpg"
            
            # Verify 2 batches were sent
            assert mock_client.get.call_count == 2
