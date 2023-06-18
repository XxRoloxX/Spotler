import datetime
from typing import Dict, List
import requests
import urllib.parse
import random
import string
import base64
import os

# Not used
USER_ID = "spotify"

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

REDIRECT_URI = "http://localhost:3000/spotify-redirect"

SCOPE = "user-read-private user-top-read playlist-read-collaborative"


SPOTIFY_GET_CURRENT_USER_PLAYLIST_URL = (
    "https://api.spotify.com/v1/me/playlists?limit=50"
)
SPOTIFY_GET_TRACKS_URL = "https://api.spotify.com/v1/playlists/"
SPOTIFY_GET_TRACK_URL = "https://api.spotify.com/v1/tracks/"
SPOTIFY_GET_ARTIST_URL = "https://api.spotify.com/v1/artists/"
SPOTIFY_GET_TRACK_FEATURES_URL = "https://api.spotify.com/v1/audio-features/"
SPOTIFY_GET_TOP_TRACKS_URL = (
    "https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=500&offset=0"
)
SPOTIFY_REFRESH_ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"

SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"

SPOTIFY_USER_PROFILE_INFO_URL = "https://api.spotify.com/v1/me"

AUTH_STATE_LENGTH = 10


class SpotifyWrapper:
    """ Wrapper for Spotify API """
    
    def __init__(self, **kwargs):
        self.code = kwargs.get("code", None)
        self.refresh_token = kwargs.get("refresh_token", None)

        if self.code and self.refresh_token:
            self.get_new_access_token()

        else:
            self.access_token = None
            self.state = generate_random_string(AUTH_STATE_LENGTH)
            self.refresh_token = None
            self.expires_in = None

    

    def get_refresh_token(self)->Dict[str, str]:
        """
        Sets refresh token and gets new access token
        return error if refresh token is not valid

        """
        post_json = {
            "grant_type": "authorization_code",
            "code": self.code,
            "redirect_uri": REDIRECT_URI,
        }
        headers = {
            "Authorization": "Basic "
            + base64.b64encode(
                (CLIENT_ID + ":" + CLIENT_SECRET).encode("ascii")
            ).decode("ascii"),
        }

        response = requests.post(
            SPOTIFY_REFRESH_ACCESS_TOKEN_URL,
            data=post_json,
            headers=headers,
            timeout=100,
        )

        if response.ok:
            response_json = response.json()
            self.refresh_token = response_json["refresh_token"]
            self.access_token = response_json["access_token"]
            self.expires_in = datetime.datetime.now() + datetime.timedelta(
                seconds=response_json["expires_in"]
            )
            return {"refresh_token": self.refresh_token}

        else:
            print(response.status_code)
            return {"error": f"Could not get refresh token. {response.reason}"}

    def get_new_access_token(self)->Dict[str, str]:
        """Get access token from refresh token. Returns error if refresh token is not valid.

        """
        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        headers = {
            "Authorization": "Basic "
            + base64.b64encode(
                (CLIENT_ID + ":" + CLIENT_SECRET).encode("ascii")
            ).decode("ascii"),
        }

        response = requests.post(
            SPOTIFY_REFRESH_ACCESS_TOKEN_URL, data=params, headers=headers, timeout=100
        )

        if not response.ok:
            return {"error": f"Could not get new access token. {response.reason}"}
        else:
            response_json = response.json()
            self.access_token = response_json["access_token"]
            self.expires_in = datetime.datetime.now() + datetime.timedelta(
                seconds=response_json["expires_in"]
            )
            return {"access_token": self.access_token}

    def validate_refresh_token(self)->bool:
        """Validate refresh token. Returns false if refresh token is not valid."""

        new_token = self.get_new_access_token()
        if "error" in new_token:
            return False
        return True

    def auth_get(self, url, access_token)->requests.Response:
        """Wrapper method to get data from Spotify API. 
        Appends Authorization header to the request to provided url.
        Returns an requests Reponse object. Data from Response is stored in .data attribute."""

        response = requests.get(
            url, headers={"Authorization": f"Bearer {access_token}"}, timeout=100
        )

        if response.ok:
            resp_json = response.json()
            return resp_json
        else:
            return {"error": f"Could not get {url}. {response.reason}"}

    def refresh_token_if_needed(self)->None:
        """Refreshes access token if it has expired."""

        if (self.expires_in - datetime.datetime.now()).total_seconds() < 60:
            self.get_new_access_token()

    def get_current_user_playlists(self)->requests.Response:

        """Returns current user's playlists from endpoint: /playlists. Return is a requests Reponse object. 
        Data from Response is stored in .data attribute."""


        self.refresh_token_if_needed()
        resp_json = self.auth_get(
            SPOTIFY_GET_CURRENT_USER_PLAYLIST_URL, self.access_token
        )

        return resp_json

    def get_user_playlists(self, user_id:str, offset=0, limit=50)->requests.Response:

        """Returns user's playlists from endpoint: /users/{user_id}/playlists. 
        Return is a requests Reponse object. Data from Response is stored in .data attribute."""

        self.refresh_token_if_needed()
        resp_json = self.auth_get(
            self.get_user_playlists_url(user_id, offset, limit), self.access_token
        )
        return resp_json

    def get_tracks(self, playlist_id:str)->requests.Response:
        """Returns all tracks in a playlist from endpoint: /users/{user_id}/playlists/{playlist_id}/"""

        self.refresh_token_if_needed()
        resp_json = self.auth_get(
            SPOTIFY_GET_TRACKS_URL + playlist_id + "/tracks?offset=0", self.access_token
        )
        return resp_json

    def get_track(self, track_id:str)->requests.Response:
        """Returns detailed information about a track from endpoint :/tracks/{track_id}"""

        self.refresh_token_if_needed()
        resp_json = self.auth_get(SPOTIFY_GET_TRACK_URL + track_id, self.access_token)
        return resp_json

    def get_track_features(self, track_id:str)->requests.Response:
        """Returns tracks metadata from endpoint: /tracks/{track_id}/features"""

        self.refresh_token_if_needed()
        resp_json = self.auth_get(
            SPOTIFY_GET_TRACK_FEATURES_URL + track_id, self.access_token
        )
        return resp_json
        

    def get_artists_genres(self, artist_id:str)->List[str]:

        """Returns artists genres from endpoint: /artists/{artist_id}"""

        self.refresh_token_if_needed()
        resp_json = self.auth_get(SPOTIFY_GET_ARTIST_URL + artist_id, self.access_token)
        if resp_json:
            return resp_json["genres"]
        else:
            return []

    def get_top_tracks(self)->requests.Response:
        """Returns top tracks from endpoint: /me/top/tracks"""
        self.refresh_token_if_needed()
        resp_json = self.auth_get(SPOTIFY_GET_TOP_TRACKS_URL, self.access_token)
        return resp_json

    def get_user_playlists_url(self, user_id:str, offset:int, limit:int)->str:
        return f"https://api.spotify.com/v1/users/{user_id}/playlists?offset={offset}&limit={limit}"

    def prepare_authorization_code_url(self, state:str)->str:
        """Creates redirect url for authorization code flow"""
        url = "https://accounts.spotify.com/authorize?"
        url += urllib.parse.urlencode(
            {
                "response_type": "code",
                "client_id": CLIENT_ID,
                "scope": SCOPE,
                "redirect_uri": REDIRECT_URI,
                "state": state,
            }
        )
        return url

    def track_search(self, track_name:str)->requests.Response:
        """Search for a track from Spotify"""
        self.refresh_token_if_needed()
        resp_json = self.auth_get(
            SPOTIFY_SEARCH_URL + f"?q={track_name}&type=track", self.access_token
        )
        return resp_json

    def simplified_tracks_search(self, track_name:str)->requests.Response:

        """
        Get simplified info for a track, returns contains: name, id, preview_url, image_url
        """
        searched_tracks = self.track_search(track_name)

        return [
            {
                "name": track["name"],
                "id": track["id"],
                "preview_url": track["preview_url"],
                "image_url": track["album"]["images"][0]["url"],
            }
            for track in searched_tracks["tracks"]["items"]
        ]

    def get_profile_info(self)->requests.Response:

        """Returns user's profile info from endpoint: /me"""
        self.refresh_token_if_needed()
        return self.auth_get(SPOTIFY_USER_PROFILE_INFO_URL, self.access_token)
    

    def get_authorization_code(self)->None:
            """Prompts user to set authorization code"""
            url = self.prepare_authorization_code_url(self.state)
            print(url)
            self.code = input("Paste authorization code: ")


def generate_random_string(n:int)->str:
    """Generates random string of length n"""
    res = "".join(random.choices(string.ascii_uppercase + string.digits, k=n))
    return res
