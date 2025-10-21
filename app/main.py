from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.tools.tmdb_fetcher import fetch_from_tmdb
from app.tools.omdb_fetcher import fetch_ratings_from_omdb

app = FastAPI(title="Movie Recommender API")

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
