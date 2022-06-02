from pydantic import BaseModel

class Audios(BaseModel):
  id: int
  title: str
  slug: str

  class Config:
    orm_mode = True
