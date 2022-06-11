from fastapi import APIRouter
from app.model import CF
import pandas as pd
from app.models.ratings import get_rating_histories
from app.models.audios import get_audios_by_ids
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/predict')
async def get_recommend_audios(user_id: int):
  rating_histories = await get_rating_histories()
  df = pd.DataFrame(item.__dict__ for item in rating_histories).drop(['_sa_instance_state', 'id'], axis=1)
  ratings = df.values
  rs = CF(ratings, k=2, uuCF=1)
  rs.fit()
  recommend_id_list = rs.recommend(user_id)
  recommend_audio_list = []
  recommend_audio_list = await get_audios_by_ids(recommend_id_list)
  json_compatible_data = jsonable_encoder(recommend_audio_list)

  return JSONResponse(content=json_compatible_data)
