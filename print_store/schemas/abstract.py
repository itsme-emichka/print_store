from pydantic import BaseModel


class AbstractId(BaseModel):
    id: int
