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
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class BaseStatistic:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class GlobalStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindCompositeIndexStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindNonRootEntityStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindPropertyNamePropertyTypeStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindPropertyNameStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindPropertyTypeStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindRootEntityStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class KindStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceGlobalStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindCompositeIndexStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindNonRootEntityStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindPropertyNamePropertyTypeStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindPropertyNameStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindPropertyTypeStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindRootEntityStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceKindStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespacePropertyTypeStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class NamespaceStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class PropertyTypeStat:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        raise NotImplementedError
