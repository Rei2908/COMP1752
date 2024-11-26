import tkinter as tk
from tkinter import messagebox, simpledialog

class CreateTrackList:
    def __init__(self, root, track_library):
        self.track_library = track_library
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Dictionary to store multiple playlists
        self.playlists = {}
        self.current_playlist_name = None

        # Label for Create Track List section
        tk.Label(self.frame, text="Create Track List").grid(row=0, column=0, columnspan=2, sticky='nsew')

        # Button to create a new playlist
        self.new_playlist_button = tk.Button(self.frame, text="New Playlist", command=self.create_new_playlist)
        self.new_playlist_button.grid(row=1, column=0, columnspan=2, sticky='nsew')

        # Button to select an existing playlist
        self.select_playlist_button = tk.Button(self.frame, text="Select Playlist", command=self.select_playlist)
        self.select_playlist_button.grid(row=2, column=0, columnspan=2, sticky='nsew')

        # Entry field for track number input
        tk.Label(self.frame, text="Track Number:").grid(row=3, column=0, sticky='nsew')
        self.track_number_entry = tk.Entry(self.frame)
        self.track_number_entry.grid(row=3, column=1, sticky='nsew')

        # Button to add track to the current playlist
        self.add_track_button = tk.Button(self.frame, text="Add to Playlist", command=self.add_to_playlist)
        self.add_track_button.grid(row=4, column=0, columnspan=2, sticky='nsew')

        # Button to automatically add all tracks to the playlist
        self.add_all_tracks_button = tk.Button(self.frame, text="Add All Tracks to Playlist", command=self.add_all_tracks_to_playlist)
        self.add_all_tracks_button.grid(row=5, column=0, columnspan=2, sticky='nsew')

        # Text area to display the current playlist
        self.playlist_text_area = tk.Text(self.frame, height=10, width=30)
        self.playlist_text_area.grid(row=6, column=0, columnspan=2, sticky='nsew')

        # Button to reset the current playlist
        self.reset_playlist_button = tk.Button(self.frame, text="Reset Playlist", command=self.reset_playlist)
        self.reset_playlist_button.grid(row=7, column=0, columnspan=2, sticky='nsew')

        # Configure grid to auto-resize
        for i in range(8):
            self.frame.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.frame.grid_columnconfigure(j, weight=1)

    def create_new_playlist(self):
        # Prompt the user for a playlist name
        playlist_name = simpledialog.askstring("New Playlist", "Enter a name for the new playlist:")
        if playlist_name:
            if playlist_name in self.playlists:
                messagebox.showerror("Error", "A playlist with this name already exists.")
            else:
                self.playlists[playlist_name] = []
                self.current_playlist_name = playlist_name
                self.update_playlist_display()

    def select_playlist(self):
        # Prompt the user for a playlist to select
        if not self.playlists:
            messagebox.showerror("Error", "No playlists available. Please create a new playlist first.")
            return

        playlist_name = simpledialog.askstring("Select Playlist", "Enter the name of the playlist to select:")
        if playlist_name in self.playlists:
            self.current_playlist_name = playlist_name
            self.update_playlist_display()
        else:
            messagebox.showerror("Error", "Playlist not found.")

    def add_to_playlist(self):
        if not self.current_playlist_name:
            messagebox.showerror("Error", "No playlist selected. Please create or select a playlist first.")
            return

        track_number = self.track_number_entry.get()
        # Validate track number
        track = self.track_library.get_track(track_number)
        if track:
            # Add track to the current playlist if valid and display in the text area
            self.playlists[self.current_playlist_name].append(track)
            self.update_playlist_display()
        else:
            # Show error if track number is invalid
            messagebox.showerror("Error", "Invalid track number")

    def add_all_tracks_to_playlist(self):
        if not self.current_playlist_name:
            messagebox.showerror("Error", "No playlist selected. Please create or select a playlist first.")
            return

        # Automatically add all tracks from the track library to the current playlist
        for track_number, track in self.track_library.tracks.items():
            self.playlists[self.current_playlist_name].append(track)
        self.update_playlist_display()

    def reset_playlist(self):
        if not self.current_playlist_name:
            messagebox.showerror("Error", "No playlist selected. Please create or select a playlist first.")
            return

        # Clear the current playlist
        self.playlists[self.current_playlist_name] = []
        self.update_playlist_display()

    def update_playlist_display(self):
        # Update the playlist display in the text area
        self.playlist_text_area.delete("1.0", tk.END)
        if self.current_playlist_name:
            self.playlist_text_area.insert(tk.END, f"Playlist: {self.current_playlist_name}\n")
            for track in self.playlists[self.current_playlist_name]:
                self.playlist_text_area.insert(tk.END, f"Track: {track['name']} by {track['artist']} (Rating: {track['rating']})\n")
