from loguru import logger

from src.spotify import Spotify
from src.utils import format_response


def lambda_handler(event, context):
    # Get the Spotify access token from the event data in the body key
    logger.info(event)
    access_token = event["headers"]["X-Spotify-Token"]

    spotify = Spotify(access_token)

    user_id = spotify.get_user_id()
    playlists = spotify.get_user_playlists(user_id)

    playlists_dict = [playlist.to_dict() for playlist in playlists]

    return format_response("Updated playlist cover!", 200, playlists_dict)
