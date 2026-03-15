from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import logging

from services.retrieval import get_context
from services.bedrock import call_nova_lite

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SAGE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class AutomateRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=500)


@app.get("/")
def root():
    return {"message": "SAGE Backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query")
async def query(request: QueryRequest):
    try:
        context = get_context(request.text)
        combined_prompt = f"""Use the context below to answer the user's question clearly and simply.

Context:
{context}

User question:
{request.text}
"""
        response = call_nova_lite(combined_prompt)
        return {"response": response}
    except Exception as e:
        logger.exception("Query endpoint failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/automate")
async def automate(request: AutomateRequest):
    return {"task_id": "task_001", "status": "queued", "task": request.task}