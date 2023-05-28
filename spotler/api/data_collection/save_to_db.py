import traceback
from api.models import Genre, Track, Artist

from api.serializers import ArtistSerializer, GenreSerializer, TrackSerializer


def save_track_to_db(track_data: dict, api_wrapper):

    track_found = Track.objects.filter(track_id=track_data["track_id"]).first()

    if not track_found:
        try:
            track_features = api_wrapper.getTrackFeatures(
                track_data["track_id"])

            track_data.update(track_features)
            track_serializer = TrackSerializer(data=track_data)

           

            if not track_serializer.is_valid():
                raise Exception("Incorrect track data: "+str(track_serializer.errors))
            
            print("New Track: "+track_serializer.validated_data.get("name"))


            track_found = track_serializer.save()

            artists = [{"artist_id": artist["id"], "name":artist["name"]}
                       for artist in track_data["artists"]]

            for artist in artists:
                artist_found = save_artist_to_db(artist_id=artist["artist_id"], artist_name=artist["name"], spotify_wrapper=api_wrapper)
                track_found.artists.add(artist_found)

        except Exception as e:
            if track_found:
                track_found.delete()
            traceback.print_exc()
            print("Unexpected exception during track saving: "+str(e))

    else:
        print((f"Track with id {track_found.track_id} was already found!"))

    if track_found:
        return track_found.name


def save_artist_to_db(artist_id: str, artist_name: str, spotify_wrapper):

    artist_found = Artist.objects.filter(artist_id=artist_id).first()

    if not artist_found:
        try:
            artists_serializer = ArtistSerializer(data={"artist_id":artist_id, "name":artist_name})

            if not artists_serializer.is_valid():
                raise Exception("Incorrent Artist data: "+str(artists_serializer.errors))
            
            artist_found = artists_serializer.save()

            artist_genres = spotify_wrapper.getArtistGenres(
                    artists_serializer.validated_data["artist_id"])

            for genre in artist_genres:
                    
                found_genres = save_genre_to_db(genre)
                artist_found.genres.add(found_genres)

            return artist_found

        except Exception as exception:
            if artist_found:
                artist_found.delete()
            raise Exception("Unexpected exception during artist addition: "+str(exception) + " "+str(artists_serializer.validated_data))
        
    
    return artist_found

def save_genre_to_db(genre_name):

    genre_serializer = GenreSerializer(data={"name": genre_name})
    found_genres = Genre.objects.filter(name=genre_name).first()

    if not found_genres:
        if genre_serializer.is_valid():
            found_genres = genre_serializer.save()
            print("Found genre: "+str(found_genres.name))
        else:
            raise Exception("Incorrect genre name: "+str(genre_serializer.data))

    return found_genres
