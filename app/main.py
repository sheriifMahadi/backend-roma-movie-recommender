from fastapi import FastAPI
from pydantic import BaseModel
from app.tools.tmdb_fetcher import fetch_movies_from_tmdb
from app.tools.omdb_fetcher import fetch_ratings_from_omdb

app = FastAPI(title="Movie Recommender API")

class QueryRequest(BaseModel):
    query: str

@app.post("/recommend")
def recommend(req: QueryRequest):
    """
    Takes a text query, fetches movie data from TMDb, and returns basic info. 
    Then fetches ratings from OMDb for each movie.
    """
    tmdb_movies = fetch_movies_from_tmdb(req.query)
    enriched = []

    for m in tmdb_movies:
        title = m.get("title")
        if not title:
            continue
        ratings = fetch_ratings_from_omdb(title)
        m["ratings"] = ratings
        enriched.append(m)

    return {"query": req.query, "movies": enriched}