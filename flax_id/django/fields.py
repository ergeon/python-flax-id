from django.db.models import CharField

class FlaxId(CharField):
    """Django field to generate a simple flax id"""

    description = "Flax ID field"

    def __init__(self, *args, **kwargs):
        assert 'max_length' not in kwargs, ('FlaxID does not support custom'
                                            '`max_length`')
        kwargs['max_length'] = 16
        kwargs['blank'] = True
        kwargs['primary_key'] = True
        kwargs['editable'] = False
        super(FlaxId, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(FlaxId, self).deconstruct()
        del kwargs['max_length']
        kwargs['primary_key'] = True
        return name, path, tuple(), kwargs

    def formfield(self, **kwargs):
        return None
