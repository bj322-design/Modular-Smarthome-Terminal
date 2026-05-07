from flask import Blueprint, jsonify, redirect, request
import base64
import requests

# Blueprint for Spotify
spotify_bp = Blueprint("spotify_bp", __name__)

# Spotify API credentials that are needed 
CLIENT_ID = "f77a81fa784b46d6a3513a1fddbd3a2f"
CLIENT_SECRET = "8ea40647f6c34ed7bae3afa7c5e1a267"
REDIRECT_URI = "http://127.0.0.1:5000/callback"

# Stores access
access_token = None
refresh_token = None


# Authorization header for token request
def get_auth_header():
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    return {"Authorization": f"Basic {auth_base64}"}


# Creates a bearer token header for the API calls 
def get_bearer_header():
    return {"Authorization": f"Bearer {access_token}"}


# When tokens expire this will refresh them
def refresh_access_token():
    global access_token, refresh_token

    if not refresh_token:
        return False

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=get_auth_header(),
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    )

    if response.status_code != 200:
        return False

    token_data = response.json()
    access_token = token_data.get("access_token")
    return True


# Route needed to redirect user to Spotify login page 
@spotify_bp.route("/login")
def spotify_login():
    scope = "user-read-currently-playing user-modify-playback-state"
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={scope}"
    )
    return redirect(auth_url)


# Call back route after Spotify login 
@spotify_bp.route("/callback")
def spotify_callback():
    global access_token, refresh_token

    code = request.args.get("code")

    if not code:
        return jsonify({"error": "No code returned from Spotify"}), 400

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers=get_auth_header(),
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Token exchange failed",
            "status": response.status_code,
            "body": response.text
        }), response.status_code

    token_data = response.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    return redirect(request.referrer )#or ('/'))


# Main API route
@spotify_bp.route("/api/spotify", methods=["GET"])
def get_spotify():

    # If not logged in yet
    if not access_token:
        return jsonify({
            "track": "Connect Spotify",
            "artist": """<button class="login" onclick= window.location.replace("/login");>Login</button>""",
            "albumArt": "static\images\spotify-image-placeholder.png",
            "isPlaying": False
        })

    # Request current playback 
    response = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers=get_bearer_header()
    )

    # This is when no song is playing 
    if response.status_code == 204:
        return jsonify({
            "track": "Nothing Playing",
            "artist": "",
            "albumArt": "https://via.placeholder.com/120",
            "isPlaying": False
        })

    # Token has expired
    if response.status_code == 401:
        if refresh_access_token():
            response = requests.get(
                "https://api.spotify.com/v1/me/player/currently-playing",
                headers=get_bearer_header()
            )
        else:
            return jsonify({
                "track": "Connect Spotify",
                "artist": "Login required",
                "albumArt": "static\images\spotify-image-placeholder.png",
                "isPlaying": False
            })

    # Handles any API errors
    if response.status_code != 200:
        return jsonify({
            "track": "Error",
            "artist": "Could not fetch",
            "albumArt": "static\images\spotify-image-placeholder.png",
            "isPlaying": False
        })

    data = response.json()
    item = data.get("item")

    # If nothing playing
    if not item:
        return jsonify({
            "track": "Nothing Playing",
            "artist": "",
            "albumArt": "static\images\spotify-image-placeholder.png",
            "isPlaying": data.get("is_playing", False)
        })

    # Artist name and art
    artists = ", ".join(artist["name"] for artist in item.get("artists", []))
    images = item.get("album", {}).get("images", [])
    album_art = images[0]["url"] if images else "https://via.placeholder.com/120"

    return jsonify({
        "track": item.get("name", "Unknown Track"),
        "artist": artists,
        "albumArt": album_art,
        "isPlaying": data.get("is_playing", False)
    })


@spotify_bp.route("/api/spotify/playpause", methods=["POST"])
def spotify_playpause():
    if not access_token:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    current = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers=get_bearer_header()
    )

    if current.status_code == 200 and current.json().get("is_playing"):
        endpoint = "https://api.spotify.com/v1/me/player/pause"
    else:
        endpoint = "https://api.spotify.com/v1/me/player/play"

    response = requests.put(endpoint, headers=get_bearer_header())

    return jsonify({
        "success": response.status_code in [200, 202, 204],
        "status": response.status_code
    })


@spotify_bp.route("/api/spotify/next", methods=["POST"])
def spotify_next():
    if not access_token:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    response = requests.post(
        "https://api.spotify.com/v1/me/player/next",
        headers=get_bearer_header()
    )

    return jsonify({
        "success": response.status_code in [200, 202, 204],
        "status": response.status_code
    })


@spotify_bp.route("/api/spotify/previous", methods=["POST"])
def spotify_previous():
    if not access_token:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    response = requests.post(
        "https://api.spotify.com/v1/me/player/previous",
        headers=get_bearer_header()
    )

    return jsonify({
        "success": response.status_code in [200, 202, 204],
        "status": response.status_code
    })