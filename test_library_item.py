# test_library_item.py
import pytest
from track_library import TrackLibrary

def test_get_track():
    library = TrackLibrary(music_folder="music")
    library.tracks = {
        '1': {'name': 'Track1', 'artist': 'Artist1', 'rating': 3, 'file_path': 'path/to/file1.mp3'},
        '2': {'name': 'Track2', 'artist': 'Artist2', 'rating': 4, 'file_path': 'path/to/file2.mp3'}
    }

    # Test valid track
    track = library.get_track('1')
    assert track['name'] == 'Track1'
    assert track['artist'] == 'Artist1'
    assert track['rating'] == 3

    # Test invalid track
    track = library.get_track('99')
    assert track is None