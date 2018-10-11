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
    "BlobKey",
    "BlobKeyProperty",
    "BlobProperty",
    "BooleanProperty",
    "ComputedProperty",
    "ComputedPropertyError",
    "DateProperty",
    "DateTimeProperty",
    "delete_multi",
    "delete_multi_async",
    "Expando",
    "FloatProperty",
    "GenericProperty",
    "GeoPt",
    "GeoPtProperty",
    "get_indexes",
    "get_indexes_async",
    "get_multi",
    "get_multi_async",
    "in_transaction",
    "Index",
    "IndexProperty",
    "IndexState",
    "IntegerProperty",
    "InvalidPropertyError",
    "BadProjectionError",
    "JsonProperty",
    "Key",
    "KeyProperty",
    "KindError",
    "LocalStructuredProperty",
    "make_connection",
    "MetaModel",
    "Model",
    "ModelAdapter",
    "ModelAttribute",
    "ModelKey",
    "non_transactional",
    "PickleProperty",
    "Property",
    "put_multi",
    "put_multi_async",
    "ReadonlyPropertyError",
    "Rollback",
    "StringProperty",
    "StructuredProperty",
    "TextProperty",
    "TimeProperty",
    "transaction",
    "transaction_async",
    "transactional",
    "transactional_async",
    "transactional_tasklet",
    "UnprojectedPropertyError",
    "UserProperty",
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


class BlobKeyProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BlobProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BooleanProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ComputedProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class DateProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class DateTimeProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def delete_multi(*args, **kwargs):
    raise NotImplementedError


def delete_multi_async(*args, **kwargs):
    raise NotImplementedError


class Expando:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class FloatProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class GenericProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class GeoPtProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def get_indexes(*args, **kwargs):
    raise NotImplementedError


def get_indexes_async(*args, **kwargs):
    raise NotImplementedError


def get_multi(*args, **kwargs):
    raise NotImplementedError


def get_multi_async(*args, **kwargs):
    raise NotImplementedError


def in_transaction(*args, **kwargs):
    raise NotImplementedError


class Index:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class IndexProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class IndexState:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class IntegerProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class JsonProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KeyProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class LocalStructuredProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def make_connection(*args, **kwargs):
    raise NotImplementedError


class MetaModel:
    def __init__(self, *args, **kwargs):
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


class ModelAdapter:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ModelAttribute:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class ModelKey:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def non_transactional(*args, **kwargs):
    raise NotImplementedError


class PickleProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Property:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def put_multi(*args, **kwargs):
    raise NotImplementedError


def put_multi_async(*args, **kwargs):
    raise NotImplementedError


class StringProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class StructuredProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class TextProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class TimeProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def transaction(*args, **kwargs):
    raise NotImplementedError


def transaction_async(*args, **kwargs):
    raise NotImplementedError


def transactional(*args, **kwargs):
    raise NotImplementedError


def transactional_async(*args, **kwargs):
    raise NotImplementedError


def transactional_tasklet(*args, **kwargs):
    raise NotImplementedError


class UserProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
