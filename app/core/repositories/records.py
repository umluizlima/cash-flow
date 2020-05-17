from ..models import Record
from .base import BaseRepository


class RecordsRepository(BaseRepository):
    __model__ = Record
