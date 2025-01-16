from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#client_ids = "your_client_id"
#client_secrets = "your_secret"
date = input("In what year would you like to travel? please enter the date in this format (YYYY-MM-DD): ")
# response = requests.get("https://www.billboard.com/charts/hot-100/"+date)
# webpage = response.text

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
billboard_url = "https://www.billboard.com/charts/hot-100/" + date

response = requests.get(url=billboard_url, headers=header)
soup = BeautifulSoup(response.text,'html.parser')
song_names_spans = soup.select("li ul li h3")
song_name = [song.getText().strip() for song in song_names_spans]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                              redirect_uri="http://example.com",
                              client_id="your_client_id",
                              client_secret="your_secret",
                              show_dialog=True,
                              cache_path="token.txt"))


user_id = sp.current_user()["id"]
print(user_id)
song_uri = []
year = date.split("-")[0]
for song in song_name:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} does not exist in spotify. Skipped")
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)

