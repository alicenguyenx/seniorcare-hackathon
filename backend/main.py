from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SAGE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SAGE Backend is running"}

@app.post("/query")
async def query(text: str):
    return {"response": "mock response", "text": text}

@app.post("/automate")
async def automate(task: str):
    return {"task_id": "task_001", "status": "queued", "task": task}
