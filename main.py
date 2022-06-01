from fastapi import FastAPI

app = FastAPI()

@app.get("/helloworld")
def helloworld():
    return {"Hello": "World"}
