# ROMAMDB backend

This is the **FastAPI backend** powering the ROMA Movie Recommendation App.  
It receives text queries, processes them through the ROMA AI recommendation engine, and returns structured movie data.

## 🚀 Features
- **AI Recommendation Engine (ROMA)** — Generates intelligent movie & show recommendations.
- **REST API** — Simple `/analyze` POST endpoint.
- **CORS Ready** — Configured for cross-origin requests from frontend.
- **Error Handling** — Returns standardized error messages.
- **JSON Response** — Clean structured movie metadata and reasoning.



---

## ⚙️ Setup Instructions

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
### 2. Install dependecies
```
pip install -r requirements.txt
```

### 3. Run the development server
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---
### API ENDPOINTS
#### POST /analyze
{ "query": "Cyberpunk Anime" }

NOTE - You need to have a ROMA server running. Go to app/tools/query_roma.py
 change ROMA_API_URL to "http://yourhost:5000/api/simple/execute" . Also check the main.py file and add your frontend address
