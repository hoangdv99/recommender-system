from sqlalchemy import Column, Integer
from app.database import Base, get_db
from sqlalchemy.orm import Session

class RatingHistories(Base):
  __tablename__ = 'audio_user_ratings'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer)
  audio_id = Column(Integer)
  rating = Column(Integer)

async def get_rating_histories(db: Session = next(get_db())):
  return db.query(RatingHistories).all()
