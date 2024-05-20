import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from spotipy.oauth2 import SpotifyOAuth
import spotipy

# Spotify API credentials
SPOTIPY_CLIENT_ID = "YOUR_SPOTIPY_CLIENT_ID"
SPOTIPY_CLIENT_SECRET = "YOUR_SPOTIPY_CLIENT_SECRET"
SPOTIPY_REDIRECT_URI = "YOUR_SPOTIPY_REDIRECT_URI"


class YouTubeToSpotifyApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=10)

        self.youtube_playlist_id_input = TextInput(
            hint_text="Enter YouTube Playlist ID", multiline=False, size_hint=(1, 0.1)
        )
        layout.add_widget(self.youtube_playlist_id_input)

        authenticate_button = Button(
            text="Authenticate with Spotify", size_hint=(1, 0.1)
        )
        authenticate_button.bind(on_press=self.authenticate_spotify)
        layout.add_widget(authenticate_button)

        self.message_label = Label(text="", size_hint=(1, 0.1))
        layout.add_widget(self.message_label)

        return layout

    def authenticate_spotify(self, instance):
        # Authenticate with Spotify
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET,
                redirect_uri=SPOTIPY_REDIRECT_URI,
                scope="playlist-modify-public",
            )
        )
        self.message_label.text = "Spotify authenticated successfully!"


if __name__ == "__main__":
    YouTubeToSpotifyApp().run()
