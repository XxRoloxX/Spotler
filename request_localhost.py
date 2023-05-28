
from spotler.api.spotifyWrapper import SpotifyWrapper
import requests
import sys
USER_ID = 'spotify'
LOCAL_URL = "http://localhost:3000/api/playlist"


def post_playlist_ids(user_id, wrapper,offset=0,limit=50):

    try:
        with open("demofile2.txt", "a") as file:
            while True:
                current_playlists = wrapper.getUsersPlaylist(USER_ID,offset,limit)["items"]
                for indx, current_playlist in enumerate(current_playlists):
                    response = requests.post(LOCAL_URL, json={"playlist_id":current_playlist["id"]})
                    print(response)
                    current_playlist_analyzed = "Offset "+ str(offset+indx)+ "| Id: "+current_playlist["id"]+" | Name: "+current_playlist["name"]+"\n"
                    file.write(current_playlist_analyzed)
                    print(current_playlist_analyzed)
                offset+=limit
    
    except Exception as error:
        print(error)


if __name__=="__main__":
    wrapper = SpotifyWrapper()
    wrapper.get_authorization_code()
    print(wrapper.get_refresh_token())
    print(wrapper.get_new_access_token())
    post_playlist_ids(USER_ID, wrapper, int(sys.argv[1]))
    