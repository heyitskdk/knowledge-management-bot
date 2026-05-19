import uvicorn

from fastapi import FastAPI
from api.knowledge import router as KnowledgeRouter

app = FastAPI()
app.include_router(KnowledgeRouter, prefix="/knowledge")

@app.get("/")
async def test():
    return {"message": "hello world"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
