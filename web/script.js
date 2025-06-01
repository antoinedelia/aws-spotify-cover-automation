var client_id = '3cc70e52f21c435ca4bfdbbb07261f3c';
var redirect_uri = 'http://antoinedelia.s3-website-eu-west-1.amazonaws.com/';
var loadingMessage = document.getElementById("loadingMessage")
var successMessage = document.getElementById("successMessage")
var errorMessage = document.getElementById("errorMessage")
var responseMessage = document.getElementById("responseMessage")
var playlists = document.getElementById("playlists")
var playlistImage = document.getElementById("playlistImage")
var isLoading = false;

function login() {
    var scope = 'user-library-read playlist-modify-public playlist-modify-private playlist-read-private ugc-image-upload';
    var url = "https://accounts.spotify.com/authorize?response_type=token&scope=" + scope + "&client_id=" + client_id + "&redirect_uri=" + redirect_uri;
    window.location = url;
}

function getAllPlaylists() {
    isLoading = true;
    loadingMessage.style.visibility = "visible";
    playlists.style.visibility = "hidden";
    var apiUrl = "https://8dq0nboksj.execute-api.eu-west-1.amazonaws.com/prod/playlists"
    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'X-Spotify-Token': localStorage.getItem('access_token')
        },
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            playlists.style.visibility = "visible";
            playlists.innerHTML = result.body;
        }).catch(function (error) {
            console.log(error);
        }).finally(function () {
            isLoading = false;
            loadingMessage.style.visibility = "hidden";
        });
}

function updateArtCover() {
    isLoading = true;
    loadingMessage.style.visibility = "visible";
    successMessage.style.visibility = "hidden";
    errorMessage.style.visibility = "hidden";
    var apiUrl = "https://dn3etvqcik.execute-api.eu-west-1.amazonaws.com/prod/spotify/cover-automation"
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'X-Spotify-Token': localStorage.getItem('access_token')
        },
        body: JSON.stringify({
            "playlist_id": "0JP3smzah2mTnxIZIVjVX0"  // TODO: Update with user's choice
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            successMessage.style.visibility = "visible";
            responseMessage.innerHTML = result.body[0].artists;
            playlistImage.src = "data:image/jpeg;base64," + result.body[0].playlist_cover_b64;
        }).catch(function (error) {
            console.log(error);
            errorMessage.style.visibility = "visible";
        }).finally(function () {
            isLoading = false;
            loadingMessage.style.visibility = "hidden";
        });
}

window.onload = async function () {
    if (window.location.hash) {
        var values = window.location.hash.substring(1).split("&");
        for (var i = 0; i < values.length; i++) {
            var value = values[i].split("=");
            if (value[0] == "access_token") {
                access_token = value[1];
                localStorage.setItem("access_token", access_token);
            }
        }
    }
};
