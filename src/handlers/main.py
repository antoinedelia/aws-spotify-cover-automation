import base64
import json
from collections import Counter
from io import BytesIO

import requests
from loguru import logger
from PIL import Image, ImageDraw, ImageFont

from spotify import Spotify, SpotifyPlaylist
from utils import format_response

ARTIST_IMAGE_SIZE = 640
IMAGE_SIZE = ARTIST_IMAGE_SIZE * 2


def lambda_handler(event, context):
    # Get the Spotify access token from the event data in the body key
    logger.info(event)
    body = event["body"]

    try:
        access_token = event["headers"]["X-Spotify-Token"]
    except KeyError:
        return format_response("Token was not provided in the X-Spotify-Token header", 400)

    try:
        playlist_id = json.loads(body)["playlist_id"]
    except KeyError:
        return format_response("Playlist id was not provided in the payload", 400)

    spotify = Spotify(access_token)
    playlist_name = spotify.get_playlist_name(playlist_id)

    playlist = SpotifyPlaylist(playlist_id, playlist_name)

    logger.info(f"Playlist: {playlist.name}")

    # Get the tracks from the playlist
    tracks = spotify.get_playlist_tracks(playlist.id)

    artists = []
    for track in tracks:
        for artist in track["artists"]:
            artists.append({"id": artist["id"], "name": artist["name"]})

    playlist_cover = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE))

    counter = Counter([artist["name"] for artist in artists])
    four_most_common = counter.most_common(4)
    for index, (artist_name, occurrence) in enumerate(four_most_common):
        logger.info(f"{index} - Found {occurrence} song(s) from {artist_name}")
        current_artist = next(artist for artist in artists if artist["name"] == artist_name)
        image_url = spotify.get_artist_image_by_id(current_artist["id"])

        image_response = requests.get(image_url, timeout=5)
        img = Image.open(BytesIO(image_response.content))
        img.thumbnail((ARTIST_IMAGE_SIZE, ARTIST_IMAGE_SIZE), Image.ANTIALIAS)
        x = index % 2 * ARTIST_IMAGE_SIZE
        y = index // 2 * ARTIST_IMAGE_SIZE
        w, h = img.size
        playlist_cover.paste(img, (x, y, x + w, y + h))

    # Converting back to RGBA to apply gradient
    playlist_cover = playlist_cover.convert("RGBA")
    gradient = Image.new("L", (1, IMAGE_SIZE), color=0xFF)
    current_color = 255
    for y in range(IMAGE_SIZE):
        if y % 2 == 0:
            current_color -= 1
        current_y = IMAGE_SIZE - y - 1
        gradient.putpixel((0, current_y), current_color)
    alpha = gradient.resize(playlist_cover.size)
    black_im = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE), color=0)
    black_im.putalpha(alpha)
    playlist_cover = Image.alpha_composite(playlist_cover, black_im)

    # Adding the text
    draw = ImageDraw.Draw(playlist_cover)
    font = ImageFont.truetype("./src/fonts/Montserrat-Bold.ttf", 120)
    draw.text(
        xy=(ARTIST_IMAGE_SIZE, IMAGE_SIZE - 50),
        text=playlist.name,
        fill=(255, 255, 255),
        anchor="ms",
        font=font,
        align="center",
    )

    # Converting back to RGB
    playlist_cover = playlist_cover.convert("RGB")

    # Reduce the size of the image
    playlist_cover.thumbnail((ARTIST_IMAGE_SIZE, ARTIST_IMAGE_SIZE), Image.ANTIALIAS)

    logger.info("Updating playlist cover...")
    buffered = BytesIO()
    playlist_cover.save(buffered, format="JPEG")
    playlist_cover_string = base64.b64encode(buffered.getvalue())
    spotify.update_playlist_cover_image(playlist.id, playlist_cover_string)

    result = {
        "playlist_name": playlist.name,
        "artists": [f"{artist_name} ({occurrence})" for artist_name, occurrence in four_most_common],
        "playlist_cover_b64": playlist_cover_string.decode("utf-8"),
    }

    return format_response("Updated playlist cover!", 200, result)
