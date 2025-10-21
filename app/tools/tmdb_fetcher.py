import os
import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def fetch_movies_from_tmdb(query: str, limit: int = 5):
    """
    Fetch movies from TMDb matching the search query.
    """
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "include_adult": False,
        "language": "en-US",
        "page": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"TMDb request failed: {e}"}

    data = response.json()
    results = []

    for movie in data.get("results", [])[:limit]:
        results.append({
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average"),
            "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get("poster_path") else None
        })

    return results
