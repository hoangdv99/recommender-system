from sqlalchemy import Column, Integer, String, DECIMAL, Text, SmallInteger, DateTime
from app.database import Base, get_db
from sqlalchemy.orm import Session

class Audios(Base):
  __tablename__ = 'audios'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  description = Column(Text)
  url = Column(Text)
  author = Column(String)
  thumbnail_url = Column(String)
  posted_by = Column(Integer)
  voice_id = Column(Integer)
  rating = Column(DECIMAL, default=0.00)
  views = Column(Integer, default=0)
  status = Column(SmallInteger, default=1)
  slug = Column(String)
  rating_count = Column(Integer, default=0)
  type = Column(SmallInteger, default=1)
  created_at = Column(DateTime)
  updated_at = Column(DateTime)

async def get_audio_by_id(id: int, db: Session = next(get_db())):
  return db.query(Audios).get(id)
