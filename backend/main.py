from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from services.bedrock import call_nova_lite

load_dotenv()

app = FastAPI(title="SAGE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    text: str


class AutomateRequest(BaseModel):
    task: str


@app.get("/")
def root():
    return {"message": "SAGE Backend is running"}


@app.post("/query")
async def query(request: QueryRequest):
    try:
        response = call_nova_lite(request.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/automate")
async def automate(request: AutomateRequest):
    return {"task_id": "task_001", "status": "queued", "task": request.task}
