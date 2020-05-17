from datetime import datetime

from pydantic import BaseModel, constr, condecimal


class RecordBase(BaseModel):
    amount: condecimal(decimal_places=2)
    description: constr(max_length=140)
    happened_at: datetime
    title: constr(min_length=3, max_length=50)


class RecordCreate(RecordBase):
    description: constr(max_length=140) = None
    happened_at: datetime = None
    title: constr(min_length=3, max_length=50) = None


class RecordUpdate(RecordBase):
    amount: condecimal(decimal_places=2) = None
    description: constr(max_length=140) = None
    happened_at: datetime = None
    title: constr(min_length=3, max_length=50) = None


class RecordRead(RecordBase):
    id: int
