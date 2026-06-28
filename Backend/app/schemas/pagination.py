from pydantic import BaseModel
from typing import Generic,TypeVar,List

T=TypeVar("T")

class Meta(BaseModel):
    page:int
    total:int
    limit:int
    pages:int

class PaginatedResponse(BaseModel,Generic[T]):
    meta:Meta
    data:List[T]
