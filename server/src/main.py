import uvicorn
from fastapi import FastAPI

from api.document import router as DocumentRouter
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(DocumentRouter, prefix="/document")

@app.get("/")
async def test():
    return {"message": "hello world"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
