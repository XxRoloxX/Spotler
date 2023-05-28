
import requests
import urllib.parse 

#Not used
USER_ID = 'spotify'

CLIENT_ID='1887458e0b984c799d0b33b320fbf25e'
CLIENT_SECRET = ''
redirect_uri='http://localhost:3000'
SCOPE='user-read-private user-top-read playlist-read-collaborative'

#Your access token
SPOTIFY_ACCESS_TOKEN="BQD_TiIlkAgyNxPXKI-5RsxPs6sSCkvvSk7c-1XKw7b7yC5m0jvEgLUYo_5uKdxg_b9d74GZcJBpKeXhQyVLzwSyjlbiaCU3nd1p-k6sUgomgP7DBtPEh-peXDb1bKedMh_mjcs0C0rDc7prpsY97294Uq6A2mmNvK4O6cpruI0kaTk_-SoumyPraROCoPYiA_zLpFAbKfKEAjSGvKjvOg"

#Not used
SPOTIFY_GET_PLAYLIST_URL=f"https://api.spotify.com/v1/users/{USER_ID}/playlists?offset=0&limit=50"

def get_user_playlists_url(user_id, offset, limit):
    return f"https://api.spotify.com/v1/users/{user_id}/playlists?offset={offset}&limit={limit}"


SPOTIFY_GET_CURRENT_USER_PLAYLIST_URL="https://api.spotify.com/v1/me/playlists?limit=50"
SPOTIFY_GET_TRACKS_URL="https://api.spotify.com/v1/playlists/"
SPOTIFY_GET_TRACK_URL="https://api.spotify.com/v1/tracks/"
SPOTIFY_GET_ARTIST_URL="https://api.spotify.com/v1/artists/"
SPOTIFY_GET_TRACK_FEATURES_URL="https://api.spotify.com/v1/audio-features/"
SPOTIFY_GET_TOP_TRACKS_URL="https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=500&offset=0"
SPOTIFY_REFRESH_ACCESS_TOKEN_URL = "https://api.spotify.com/v1/api/token"




def auth_get(url,access_token):

    response = requests.get(url,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
        )
    resp_json = response.json()

    return resp_json

def getCurrentUserPlaylist(access_token):

    resp_json = auth_get(SPOTIFY_GET_CURRENT_USER_PLAYLIST_URL,access_token)
    return resp_json

def getUsersPlaylist(user_id, access_token, offset=0, limit=50):
    resp_json = auth_get(get_user_playlists_url(user_id, offset, limit),access_token)
    return resp_json

def getTracks(playlist_id, access_token):
    resp_json = auth_get(SPOTIFY_GET_TRACKS_URL+playlist_id+"/tracks?offset=0",access_token)
    #pprint.pprint(resp_json)
    return resp_json

def getTrack(track_id, access_token):
    resp_json = auth_get(SPOTIFY_GET_TRACK_URL+track_id,access_token)
    return resp_json
def getTrackFeatures(track_id, access_token):
    resp_json=auth_get(SPOTIFY_GET_TRACK_FEATURES_URL+track_id,access_token)
    return resp_json

def getArtistGenres(artist_id,access_token):
    resp_json = auth_get(SPOTIFY_GET_ARTIST_URL+artist_id,access_token)
    return resp_json["genres"]
def getTopTracks(access_token):
    resp_json=auth_get(SPOTIFY_GET_TOP_TRACKS_URL, access_token)
    return resp_json
def prepareUrl():
    url='https://accounts.spotify.com/authorize'
    url+='?response_type=token&'
    url+=urllib.parse.urlencode({'client_id':CLIENT_ID,'scope': SCOPE,'redirect_uri':redirect_uri  })
    return url
def prepareAuthorizationCodeUrl(state):
    url='https://accounts.spotify.com/authorize?'
    url+=urllib.parse.urlencode({'response-type':'code','client_id':CLIENT_ID,'scope': SCOPE,'redirect_uri':redirect_uri  })
    return url


#print(prepareUrl())

#https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=f8275e36fb254e69
PLAYLIST_ID  = "37i9dQZF1DXcBWIGoYBM5M"
{"playlist_id": "37i9dQZF1DXcBWIGoYBM5M"}

#{"playlist_id":"37i9dQZF1DXcBWIGoYBM5M"}

#print(prepareUrl())

#print(getTracks(PLAYLIST_ID, SPOTIFY_ACCESS_TOKEN))
#response = getUsersPlaylist(None,SPOTIFY_ACCESS_TOKEN)
#print(response)

def post_playlist_ids(user_id, access_token):
    offset=0
    limit=50
    localurl = "http://localhost:3000/api/playlist"
    try:
        while True:
            current_playlists = getUsersPlaylist(USER_ID, SPOTIFY_ACCESS_TOKEN,offset,limit)["items"]
            for current_playlist in current_playlists:
                response = requests.post(localurl, json={"playlist_id":current_playlist["id"]})
                print(response)
            offset+=limit
    
    except Exception as error:
        print(error)

if __name__=="__main__":
    post_playlist_ids(USER_ID, SPOTIFY_ACCESS_TOKEN)

