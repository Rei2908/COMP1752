import os
import tkinter as tk
from create_track_list import CreateTrackList
from update_tracks import UpdateTracks
from track_library import TrackLibrary
from music_player_controls import MusicPlayerControls
from filter import TrackFilter

# Set the base directory for relative paths to ensure compatibility across devices
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path for the music folder relative to the base directory
MUSIC_FOLDER = os.path.join(BASE_DIR, "music")

class MusicBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Box Prototype")  # Set the window title
        
        # Create a TrackLibrary instance using the specified music folder
        self.track_library = TrackLibrary(MUSIC_FOLDER)
        
        # Create Track List GUI to manage playlist creation
        self.create_track_list = CreateTrackList(self.root, self.track_library)
        self.create_track_list.frame.pack(pady=10)  # Add padding between elements
        
        # Update Tracks GUI to manage track ratings, names, etc.
        self.update_tracks = UpdateTracks(self.root, self.track_library)
        self.update_tracks.frame.pack(pady=10)
        
        # Music Player Controls GUI to manage playback
        self.music_player_controls = MusicPlayerControls(self.root, self.track_library, self.create_track_list)
        self.music_player_controls.frame.pack(pady=10)
        
        # Track Filter GUI for filtering the tracks
        self.track_filter = TrackFilter(root, self.track_library, None)

if __name__ == "__main__":
    root = tk.Tk()  # Create the root Tkinter window
    app = MusicBoxApp(root)  # Instantiate the app
    root.mainloop()  # Start the GUI main loop
