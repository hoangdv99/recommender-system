from fastapi import FastAPI
from routers import audios

app = FastAPI()

app.include_router(audios.router)

@app.get("/helloworld")
def helloworld():
    return {"Hello": "World"}
