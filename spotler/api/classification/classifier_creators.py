from abc import ABCMeta, abstractmethod
from typing import Protocol
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (
    top_k_accuracy_score,
    make_scorer,
    balanced_accuracy_score,
    accuracy_score,
)


class ScikitModel(Protocol):
    def fit(self, X, y, sample_weight=None): ...
    def predict(self, X): ...
    def score(self, X, y, sample_weight=None): ...
    def set_params(self, **params): ...
    def predict_proba(self, X): ...


class OptimizedClassifierCreator(metaclass=ABCMeta):
    """
    Abstract Factory for optimized classification models
    """

    def _get_model_wrapped_in_pipeline(self, model, grid_parameters,scoring_strategy):
        """
        Default strategy for model optimization based on GridSearch and data standarization
        """
        return make_pipeline(
            StandardScaler(),
            GridSearchCV(
                model,
                param_grid=grid_parameters,
                scoring=scoring_strategy,
                )
            )

    @abstractmethod
    def create_optimized_model(self, scoring_strategy,grid_parameters)->"ScikitModel":
        """
        Abstract factory method for optimized models
        """

class RandomForestClassifierCreator(OptimizedClassifierCreator):
    """
    Optimized Random Forest Classifier model Factory
    """
    def create_optimized_model(self,scoring_strategy=make_scorer(balanced_accuracy_score),grid_parameters= {"n_estimators": [100, 300]})->"ScikitModel":
        return super()._get_model_wrapped_in_pipeline(RandomForestClassifier(),grid_parameters, scoring_strategy)
    
class LinearDiscriminantAnalysisCreator(OptimizedClassifierCreator):
    """
    Optimized Linear Discriminant Analysis model Factory
    """
    def create_optimized_model(self,scoring_strategy=make_scorer(balanced_accuracy_score), grid_parameters= {"n_components": [1, 12]})->"ScikitModel":
        return super()._get_model_wrapped_in_pipeline(LinearDiscriminantAnalysis(),grid_parameters,scoring_strategy)


CLASSIFIERS_CREATORS_MAP = {
    "LinearDiscriminantAnalysis": LinearDiscriminantAnalysisCreator(),
    "RandomForestClassifier": RandomForestClassifierCreator()
}


class ClassifierNotSupportedException(Exception):
    pass
