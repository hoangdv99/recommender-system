from pandas import DatetimeIndex
from sqlalchemy import Column, Integer, String, DECIMAL, Text, SmallInteger, DateTime
from database import Base

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
