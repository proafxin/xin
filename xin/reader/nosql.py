from typing import Any

from polars import DataFrame
from pymongo import AsyncMongoClient


async def query_collection_with_result(
    query: dict[str, Any], client: AsyncMongoClient, dbname: str, collection_name: str
) -> DataFrame:
    dbs = await client.list_database_names()

    if dbname not in dbs:
        raise KeyError(f"{dbname} not in {dbs}")

    db = client[dbname]

    collections = await db.list_collection_names()

    if collection_name not in collections:
        raise KeyError(f"{collection_name} not in {collections}")

    collection = db[collection_name]

    documents = collection.find(query)

    return DataFrame(data=[document async for document in documents])
