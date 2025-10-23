import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # Your v3 API key
BASE_URL = "https://api.themoviedb.org/3"

def search_movies(query: str, include_adult: bool = False, language: str = "en-US", page: int = 1):
    """
    Search for movies on TMDb using API key.
    """
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "include_adult": str(include_adult).lower(),
        "language": language,
        "page": page
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"[TMDb] Movie search failed: {e}")
        return []

def search_shows(query: str, include_adult: bool = False, language: str = "en-US", page: int = 1):
    """
    Search for TV shows on TMDb using API key.
    """
    url = f"{BASE_URL}/search/tv"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "include_adult": str(include_adult).lower(),
        "language": language,
        "page": page
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.RequestException as e:
        print(f"[TMDb] TV show search failed: {e}")
        return []

def fetch_from_tmdb(query: str, mode: str = "movie"):
    """
    Route requests to movie or show search depending on mode.
    """
    if mode == "movie":
        return search_movies(query)
    elif mode == "tv":
        return search_shows(query)
    else:
        raise ValueError("Mode must be 'movie' or 'tv'")
