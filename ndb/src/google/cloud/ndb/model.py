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


from google.cloud.ndb import key


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


class BlobKey:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


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


class ComputedPropertyError:
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


class GeoPt:
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


class InvalidPropertyError:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


BadProjectionError = InvalidPropertyError


class JsonProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


Key = key.Key


class KeyProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindError:
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


class ReadonlyPropertyError:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Rollback:
    def __init__(self, *args, **kwargs):
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


class UnprojectedPropertyError:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class UserProperty:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
