class SpotifyWidget:
    def __init__(self):
        self.name = "Spotify"
        self.route = "/api/spotify"
        self.update_interval = 5

    def update(self):
        return {
            "track": "Connect Spotify",
            "artist": "Go to /login",
            "albumArt": "https://via.placeholder.com/120",
            "isPlaying": False
        }