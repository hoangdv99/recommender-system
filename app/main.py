from email.mime import audio
from fastapi import FastAPI
from routers import audios, ratings

app = FastAPI()

app.include_router(audios.router)
app.include_router(ratings.router)

@app.get("/helloworld")
def helloworld():
    return {"Hello": "World"}
