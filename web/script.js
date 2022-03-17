var client_id = '3cc70e52f21c435ca4bfdbbb07261f3c';
var redirect_uri = 'http://antoinedelia.s3-website-eu-west-1.amazonaws.com/';
var loadingMessage = document.getElementById("loadingMessage")
var successMessage = document.getElementById("successMessage")
var errorMessage = document.getElementById("errorMessage")
var responseMessage = document.getElementById("responseMessage")
var playlistImage = document.getElementById("playlistImage")
var isLoading = false;

function login() {
    var scope = 'user-library-read playlist-modify-public playlist-modify-private playlist-read-private ugc-image-upload';                
    var url = "https://accounts.spotify.com/authorize?response_type=token&scope=" + scope + "&client_id=" + client_id + "&redirect_uri=" + redirect_uri;
    window.location = url;
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
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
            "access_token": localStorage.getItem('access_token')
        })
    }).then(function(response) {
        console.log(response.json());
        successMessage.style.visibility = "visible";
        responseMessage.innerHTML = response.json().artists;
        playlistImage.src = "data:image/jpeg;base64," + response.json().playlist_cover_b64;
    }).catch(function(error) {
        console.log(error);
        errorMessage.style.visibility = "visible";
    }).finally(function() {
        isLoading = false;
        loadingMessage.style.visibility = "hidden";
    });
}

window.onload = async function() {
    if(window.location.hash) {
        var values = window.location.hash.substring(1).split("&");
        for(var i = 0; i < values.length; i++) {
            var value = values[i].split("=");
            if(value[0] == "access_token") {
                access_token = value[1];
                localStorage.setItem("access_token", access_token);
            }
        }
    }
};
