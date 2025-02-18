from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from stations.models import Station, Utterance


@registry.register_document
class StationDocument(Document):
    class Index:
        name = "stations"

    class Django:
        model = Station
        fields = [
            "name",
            "code",
            "name_hi",
        ]
        related_models = [Utterance]

        def get_queryset(self):
            return super().get_queryset().select_related("district", "state")

        def get_instances_from_related(self, related_instance):
            if isinstance(related_instance, Utterance):
                return related_instance.station
            return None
