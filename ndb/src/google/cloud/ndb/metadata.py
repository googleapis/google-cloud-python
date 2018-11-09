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

"""Access datastore metadata."""


__all__ = [
    "EntityGroup",
    "get_entity_group_version",
    "get_kinds",
    "get_namespaces",
    "get_properties_of_kind",
    "get_representations_of_kind",
    "Kind",
    "Namespace",
    "Property",
]


class EntityGroup:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def get_entity_group_version(*args, **kwargs):
    raise NotImplementedError


def get_kinds(*args, **kwargs):
    raise NotImplementedError


def get_namespaces(*args, **kwargs):
    raise NotImplementedError


def get_properties_of_kind(*args, **kwargs):
    raise NotImplementedError


def get_representations_of_kind(*args, **kwargs):
    raise NotImplementedError


class Kind:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Namespace:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Property:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError
