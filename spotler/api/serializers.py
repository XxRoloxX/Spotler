from rest_framework import serializers
from .models import Track, Artist, TrackFeatures, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]

class ArtistSerializer(serializers.ModelSerializer):
    #genres = GenreSerializer(read_only=False, many=True)
    #genres = serializers.PrimaryKeyRelatedField(queryset = Genre.objects.all())
    class Meta:
        model = Artist
        fields = ["artist_id", "name"]
       

class TrackFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackFeatures
        fields = "__all__"

   



class TrackSerializer(serializers.ModelSerializer):
    
    #features = serializers.PrimaryKeyRelatedField(queryset = TrackFeatures.objects.all())

    class Meta:
        model = Track
        fields = ["track_id", 
                  "name", 
                  "acousticness",
                  "danceability",
                  "energy",
                  "instrumentalness",
                  "key",
                  "liveness",
                  "loudness",
                  "liveness",
                  "mode",
                  "speechiness",
                  "tempo",
                  "time_signature",
                  "valence"
                  ]
        



