from datetime import datetime

import pytest
from pandas import DataFrame
from pydantic import BaseModel

from xin.parser import Base, serialize_table_pandas


@pytest.mark.asyncio
async def test_base() -> None:
    assert isinstance(Base(), BaseModel)


@pytest.mark.asyncio
async def test_serialize_pandas_table() -> None:
    data1 = {"name": "xin", "id": 200100, "email": "anemail@email.com", "created_at": datetime.now(), "balance": 200.0}
    data2 = {"name": "xin", "id": 200100, "email": "someemail@email.com", "created_at": datetime.now(), "balance": None}

    pydantic_objects = await serialize_table_pandas(table_name="some_table", data=DataFrame(data=[data1, data2]))

    assert isinstance(pydantic_objects, list)
