from uuid import UUID

from pydantic import BaseModel


class IDOutputSchema(BaseModel):
    id: UUID
