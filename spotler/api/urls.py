from django.urls import path
from . import views


urlpatterns = [
    path('playlist', views.retrieve_tracks_from_playlist),
    path('test', views.train_model),
    path('track-genres', views.track_genres),
    path('authorize-with-spotify', views.authorize_with_spotify),
    path('verify-cookies', views.verify_cookies),
    path('search-tracks', views.search_tracks),
    path('profile-info', views.profile_info),
    path('delete-cookies', views.delete_cookies),
]