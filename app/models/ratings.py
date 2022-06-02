from sqlalchemy import Column, Integer, String, DECIMAL, Text, SmallInteger, DateTime
from database import Base

class RatingHistories(Base):
  __tablename__ = 'audio_user_ratings'

  id = Column(Integer, primary_key=True)
  audio_id = Column(Integer)
  user_id = Column(Integer)
  rating = Column(Integer)
