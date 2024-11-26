# playlist_manager.py
import os
import json

# Set the base directory for relative paths to ensure compatibility across devices
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PlaylistManager:
    def __init__(self, playlist_file="playlist_manager.json"):
        self.playlist_file = os.path.join(BASE_DIR, playlist_file)
        self.playlists = {}
        
        # Load existing playlists if the file exists
        if os.path.exists(self.playlist_file) and os.path.getsize(self.playlist_file) > 0:
            self.load_playlists()
        else:
            self.save_playlists()

    def save_playlist(self, playlist_name, track_number):
        # Save a single playlist to the playlists dictionary and save to the JSON file
        self.playlists[playlist_name] = {'track_number': track_number}
        self.save_playlists()

    def load_playlist(self, playlist_name):
        # Load a specific playlist from the playlists dictionary
        return self.playlists.get(playlist_name)

    def save_playlists(self):
        # Save all playlists to the JSON file for persistence
        try:
            with open(self.playlist_file, 'w') as f:
                json.dump(self.playlists, f, indent=4)
        except Exception as e:
            print(f"Failed to save playlists: {e}")

    def load_playlists(self):
        # Load all playlists from the JSON file
        try:
            with open(self.playlist_file, 'r') as f:
                self.playlists = json.load(f)
        except FileNotFoundError:
            print(f"Playlist file {self.playlist_file} not found. Creating a new one.")
            self.playlists = {}
            self.save_playlists()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {self.playlist_file}: {e}. Creating a new one.")
            self.playlists = {}
            self.save_playlists()

    def list_playlists(self):
        # List all available playlists
        return list(self.playlists.keys())

    def delete_playlist(self, playlist_name):
        # Delete a specific playlist
        if playlist_name in self.playlists:
            del self.playlists[playlist_name]
            self.save_playlists()
        else:
            raise ValueError("Playlist does not exist")
