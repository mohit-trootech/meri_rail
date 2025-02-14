from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from trains.models import Train, TrainDetail, Schedule, Route


@registry.register_document
class TrainDocument(Document):
    class Index:
        name = "trains"

    class Django:
        model = Train
        fields = ["name", "number"]
        related_models = [TrainDetail, Schedule, Route]

        def get_queryset(self):
            return (
                super(TrainDocument, self)
                .get_queryset()
                .select_related("details", "schedule")
                .prefetch_related("route")
            )

        def get_instances_from_related(self, related_instance):
            if isinstance(related_instance, TrainDetail):
                return related_instance.train
            elif isinstance(related_instance, Schedule):
                return related_instance.train
            elif isinstance(related_instance, Route):
                return related_instance.train
            return None
