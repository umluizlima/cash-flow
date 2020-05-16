from sqlalchemy import Column, DateTime, Numeric, Text

from .base import BaseModel


class Record(BaseModel):
    __tablename__ = "records"

    amount = Column(Numeric, nullable=False)
    description = Column(Text, nullable=True)
    happened_at = Column(DateTime, nullable=True)
    title = Column(Text, nullable=True)
