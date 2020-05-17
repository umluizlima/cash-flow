from datetime import datetime

from pydantic import BaseModel, constr, condecimal


class RecordBase(BaseModel):
    amount: condecimal(decimal_places=2)
    description: constr(max_length=140) = None
    happened_at: datetime = None
    title: constr(min_length=3, max_length=50) = None


class RecordCreate(RecordBase):
    ...


class RecordUpdate(RecordBase):
    amount: condecimal(decimal_places=2) = None


class RecordRead(RecordBase):
    id: int

    class Config:
        orm_mode = True
