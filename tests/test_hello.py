import pytest

from xin.db import SQL_DRIVERS


@pytest.mark.asyncio
async def test_hello():
    assert isinstance(SQL_DRIVERS, dict)
