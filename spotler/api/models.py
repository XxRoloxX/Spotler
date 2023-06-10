from django.db import models
from jsonfield import JSONField


# Create your models here.

class Genre(models.Model):
    """
    Name of genres
    """
    name = models.CharField(max_length=70, unique=True)
    simplyfied_name = models.CharField(max_length=70, null=True, blank=True)

class Artist(models.Model):
    """
    Basic info about artist
    """
    artist_id = models.CharField(max_length=70, unique=True,primary_key=True)
    name = models.CharField(max_length=70)
    genres = models.ManyToManyField(Genre)


class TrackFeatures(models.Model):
    """
    Details about tracks' audio features
    """

    acousticness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    danceability = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    energy = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    instrumentalness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    key = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    liveness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    loudness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    liveness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    mode = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    speechiness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    tempo = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    time_signature = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    valence = models.DecimalField(max_digits=15, decimal_places=10, default=0)


class Track(models.Model):
    """
    Basic track info
    """
    track_id = models.CharField(max_length=70,primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    artists = models.ManyToManyField(Artist)
    acousticness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    danceability = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    energy = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    instrumentalness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    key = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    liveness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    loudness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    liveness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    mode = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    speechiness = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    tempo = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    time_signature = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    valence = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    
class ClassificationModel(models.Model):
    model_id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=70, unique=True)

class ClassificationParamter(models.Model):
    parameters_id = models.AutoField(primary_key=True)
    model_id = models.ForeignKey(ClassificationModel, on_delete=models.CASCADE)
    parameters = JSONField()

