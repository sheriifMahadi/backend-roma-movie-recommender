import requests

ROMA_API_URL = "http://localhost:5000/api/simple/execute"

def query_roma(user_req: str):
    """Send user request to ROMA and collect response to query movie db"""

    payload = {
    "goal": (
        
            f"""user_query: {user_req},
            You are an expert movie and TV show recommender system.
            Given a user query, recommend a list of movies or TV shows that best fit the user's needs.
            Use your knowledge of movies and TV shows to provide accurate recommendations. 
            Give detailed reason why you are recommending this movie or show.
            Give your recommendations as a valid JSON array, with each object containing:
            - title
            - reason
            - type (either 'movie' or 'show')
            Do not include explanations outside the JSON.
            Example:
            [
            {{"title": "Inception", "reason": "Mind-bending sci-fi thriller", "type": "movie"}},
            {{"title": "Dark", "reason": "Philosophical and mysterious", "type": "show"}}
            ]
            """
        )
    }
    response = requests.post(ROMA_API_URL, json=payload)
    return response.json()



import json
import re

def parse_roma_response(roma_response: str):
    """
    Extract valid JSON from ROMA's markdown-style response.
    Example input:
    ```json
    [ { ... }, { ... } ]
    ```
    """
    # Extract JSON block between ```json ... ```
    match = re.search(r"```json\s*(.*?)\s*```", roma_response, re.DOTALL)
    if not match:
        print("No JSON block found. Returning raw text.")
        return roma_response

    json_text = match.group(1).strip()

    try:
        data = json.loads(json_text)
        return data
    except json.JSONDecodeError:
        print("Failed to decode ROMA JSON. Returning raw text.")
        return json_text





# cache roma data for a period of time
#cache spotify data also for a period of time. or only allow a login to fetch new data every x hours.
# could store in a db or in memory with a timestamp.






