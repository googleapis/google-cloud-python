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

from google.cloud.ndb import model


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


class BaseStatistic(model.Model):
    """Base Statistic Model class.

    Attributes:
      bytes: the total number of bytes taken up in Cloud Datastore for the
      statistic instance.
      count: attribute is the total number of occurrences of the statistic
      in Cloud Datastore.
      timestamp: the time the statistic instance was written to Cloud
      Datastore.
    """

    __slots__ = ()

    # This is necessary for the _get_kind() classmethod override.
    STORED_KIND_NAME = "__BaseStatistic__"

    # The number of bytes that is taken up.
    bytes = model.IntegerProperty()

    # The number of entity records.
    count = model.IntegerProperty()

    # When this statistic was inserted into Cloud Datastore.
    timestamp = model.DateTimeProperty()

    @classmethod
    def _get_kind(cls):
        """Kind name override."""
        return cls.STORED_KIND_NAME


class BaseKindStatistic(BaseStatistic):
    """Base Statistic Model class for stats associated with kinds.

    Attributes:
      kind_name: the name of the kind associated with the statistic instance.
      entity_bytes: the number of bytes taken up to store the statistic
        in Cloud Datastore minus the cost of storing indices.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__BaseKindStatistic__"

    # The name of the kind.
    kind_name = model.StringProperty()

    # The number of bytes that is taken up in entity table. entity_bytes does
    # not reflect the storage allocated for indexes, either built-in or
    # composite indexes.
    entity_bytes = model.IntegerProperty(default=0)


class GlobalStat(BaseStatistic):
    """An aggregate of all entities across the entire application.

    This statistic only has a single instance in Cloud Datastore that contains
    the total number of entities stored and the total number of bytes they take
    up.

    Attributes:
      entity_bytes: the number of bytes taken up to store the statistic
        in Cloud Datastore minus the cost of storing indices.
      builtin_index_bytes: the number of bytes taken up to store builtin-in
        index entries
      builtin_index_count: the number of built-in index entries.
      composite_index_bytes: the number of bytes taken up to store composite
        index entries
      composite_index_count: the number of composite index entries.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Total__"

    # The number of bytes that is taken up in entity storage.
    entity_bytes = model.IntegerProperty(default=0)

    # The number of bytes taken up for built-in index entries.
    builtin_index_bytes = model.IntegerProperty(default=0)

    # The number of built-in index entries.
    builtin_index_count = model.IntegerProperty(default=0)

    # The number of bytes taken up for composite index entries.
    composite_index_bytes = model.IntegerProperty(default=0)

    # The number of composite indexes entries.
    composite_index_count = model.IntegerProperty(default=0)


class NamespaceStat(BaseStatistic):
    """An aggregate of all entities across an entire namespace.

    This statistic has one instance per namespace.  The key_name is the
    represented namespace. NamespaceStat entities will only be found
    in the namespace "" (empty string). It contains the total
    number of entities stored and the total number of bytes they take up.

    Attributes:
      subject_namespace: the namespace associated with the statistic instance.
      entity_bytes: the number of bytes taken up to store the statistic
        in Cloud Datastore minus the cost of storing indices.
      builtin_index_bytes: the number of bytes taken up to store builtin-in
        index entries
      builtin_index_count: the number of built-in index entries.
      composite_index_bytes: the number of bytes taken up to store composite
        index entries
      composite_index_count: the number of composite index entries.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Namespace__"

    # The namespace name this NamespaceStat refers to.
    subject_namespace = model.StringProperty()

    # The number of bytes that is taken up in entity storage.
    entity_bytes = model.IntegerProperty(default=0)

    # The number of bytes taken up for built-in index entries.
    builtin_index_bytes = model.IntegerProperty(default=0)

    # The number of built-in index entries.
    builtin_index_count = model.IntegerProperty(default=0)

    # The number of bytes taken up for composite index entries.
    composite_index_bytes = model.IntegerProperty(default=0)

    # The number of composite indexes entries.
    composite_index_count = model.IntegerProperty(default=0)


class KindStat(BaseKindStatistic):
    """An aggregate of all entities at the granularity of their Kind.

    There is an instance of the KindStat for every Kind that is in the
    application's datastore.  This stat contains per-Kind statistics.

    Attributes:
      builtin_index_bytes: the number of bytes taken up to store builtin-in
        index entries
      builtin_index_count: the number of built-in index entries.
      composite_index_bytes: the number of bytes taken up to store composite
        index entries
      composite_index_count: the number of composite index entries.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Kind__"

    # The number of bytes taken up for built-in index entries.
    builtin_index_bytes = model.IntegerProperty(default=0)

    # The number of built-in index entries.
    builtin_index_count = model.IntegerProperty(default=0)

    # The number of bytes taken up for composite index entries.
    composite_index_bytes = model.IntegerProperty(default=0)

    # The number of composite indexes entries.
    composite_index_count = model.IntegerProperty(default=0)


