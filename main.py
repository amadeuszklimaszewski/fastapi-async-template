from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.on_event("startup")
async def on_startup():
    print("startup fastapi")
