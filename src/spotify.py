from dataclasses import asdict, dataclass

import requests
from loguru import logger
from typing import Any, Optional

@dataclass
class SpotifyPlaylist:
    id: str
    name: str

    def to_dict(self):
        return asdict(self)


@dataclass
class SpotifyArtist:
    id: str
    name: str


@dataclass
class SpotifyTrack:
    id: str
    name: str
    artists: list[SpotifyArtist]


class Spotify:
    BASE_URL = "https://api.spotify.com/v1"

    def __init__(self, access_token: str) -> None:
        self.token = access_token
        self._headers = {"Authorization": f"Bearer {self.token}"}

    def _request(self, method: str, url: str, **kwargs: Any) -> Optional[requests.Response]:
        """
        A centralized method to make HTTP requests and handle common errors.
        
        Args:
            method: The HTTP method to use (e.g., "GET", "POST", "PUT").
            url: The full URL for the request.
            **kwargs: Additional keyword arguments to pass to requests (e.g., params, data, json, headers).

        Returns:
            A requests.Response object if successful, None otherwise.
        """
        headers = {**self._headers, **kwargs.pop("headers", {})}
        
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                timeout=kwargs.pop("timeout", 10),
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error {e.response.status_code} for {method} {url}: {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {method} {url}: {e}")
            raise
            
    @staticmethod
    def get_playlist_id_from_uri(uri: str) -> str:
        playlist_id = uri.split("/")[-1]
        if "?" in playlist_id:
            playlist_id = playlist_id.split("?")[0]
        return playlist_id

    def get_user_id(self) -> str:
        response = self._request("GET", f"{self.BASE_URL}/me")
        return response.json()["id"]

    def get_user_playlists(self, user_id: str, limit: int = 20) -> list[SpotifyPlaylist]:
        playlists: list[SpotifyPlaylist] = []
        url = f"{self.BASE_URL}/users/{user_id}/playlists?limit={limit}"

        while url:
            try:
                response = self._request("GET", url)
                if not response: break

                results = response.json()
                logger.debug(f"Fetched user playlists page: {url}, Items: {len(results.get('items', []))}")

                for item in results.get("items", []):
                    playlists.append(SpotifyPlaylist(id=item.get("id"), name=item.get("name")))

                url = results.get("next")
            except requests.exceptions.RequestException:
                break
        return playlists

    def get_playlist_tracks(self, playlist_id: str) -> list[SpotifyTrack]:
        tracks: list[SpotifyTrack] = []
        url = f"{self.BASE_URL}/playlists/{playlist_id}/tracks"
        params = {"fields": "items(track(id,name,artists(id,name))),next"}

        while url:
            try:
                current_params = params if "offset" not in url else None
                response = self._request("GET", url, params=current_params)
                if not response: break

                results = response.json()
                for item in results.get("items", []):
                    if item.get("track"):
                        artists = [SpotifyArtist(a["id"], a["name"]) for a in item["track"]["artists"]]
                        tracks.append(SpotifyTrack(item["track"]["id"], item["track"]["name"], artists))

                url = results.get("next")
            except (requests.exceptions.RequestException, ValueError) as e:
                logger.error(f"Could not process playlist tracks from {url}: {e}")
                break
        return tracks

    def get_playlist_name(self, playlist_id: str) -> str:
        response = self._request(
            "GET",
            f"{self.BASE_URL}/playlists/{playlist_id}",
            params={"fields": "name"}
        )
        return response.json()["name"]

    def get_artist_image_by_id(self, artist_id: str) -> Optional[str]:
        response = self._request("GET", f"{self.BASE_URL}/artists/{artist_id}")
        data = response.json()
        return data["images"][0]["url"] if data.get("images") else None

    def update_playlist_cover_image(self, playlist_id: str, image_data: bytes) -> None:
        headers = {"Content-Type": "image/jpeg"}
        self._request(
            "PUT",
            f"{self.BASE_URL}/playlists/{playlist_id}/images",
            headers=headers,
            data=image_data
        )
        logger.info(f"Successfully sent request to update cover for playlist {playlist_id}.")
