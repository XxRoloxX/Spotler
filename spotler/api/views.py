import io
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework import status
from django import http
from .classification.classifier_loader import ClassifiersLoader
from .data_collection.data_clean_up import fit_data_to_lda, get_most_popular_genres
from .data_collection.save_to_db import save_track_to_db
from .serializers import TrackFeaturesSerializer, TrackSerializer
from .models import Track, Genre
from .spotify_wrapper.spotify_wrapper import SpotifyWrapper
from .classification.classifier_trainer import ClassifierTrainer, GenreClassifierTrainer

# Create your views here.


# spotify_wrapper = SpotifyWrapper()
# spotify_wrapper.get_authorization_code()
# spotify_wrapper.get_refresh_token()
ACTIVE_CLASSIFIERS = ClassifiersLoader()


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
def retrieve_tracks_from_playlist(request, pk=None, *args, **kwargs):
    spotify_wrapper = SpotifyWrapper(
        code=request.session.get("code"),
        refresh_token=request.session.get("refresh_token"),
    )
    if "playlist_id" not in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    playlist_id = request.data["playlist_id"]

    tracks_data = [
        {
            "track_id": track["track"]["id"],
            "name": track["track"]["name"],
            "artists": track["track"]["artists"],
        }
        for track in spotify_wrapper.getTracks(playlist_id)["items"]
    ]

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

    number_of_classes = (
        0.1 if not request.GET.get("classes") else int(request.GET.get("classes"))
    )

    most_popular_genres = get_most_popular_genres(number_of_classes, "db.sqlite3")
    print(most_popular_genres)

    genres = Genre.objects.all()

    for genre in genres:
        simplified_genre = find_simplified_genre(genre.name, most_popular_genres)
        genre.simplyfied_name = simplified_genre
        genre.save()

    return Response(most_popular_genres)


@api_view(["GET"])
def fit_model(request, pk=None, *args, **kwargs):
    criteria = (
        0.1 if not request.GET.get("criteria") else float(request.GET.get("criteria"))
    )
    correctnes = fit_data_to_lda("db.sqlite3", criteria)
    return Response(correctnes)


@api_view(["GET"])
def test_endpoint(request, pk=None, *args, **kwargs):
    genre_classifier = GenreClassifierTrainer()
    genre_classifier.create_source_dataframe()
    genre_classifier.resample_set("LexicalUndersampling", 20)
    train_result = genre_classifier.train_model(request.GET.get("classifier"))
    # print(genre_classifier.classes)
    return Response(train_result)


@api_view(["GET"])
def track_genres(request, pk=None, *args, **kwargs):
    print("Code " + request.session["code"])

    spotler_wrapper = SpotifyWrapper(
        code=request.session["code"], refresh_token=request.session["refresh_token"]
    )

    track_id = request.GET.get("track_id")
    track_features = spotler_wrapper.getTrackFeatures(track_id)
    track_features_serializer = TrackFeaturesSerializer(data=track_features)
    if track_features_serializer.is_valid():
        active_classifier = ACTIVE_CLASSIFIERS.get_classifier_trainer(0)["model"]
        return Response(
            active_classifier.predict_proba_with_classes(
                track_features_serializer.validated_data
            )
        )

    return Response(
        {"status": track_features["status"]}, status=status.HTTP_404_NOT_FOUND
    )


@api_view(["POST"])
def authorize_with_spotify(request, *args, **kwargs):
    spotler_wrapper = SpotifyWrapper()

    if "code" not in request.data:
        return Response(
            {"status": "error", "message": "No code in request"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    spotler_wrapper.code = request.data["code"]
    response = spotler_wrapper.get_refresh_token()

    print(response)

    if "error" in response:
        return Response(
            {"error": response["error"]}, status=status.HTTP_401_UNAUTHORIZED
        )

    request.session["code"] = spotler_wrapper.code
    request.session["refresh_token"] = spotler_wrapper.refresh_token

    print("SESSION UPDATED")

    return Response({"status": "Authorized successfully"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def verify_cookies(request, pk=None, *args, **kwargs):
    if "code" not in request.session or "refresh_token" not in request.session:
        return Response({"cookie_status": False})

    spotify_wrapper = SpotifyWrapper(
        code=request.session["code"], refresh_token=request.session["refresh_token"]
    )
    response_status = spotify_wrapper.get_new_access_token()
    if "error" in response_status:
        return Response({"cookie_status": False})

    return Response({"cookie_status": True})


track_list_view = TracksListAPIView.as_view()
track_create_view = TrackCreateAPIView.as_view()
