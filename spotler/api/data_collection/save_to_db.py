import traceback
from api.models import Genre, Track, Artist

from api.serializers import ArtistSerializer, GenreSerializer, TrackSerializer
from ..spotify_wrapper.spotify_wrapper import SpotifyWrapper


def save_track_to_db(track_data: dict, api_wrapper: SpotifyWrapper) -> str:
    """Adds track to database based on single track data from endpoint /playlist/tracks."""

    track_found = Track.objects.filter(track_id=track_data["track_id"]).first()

    if track_found:
        print((f"Track with id {track_found.track_id} was already found!"))
        return track_found.name

    print("Adding track: " + str(track_data["name"]))
    try:
        track_features = api_wrapper.get_track_features(track_data["track_id"])

        track_data.update(track_features)
        track_serializer = TrackSerializer(data=track_data)

        if not track_serializer.is_valid():
            raise ValueError("Incorrect track data: " + str(track_serializer.errors))

        print("New Track: " + track_serializer.validated_data.get("name"))

        track_found = track_serializer.save()

        artists = [
            {"artist_id": artist["id"], "name": artist["name"]}
            for artist in track_data["artists"]
        ]

        for artist in artists:
            artist_found = save_artist_to_db(
                artist_id=artist["artist_id"],
                artist_name=artist["name"],
                spotify_wrapper=api_wrapper,
            )
            track_found.artists.add(artist_found)
        return track_found.name

    except ValueError as exception:
        if track_found:
            track_found.delete()

        traceback.print_exc()
        print("Unexpected exception during track saving: " + str(exception))


def save_artist_to_db(
    artist_id: str, artist_name: str, spotify_wrapper: SpotifyWrapper
):
    """Adds artist to database based on single artist with artist_id, artist_name"""
    artist_found = Artist.objects.filter(artist_id=artist_id).first()

    if artist_found:
        print((f"Artist with id {artist_found.artist_id} was already found!"))
        return artist_found
    
    print("Adding artist: " + str(artist_name))

    try:
        artists_serializer = ArtistSerializer(
            data={"artist_id": artist_id, "name": artist_name}
        )

        if not artists_serializer.is_valid():
            raise ValueError("Incorrent Artist data: " + str(artists_serializer.errors))

        artist_found = artists_serializer.save()

        artist_genres = spotify_wrapper.get_artists_genres(
            artists_serializer.validated_data["artist_id"]
        )

        for genre in artist_genres:
            found_genres = save_genre_to_db(genre)
            artist_found.genres.add(found_genres)

        return artist_found

    except ValueError as exception:
        if artist_found:
            artist_found.delete()

        raise ValueError(
            "Unexpected exception during artist addition: "
            + str(exception)
            + " "
            + str(artists_serializer.validated_data)
        ) from exception


def save_genre_to_db(genre_name: str) -> Genre:
    """Add a genre to database based on genre name"""

    genre_serializer = GenreSerializer(data={"name": genre_name})
    found_genres = Genre.objects.filter(name=genre_name).first()

    print("Adding genre: " + str(found_genres))
    if not found_genres:
        if genre_serializer.is_valid():
            found_genres = genre_serializer.save()
            print("Found genre: " + str(found_genres.name))
        else:
            raise ValueError("Incorrect genre name: " + str(genre_serializer.data))

    return found_genres
