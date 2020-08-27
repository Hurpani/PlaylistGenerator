import requests
import json

########################################################################################################################
#   Create a private.py file, which contains a string variable named "token", containing an OAuth Token:               #
#   playlist-modify-private for your Spotify account. You will also need to include a user_id for Spotify.             #
########################################################################################################################

from private import token, user_id
endpoint: str = "https://api.spotify.com/v1/recommendations"


# Report available genres.
response_genres = requests.get("https://api.spotify.com/v1/recommendations/available-genre-seeds",
                               headers={"Content-Type": "application/json",
                                        "Authorization": f"Bearer {token}"})
print(response_genres.json())






# Filters for Spotify.
limit: int = 30
seed_genres: str = "ambient"#"electronic,edm"
market: str = "AU"

query: str = f"{endpoint}?limit={limit}&seed_genres={seed_genres}&market={market}"
response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

uris: [] = []
for (i, j) in enumerate(response.json()["tracks"]):
    uris.append(j["uri"])
    print(f"{i + 1}) \"{j['name']}\" by {j['artists'][0]['name']}")

print()

playlist_name: str = "Auto-generated Playlist"
playlist_desc: str = "A generic playlist"
# Creating a playlist:
request_body = json.dumps(
    {
        "name": playlist_name,
        "description": playlist_desc,
        "public": False
    }
)

playlist_endpoint: str = f"https://api.spotify.com/v1/users/{user_id}/playlists"
response_playlist_gen = requests.post(url=playlist_endpoint, data=request_body,
                                      headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})
print(response_playlist_gen.status_code)
playlist_id: str = response_playlist_gen.json()["id"]

songs_to_playlist_endpoint: str = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
request_body = json.dumps({
          "uris" : uris
        })
response = requests.post(url=songs_to_playlist_endpoint, data=request_body,
                         headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
print(response.status_code)
