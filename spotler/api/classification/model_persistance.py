from pathlib import Path
import pickle
import datetime

from sklearn.metrics import balanced_accuracy_score

from ..serializers import ClassificationParameterSerializer
from ..models import ClassificationModel, ClassificationParameter


PICKED_MODELS_DIR = str(Path(__file__).parent.absolute()) + "/pickled_models/"


def create_filestamp(model_name):
    return model_name + "_" + datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S:%f")


def pickle_model(train_function):
    """
    Decorator for models training functions. Saves created coefficient to database
    """

    def inner_train_function(classifier, *args, **kwargs):
        train_result = train_function(classifier, *args, **kwargs)

        classification_model, _ = ClassificationModel.objects.get_or_create(
            model_name=classifier.name
        )

        serialized_model_path = PICKED_MODELS_DIR + create_filestamp(classifier.name)

        with open(serialized_model_path, "wb") as file:
            pickle.dump(classifier, file)

        created_model = ClassificationParameter.objects.create(
            model=classification_model,
            serialized_model_path=serialized_model_path,
            balanced_accuracy_score=classifier.score_model_on_balanced_accuracy().mean(),
            accuracy_score=classifier.score_model_on_mean_accuracy().mean(),
            top_k_accuracy_score=classifier.score_model_on_top_k_accuracy().mean(),
        )

        return ClassificationParameterSerializer(created_model).data

    return inner_train_function
