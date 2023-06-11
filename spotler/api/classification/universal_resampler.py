from typing import Any, List
import pandas as pd
from .custom_resamplers.lexical_undersampling import LexicalUndersampling
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import EditedNearestNeighbours
import numpy as np

RESAMPLING_STRATEGIES_MAP = {
        "Undersampling": RandomUnderSampler,
        "Oversampling": RandomOverSampler,
        "NearestNeighbours": EditedNearestNeighbours,
        "LexicalUndersampling": LexicalUndersampling
    }


class UniversalResampler:
    """
    Universal Resampling Menager
    """

    def __init__(self):
        self.source_dataframe=None
        self.X_labels=[]
        self.Y_labels=[]

    def is_data_loaded_validation(self):
        if self.source_dataframe is None:
            raise SourceDataFrameIsNotLoaded("Original dataframe is not loaded. Load new data using load_dataframe() method.")
    def valid_resampling_strategy_validation(self, strategy_name:str):
        if strategy_name not in RESAMPLING_STRATEGIES_MAP:
                    raise ResamplingStrategyNotSupportedException(f"Resampling strategy: {strategy_name} is not supported. Available methods: "
                        + ", ".join(list(RESAMPLING_STRATEGIES_MAP.keys())))

    def load_dataframe(
        self, source_dataframe: pd.DataFrame, features_labels: List[str], classes_labels: List[str]
    ):
        self.source_dataframe = source_dataframe
        self.X_labels = features_labels
        self.Y_labels = classes_labels

    def __create_resampled_dataframe(self, features: List[Any], classes: List[Any]):
        combined_list = [
            np.concatenate([row_data, [row_class]]) for row_data, row_class in zip(features, classes)
        ]
        resampled_dataframe = pd.DataFrame(
            combined_list, columns=self.X_labels + self.Y_labels
        )
        
        return resampled_dataframe

    def __universal_resampling(self, resampling_strategy):
        features_res, classes_res = resampling_strategy.fit_resample(
            self.source_dataframe[self.X_labels].values,
            self.source_dataframe[self.Y_labels].values,
        )
        resampled_dataframe = self.__create_resampled_dataframe(features_res, classes_res)

        return resampled_dataframe
    
    def select_resampling_strategy(self, resampling_strategy_name, *resampling_parameters):
        self.is_data_loaded_validation()
        self.valid_resampling_strategy_validation(resampling_strategy_name)
        return self.__universal_resampling(RESAMPLING_STRATEGIES_MAP[resampling_strategy_name](*resampling_parameters))
    
    def resample_chain(self, resampling_strategies_names:List[str]):
        self.is_data_loaded_validation()
        resampled_set = original_set = self.source_dataframe
        for resampling_strategy in  resampling_strategies_names:
            self.valid_resampling_strategy_validation(resampling_strategy)
            resampled_set = self.__universal_resampling(resampling_strategy)
            self.source_dataframe = resampled_set

        self.source_dataframe = original_set
        return resampled_set


    def undersampling(self):
        self.is_data_loaded_validation()
        return self.__universal_resampling(RandomUnderSampler())
    
    def oversampling(self):
        self.is_data_loaded_validation()
        return self.__universal_resampling(RandomOverSampler())
    
    def nearest_neighbours(self):
        self.is_data_loaded_validation()
        return self.__universal_resampling(EditedNearestNeighbours())
    
    def lexical_undersampling(self, accepted_classes:int):
        self.is_data_loaded_validation()
        return self.__universal_resampling(LexicalUndersampling(accepted_classes))


class ResamplingStrategyNotSupportedException(Exception):
    pass

class SourceDataFrameIsNotLoaded(Exception):
    pass