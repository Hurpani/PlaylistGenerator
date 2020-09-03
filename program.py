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


# PERSONALISATION
# TOP ARTISTS
artists: str = ""
limit: int = 5
personal_artist_url = f'https://api.spotify.com/v1/me/top/artists?limit={limit}'
personal_track_url = f'https://api.spotify.com/v1/me/top/tracks?limit={limit}'

personalisation_response = requests.get(personal_artist_url,
                                        headers={"Content-Type": "application/json",
                                                 "Authorization": f"Bearer {token}"})
# Unpack the response and print out each artist's name.
count: int = 0
print()
for item in personalisation_response.json().get("items"):
    print(item.get("name"))
    artists += (str(item.get("id")))
    if count != limit - 1:
        artists += ','
        count += 1
print()
print(artists)
print()
# TOP SONGS
songs = ''
personalisation_artists_response = requests.get(personal_track_url,
                        headers={"Content-Type": "application/json",
                                 "Authorization": f"Bearer {token}"})
print(personalisation_artists_response)
count = 0
for i in personalisation_artists_response.json().get("items"):
    print(i.get("name"))
    songs += (str(i.get("id")))
    if count != limit - 1:
        songs += ','
        count += 1
print()
print(songs)
print()



# Filters for Spotify.
limit: int = 30
seed_genres: str = "pop"  # "ambient"#"electronic,edm"
seed_artists: str = "16yUpGkBRgc2eDMd3bB3Uw"
valence: float = 0.9;
target_popularity: int = 10000000
# target_speechiness: int = 0;
# seed_songs: str = ""
market: str = "AU"

query: str = f"{endpoint}?limit={limit}&seed_genres={seed_genres}&market={market}&seed_artists={seed_artists}&valence={valence}&target_popularity={target_popularity}"
response = requests.get(query, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})

uris: [] = []
for (i, j) in enumerate(response.json().get("tracks")):
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
    "uris": uris
})
response = requests.post(url=songs_to_playlist_endpoint, data=request_body,
                         headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
print(response.status_code)
