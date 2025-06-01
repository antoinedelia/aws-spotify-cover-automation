from dataclasses import asdict, dataclass

import requests
from loguru import logger


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
        url = f"https://api.spotify.com/v1/me/playlists?limit={limit}"

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

    def get_playlist_tracks(self, playlist_id: str) -> list[SpotifyTrack]:
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        params = {"fields": "items(track(id,name,artists(id,name)))"}
        tracks: list[SpotifyTrack] = []

        while url:
            r = requests.get(url, headers=self.headers, params=params, timeout=5)
            results = r.json()
            logger.debug(results)

            for item in results.get("items", []):
                new_artists: list[SpotifyArtist] = []
                for artist in item["track"]["artists"]:
                    new_artist = SpotifyArtist(artist["id"], artist["name"])
                    new_artists.append(new_artist)

                new_track = SpotifyTrack(id=item["track"]["id"], name=item["track"]["name"], artists=new_artists)
                tracks.append(new_track)

            url = results.get("next")

        return tracks

    def get_playlist_name(self, playlist_id: str) -> str:
        params = {"fields": "name"}
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}",
            headers=self.headers,
            params=params,
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
