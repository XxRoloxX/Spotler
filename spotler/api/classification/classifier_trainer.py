import abc
import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.metrics import balanced_accuracy_score, make_scorer, top_k_accuracy_score
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.pipeline import make_pipeline

from .parameters_persitance import save_parameters
from .classifier_creators import (
    CLASSIFIERS_CREATORS_MAP,
    ClassifierNotSupportedException,
    OptimizedClassifierCreator,
    ScikitModel,
)
from .universal_resampler import UniversalResampler
from ..models import Track
from abc import ABCMeta, abstractmethod


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
GENRE_KEY = "genre"


class ClassifierTrainer(metaclass=ABCMeta):

    """
    Universal Creator and Trainer of Classifiers
    """

    def __init__(self):
        self.source_dataframe = pd.DataFrame()
        self.classifier: ScikitModel = None
        self.resampler = UniversalResampler()
        self.features_labels = []
        self.classes_labels = []


    def update_state_after_loading_data(self, features_labels, classes_labels):
        """
        Execute this method inside create_source_dataframe, after self.source_dataframe is loaded
        """
        self.resampler.load_dataframe(self.source_dataframe, features_labels, classes_labels)
        self.features_labels = features_labels
        self.classes_labels = classes_labels

    # def loading_data_decorator(self, loading_function):
    #     def decorated_loading_function(self, features_labels, classes_labels):
    #         loading_function(self, features_labels, classes_labels)
    #         self.resampler.load_dataframe(self.source_dataframe)
    #         self.features_labels = features_labels
    #         self.classes_labels = classes_labels

    #     return decorated_loading_function

    def is_classifier_loaded_validation(self):
        if not self.classifier:
            raise ClassifierNotLoadedException(
                "Classifier is not loaded. Load classifier using train_model()."
            )

    def is_classifier_supported_validation(self, classifier_name):
        if classifier_name not in CLASSIFIERS_CREATORS_MAP:
            raise ClassifierNotSupportedException(
                f"Classifier {classifier_name} is not supported. Available classifiers: "
                + ", ".join(list(CLASSIFIERS_CREATORS_MAP.keys()))
            )

    @property
    def datasource_length(self):
        """
        Return number of rows of current dataset
        """
        return self.source_dataframe.shape[0]

    @abc.abstractmethod
    def create_source_dataframe(self, features_labels, classes_labels):
        ...

    def get_model_parameters(self):
        self.is_classifier_loaded_validation()
        return {
            "coef": self.classifier.coef_,
            "intercept": self.classifier.intercept_.tolist(),
        }
    
    @save_parameters
    def train_model(
        self, model_name: str, scoring_strategy=make_scorer(balanced_accuracy_score)
    ):
        """
        Create and train model with provided scoring strategy
        """
        model_factory = self.__get_model_factory(model_name)
        self.classifier = model_factory.create_optimized_model(scoring_strategy)
        self.classifier.fit(
            self.source_dataframe[self.features_labels].values,
            self.source_dataframe[self.classes_labels].values.ravel(),
        )

    def score_model(self):
        self.is_classifier_loaded_validation()
        return cross_val_score(self.classifier,
                                self.source_dataframe[self.features_labels].values,
                                self.source_dataframe[self.classes_labels].values.ravel(),
                               scoring=make_scorer(top_k_accuracy_score, k=3, needs_proba=True) )
    

    def resample_set(self, resampling_strategy_name: str, *resampling_strategy_parameters):
        """
        Replace source dataframe with resampled dataframe accoringly to resampling_strategy_name
        """
        self.source_dataframe = self.resampler.select_resampling_strategy(
            resampling_strategy_name,
            *resampling_strategy_parameters
        )

    def __get_model_factory(self, model_name: str) -> OptimizedClassifierCreator:
        self.is_classifier_supported_validation(model_name)
        return CLASSIFIERS_CREATORS_MAP[model_name]
    


class ClassifierNotLoadedException(Exception):
    pass


class GenreClassifierTrainer(ClassifierTrainer):


    def create_source_dataframe(
        self, features_labels=TRACK_METADATA_KEYS, classes_labels=[GENRE_KEY]
    ):
        """
        Load tracks metadata and genres from database
        """
        tracks_with_genres_query = Track.objects.all().prefetch_related(
            "artists__genres"
        )
        track_genres_dict = {}

        for track in tracks_with_genres_query:
            for artist in track.artists.all():
                for genre in artist.genres.all():
                    for feature_label in features_labels:
                        track_genres_dict.setdefault(feature_label, []).append(
                            getattr(track, feature_label)
                        )
                    track_genres_dict.setdefault(classes_labels[0], []).append(
                        getattr(genre, "name")
                    )

        self.source_dataframe = pd.DataFrame(track_genres_dict)
        self.update_state_after_loading_data(features_labels,classes_labels)
