import requests

ROMA_API_URL = "http://localhost:5000/api/simple/execute"


def query_roma(user_data: dict):
    """Send user request to ROMA and collect response to query movie db"""

    payload = {
    "goal": (
            "Analyze the user's Spotify top artists and tracks (short, medium, long term).\n"
            "Recommend at least 10 new songs or artists for a new playlist (numbered list, each with a brief reason).\n"
            "Provide some commentary on their music taste and trends you observe.\n"
            f"User Data:\n{user_data}"
        )
    }
    print(len(payload["goal"]))
    response = requests.post(ROMA_API_URL, json=payload)
    return response.json()



# cache roma data for a period of time
#cache spotify data also for a period of time. or only allow a login to fetch new data every x hours.
# could store in a db or in memory with a timestamp.