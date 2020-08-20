import requests
import json

########################################################################################################################
#   Create a private.py file, which contains a string variable named "token", containing an OAuth Token:               #
#   playlist-modify-private for your Spotify account.                                                                  #
########################################################################################################################

from private import token
endpoint: str = "https://api.spotify.com/v1/recommendations"

# Filters for Spotify.
limit: int = 10
seed_genres: str = "pop"
market: str = "AU"

query: str = f"{endpoint}?limit={limit}&seed_genres={seed_genres}&market={market}"
response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

uris: [] = []
for (i, j) in enumerate(response.json()["tracks"]):
    uris.append(j["uri"])
    print(f"{i + 1}) \"{j['name']}\" by {j['artists'][0]['name']}")

print()

# Report available genres.
response_genres = requests.get("https://api.spotify.com/v1/recommendations/available-genre-seeds",
                               headers={"Content-Type": "application/json",
                                        "Authorization": f"Bearer {token}"})
print(response_genres.json())
