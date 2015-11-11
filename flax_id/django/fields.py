from django.db.models import CharField
from django.db.models import AutoField
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text
from django.utils.six import string_types
from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper

from django.utils import six

DatabaseWrapper.data_types['FlaxField'] = 'varchar(16)'


class FlaxId(AutoField, CharField):
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

    def get_internal_type(self):
        return "FlaxField"

    def formfield(self, **kwargs):
        return None

    def to_python(self, value):
        if isinstance(value, six.string_types) or value is None:
            return value
        return smart_text(value)

    def get_prep_value(self, value):
        value = super(CharField, self).get_prep_value(value)
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return value

    def contribute_to_class(self, cls, name, **kwargs):
        assert not cls._meta.has_auto_field, \
            "A model can't have more than one AutoField."
        super(FlaxId, self).contribute_to_class(cls, name, **kwargs)
        cls._meta.has_auto_field = True
        cls._meta.auto_field = self
