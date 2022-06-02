from email.mime import audio
from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from schemas import audios
from models.audios import Audios
from database import SessionLocal

router = APIRouter()

def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
      db.close()

@router.get('/audios', response_model=List[audios.Audios])
async def get_audios(db: Session = Depends(get_db)):
   return db.query(Audios).all()