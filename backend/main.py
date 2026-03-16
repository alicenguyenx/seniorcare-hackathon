from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from automation.core.models import AutomationRequest
from automation.nova_act import run_automation_task
from services.bedrock import call_nova_lite
from services.retrieval import get_context

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SAGE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


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
async def automate(request: AutomationRequest):
    try:
        return run_automation_task(
            task_name=request.task_name,
            profile_overrides=request.profile_overrides,
            headless=request.headless,
            keep_browser_open=request.keep_browser_open,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
