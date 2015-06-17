from elasticsearch_dsl import field


class ImageField(field.String):
    def to_es(self, data):
        return str(data)
