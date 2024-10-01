from datetime import datetime

import pytest
from pandas import DataFrame
from pydantic import BaseModel

from xin.parser import Base, serialize_table


@pytest.mark.asyncio
async def test_base() -> None:
    assert isinstance(Base(), BaseModel)


@pytest.mark.asyncio
async def test_serialize_pandas_table() -> None:
    now = datetime.now()
    data1 = {"n": "xin", "id": 200, "f": ["a", "b", "c"], "c": now, "b": 20.0, "d": {"a": 1}}
    data2 = {"n": "xin", "id": 200, "f": ["d", "e", "f"], "c": now, "b": None, "d": {"a": 1}}

    pydantic_objects = await serialize_table(table_name="some_table", data=DataFrame(data=[data1, data2]))

    assert isinstance(pydantic_objects, list)
    for entry in pydantic_objects:
        assert isinstance(entry, BaseModel)
        assert len(entry.model_fields.keys()) >= 5


@pytest.mark.asyncio
async def test_serialize_polars_table() -> None:
    pass
