# update_tracks.py
import tkinter as tk
from tkinter import messagebox

class UpdateTracks:
    def __init__(self, root, track_library):
        self.track_library = track_library
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Label for Update Tracks section
        tk.Label(self.frame, text="Update Tracks").grid(row=0, column=0, columnspan=2, sticky='nsew')
        
        # Entry field for track number input
        tk.Label(self.frame, text="Track Number:").grid(row=1, column=0, sticky='nsew')
        self.update_track_number_entry = tk.Entry(self.frame)
        self.update_track_number_entry.grid(row=1, column=1, sticky='nsew')
        
        # Entry field for new rating input (1-5)
        tk.Label(self.frame, text="New Rating (1-5):").grid(row=2, column=0, sticky='nsew')
        self.new_rating_entry = tk.Entry(self.frame)
        self.new_rating_entry.grid(row=2, column=1, sticky='nsew')
        
        # Entry field for new track name
        tk.Label(self.frame, text="New Track Name:").grid(row=3, column=0, sticky='nsew')
        self.new_track_name_entry = tk.Entry(self.frame)
        self.new_track_name_entry.grid(row=3, column=1, sticky='nsew')
        
        # Entry field for new artist name
        tk.Label(self.frame, text="New Artist Name:").grid(row=4, column=0, sticky='nsew')
        self.new_artist_name_entry = tk.Entry(self.frame)
        self.new_artist_name_entry.grid(row=4, column=1, sticky='nsew')
        
        # Button to update the rating of a track
        self.update_button = tk.Button(self.frame, text="Update", command=self.update_track_info)
        self.update_button.grid(row=5, column=0, columnspan=2, sticky='nsew')
        
        # Configure grid to auto-resize
        for i in range(6):
            self.frame.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.frame.grid_columnconfigure(j, weight=1)

    def update_track_info(self):
        track_number = self.update_track_number_entry.get()
        new_rating = self.new_rating_entry.get()
        new_track_name = self.new_track_name_entry.get()
        new_artist_name = self.new_artist_name_entry.get()
        
        # Validate track number and update fields
        if track_number:
            updates = {}
            if new_rating.isdigit() and 1 <= int(new_rating) <= 5:
                updates['rating'] = int(new_rating)
            if new_track_name:
                updates['name'] = new_track_name
            if new_artist_name:
                updates['artist'] = new_artist_name
            
            if updates:
                try:
                    # Update track information and save changes to JSON file
                    self.track_library.update_track_info(track_number, **updates)
                    messagebox.showinfo("Update Track", f"Track {track_number} updated successfully.")
                except ValueError:
                    messagebox.showerror("Error", "Invalid track number")
            else:
                messagebox.showerror("Error", "Please provide valid information to update.")
        else:
            messagebox.showerror("Error", "Please enter a valid track number.")
