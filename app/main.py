from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.tools.tmdb_fetcher import fetch_from_tmdb
from app.tools.omdb_fetcher import fetch_ratings_from_omdb
from app.tools.query_roma import query_roma, parse_roma_response

app = FastAPI(title="Movie Recommender API")



class TextQuery(BaseModel):
    query: str

@app.post("/analyze")
def analyze(req: TextQuery):
    """
    Sends a user text query to ROMA service and returns structured recommendations with reasoning.
    """
    roma_response = query_roma(req.query)
    # roma_result = response.json() 
    final_output = None

    # Safely extract "final_output" regardless of nesting
    if isinstance(roma_response, dict):
        final_output = roma_response.get("final_output", {}) or roma_response.get("result", {})

    if not final_output:
        print("ROMA did not return 'final_output'")
    else:
        print("Extracted final_output:")
    return {
        "query": req.query,
        "roma_response": parse_roma_response(final_output)
    }


class QueryRequest(BaseModel):
    query: str
    mode: str = "movie"  # "movie" or "tv"

@app.post("/recommend")
def recommend(req: QueryRequest):
    """
    Takes a text query, fetches movie or TV show data from TMDb,
    enriches each result with ratings from OMDb.
    """
    # Fetch TMDb results based on mode
    tmdb_results = fetch_from_tmdb(req.query, mode=req.mode)
    enriched = []

    for item in tmdb_results:
        # Movie titles are 'title', TV shows are also standardized in fetch_from_tmdb
        title = item.get("title") or item.get("original_name")
        if not title:
            continue
        ratings = fetch_ratings_from_omdb(title)
        item["ratings"] = ratings
        enriched.append(item)

    return {
        "query": req.query,
        "mode": req.mode,
        "results": enriched
    }
