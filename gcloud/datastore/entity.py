# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Class for representing a single entity in the Cloud Datastore."""


from gcloud._helpers import _ensure_tuple_or_list


class Entity(dict):
    """Entities are akin to rows in a relational database

    An entity storing the actual instance of data.

    Each entity is officially represented with a
    :class:`gcloud.datastore.key.Key` class, however it is possible that
    you might create an Entity with only a partial Key (that is, a Key
    with a Kind, and possibly a parent, but without an ID).  In such a
    case, the datastore service will automatically assign an ID to the
    partial key.

    Entities in this API act like dictionaries with extras built in that
    allow you to delete or persist the data stored on the entity.

    Entities are mutable and act like a subclass of a dictionary.
    This means you could take an existing entity and change the key
    to duplicate the object.

    Use :func:`gcloud.datastore.get` to retrieve an existing entity.

      >>> datastore.get(key)
      <Entity[{'kind': 'EntityKind', id: 1234}] {'property': 'value'}>

    You can the set values on the entity just like you would on any
    other dictionary.

    >>> entity['age'] = 20
    >>> entity['name'] = 'JJ'
    >>> entity
    <Entity[{'kind': 'EntityKind', id: 1234}] {'age': 20, 'name': 'JJ'}>

    And you can convert an entity to a regular Python dictionary with the
    ``dict`` builtin:

    >>> dict(entity)
    {'age': 20, 'name': 'JJ'}

    .. note::

       When saving an entity to the backend, values which are "text"
       (``unicode`` in Python2, ``str`` in Python3) will be saved using
       the 'text_value' field, after being encoded to UTF-8.  When
       retrieved from the back-end, such values will be decoded to "text"
       again.  Values which are "bytes" (``str`` in Python2, ``bytes`` in
       Python3), will be saved using the 'blob_value' field, without
       any decoding / encoding step.

    :type key: :class:`gcloud.datastore.key.Key`
    :param key: Optional key to be set on entity. Required for
                :func:`gcloud.datastore.put()` and
                :func:`gcloud.datastore.put_multi()`

    :type exclude_from_indexes: tuple of string
    :param exclude_from_indexes: Names of fields whose values are not to be
                                 indexed for this entity.
    """

    def __init__(self, key=None, exclude_from_indexes=()):
        super(Entity, self).__init__()
        self.key = key
        self._exclude_from_indexes = set(_ensure_tuple_or_list(
            'exclude_from_indexes', exclude_from_indexes))

    def __eq__(self, other):
        """Compare two entities for equality.

        Entities compare equal if their keys compare equal, and their
        properties compare equal.

        :rtype: boolean
        :returns: True if the entities compare equal, else False.
        """
        if not isinstance(other, Entity):
            return NotImplemented

        return (self.key == other.key and
                super(Entity, self).__eq__(other))

    def __ne__(self, other):
        """Compare two entities for inequality.

        Entities compare equal if their keys compare equal, and their
        properties compare equal.

        :rtype: boolean
        :returns: False if the entities compare equal, else True.
        """
        return not self == other

    @property
    def kind(self):
        """Get the kind of the current entity.

        .. note::
          This relies entirely on the :class:`gcloud.datastore.key.Key`
          set on the entity.  That means that we're not storing the kind
          of the entity at all, just the properties and a pointer to a
          Key which knows its Kind.
        """
        if self.key:
            return self.key.kind

    @property
    def exclude_from_indexes(self):
        """Names of fields which are *not* to be indexed for this entity.

        :rtype: sequence of field names
        """
        return frozenset(self._exclude_from_indexes)

    def __repr__(self):
        if self.key:
            return '<Entity%s %s>' % (self.key.path,
                                      super(Entity, self).__repr__())
        else:
            return '<Entity %s>' % (super(Entity, self).__repr__())
