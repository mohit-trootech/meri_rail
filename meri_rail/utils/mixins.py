from django.utils.translation import gettext_lazy as _
from elasticsearch_dsl import Q

DOCUMENT_CLASS_REQUIRED = _("document_class is required")


class ElasticFilterMixin:
    document_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.document_class is None:
            raise ValueError(DOCUMENT_CLASS_REQUIRED)

    def get_search_term(self):
        """
        Get search term from request.
        """
        search_term = self.request.query_params.get("search")
        if search_term:
            return search_term
        return None

    def get_elastic_search_fields(self):
        """
        Get elasticsearch fields from document class.
        """
        return self.document_class.Django.fields

    def get_elastic_queryset(self, search_term):
        query = Q(
            "multi_match",
            query=search_term,
            fields=self.get_elastic_search_fields(),
            fuzziness="auto",
        )
        wildcard_query = Q(
            "bool",
            should=[
                Q("wildcard", **{field: "*{search_term.lower()}*"})
                for field in self.get_elastic_search_fields()
            ],
        )
        query = query | wildcard_query
        param_filters = list(self.request.query_params.values())
        filter_fields = self.document_class.Django.fields
        if len(param_filters) > 0:
            filters = []
            for field in filter_fields:
                if field in param_filters:
                    filters.append(Q("term", **{field: param_filters[field]}))
            filter_query = Q("bool", should=[query], filter=filters)
            query = query & filter_query
        return query

    def filter_queryset(self, queryset):
        """

        Filter queryset using elasticsearch.
        """
        return self.filter_queryset_by_elastic(queryset)

    def filter_queryset_by_elastic(self, queryset):
        """
        Filter queryset by elasticsearch.
        """
        search_term = self.get_search_term()
        if not search_term:
            return queryset
        query = self.get_elastic_queryset(search_term)
        search = self.document_class.search().query(query)
        return search.to_queryset()
