from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import creds


URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = creds.CLIENT_ID
CLIENT_SECRET = creds.CLIENT_SECRET
REDIRECT_URI = "http://example.com"

TITLES_CLASS = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
FIRST_CLASS = "c-title a-font-primary-bold-l a-font-primary-bold-m@mobile-max lrv-u-color-black u-color-white@mobile-max lrv-u-margin-r-150"

SINGER_CLASS = "c-label  a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only"

def fetchTop100(date):
    try:
        response = (requests.get(f"{URL}{date}/")).text
    except Exception:
        print(f"List not yet Released")
        
    soup = BeautifulSoup(response, "html.parser")

    top_titles = []
    artists = []

    result = soup.find_all('div', class_='o-chart-results-list-row-container')
    
    for res in result:
        songName = res.find('h3').text.strip()
        top_titles.append(songName)
        
        artist = res.find('h3').find_next('span').text.strip()
        artists.append(artist)
        
        # print("Song: " + songName)
        # print("Artist: " + str(artist))
        # print("___________________________________________________")
    
    return top_titles, artists

def playlistMaker(date, top_titles):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="http://example.com",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            show_dialog=True,
            cache_path="token.txt",
        )
    )
    user_id = sp.current_user()["id"]

    song_uris = []
    year = date.split("-")[0]
    for title in top_titles:
        result = sp.search(q=f"track:{title} year:{year}", type="track", market=None)
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{title} doesn't exist in Spotify. Skipped.")
        
    if(song_uris == []):
        print(f"List not yet Released")
        return

    playlist = sp.user_playlist_create(
        user=user_id, name=f"{date} Billboard 100", public=False
    )

    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
    print("Succesfully Created")
    
    return playlist["id"]
    
