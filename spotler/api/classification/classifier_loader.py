from pathlib import Path
import pickle
from typing import List
from .classifier_trainer import ClassifierTrainer
from ..models import ClassificationParameter


class ClassifiersLoader:
    def __init__(self):
        print("Constructor is run")
        self.active_classifiers: List[ClassifierTrainer] = []
        self.__load_serialized_models()

    def __load_serialized_models(self):
        active_classifiers_info = ClassificationParameter.objects.filter(is_active=True)
        print("Started loading")
        print(active_classifiers_info)
        for classifier_info in active_classifiers_info:
            classifier_path = classifier_info.serialized_model_path
            with open(classifier_path, "rb") as file:
                if Path(classifier_path).exists():
                    print("Loaded model")
                    self.active_classifiers.append(
                        {
                            "model": pickle.load(file),
                            "parameters_id": active_classifiers_info.model.model_id,
                        }
                    )

    def get_classifier_trainer(self, index):
        """
        Returns classification model with id of its parameters in form of {"model":estimator, "parameters_id":id}
        """
        if index < 0 or index >= len(self.active_classifiers):
            raise IndexError

        return self.active_classifiers[index]
