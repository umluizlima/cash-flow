from datetime import datetime, MINYEAR
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import RecordCreate, RecordRead, RecordUpdate
from app.core.database import get_db
from app.core.repositories import RecordsRepository

router = APIRouter()


@router.post("/records", response_model=RecordRead, status_code=201)
def create(record: RecordCreate, db: Session = Depends(get_db)):
    return RecordsRepository(db).create(record.dict())


@router.get("/records", response_model=List[RecordRead])
def list(db: Session = Depends(get_db)):
    return sorted(
        RecordsRepository(db).find_all(),
        key=lambda record: record.happened_at or datetime(MINYEAR, 1, 1),
        reverse=True,
    )


@router.get("/records/{record_id}", response_model=RecordRead)
def read(record_id: int, db: Session = Depends(get_db)):
    try:
        return RecordsRepository(db).find_by_id(record_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Record not found")


@router.put("/records/{record_id}", response_model=RecordRead)
def update(record_id: int, record: RecordUpdate, db: Session = Depends(get_db)):
    try:
        return RecordsRepository(db).update_by_id(
            record_id, record.dict(exclude_unset=True)
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Record not found")


@router.delete("/records/{record_id}", status_code=204)
def delete(record_id: int, db: Session = Depends(get_db)):
    try:
        return RecordsRepository(db).delete_by_id(record_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Record not found")
