from typing import Any, List, Tuple

import numpy as np



class LexicalUndersampling:
    """
    Undersampling based on lexical analysis of classes. 
    Objects with classes that have one of the most popular classes as substring, are replaced with this simplified class.
    Objects with classes that don't have most popular classes as substrings are ignored.
    
    """

    def __init__(self,accepted_classes:int):
        self.accepted_classes = accepted_classes


    def __get_most_popular_classes(self,classes_list:List[Any]):
        unique, counts = np.unique(np.array(classes_list), return_counts=True)
        unique_count = list(zip(unique, counts))      
        unique_count.sort(key=lambda item: item[1], reverse=True)
        most_popular_classes = list(map(lambda unique: unique[0], unique_count[:self.accepted_classes]))
        return most_popular_classes
    


    def fit_resample(self, features_list:List[List[Any]], classes_list:List[Any])->Tuple[List[Any], List[Any]]:
        """
        Return resampled set, as tuple (features, classes)
        """
        result_features = []
        result_classes = []

        most_popular_classes = self.__get_most_popular_classes(classes_list)

        for features, actual_class in zip(features_list, classes_list):
            simpified_class = list(filter(lambda accepted_class: accepted_class in actual_class, most_popular_classes))
            if simpified_class:
                result_features.append(features)
                result_classes.append(simpified_class[0])

        return result_features, result_classes
        