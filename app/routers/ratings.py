from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from schemas import ratings
from models.ratings import RatingHistories
from database import get_db

router = APIRouter()

@router.get('/ratings', response_model=List[ratings.RatingHistories])
async def get_ratings(db: Session = Depends(get_db)):
   return db.query(RatingHistories).all()
