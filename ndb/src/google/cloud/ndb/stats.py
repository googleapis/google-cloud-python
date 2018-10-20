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

"""Models for accessing datastore usage statistics."""


__all__ = [
    "BaseKindStatistic",
    "BaseStatistic",
    "GlobalStat",
    "KindCompositeIndexStat",
    "KindNonRootEntityStat",
    "KindPropertyNamePropertyTypeStat",
    "KindPropertyNameStat",
    "KindPropertyTypeStat",
    "KindRootEntityStat",
    "KindStat",
    "NamespaceGlobalStat",
    "NamespaceKindCompositeIndexStat",
    "NamespaceKindNonRootEntityStat",
    "NamespaceKindPropertyNamePropertyTypeStat",
    "NamespaceKindPropertyNameStat",
    "NamespaceKindPropertyTypeStat",
    "NamespaceKindRootEntityStat",
    "NamespaceKindStat",
    "NamespacePropertyTypeStat",
    "NamespaceStat",
    "PropertyTypeStat",
]


class BaseKindStatistic:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BaseStatistic:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class GlobalStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindCompositeIndexStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindNonRootEntityStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindPropertyNamePropertyTypeStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindPropertyNameStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindPropertyTypeStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindRootEntityStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceGlobalStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindCompositeIndexStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindNonRootEntityStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindPropertyNamePropertyTypeStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindPropertyNameStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindPropertyTypeStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindRootEntityStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespacePropertyTypeStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class PropertyTypeStat:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
