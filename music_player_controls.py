# Import necessary modules
import tkinter as tk  # GUI framework
from tkinter import messagebox  # To show message boxes for user prompts
import pygame  # Pygame library for music playback
import os  # To handle file operations
import time  # For managing time delays in the update thread
from threading import Thread  # To run a thread for updating time display
import random

class MusicPlayerControls:
    def __init__(self, root, track_library, create_track_list):
        # Store the track library and track list objects
        self.track_library = track_library
        self.create_track_list = create_track_list
        # Create a frame for the music player controls and pack it on the right side
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initialize pygame mixer to handle audio playback
        pygame.mixer.init()

        # Label for music player controls section
        tk.Label(self.frame, text="Music Player Controls").grid(row=0, column=0, columnspan=3, sticky='nsew')

        # Button to play/pause music
        self.play_pause_button = tk.Button(self.frame, text="Play", command=self.toggle_play_pause)
        self.play_pause_button.grid(row=1, column=0, columnspan=3, sticky='nsew')

        # Button to play the next track
        self.next_button = tk.Button(self.frame, text="Next", command=self.play_next)
        self.next_button.grid(row=2, column=0, sticky='nsew')

        # Button to play the previous track
        self.previous_button = tk.Button(self.frame, text="Previous", command=self.play_previous)
        self.previous_button.grid(row=2, column=1, sticky='nsew')

        # Button to toggle shuffle mode
        self.shuffle_button = tk.Button(self.frame, text="Shuffle", command=self.toggle_shuffle)
        self.shuffle_button.grid(row=3, column=0, columnspan=2, sticky='nsew')

        # Button to toggle repeat mode
        self.repeat_button = tk.Button(self.frame, text="Repeat", command=self.toggle_repeat)
        self.repeat_button.grid(row=4, column=0, columnspan=2, sticky='nsew')

        # Slider to control the current track's position (seek functionality)
        self.track_position_slider = tk.Scale(self.frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.seek_track)
        self.track_position_slider.grid(row=5, column=0, columnspan=3, sticky='nsew')

        # Label to display the current time of the track
        self.current_time_label = tk.Label(self.frame, text="00:00")
        self.current_time_label.grid(row=6, column=0, sticky='w')

        # Label to display the total length of the track
        self.total_time_label = tk.Label(self.frame, text="00:00")
        self.total_time_label.grid(row=6, column=2, sticky='e')

        # Variables to track the current playback state
        self.is_playing = False  # Track if music is playing
        self.current_track = None  # Store current track info
        self.current_playlist_name = None  # Store the name of the current playlist
        self.track_numbers = []  # List of track numbers for the selected playlist
        self.current_index = 0  # Track the current index in the playlist
        self.is_repeat = False  # Flag to enable/disable repeat mode
        self.is_shuffle = False  # Flag to enable/disable shuffle mode

        # Start a thread to update the time display of the currently playing track
        self.update_thread = Thread(target=self.update_time_display)
        self.update_thread.daemon = True  # Set as daemon so it closes when the app closes
        self.update_thread.start()

    def update_playlist(self):
        """Update the current playlist when a new one is selected."""
        selected_playlist_name = self.create_track_list.current_playlist_name
        if selected_playlist_name != self.current_playlist_name:
            self.current_playlist_name = selected_playlist_name
            self.track_numbers = list(range(len(self.create_track_list.playlists[selected_playlist_name])))
            self.current_index = 0  # Reset current index when changing playlist
            self.current_track = None  # Reset current track

    def toggle_play_pause(self):
        # Update the playlist before playing to ensure we have the correct one
        self.update_playlist()
        # Play or pause the track depending on current state
        if self.is_playing:
            pygame.mixer.music.pause()  # Pause the music
            self.play_pause_button.config(text="Play")  # Change button text to "Play"
            self.is_playing = False  # Update state
        else:
            if not self.current_track:  # If no track is loaded, load the first track
                self.load_track()
            pygame.mixer.music.unpause()  # Resume music
            self.play_pause_button.config(text="Pause")  # Change button text to "Pause"
            self.is_playing = True  # Update state

    def load_track(self, track_number=None):
        # Load a track for playing, default to the current playlist and track index
        self.update_playlist()  # Ensure we are using the current playlist
        if track_number is None:
            if self.current_index >= len(self.track_numbers):
                self.current_index = 0
            track_number = self.track_numbers[self.current_index]

        if self.current_playlist_name:
            track = self.create_track_list.playlists[self.current_playlist_name][track_number]  # Get track details from the current playlist
            if track:
                file_path = track['file_path']
                if os.path.exists(file_path):  # Ensure the file exists
                    pygame.mixer.music.load(file_path)  # Load the track into the mixer
                    pygame.mixer.music.play()  # Play the track
                    self.current_track = track  # Store the current track
                    self.is_playing = True  # Update playing state
                    self.play_pause_button.config(text="Pause")  # Update button text
                    # Set slider range and total time label to track duration
                    track_length = pygame.mixer.Sound(file_path).get_length()
                    self.track_position_slider.config(to=track_length)
                    self.total_time_label.config(text=self.format_time(track_length))
                else:
                    messagebox.showerror("Error", f"File not found: {file_path}")
            else:
                messagebox.showerror("Error", "Invalid track number")
        else:
            messagebox.showerror("Error", "No playlist selected")

    def play_next(self):
        # Play the next track in the playlist
        self.update_playlist()  # Ensure the current playlist is loaded
        if self.is_shuffle:
            # Select a random track if shuffle is enabled
            self.current_index = random.randint(0, len(self.track_numbers) - 1)
        else:
            # Go to the next track in sequence, wrap around if at the end
            self.current_index = (self.current_index + 1) % len(self.track_numbers)
        self.load_track(self.current_index)  # Load the next track

    def play_previous(self):
        # Play the previous track in the playlist
        self.update_playlist()  # Ensure the current playlist is loaded
        if self.is_shuffle:
            # Select a random track if shuffle is enabled
            self.current_index = random.randint(0, len(self.track_numbers) - 1)
        else:
            # Go to the previous track in sequence, wrap around if at the beginning
            self.current_index = (self.current_index - 1) % len(self.track_numbers)
        self.load_track(self.current_index)  # Load the previous track

    def toggle_shuffle(self):
        # Toggle shuffle mode on or off
        self.is_shuffle = not self.is_shuffle
        if self.is_shuffle:
            messagebox.showinfo("Shuffle", "Shuffle mode enabled")
        else:
            messagebox.showinfo("Shuffle", "Shuffle mode disabled")

    def toggle_repeat(self):
        # Toggle repeat mode on or off
        self.is_repeat = not self.is_repeat
        if self.is_repeat:
            messagebox.showinfo("Repeat", "Repeat mode enabled")
        else:
            messagebox.showinfo("Repeat", "Repeat mode disabled")

    def seek_track(self, value):
        # Seek to a particular position in the current track
        pygame.mixer.music.set_pos(float(value))  # Set the position in seconds

    def update_time_display(self):
        # Continuously update the current playback time on the slider and label
        while True:
            if self.is_playing and pygame.mixer.music.get_busy():  # Check if music is playing
                current_time = pygame.mixer.music.get_pos() / 1000  # Get the current position in seconds
                self.current_time_label.config(text=self.format_time(current_time))  # Update time label
                self.track_position_slider.set(current_time)  # Update the slider position
                
                # Automatically play the next track if the current one has ended
                if not pygame.mixer.music.get_busy() and not self.is_repeat:
                    self.play_next()  # Play the next track
                elif not pygame.mixer.music.get_busy() and self.is_repeat:
                    self.load_track(self.current_index)  # Reload the same track if repeat is on
                    
            time.sleep(1)  # Update every second

    def format_time(self, seconds):
        # Format seconds into minutes:seconds format
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"  # Format as MM:SS
