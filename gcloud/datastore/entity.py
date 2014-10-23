"""Class for representing a single entity in the Cloud Datastore.

Entities are akin to rows in a relational database,
storing the actual instance of data.

Each entity is officially represented with
a :class:`gcloud.datastore.key.Key` class,
however it is possible that you might create
an Entity with only a partial Key
(that is, a Key with a Kind,
and possibly a parent, but without an ID).

Entities in this API act like dictionaries
with extras built in that allow you to
delete or persist the data stored on the entity.
"""

from gcloud.datastore import datastore_v1_pb2 as datastore_pb
from gcloud.datastore.key import Key


class NoKey(RuntimeError):
    """Exception raised by Entity methods which require a key."""


class NoDataset(RuntimeError):
    """Exception raised by Entity methods which require a dataset."""


class Entity(dict):
    """:type dataset: :class:`gcloud.datastore.dataset.Dataset`
    :param dataset: The dataset in which this entity belongs.

    :type kind: string
    :param kind: The kind of entity this is, akin to a table name in a
                 relational database.

    Entities are mutable and act like a subclass of a dictionary.
    This means you could take an existing entity and change the key
    to duplicate the object.

    This can be used on its own, however it is likely easier to use
    the shortcut methods provided by :class:`gcloud.datastore.dataset.Dataset`
    such as:

    - :func:`gcloud.datastore.dataset.Dataset.entity` to create a new entity.

      >>> dataset.entity('MyEntityKind')
      <Entity[{'kind': 'MyEntityKind'}] {}>

    - :func:`gcloud.datastore.dataset.Dataset.get_entity`
      to retrieve an existing entity.

      >>> dataset.get_entity(key)
      <Entity[{'kind': 'EntityKind', id: 1234}] {'property': 'value'}>

    You can the set values on the entity
    just like you would on any other dictionary.

    >>> entity['age'] = 20
    >>> entity['name'] = 'JJ'
    >>> entity
    <Entity[{'kind': 'EntityKind', id: 1234}] {'age': 20, 'name': 'JJ'}>

    And you can cast an entity to a regular Python dictionary
    with the `dict` builtin:

    >>> dict(entity)
    {'age': 20, 'name': 'JJ'}

    """

    def __init__(self, dataset=None, kind=None):
        super(Entity, self).__init__()
        self._dataset = dataset
        if kind:
            self._key = Key().kind(kind)
        else:
            self._key = None

    def dataset(self):
        """Get the :class:`.dataset.Dataset` in which this entity belongs.

        :rtype: :class:`gcloud.datastore.dataset.Dataset`
        :returns: The Dataset containing the entity if there is a key,
                  else None.

        .. note::
          This is based on the :class:`gcloud.datastore.key.Key` set on the
          entity. That means that if you have no key set, the dataset might
          be `None`. It also means that if you change the key on the entity,
          this will refer to that key's dataset.
        """
        return self._dataset

    def key(self, key=None):
        """Get or set the :class:`.datastore.key.Key` on the current entity.

        :type key: :class:`glcouddatastore.key.Key`
        :param key: The key you want to set on the entity.

        :rtype: :class:`gcloud.datastore.key.Key` or :class:`Entity`.
        :returns: Either the current key (on get) or the current
                  object (on set).

        >>> entity.key(my_other_key)  # This returns the original entity.
        <Entity[{'kind': 'OtherKeyKind', 'id': 1234}] {'property': 'value'}>
        >>> entity.key()  # This returns the key.
        <Key[{'kind': 'OtherKeyKind', 'id': 1234}]>
        """

        if key is not None:
            self._key = key
            return self
        else:
            return self._key

    def kind(self):
        """Get the kind of the current entity.

        .. note::
          This relies entirely on
          the :class:`gcloud.datastore.key.Key`
          set on the entity.
          That means that we're not storing the kind of the entity at all,
          just the properties and a pointer to a Key
          which knows its Kind.
        """

        if self._key:
            return self._key.kind()

    @classmethod
    def from_key(cls, key, dataset=None):
        """Create entity based on :class:`.datastore.key.Key`.

        .. note::
          This is a factory method.

        :type key: :class:`gcloud.datastore.key.Key`
        :param key: The key for the entity.

        :returns: The :class:`Entity` derived from the
                  :class:`gcloud.datastore.key.Key`.
        """

        return cls(dataset).key(key)

    @property
    def _must_key(self):
        """Return our key, or raise NoKey if not set.

        :rtype: :class:`gcloud.datastore.key.Key`.
        :returns: our key
        :raises: NoKey if key is None
        """
        if self._key is None:
            raise NoKey()
        return self._key

    @property
    def _must_dataset(self):
        """Return our dataset, or raise NoDataset if not set.

        :rtype: :class:`gcloud.datastore.key.Key`.
        :returns: our key
        :raises: NoDataset if key is None
        """
        if self._dataset is None:
            raise NoDataset()
        return self._dataset

    def reload(self):
        """Reloads the contents of this entity from the datastore.

        This method takes the :class:`gcloud.datastore.key.Key`, loads all
        properties from the Cloud Datastore, and sets the updated properties on
        the current object.

        .. warning::
          This will override any existing properties if a different value
          exists remotely, however it will *not* override any properties that
          exist only locally.
        """
        key = self._must_key
        dataset = self._must_dataset
        entity = dataset.get_entity(key.to_protobuf())

        if entity:
            self.update(entity)
        return self

    def save(self):
        """Save the entity in the Cloud Datastore.

        .. note::
           Any existing properties for the entity will be replaced by those
           currently set on this instance.  Already-stored properties which do
           not correspond to keys set on this instance will be removed from
           the datastore.

        .. note::
           Property values which are "text" ('unicode' in Python2, 'str' in
           Python3) map to 'string_value' in the datastore;  values which are
           "bytes" ('str' in Python2, 'bytes' in Python3) map to 'blob_value'.

        :rtype: :class:`gcloud.datastore.entity.Entity`
        :returns: The entity with a possibly updated Key.
        """
        key = self._must_key
        dataset = self._must_dataset
        connection = dataset.connection()
        key_pb = connection.save_entity(
            dataset_id=dataset.id(),
            key_pb=key.to_protobuf(),
            properties=dict(self))

        # If we are in a transaction and the current entity needs an
        # automatically assigned ID, tell the transaction where to put that.
        transaction = connection.transaction()
        if transaction and key.is_partial():
            transaction.add_auto_id_entity(self)

        if isinstance(key_pb, datastore_pb.Key):
            path = []
            for element in key_pb.path_element:
                key_part = {}
                for descriptor, value in element._fields.items():
                    key_part[descriptor.name] = value
                path.append(key_part)
            # Update the path (which may have been altered).
            self._key = key.path(path)

        return self

    def delete(self):
        """Delete the entity in the Cloud Datastore.

        .. note::
          This is based entirely off of the :class:`gcloud.datastore.key.Key`
          set on the entity. Whatever is stored remotely using the key on the
          entity will be deleted.
        """
        key = self._must_key
        dataset = self._must_dataset
        dataset.connection().delete_entities(
            dataset_id=dataset.id(),
            key_pbs=[key.to_protobuf()],
            )

    def __repr__(self):
        if self._key:
            return '<Entity%s %s>' % (self._key.path(),
                                      super(Entity, self).__repr__())
        else:
            return '<Entity %s>' % (super(Entity, self).__repr__())
