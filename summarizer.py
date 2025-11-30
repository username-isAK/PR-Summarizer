import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def summarize_pr(pr_data: dict) -> dict:
    prompts = {
        "short": f"Summarize the PR in 3-4 concise bullet points:\nTitle: {pr_data['title']}\nDescription: {pr_data['body'] or 'No description'}\nFiles changed: {len(pr_data['diff_summary'])}",
        "detailed": f"Explain the PR in detail, including code changes:\nTitle: {pr_data['title']}\nDescription: {pr_data['body'] or 'No description'}",
        "release": f"Write release notes for end users:\nTitle: {pr_data['title']}\nDescription: {pr_data['body'] or 'No description'}"
    }

    summaries = {}
    for key, prompt in prompts.items():
        try:
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You summarize GitHub PRs clearly."},
                    {"role": "user", "content": prompt}
                ]
            )
            summaries[key] = resp.choices[0].message.content
        except Exception as e:
            summaries[key] = f"Error: {e}"
    return summaries
