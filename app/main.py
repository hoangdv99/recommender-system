from fastapi import FastAPI
from routers import predict

app = FastAPI()

app.include_router(predict.router)

@app.get("/helloworld")
def helloworld():
    return {"Hello": "World"}
