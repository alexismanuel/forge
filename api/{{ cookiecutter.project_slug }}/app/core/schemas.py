from pydantic import BaseModel
from app.lib.types import ID

class Request(BaseModel):
    id: ID
