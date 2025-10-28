from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.tools.query_roma import query_roma, parse_roma_response
from app.tools.recommend import RomaItem, RomaResponse, recommend
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Movie Recommender API")

origins = [
    "http://localhost:5173",  
    "http://localhost:3000",  
    "http://romamdb.vercel.app",
    "https://romamdb.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextQuery(BaseModel):
    query: str

@app.post("/analyze")
def analyze(req: TextQuery):
    """
    Sends a user text query to ROMA service and returns structured recommendations with reasoning.
    """
    roma_response = query_roma(req.query)
    final_output = None

    # Safely extract "final_output" regardless of nesting
    if isinstance(roma_response, dict):
        final_output = roma_response.get("final_output", {}) or roma_response.get("result", {})

    if not final_output:
        print("ROMA did not return 'final_output'")
        return {"query": req.query, "roma_response": []}

    # parse roma response to extract JSON
    parsed_items = parse_roma_response(final_output)
    roma_dicts = [item for item in parsed_items if isinstance(item, dict)]
    if not roma_dicts:
        return {"query": req.query, "roma_response": [], "error": "No valid ROMA items found"}
    
    # convert to pydantic models
    roma_items = [RomaItem(**item) for item in roma_dicts]

    # build RomaResponse model
    roma_payload = RomaResponse(query=req.query, roma_response=roma_items)

    # call recommend function to enrich data
    enriched_data = recommend(roma_payload)

    return enriched_data



