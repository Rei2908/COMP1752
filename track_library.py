# track_library.py
import os
import json

class TrackLibrary:
    def __init__(self, music_folder, track_library_file="track_library.json"):
        self.tracks = {}
        self.track_number = 1
        self.track_library_file = track_library_file
        if os.path.exists(self.track_library_file):
            self.load_track_library()
        else:
            self.load_tracks_from_folder(music_folder)
            self.save_track_library()

    def load_tracks_from_folder(self, folder_path):
        # Load tracks from the specified folder and assign track details
        for file_name in sorted(os.listdir(folder_path), key=lambda x: os.path.getctime(os.path.join(folder_path, x))):
            if file_name.endswith(('.mp3', '.wav')):
                track_name = os.path.splitext(file_name)[0]
                self.tracks[str(self.track_number)] = {
                    'name': track_name,
                    'artist': 'Unknown Artist',
                    'rating': 0,
                    'play_count': 0,
                    'file_path': os.path.join(folder_path, file_name)
                }
                self.track_number += 1

    def save_track_library(self):
        # Save track library to JSON file for persistence
        with open(self.track_library_file, 'w') as f:
            json.dump(self.tracks, f, indent=4)

    def load_track_library(self):
        # Load track library from JSON file
        with open(self.track_library_file, 'r') as f:
            self.tracks = json.load(f)

    def get_track(self, track_number):
        # Get track information by track number
        return self.tracks.get(track_number)

    def list_all(self):
        # List all tracks in the library
        return self.tracks.values()

    def update_track_info(self, track_number, **kwargs):
        # Update track information and save to JSON file
        if track_number in self.tracks:
            for key, value in kwargs.items():
                if key in self.tracks[track_number]:
                    self.tracks[track_number][key] = value
            self.save_track_library()  # Save changes to the JSON file
        else:
            raise ValueError("Track number does not exist")


