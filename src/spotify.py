from dataclasses import asdict, dataclass

import requests
from loguru import logger


@dataclass
class SpotifyPlaylist:
    id: str
    name: str

    def to_dict(self):
        return asdict(self)


class Spotify:
    def __init__(self, access_token) -> None:
        self.token = access_token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @staticmethod
    def get_playlist_id_from_uri(uri: str) -> str:
        playlist_id = uri.split("/")[-1]
        if "?" in playlist_id:
            playlist_id = playlist_id.split("?")[0]
        return playlist_id

    def get_user_id(self) -> str:
        r = requests.get("https://api.spotify.com/v1/me", headers=self.headers, timeout=5)
        if r.ok:
            return r.json()["id"]
        else:
            raise Exception(f"Error fetching user id: {r.json()['error']['message']}")

    def get_user_playlists(self, user_id: str, limit: int = 10) -> list[SpotifyPlaylist]:
        playlists: list[SpotifyPlaylist] = []
        url = f"https://api.spotify.com/v1/users/{user_id}/playlists?limit={limit}"

        while url:
            try:
                response = requests.get(url, headers=self.headers, timeout=5)
                response.raise_for_status()
                results = response.json()
                logger.debug(f"Fetched user playlists page: {url}, Items: {len(results.get('items', []))}")

                for item in results.get("items", []):
                    playlists.append(SpotifyPlaylist(id=item.get("id"), name=item.get("name")))

                url = results.get("next")
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching user playlists from {url}: {e}")
                break
            except ValueError as e:
                logger.error(f"Error decoding JSON from {url} for user playlists: {e}")
                break

        return playlists

    def get_playlist_tracks(self, playlist_id: str) -> list:
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
            headers=self.headers,
            timeout=5,
        )
        logger.debug(response.json())
        results = response.json()

        tracks = []
        while results["next"]:
            for item in results["items"]:
                tracks.append(item["track"])
            results = requests.get(
                f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
                headers=self.headers,
                timeout=5,
            ).json()

        # We do an extra for loop to get the last tracks
        for item in results["items"]:
            tracks.append(item["track"])

        return tracks

    def get_playlist_name(self, playlist_id: str) -> str:
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}",
            headers=self.headers,
            timeout=5,
        )
        logger.debug(response.json())
        return response.json()["name"]

    def get_artist_image_by_id(self, artist_id: str) -> str:
        response = requests.get(
            f"https://api.spotify.com/v1/artists/{artist_id}",
            headers=self.headers,
            timeout=5,
        )
        logger.debug(response.json())
        return response.json()["images"][0]["url"]

    def update_playlist_cover_image(self, playlist_id: str, image) -> None:
        self.headers["Content-Type"] = "image/jpeg"
        response = requests.put(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/images",
            headers=self.headers,
            data=image,
            timeout=10,
        )
        logger.info(response.status_code)
