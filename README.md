# Spotify Cover Automation

App that automates the creation of covers for playlists in Spotify

## Getting Started

Create a new application in the [Spotify Dashboard](https://developer.spotify.com/dashboard/applications) to get your client id and client secret.

```shell
$ pip install -r requirements.txt

# Spotify Credentials
$ export SPOTIPY_CLIENT_ID="your-client-id"
$ export SPOTIPY_CLIENT_SECRET="your-client-secret"
$ export SPOTIPY_REDIRECT_URI="http://localhost:8080"

$ python src/main.py
```

## Docker configuration on WSL
```sh
sudo usermod -a -G docker $USER
grep docker /etc/group
newgrp docker
```