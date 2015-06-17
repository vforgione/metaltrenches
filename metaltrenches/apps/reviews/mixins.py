from django.utils import timezone
from elasticsearch_dsl.filter import Term, Range, MatchAll, Nested, Missing


class Searchable(object):
    """adds a search method to the object to allow for es querying
    """

    @staticmethod
    def _build_filter(filters):
        f = MatchAll()

        for key, value in filters.items():
            if key == "status":
                now = timezone.now()
                if value == "published":
                    f &= Range(published={"lte": now})
                elif value == "scheduled":
                    f &= Range(published={"gte": now})
                elif value == "draft":
                    f &= Missing(field="published")
                else:
                    raise Exception("status meta values must be 'published', 'scheduled' or 'draft'")

            elif "." in key:
                path = key.split(".")[0]
                f &= Nested(path=path, filter=Term(**{key: value}))

            else:
                f &= Term(**{key: value})

        return f

    @classmethod
    def search(cls, query=None, filters=None):
        qs = cls.search_objects.search()

        # build filters
        if filters:
            built_filters = cls._build_filter(filters)
            qs = qs.filter(built_filters)

        # build query
        if query:
            qs = qs.query("match", _all=query)

        # raise Exception(qs.to_dict())

        # done
        return qs
