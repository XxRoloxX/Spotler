from django.urls import path
from . import views


urlpatterns = [
    path('list',views.track_list_view),
    path('create',views.track_create_view),
    path('playlist', views.retrieve_tracks_from_playlist),
    path('cluster', views.cluster_genres_with_simplified_names),
    path('model', views.fit_model),
    path('test', views.test_endpoint),
    path('track-genres', views.track_genres),
    path('authorize-with-spotify', views.authorize_with_spotify),
    path('verify-cookies', views.verify_cookies)
]