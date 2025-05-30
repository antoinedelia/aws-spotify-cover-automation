import pytest

from src import spotify

uri_test_cases = [
    ("https://open.spotify.com/playlist/0JP3smzah2mTnxIZIVjVX0?si=e33aaca9d1334dc6", "0JP3smzah2mTnxIZIVjVX0"),
    ("https://open.spotify.com/playlist/0JP3smzah2mTnxIZIVjVX0", "0JP3smzah2mTnxIZIVjVX0"),
]


@pytest.mark.parametrize("uri_input, expected_id", uri_test_cases)
def test_get_playlist_id_from_uri(uri_input, expected_id):
    """
    Tests the static method get_playlist_id_from_uri with various URI inputs.
    """
    if spotify.Spotify.get_playlist_id_from_uri(uri_input) != expected_id:
        raise ValueError("Expected id is not valid")


def test_playlist_creation_and_to_dict():
    """
    Tests the creation of a SpotifyPlaylist object and its to_dict method using pytest.
    """
    expected_id = "playlist123"
    expected_name = "My Test Playlist"
    expected_dict = {"id": expected_id, "name": expected_name}

    playlist = spotify.SpotifyPlaylist(id=expected_id, name=expected_name)

    assert playlist.id == expected_id, "Playlist ID should match"
    assert playlist.name == expected_name, "Playlist name should match"

    assert playlist.to_dict() == expected_dict, "to_dict() should return the correct dictionary"
