from pydantic import BaseModel

class RatingHistories(BaseModel):
  id: int
  audio_id: int
  user_id: int

  class Config:
    orm_mode = True
