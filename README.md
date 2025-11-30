# GitHub PR Summarizer

An **AI Agent** to fetch and summarize GitHub Pull Requests (PRs) using the **GROQ API**. It displays PR metadata, file changes, and generates quick summaries in multiple formats.

---

## Features

- Fetch PR metadata: title, author, state, labels, assignees, URL.  
- Show **file changes** with additions, deletions, and total changes.  
- Generate **summaries**:
  - Short summary  
  - Detailed explanation  
  - Release notes  
- Copy summaries to clipboard.  
- Responsive UI built with **Tailwind CSS**.  
- Backend uses **FastAPI** and **GROQ API** to fetch PR data and generate summaries.  

---

## Technologies Used

- **Frontend**: HTML, JavaScript, Tailwind CSS  
- **Backend**: FastAPI, Python  
- **API**: GROQ API (Sanity or other CMS)  
- **Optional**: OpenAI API for automatic PR summarization
