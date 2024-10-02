import pytest
from polars import DataFrame
from pymongo import AsyncMongoClient

from xin.reader.nosql import query_collection_with_result


@pytest.mark.asyncio
async def test_query_with_result(mongo_client: AsyncMongoClient) -> None:
    df = await query_collection_with_result(query={}, client=mongo_client, dbname="test", collection_name="test")
    assert isinstance(df, DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 1

    with pytest.raises(KeyError):
        await query_collection_with_result(query={}, client=mongo_client, dbname="randomdb", collection_name="random")

    with pytest.raises(KeyError):
        await query_collection_with_result(query={}, client=mongo_client, dbname="test", collection_name="random")