class KindRootEntityStat(BaseKindStatistic):
    """Statistics of the number of root entities in Cloud Datastore by Kind.

    There is an instance of the KindRootEntityState for every Kind that is in
    the application's datastore and has an instance that is a root entity.  This
    stat contains statistics regarding these root entity instances.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Kind_IsRootEntity__"


class KindNonRootEntityStat(BaseKindStatistic):
    """Statistics of the number of non root entities in Cloud Datastore by Kind.

    There is an instance of the KindNonRootEntityStat for every Kind that is in
    the application's datastore that is a not a root entity.  This stat contains
    statistics regarding thse non root entity instances.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Kind_NotRootEntity__"


class PropertyTypeStat(BaseStatistic):
    """An aggregate of all properties across the entire application by type.

    There is an instance of the PropertyTypeStat for every property type
    (google.appengine.api.datastore_types._PROPERTY_TYPES) in use by the
    application in its datastore.

    Attributes:
      property_type: the property type associated with the statistic instance.
      entity_bytes: the number of bytes taken up to store the statistic
        in Cloud Datastore minus the cost of storing indices.
      builtin_index_bytes: the number of bytes taken up to store builtin-in
        index entries
      builtin_index_count: the number of built-in index entries.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_PropertyType__"

    # The name of the property_type.
    property_type = model.StringProperty()

    # The number of bytes that is taken up in entity storage.
    entity_bytes = model.IntegerProperty(default=0)

    # The number of bytes taken up for built-in index entries.
    builtin_index_bytes = model.IntegerProperty(default=0)

    # The number of built-in index entries.
    builtin_index_count = model.IntegerProperty(default=0)


class KindPropertyTypeStat(BaseKindStatistic):
    """Statistics on (kind, property_type) tuples in the app's datastore.

    There is an instance of the KindPropertyTypeStat for every
    (kind, property_type) tuple in the application's datastore.

    Attributes:
      property_type: the property type associated with the statistic instance.
      builtin_index_bytes: the number of bytes taken up to store builtin-in
        index entries
      builtin_index_count: the number of built-in index entries.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_PropertyType_Kind__"

    # The name of the property_type.
    property_type = model.StringProperty()

    # The number of bytes taken up for built-in index entries.
    builtin_index_bytes = model.IntegerProperty(default=0)

    # The number of built-in index entries.
    builtin_index_count = model.IntegerProperty(default=0)


class KindPropertyNameStat(BaseKindStatistic):
    """Statistics on (kind, property_name) tuples in the app's datastore.

    There is an instance of the KindPropertyNameStat for every
    (kind, property_name) tuple in the application's datastore.

    Attributes:
      property_name: the name of the property associated with the statistic
        instance.
      builtin_index_bytes: the number of bytes taken up to store builtin-in
        index entries
      builtin_index_count: the number of built-in index entries.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_PropertyName_Kind__"

    # The name of the property.
    property_name = model.StringProperty()

    # The number of bytes taken up for built-in index entries.
    builtin_index_bytes = model.IntegerProperty(default=0)

    # The number of built-in index entries.
    builtin_index_count = model.IntegerProperty(default=0)


class KindPropertyNamePropertyTypeStat(BaseKindStatistic):
    """Statistic on (kind, property_name, property_type) tuples in Cloud
    Datastore.

    There is an instance of the KindPropertyNamePropertyTypeStat for every
    (kind, property_name, property_type) tuple in the application's datastore.

    Attributes:
      property_type: the property type associated with the statistic instance.
      property_name: the name of the property associated with the statistic
        instance.
      builtin_index_bytes: the number of bytes taken up to store builtin-in
        index entries
      builtin_index_count: the number of built-in index entries.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_PropertyType_PropertyName_Kind__"

    # The name of the property type.
    property_type = model.StringProperty()

    # The name of the property.
    property_name = model.StringProperty()

    # The number of bytes taken up for built-in index entries.
    builtin_index_bytes = model.IntegerProperty(default=0)

    # The number of built-in index entries.
    builtin_index_count = model.IntegerProperty(default=0)


