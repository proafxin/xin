from datetime import datetime
from enum import Enum, auto
from typing import Any, Type

import numpy as np
import pandas as pd
import polars as pl
from pydantic import BaseModel, TypeAdapter, create_model


class Base(BaseModel):
    """All models must be a pydantic model."""


class QueryResult(Base):
    table_name: str


class DataFrameBackend(Enum):
    PANDAS = auto()
    POLARS = auto()


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


async def serialize_table(
    table_name: str, data: pd.DataFrame | pl.DataFrame, backend: DataFrameBackend = DataFrameBackend.PANDAS
) -> list[BaseModel]:
    if isinstance(data, pd.DataFrame):
        return await _serialize_table_pandas(table_name=table_name, data=data)

    return await _serialize_table_polars(table_name=table_name, data=data)
