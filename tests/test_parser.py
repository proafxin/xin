import pytest
from pydantic import BaseModel

from xin.parser import Base


@pytest.mark.asyncio
async def test_base() -> None:
    assert isinstance(Base(), BaseModel)
