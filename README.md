# Virtual-AI-Assistant

Incremental build of a personal AI assistant (Python).  
Current increment: **JIRA Cloud Daily Report via JQL filter**.

## Setup

### 1) Create virtualenv & install deps
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
```

### 2) Configure environment
Copy `.env.example` to `.env` and fill:
- `JIRA_BASE_URL` (e.g. `https://your-domain.atlassian.net`)
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`
- `JIRA_JQL`

### 3) Run daily JIRA report
```bash
python main.py jira-report
```

## Next increments
- Add ticket health heuristics (stale/blocked/overdue)
- Add MS Teams scheduling (Microsoft Graph)
- Add memory + agent orchestration (LangGraph/CrewAI)