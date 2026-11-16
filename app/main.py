from fastapi import FastAPI
from app.routes import study

app = FastAPI() 

@app.get("/") 
async def get_root(): 
    return {"message": "Welcome to AI Study Assistant!"}

app.include_router(study.router, prefix = "/api/v1")
