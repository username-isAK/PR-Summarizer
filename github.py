import os
import httpx
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@lru_cache(maxsize=128)
def get_pull_request(owner: str, repo: str, pr_number: int) -> dict:
    if not GITHUB_TOKEN:
        raise Exception("GITHUB_TOKEN not set in .env")

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    url_pr = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    resp = httpx.get(url_pr, headers=headers)
    if resp.status_code == 404:
        raise Exception(f"PR #{pr_number} not found in {owner}/{repo}")
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch PR: {resp.status_code}, {resp.text}")
    pr_data = resp.json()

    url_files = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    resp_files = httpx.get(url_files, headers=headers)
    if resp_files.status_code != 200:
        raise Exception(f"Failed to fetch PR files: {resp_files.status_code}")
    files_data = resp_files.json()

    diff_summary = [
        {
            "filename": f.get("filename"),
            "additions": f.get("additions"),
            "deletions": f.get("deletions"),
            "changes": f.get("changes")
        }
        for f in files_data
    ]

    return {
        "title": pr_data.get("title"),
        "body": pr_data.get("body"),
        "user": pr_data.get("user", {}).get("login"),
        "url": pr_data.get("html_url"),
        "state": pr_data.get("state"),
        "labels": [label["name"] for label in pr_data.get("labels", [])],
        "assignees": [user["login"] for user in pr_data.get("assignees", [])],
        "diff_summary": diff_summary
    }
