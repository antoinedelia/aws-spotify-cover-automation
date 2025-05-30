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
