from fastapi import FastAPI
from app.routers import predict
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://staging-bkradio-fe-6xoiukrslq-an.a.run.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)

@app.get("/helloworld")
def helloworld():
    return {"Hello": "World"}
