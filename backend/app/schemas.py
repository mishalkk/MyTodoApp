from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints, Field


class CategoryCreate(BaseModel):
    name: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1)
    ]
    description: str | None = None


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str|None
    created_at: datetime


# Epic Schema
class EpicCreate(BaseModel):
    category_id: Annotated[int, Field(gt=0)]
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    description: str | None = None


class EpicRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    name: str
    description: str|None
    created_at: datetime


class TaskCreate(BaseModel):
    catefory_id: Annotated[int, Field(gt=0)]
    epic_id: Annotated[int, Field(gt=0)] | None = None
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    description: str | None = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int