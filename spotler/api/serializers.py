from rest_framework import serializers
from .models import ClassificationModel, ClassificationParameter, Track, Artist, Genre

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
        
class ClassificationModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClassificationModel
        fields = "__all__"


class ClassificationParameterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ClassificationParameter
        fields = '__all__'
TRACK_METADATA_KEYS = [
    "acousticness",
    "danceability",
    "energy",
    "instrumentalness",
    "key",
    "loudness",
    "liveness",
    "mode",
    "speechiness",
    "tempo",
    "time_signature",
    "valence",
]

class TrackFeaturesSerializer(serializers.Serializer):
    acousticness = serializers.FloatField()
    danceability = serializers.FloatField()
    energy = serializers.FloatField()
    instrumentalness = serializers.FloatField()
    key = serializers.FloatField()
    loudness = serializers.FloatField()
    liveness = serializers.FloatField()
    mode = serializers.FloatField()
    speechiness = serializers.FloatField()
    tempo = serializers.FloatField()
    time_signature = serializers.FloatField()
    valence = serializers.FloatField()

