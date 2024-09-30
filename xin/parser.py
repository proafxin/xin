from datetime import datetime
from typing import Any, Type

import numpy as np
import pandas as pd
from pydantic import BaseModel, TypeAdapter, create_model


class Base(BaseModel):
    """All models must be a pydantic model."""


class QueryResult(Base):
    table_name: str


async def serialize_table_pandas(table_name: str, data: pd.DataFrame) -> list[BaseModel]:
    dtypes = data.dtypes
    fields: dict[str, Any] = {}

    columns = data.columns.tolist()
    dtypes = data.dtypes
    field_type: Type[int | str | float | datetime] | None

    for dtype, column in zip(dtypes, columns):
        if np.issubdtype(dtype, np.integer):
            field_type = int
        elif np.issubdtype(dtype, np.number):
            field_type = float
        elif np.issubdtype(dtype, np.datetime64):
            field_type = datetime
        else:
            field_type = str

        if data[column].dropna().shape[0] < data.shape[0]:
            fields[column] = (field_type | None, ...)
        else:
            fields[column] = (field_type, ...)

    Model = create_model(table_name.capitalize(), **fields, __base__=BaseModel)
    ta = TypeAdapter(list[Model])  # type: ignore[valid-type]

    return ta.validate_python(data.to_dict("records"))
