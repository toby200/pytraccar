"""Communication tests."""
import json

import aiohttp
import pytest

from pytraccar.api import API
from pytraccar.const import HEADERS

from .const import TEST_HOST, TEST_PASS, TEST_PORT, TEST_USER
from .fixtrues import geofence_response


@pytest.mark.asyncio
async def test_geofences(aresponses, event_loop, geofence_response):
    """Test geofences."""
    aresponses.add(
        "example.com:7728",
        "/api/geofences",
        "get",
        aresponses.Response(
            text=json.dumps(geofence_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        traccar = API(event_loop, session, TEST_USER, TEST_PASS, TEST_HOST, TEST_PORT)
        await traccar.get_geofences()
        assert isinstance(traccar.geofences, dict)
