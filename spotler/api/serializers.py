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

    model_name = serializers.SerializerMethodField('parse_model_name')

    def parse_model_name(self, model:ClassificationParameter):
      splited_model_name = model.serialized_model_path.split("/")[-1].split("_")
      
      if model.serialized_model_path.split("/")[-1][0]=="_":
          return splited_model_name[1]
          
      return splited_model_name[0]
    
    class Meta:
        model=ClassificationParameter
        exclude = ["serialized_model_path", "classes"]



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

class BasicSearchTrackInfoSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    image_url = serializers.CharField()
    preview_url = serializers.CharField()

