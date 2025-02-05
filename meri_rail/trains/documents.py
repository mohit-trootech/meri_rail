from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from trains.models import Train


@registry.register_document
class TrainDocument(Document):
    class Index:
        name = "trains"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Train
        fields = ["name", "number"]
        related_models = [Train]
