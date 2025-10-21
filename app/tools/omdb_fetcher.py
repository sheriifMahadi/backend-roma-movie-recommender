# backend/app/tools/omdb_fetcher.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

def fetch_ratings_from_omdb(title: str) -> dict:
    """
    Fetch ratings and other metadata for a movie title from OMDb.
    """
    url = "https://www.omdbapi.com/"
    params = {"t": title, "apikey": OMDB_API_KEY}

    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        return {"error": f"OMDb request failed: {e}"}

    if data.get("Response") == "False":
        return {"error": data.get("Error", "No data found")}

    ratings = {r["Source"]: r["Value"] for r in data.get("Ratings", [])}

    return {
        "title": data.get("Title"),
        "year": data.get("Year"),
        "imdb_id": data.get("imdbID"),
        "imdb_rating": data.get("imdbRating"),
        "metascore": data.get("Metascore"),
        "rotten_tomatoes": ratings.get("Rotten Tomatoes"),
        "ratings": ratings,
    }
