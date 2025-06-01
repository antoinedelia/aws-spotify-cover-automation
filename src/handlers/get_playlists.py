from spotify import Spotify
from utils import format_response


def lambda_handler(event, context):
    # Get the Spotify access token from the event data in the body key
    try:
        access_token = event["headers"]["X-Spotify-Token"]
    except KeyError:
        return format_response("Token was not provided in the X-Spotify-Token header", 400)

    spotify = Spotify(access_token)

    try:
        user_id = spotify.get_user_id()
    except Exception as e:
        return format_response("Error while trying to get playlists", 500, str(e))

    playlists = spotify.get_user_playlists(user_id)

    playlists_dict = [playlist.to_dict() for playlist in playlists]

    return format_response(f"Retrieved {len(playlists_dict)} playlists!", 200, playlists_dict)
