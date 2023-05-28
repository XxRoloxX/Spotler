
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from .data_collection.data_clean_up import fit_data_to_lda, get_most_popular_genres
from .data_collection.save_to_db import save_track_to_db
from .spotifyWrapper import SpotifyWrapper
from .serializers import TrackSerializer
from .models import Track, Genre
from .spotifyWrapper import SpotifyWrapper
# Create your views here.


spotify_wrapper = SpotifyWrapper()
spotify_wrapper.get_authorization_code()
spotify_wrapper.get_refresh_token()


class TracksListAPIView(generics.ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class TrackCreateAPIView(generics.CreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def perform_create(self, serializer):

        track_id = serializer.validated_data.get("track_id")
        name = serializer.validated_data.get("name")

        if not Track.objects.filter(track_id=track_id).exists():
            serializer.save()

        else:
            print("Track already in db")


@api_view(["POST"])
def retrieveTracksFromPlaylistAPI(request, pk=None, *args, **kwargs):

    playlist_id = request.data["playlist_id"]

    print(playlist_id)

    tracks_data = [{"track_id": track["track"]["id"], "name":track["track"]["name"],
                    "artists":track["track"]["artists"]} for track in spotify_wrapper.getTracks(playlist_id)["items"]]

    response_list = []

    for track_item in tracks_data:
        response_list.append(save_track_to_db(track_item, spotify_wrapper))

    return Response(response_list)


@api_view(["GET"])
def cluster_genres_with_simplified_names(request, pk=None, *args, **kwargs):

    def find_simplified_genre(current_genre: str, list_of_popular_genres: list):
        for popular_genre in list_of_popular_genres:
            if popular_genre[0] in current_genre:
                return popular_genre[0]
        return None

    number_of_classes = 0.1 if not request.GET.get(
        'classes') else int(request.GET.get('classes'))

    most_popular_genres = get_most_popular_genres(
        number_of_classes, "db.sqlite3")
    print(most_popular_genres)

    genres = Genre.objects.all()

    for genre in genres:
        simplified_genre = find_simplified_genre(
            genre.name, most_popular_genres)
        genre.simplyfied_name = simplified_genre
        genre.save()

    return Response(most_popular_genres)


@api_view(["GET"])
def fit_model(request, pk=None, *args, **kwargs):

    criteria = 0.1 if not request.GET.get(
        'criteria') else float(request.GET.get('criteria'))
    correctnes = fit_data_to_lda('db.sqlite3', criteria)
    return Response(correctnes)


track_list_view = TracksListAPIView.as_view()
track_create_view = TrackCreateAPIView.as_view()
