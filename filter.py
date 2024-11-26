# filter.py
import tkinter as tk
from tkinter import messagebox

class TrackFilter:
    def __init__(self, root, track_library, create_track_list):
        self.track_library = track_library
        self.create_track_list = create_track_list
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Label for Track Filter section
        tk.Label(self.frame, text="Filter Tracks").grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        # Entry field for author name
        tk.Label(self.frame, text="Author Name:").grid(row=1, column=0, sticky='nsew')
        self.author_entry = tk.Entry(self.frame)
        self.author_entry.grid(row=1, column=1, sticky='nsew')
        
        # Entry field for rating
        tk.Label(self.frame, text="Rating (1-5):").grid(row=2, column=0, sticky='nsew')
        self.rating_entry = tk.Entry(self.frame)
        self.rating_entry.grid(row=2, column=1, sticky='nsew')
        
        # Button to apply filter
        self.filter_button = tk.Button(self.frame, text="Apply Filter", command=self.apply_filter)
        self.filter_button.grid(row=3, column=0, columnspan=2, sticky='nsew')
        
        # Text area to display filtered tracks
        self.filtered_tracks_text_area = tk.Text(self.frame, height=10, width=30)
        self.filtered_tracks_text_area.grid(row=4, column=0, columnspan=2, sticky='nsew')
        
        # Configure grid to auto-resize
        for i in range(5):
            self.frame.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.frame.grid_columnconfigure(j, weight=1)

    def apply_filter(self):
        author_name = self.author_entry.get().lower()
        rating = self.rating_entry.get()
        filtered_tracks = []
        
        # Filter tracks based on author and rating
        for track in self.track_library.list_all():
            if author_name in track['artist'].lower() and (rating == '' or track['rating'] == int(rating)):
                filtered_tracks.append(track)
        
        # Display filtered results
        self.filtered_tracks_text_area.delete("1.0", tk.END)
        if filtered_tracks:
            for track in filtered_tracks:
                self.filtered_tracks_text_area.insert(tk.END, f"Track: {track['name']} by {track['artist']} (Rating: {track['rating']})\n")
        else:
            messagebox.showinfo("No Results", "No tracks found matching the criteria")