class KindCompositeIndexStat(BaseStatistic):
    """Statistic on (kind, composite_index_id) tuples in Cloud Datastore.

    There is an instance of the KindCompositeIndexStat for every unique
    (kind, composite_index_id) tuple in the application's datastore indexes.

    Attributes:
      index_id: the id of the composite index associated with the statistic
        instance.
      kind_name: the name of the kind associated with the statistic instance.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Kind_CompositeIndex__"

    # The id of the composite index
    index_id = model.IntegerProperty()

    # The name of the kind.
    kind_name = model.StringProperty()


# The following specify namespace-specific stats.
# These types are specific to Cloud Datastore namespace they are located
# within. These will only be produced if datastore entities exist
# in a namespace other than the empty namespace (i.e. namespace="").


class NamespaceGlobalStat(GlobalStat):
    """GlobalStat equivalent for a specific namespace.

    These may be found in each specific namespace and represent stats for
    that particular namespace.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Ns_Total__"


class NamespaceKindStat(KindStat):
    """KindStat equivalent for a specific namespace.

    These may be found in each specific namespace and represent stats for
    that particular namespace.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Ns_Kind__"


class NamespaceKindRootEntityStat(KindRootEntityStat):
    """KindRootEntityStat equivalent for a specific namespace.

    These may be found in each specific namespace and represent stats for
    that particular namespace.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Ns_Kind_IsRootEntity__"


class NamespaceKindNonRootEntityStat(KindNonRootEntityStat):
    """KindNonRootEntityStat equivalent for a specific namespace.

    These may be found in each specific namespace and represent stats for
    that particular namespace.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Ns_Kind_NotRootEntity__"


class NamespacePropertyTypeStat(PropertyTypeStat):
    """PropertyTypeStat equivalent for a specific namespace.

    These may be found in each specific namespace and represent stats for
    that particular namespace.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Ns_PropertyType__"


class NamespaceKindPropertyTypeStat(KindPropertyTypeStat):
    """KindPropertyTypeStat equivalent for a specific namespace.

    These may be found in each specific namespace and represent stats for
    that particular namespace.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Ns_PropertyType_Kind__"


class NamespaceKindPropertyNameStat(KindPropertyNameStat):
    """KindPropertyNameStat equivalent for a specific namespace.

    These may be found in each specific namespace and represent stats for
    that particular namespace.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Ns_PropertyName_Kind__"


class NamespaceKindPropertyNamePropertyTypeStat(
    KindPropertyNamePropertyTypeStat
):
    """KindPropertyNamePropertyTypeStat equivalent for a specific namespace.

    These may be found in each specific namespace and represent stats for
    that particular namespace.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Ns_PropertyType_PropertyName_Kind__"


class NamespaceKindCompositeIndexStat(KindCompositeIndexStat):
    """KindCompositeIndexStat equivalent for a specific namespace.

    These may be found in each specific namespace and represent stats for
    that particular namespace.
    """

    __slots__ = ()

    STORED_KIND_NAME = "__Stat_Ns_Kind_CompositeIndex__"


# Maps a datastore stat entity kind name to its respective model class.
# NOTE: Any new stats added to this module should also be added here.
_DATASTORE_STATS_CLASSES_BY_KIND = {
    GlobalStat.STORED_KIND_NAME: GlobalStat,
    NamespaceStat.STORED_KIND_NAME: NamespaceStat,
    KindStat.STORED_KIND_NAME: KindStat,
    KindRootEntityStat.STORED_KIND_NAME: KindRootEntityStat,
    KindNonRootEntityStat.STORED_KIND_NAME: KindNonRootEntityStat,
    PropertyTypeStat.STORED_KIND_NAME: PropertyTypeStat,
    KindPropertyTypeStat.STORED_KIND_NAME: KindPropertyTypeStat,
    KindPropertyNameStat.STORED_KIND_NAME: KindPropertyNameStat,
    KindPropertyNamePropertyTypeStat.STORED_KIND_NAME: KindPropertyNamePropertyTypeStat,
    KindCompositeIndexStat.STORED_KIND_NAME: KindCompositeIndexStat,
    NamespaceGlobalStat.STORED_KIND_NAME: NamespaceGlobalStat,
    NamespaceKindStat.STORED_KIND_NAME: NamespaceKindStat,
    NamespaceKindRootEntityStat.STORED_KIND_NAME: NamespaceKindRootEntityStat,
    NamespaceKindNonRootEntityStat.STORED_KIND_NAME: NamespaceKindNonRootEntityStat,
    NamespacePropertyTypeStat.STORED_KIND_NAME: NamespacePropertyTypeStat,
    NamespaceKindPropertyTypeStat.STORED_KIND_NAME: NamespaceKindPropertyTypeStat,
    NamespaceKindPropertyNameStat.STORED_KIND_NAME: NamespaceKindPropertyNameStat,
    NamespaceKindPropertyNamePropertyTypeStat.STORED_KIND_NAME: NamespaceKindPropertyNamePropertyTypeStat,
    NamespaceKindCompositeIndexStat.STORED_KIND_NAME: NamespaceKindCompositeIndexStat,
}
