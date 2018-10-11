# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Model classes for datastore objects and properties for models."""


from google.cloud.ndb import _exceptions
from google.cloud.ndb import key as key_module


__all__ = [
    "Key",
    "BlobKey",
    "GeoPt",
    "Rollback",
    "KindError",
    "InvalidPropertyError",
    "BadProjectionError",
    "UnprojectedPropertyError",
    "ReadonlyPropertyError",
    "ComputedPropertyError",
    "IndexProperty",
    "Index",
    "IndexState",
    "ModelAdapter",
    "make_connection",
    "ModelAttribute",
    "Property",
    "ModelKey",
    "BooleanProperty",
    "IntegerProperty",
    "FloatProperty",
    "BlobProperty",
    "TextProperty",
    "StringProperty",
    "GeoPtProperty",
    "PickleProperty",
    "JsonProperty",
    "UserProperty",
    "KeyProperty",
    "BlobKeyProperty",
    "DateTimeProperty",
    "DateProperty",
    "TimeProperty",
    "StructuredProperty",
    "LocalStructuredProperty",
    "GenericProperty",
    "ComputedProperty",
    "MetaModel",
    "Model",
    "Expando",
    "transaction",
    "transaction_async",
    "in_transaction",
    "transactional",
    "transactional_async",
    "transactional_tasklet",
    "non_transactional",
    "get_multi_async",
    "get_multi",
    "put_multi_async",
    "put_multi",
    "delete_multi_async",
    "delete_multi",
    "get_indexes_async",
    "get_indexes",
]


Key = key_module.Key
BlobKey = NotImplemented  # From `google.appengine.api.datastore_types`
GeoPt = NotImplemented  # From `google.appengine.api.datastore_types`
Rollback = _exceptions.Rollback


class KindError(_exceptions.BadValueError):
    """Raised when an implementation for a kind can't be found.

    May also be raised when the kind is not a byte string.
    """


class InvalidPropertyError(_exceptions.Error):
    """Raised when a property is not applicable to a given use.

    For example, a property must exist and be indexed to be used in a query's
    projection or group by clause.
    """


BadProjectionError = InvalidPropertyError
"""This alias for :class:`InvalidPropertyError` is for legacy support."""


class UnprojectedPropertyError(_exceptions.Error):
    """Raised when getting a property value that's not in the projection."""


class ReadonlyPropertyError(_exceptions.Error):
    """Raised when attempting to set a property value that is read-only."""


class ComputedPropertyError(ReadonlyPropertyError):
    """Raised when attempting to set or delete a computed property."""


class IndexProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Index:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class IndexState:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ModelAdapter:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def make_connection(*args, **kwargs):
    raise NotImplementedError


class ModelAttribute:
    """Base for :meth:`_fix_up` implementing classes."""

    def _fix_up(self, cls, code_name):
        """Fix-up property name. To be implemented by subclasses.

        Args:
            cls (type): The model class that owns the property.
            code_name (str): The name of the :class:`Property` being fixed up.
        """


class Property(ModelAttribute):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ModelKey(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BooleanProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class IntegerProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class FloatProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BlobProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class TextProperty(BlobProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class StringProperty(TextProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class GeoPtProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class PickleProperty(BlobProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class JsonProperty(BlobProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class UserProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KeyProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BlobKeyProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class DateTimeProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class DateProperty(DateTimeProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class TimeProperty(DateTimeProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class StructuredProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class LocalStructuredProperty(BlobProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class GenericProperty(Property):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ComputedProperty(GenericProperty):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class MetaModel(type):
    def __new__(self, *args, **kwargs):
        raise NotImplementedError


class Model:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def _get_kind(cls):
        """Return the kind name for this class.

        This defaults to ``cls.__name__``; users may override this to give a
        class a different name when stored in Google Cloud Datastore than the
        name of the class.
        """
        return cls.__name__


class Expando(Model):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def transaction(*args, **kwargs):
    raise NotImplementedError


def transaction_async(*args, **kwargs):
    raise NotImplementedError


def in_transaction(*args, **kwargs):
    raise NotImplementedError


def transactional(*args, **kwargs):
    raise NotImplementedError


def transactional_async(*args, **kwargs):
    raise NotImplementedError


def transactional_tasklet(*args, **kwargs):
    raise NotImplementedError


def non_transactional(*args, **kwargs):
    raise NotImplementedError


def get_multi_async(*args, **kwargs):
    raise NotImplementedError


def get_multi(*args, **kwargs):
    raise NotImplementedError


def put_multi_async(*args, **kwargs):
    raise NotImplementedError


def put_multi(*args, **kwargs):
    raise NotImplementedError


def delete_multi_async(*args, **kwargs):
    raise NotImplementedError


def delete_multi(*args, **kwargs):
    raise NotImplementedError


def get_indexes_async(*args, **kwargs):
    raise NotImplementedError


def get_indexes(*args, **kwargs):
    raise NotImplementedError
