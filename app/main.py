from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.tools.query_roma import query_roma, parse_roma_response
from app.tools.recommend import RomaItem, RomaResponse, recommend
from typing import List, Dict, Any


app = FastAPI(title="Movie Recommender API")


roma_data = {
  "query": "some detective movies and shows to watch",
  "roma_response": [
    {
      "title": "Knives Out",
      "reason": "A modern whodunit mystery featuring an ensemble cast led by Daniel Craig as a quirky detective investigating a wealthy family's murder. The film combines classic detective elements with sharp social commentary and a clever plot structure that keeps viewers guessing. Critically acclaimed with a 94% Rotten Tomatoes score and 7.9 IMDb rating, it revitalizes the detective genre with contemporary storytelling while honoring traditional mystery conventions.",
      "type": "movie"
    },
    {
      "title": "The Girl with the Dragon Tattoo",
      "reason": "A psychological thriller and dark procedural following a journalist and a hacker as they investigate a decades-old disappearance case. Based on Stieg Larsson's novel, it features complex characters, gritty atmosphere, and themes of corruption and justice. With a 91% Rotten Tomatoes score and 7.8 IMDb rating, it represents the neo-noir subgenre with its bleak tone and morally ambiguous protagonists.",
      "type": "movie"
    },
    {
      "title": "Zodiac",
      "reason": "A procedural crime drama based on the real-life Zodiac killer investigation in San Francisco. The film meticulously follows the detectives' obsessive search for the killer, highlighting the psychological toll of unsolved cases. With an 89% Rotten Tomatoes score and 7.7 IMDb rating, it exemplifies the procedural subgenre with its detailed investigative process and exploration of obsession.",
      "type": "movie"
    },
    {
      "title": "True Detective",
      "reason": "An anthology series that combines psychological depth with procedural elements. Each season features different detectives investigating complex cases while exploring themes of darkness, corruption, and existential dread. The first season, starring Matthew McConaughey and Woody Harrelson, is particularly acclaimed with a 94% Rotten Tomatoes score and 8.3 IMDb rating, representing the psychological thriller subgenre with its atmospheric tension and character-driven narratives.",
      "type": "show"
    },
    {
      "title": "Mindhunter",
      "reason": "A psychological crime procedural about the origins of criminal profiling at the FBI. The series follows two agents as they interview imprisoned serial killers to understand their psychology, blending investigative procedural elements with deep psychological exploration. With an 82% Rotten Tomatoes score and 8.6 IMDb rating, it represents the psychological thriller subgenre with its focus on the minds of criminals and the psychological toll on investigators.",
      "type": "show"
    }
  ]
}


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



