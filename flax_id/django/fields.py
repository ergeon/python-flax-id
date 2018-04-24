from django.db.models import CharField

from ..flax_id import get_flax_id


class FlaxId(CharField):
    """Django field to generate a simple flax id"""

    description = 'Flax ID field'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 16
        kwargs['editable'] = kwargs.get('editable', False)
        kwargs['blank'] = kwargs.get('blank', False)
        kwargs['null'] = kwargs.get('null', False)
        kwargs['unique'] = kwargs.get('unique', True)
        self._auto_generate = kwargs.pop('auto_generate', True)
        super(FlaxId, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if self._auto_generate and add and not value:
            value = get_flax_id()
            setattr(model_instance, self.attname, value)
        return value

    def formfield(self, **kwargs):
        return None
