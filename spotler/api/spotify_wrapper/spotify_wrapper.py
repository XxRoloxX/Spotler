import datetime
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

redirect_uri = "http://localhost:3000"
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


class SpotifyWrapper:
    def __init__(self, **kwargs):
        self.code = kwargs.get("code", None)
        self.refresh_token = kwargs.get("refresh_token", None)

        if self.code and self.refresh_token:
            self.get_new_access_token()

        else:
            self.access_token = None
            self.state = generateRandomString(10)
            self.refresh_token = None
            self.expires_in = None

    def get_authorization_code(self):
        url = self.prepare_authorization_code_url(self.state)
        print(url)
        self.code = input("Paste authorization code: ")

    def get_refresh_token(self):
        """
        Sets refresh token and gets new access token
        return error if refresh token is not valid

        """
        post_json = {
            "grant_type": "authorization_code",
            "code": self.code,
            "redirect_uri": redirect_uri,
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
            print(response_json)
            self.refresh_token = response_json["refresh_token"]
            self.access_token = response_json["access_token"]
            self.expires_in = datetime.datetime.now() + datetime.timedelta(
                seconds=response_json["expires_in"]
            )
            return {"refresh_token": self.refresh_token}

        else:
            return {"error": f"Could not get refresh token. {response.reason}"}

    def get_new_access_token(self):
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
            print(response.reason)
            return {"error": f"Could not get new access token. {response.reason}"}
        else:
            response_json = response.json()
            self.access_token = response_json["access_token"]
            print(response_json)
            self.expires_in = datetime.datetime.now() + datetime.timedelta(
                seconds=response_json["expires_in"]
            )
            return {"access_token": self.access_token}

    def validate_refresh_token(self):
        new_token = self.get_new_access_token()
        if "error" in new_token:
            return False
        return True

    def auth_get(self, url, access_token):
        response = requests.get(
            url, headers={"Authorization": f"Bearer {access_token}"}, timeout=100
        )

        if response.ok:
            resp_json = response.json()
            return resp_json
        else:
            print("Auth_get exception: " + str(response.reason))
            raise Exception(response.reason, response.url)

    def refresh_token_if_needed(self):
        if (self.expires_in - datetime.datetime.now()).total_seconds() < 60:
            self.get_new_access_token()

    def getCurrentUserPlaylist(self):
        self.refresh_token_if_needed()
        resp_json = self.auth_get(
            SPOTIFY_GET_CURRENT_USER_PLAYLIST_URL, self.access_token
        )
        return resp_json

    def getUsersPlaylist(self, user_id, offset=0, limit=50):
        self.refresh_token_if_needed()
        resp_json = self.auth_get(
            self.get_user_playlists_url(user_id, offset, limit), self.access_token
        )
        return resp_json

    def getTracks(self, playlist_id):
        self.refresh_token_if_needed()
        resp_json = self.auth_get(
            SPOTIFY_GET_TRACKS_URL + playlist_id + "/tracks?offset=0", self.access_token
        )
        return resp_json

    def getTrack(self, track_id):
        self.refresh_token_if_needed()
        resp_json = self.auth_get(SPOTIFY_GET_TRACK_URL + track_id, self.access_token)
        return resp_json

    def getTrackFeatures(self, track_id):
        self.refresh_token_if_needed()
        try:
            resp_json = self.auth_get(
                SPOTIFY_GET_TRACK_FEATURES_URL + track_id, self.access_token
            )
            return resp_json
        except Exception as e:
            return {"status": "invalid track id"}

    def getArtistGenres(self, artist_id):
        self.refresh_token_if_needed()
        resp_json = self.auth_get(SPOTIFY_GET_ARTIST_URL + artist_id, self.access_token)
        if resp_json:
            return resp_json["genres"]
        else:
            return []

    def getTopTracks(self):
        self.refresh_token_if_needed()
        resp_json = self.auth_get(SPOTIFY_GET_TOP_TRACKS_URL, self.access_token)
        return resp_json

    def get_user_playlists_url(self, user_id, offset, limit):
        return f"https://api.spotify.com/v1/users/{user_id}/playlists?offset={offset}&limit={limit}"

    def prepare_authorization_code_url(self, state):
        url = "https://accounts.spotify.com/authorize?"
        url += urllib.parse.urlencode(
            {
                "response_type": "code",
                "client_id": CLIENT_ID,
                "scope": SCOPE,
                "redirect_uri": redirect_uri,
                "state": state,
            }
        )
        return url

    def track_search(self, track_name):
        self.refresh_token_if_needed()
        resp_json = self.auth_get(
            SPOTIFY_SEARCH_URL + f"?q={track_name}&type=track", self.access_token
        )
        return resp_json

    def simplified_tracks_search(self, track_name):

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

    def get_profile_info(self):
        self.refresh_token_if_needed()
        return self.auth_get(SPOTIFY_USER_PROFILE_INFO_URL, self.access_token)

def generateRandomString(n):
    res = "".join(random.choices(string.ascii_uppercase + string.digits, k=n))
    return res
