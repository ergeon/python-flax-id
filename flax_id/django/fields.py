from django.db.models import CharField

from ..flax_id import get_flax_id


class FlaxId(CharField):
    """Django field to generate a simple flax id"""

    description = "Flax ID field"

    def __init__(self, *args, **kwargs):
        assert 'max_length' not in kwargs, ('FlaxID does not support custom'
                                            '`max_length`')
        kwargs['max_length'] = 16
        kwargs['null'] = kwargs.get('null', False)
        kwargs['blank'] = kwargs.get('blank', False)
        super(FlaxId, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(FlaxId, self).deconstruct()
        return name, path, tuple(), {'primary_key': True}

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None) or None
        if add and not value:
            value = get_flax_id()
            setattr(model_instance, self.attname, value)
        return value

