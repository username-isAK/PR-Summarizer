from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from github import get_pull_request
from summarizer import summarize_pr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="."), name="static")

class PRRequest(BaseModel):
    owner: str
    repo: str
    pr_number: int

@app.get("/", response_class=HTMLResponse)
def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.post("/fetch-pr")
def fetch_pr(pr_request: PRRequest):
    try:
        pr_data = get_pull_request(pr_request.owner, pr_request.repo, pr_request.pr_number)
        return {"success": True, "pr": pr_data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/summarize-pr")
def summarize_pr_endpoint(pr_data: dict):
    try:
        summary = summarize_pr(pr_data)
        return {"success": True, "summary": summary}
    except Exception as e:
        return {"success": False, "error": str(e)}