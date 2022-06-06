from fastapi import APIRouter
from model import CF
import pandas as pd
from models.ratings import get_rating_histories
from models.audios import get_audio_by_id
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/predict')
async def get_recommend_audios(user_id: int):
  rating_histories = await get_rating_histories()
  df = pd.DataFrame(item.__dict__ for item in rating_histories).drop(['_sa_instance_state', 'id'], 1)
  ratings = df.values
  rs = CF(ratings, k=5, uuCF=1)
  rs.fit()
  recommend_id_list = rs.recommend(user_id)
  recommend_audio_list = []
  for id in recommend_id_list:
    audio = await get_audio_by_id(id)
    recommend_audio_list.append(audio)
  json_compatible_data = jsonable_encoder(recommend_audio_list)

  return JSONResponse(content=json_compatible_data)
