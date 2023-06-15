from django.urls import path
from . import views


urlpatterns = [
    path('list',views.track_list_view),
    path('create',views.track_create_view),
    path('playlist', views.retrieveTracksFromPlaylistAPI),
    path('cluster', views.cluster_genres_with_simplified_names),
    path('model', views.fit_model),
    path('test', views.test_endpoint),
    path('classify_test', views.classify_track),
    path('auth', views.authorize)

]