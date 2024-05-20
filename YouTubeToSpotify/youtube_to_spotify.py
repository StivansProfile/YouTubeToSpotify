from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from colorama import init as colorama_init
from colorama import Fore, Style
from tqdm import tqdm

load_dotenv()
colorama_init(autoreset=True)

# example youtube playlist id - PLeJ5DwBZKZUkIRRBH-r4DwXwAOpy_6Xlg
# executable

# Input for playlist details
playlist_ID = input("Enter the playlist ID: ")
playlist_Name = input("Enter a name for your playlist: ")
playlist_desc = input("Give your playlist a description: ")

# Authenticate with Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public",
    )
)


class TransferToSpotify:
    def __init__(self) -> None:
        self.youtube_titles = []

    # Gets titles from YouTube
    def get_playlist_video_titles(self, playlist_id):
        titles = []
        next_page_token = None
        youtube = build("youtube", "v3", developerKey=os.getenv("API_KEY"))

        print("Fetching YouTube playlist titles...")

        while True:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token,
            )
            response = request.execute()

            for item in response["items"]:
                titles.append(item["snippet"]["title"])

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        self.youtube_titles = titles
        return titles

    # Finds the corresponding tracks to the YouTube titles
    def search_spotify_tracks(self, titles):
        track_uris = []
        not_found = []

        print("Searching for tracks on Spotify...")

        for title in tqdm(titles, desc="Searching Spotify"):
            result = sp.search(q=title, type="track", limit=1)
            if result["tracks"]["items"]:
                track_uris.append(result["tracks"]["items"][0]["uri"])
            else:
                not_found.append(title)

        if not_found:
            print("The following titles were not found on Spotify:")
            for title in not_found:
                print(title)

        return track_uris

    # Creates the Spotify playlist
    def create_spotify_playlist(self):
        # Fetch Spotify URIs for the video titles
        spotify_uris = self.search_spotify_tracks(self.youtube_titles)

        if not spotify_uris:
            print("No valid tracks were found to add to the playlist.")
            return

        # Create a new playlist on Spotify
        playlist_name = playlist_Name
        playlist_description = playlist_desc
        user_id = sp.me()["id"]

        print("Creating Spotify playlist...")

        playlist = sp.user_playlist_create(
            user=user_id, name=playlist_name, description=playlist_description
        )

        # Add tracks to the playlist
        print("Adding tracks to the playlist...")
        sp.playlist_add_items(playlist_id=playlist["id"], items=spotify_uris)

        print(
            f"{Fore.GREEN}Playlist '{playlist_name}' created and songs added successfully.{Style.RESET_ALL}"
        )


# Get the video titles from the playlist and create a Spotify playlist
youtube_to_spotify = TransferToSpotify()
video_titles = youtube_to_spotify.get_playlist_video_titles(playlist_ID)
youtube_to_spotify.create_spotify_playlist()
