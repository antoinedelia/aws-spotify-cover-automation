from loguru import logger
import requests


class Spotify:
    def __init__(self, access_token) -> None:
        self.token = access_token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def get_playlist_id_from_uri(self, uri: str) -> str:
        playlist_id = uri.split("/")[-1]
        if "?" in playlist_id:
            playlist_id = playlist_id.split("?")[0]
        return playlist_id

    def get_playlist_tracks(self, playlist_id: str) -> list:
        response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=self.headers)
        logger.debug(response.json())
        results = response.json()

        tracks = []
        while results["next"]:
            for item in results["items"]:
                tracks.append(item["track"])
            results = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=self.headers).json()

        # We do an extra for loop to get the last tracks
        for item in results["items"]:
            tracks.append(item["track"])

        return tracks

    def get_playlist_name(self, playlist_id: str) -> str:
        response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=self.headers)
        logger.debug(response.json())
        return response.json()["name"]

    def get_artist_image_by_id(self, artist_id: str) -> str:
        response = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}", headers=self.headers)
        logger.debug(response.json())
        return response.json()["images"][0]["url"]

    def update_playlist_cover_image(self, playlist_id: str, image) -> None:
        self.headers["Content-Type"] = "image/jpeg"
        response = requests.put(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/images",
            headers=self.headers,
            data=image,
        )
        logger.info(response.status_code)
        logger.info(response.json())
