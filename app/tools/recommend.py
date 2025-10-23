from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi import FastAPI, Query
from app.tools.tmdb_fetcher import search_movies, search_shows
from app.tools.omdb_fetcher import fetch_ratings_from_omdb


class RomaItem(BaseModel):
    title: str
    reason: str
    type: str  # "movie" or "show"

class RomaResponse(BaseModel):
    query: str
    roma_response: List[RomaItem]


def recommend(roma_data: RomaResponse):
    """
    Takes a text query, fetches movie or TV show data from TMDb,
    enriches each result with ratings from OMDb.
    """
    enriched_results = []

    for item in roma_data.roma_response:
        title = item.title.strip()
        reason = item.reason
        mode = item.type.lower()
        # Fetch details from TMDb
        tmdb_result = []
        if mode == "movie":
            tmdb_result = search_movies(title)
        elif mode == "show":
            tmdb_result = search_shows(title)

        if not tmdb_result:
            print(f"[WARN] No TMDb results for: {title}")
            continue

        movie_data = tmdb_result[0]  # Take the top TMDb match
        ratings = fetch_ratings_from_omdb(title)

        enriched_results.append({
            "title": title,
            "type": mode,
            "reason": reason,
            "overview": movie_data.get("overview"),
            "poster": f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}" if movie_data.get("poster_path") else None,
            "release_date": movie_data.get("release_date") or movie_data.get("first_air_date"),
            "tmdb_id": movie_data.get("id"),
            "tmdb_vote": movie_data.get("vote_average"),
            "omdb_ratings": ratings
        })

    return {
        "query": roma_data.query,
        "results": enriched_results
    }
