from datetime import datetime
from typing import Any, Sequence, Type

import numpy as np
import pandas as pd
import polars as pl
from pydantic import BaseModel, TypeAdapter, create_model


async def deserialize_pydantic_objects(models: Sequence[BaseModel]) -> pl.DataFrame:
    data = [model.model_dump() for model in models]

    return pl.DataFrame(data=data)


async def flatten(data: pd.DataFrame | pl.DataFrame, depth: int) -> pl.DataFrame:
    if isinstance(data, pd.DataFrame):
        data = pl.from_pandas(data=data)

    return pl.json_normalize(data=data.to_dicts(), max_level=depth)


async def _serialize_table_pandas(table_name: str, data: pd.DataFrame) -> list[BaseModel]:
    dtypes = data.dtypes
    fields: dict[str, Any] = {}

    columns = data.columns.tolist()
    dtypes = data.dtypes
    field_type: Type[int | str | float | datetime | dict[Any, Any] | list[Any]] | None

    for dtype, column in zip(dtypes, columns):
        if np.issubdtype(dtype, np.integer):
            field_type = int
        elif np.issubdtype(dtype, np.number):
            field_type = float
        elif np.issubdtype(dtype, np.datetime64):
            field_type = datetime
        else:
            value = data[column].iloc[0]
            if isinstance(value, dict):
                field_type = dict[Any, Any]
            elif isinstance(value, list):
                field_type = list[Any]
            else:
                field_type = str

        if data[column].dropna().shape[0] < data.shape[0]:
            fields[column] = (field_type | None, ...)
        else:
            fields[column] = (field_type, ...)

    Model = create_model(table_name.capitalize(), **fields, __base__=BaseModel)
    ta = TypeAdapter(list[Model])  # type: ignore[valid-type]

    return ta.validate_python(data.to_dict("records"))


async def _serialize_table_polars(table_name: str, data: pl.DataFrame) -> list[BaseModel]:
    return []


async def serialize_table(table_name: str, data: pd.DataFrame | pl.DataFrame) -> list[BaseModel]:
    if isinstance(data, pd.DataFrame):
        return await _serialize_table_pandas(table_name=table_name, data=data)

    return await _serialize_table_polars(table_name=table_name, data=data)
