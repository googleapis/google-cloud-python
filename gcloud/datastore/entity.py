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

from datetime import datetime

from gcloud.datastore import datastore_v1_pb2 as datastore_pb
from gcloud.datastore.key import Key


class Entity(dict):
  """
  :type dataset: :class:`gcloud.datastore.dataset.Dataset`
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

  - :func:`gcloud.datastore.dataset.Dataset.get_entity` to retrive an existing entity.

    >>> dataset.get_entity(key)
    <Entity[{'kind': 'EntityKind', id: 1234}] {'property': 'value'}>

  You can the set values on the entity just like you would on any other dictionary.

  >>> entity['age'] = 20
  >>> entity['name'] = 'JJ'
  >>> entity
  <Entity[{'kind': 'EntityKind', id: 1234}] {'age': 20, 'name': 'JJ'}>

  And you can cast an entity to a regular Python dictionary with the `dict` builtin:

  >>> dict(entity)
  {'age': 20, 'name': 'JJ'}
  """

  def __init__(self, dataset=None, kind=None):
    if dataset and kind:
      self._key = Key(dataset=dataset).kind(kind)
    else:
      self._key = None

  def dataset(self):
    """Get the :class:`gcloud.datastore.dataset.Dataset` in which this entity belonds.

    .. note::
      This is based on the :class:`gcloud.datastore.key.Key` set on the entity.
      That means that if you have no key set, the dataset might be `None`.
      It also means that if you change the key on the entity, this will refer
      to that key's dataset.
    """
    if self.key():
      return self.key().dataset()

  def key(self, key=None):
    """Get or set the :class:`gcloud.datastore.key.Key` on the current entity.

    :type key: :class:`glcouddatastore.key.Key`
    :param key: The key you want to set on the entity.

    :returns: Either the current key or the :class:`Entity`.

    >>> entity.key(my_other_key)  # This returns the original entity.
    <Entity[{'kind': 'OtherKeyKind', 'id': 1234}] {'property': 'value'}>
    >>> entity.key()  # This returns the key.
    <Key[{'kind': 'OtherKeyKind', 'id': 1234}]>
    """

    if key:
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

    if self.key():
      return self.key().kind()

  @classmethod
  def from_key(cls, key):
    """Factory method for creating an entity based on the :class:`gcloud.datastore.key.Key`.

    :type key: :class:`gcloud.datastore.key.Key`
    :param key: The key for the entity.

    :returns: The :class:`Entity` derived from the :class:`gcloud.datastore.key.Key`.
    """

    return cls().key(key)

  @classmethod
  def from_protobuf(cls, pb, dataset=None):
    """Factory method for creating an entity based on a protobuf.

    The protobuf should be one returned from the Cloud Datastore Protobuf API.

    :type key: :class:`gcloud.datastore.datastore_v1_pb2.Entity`
    :param key: The Protobuf representing the entity.

    :returns: The :class:`Entity` derived from the :class:`gcloud.datastore.datastore_v1_pb2.Entity`.
    """

    # This is here to avoid circular imports.
    from gcloud.datastore import helpers

    key = Key.from_protobuf(pb.key, dataset=dataset)
    entity = cls.from_key(key)

    for property_pb in pb.property:
      value = helpers.get_value_from_protobuf(property_pb)
      entity[property_pb.name] = value

    return entity

  def reload(self):
    """Reloads the contents of this entity from the datastore.

    This method takes the :class:`gcloud.datastore.key.Key`, loads all
    properties from the Cloud Datastore, and sets the updated properties on
    the current object.

    .. warning::
      This will override any existing properties if a different value exists
      remotely, however it will *not* override any properties that exist
      only locally.
    """

    # Note that you must have a valid key, otherwise this makes no sense.
    entity = self.dataset().get_entities(self.key().to_protobuf())

    # TODO(jjg): Raise an error if something dumb happens.
    if entity:
      self.update(entity)
    return self

  def save(self):
    """Save the entity in the Cloud Datastore.

    :rtype: :class:`gcloud.datastore.entity.Entity`
    :returns: The entity with a possibly updated Key.
    """
    key_pb = self.dataset().connection().save_entity(
        dataset_id=self.dataset().id(), key_pb=self.key().to_protobuf(),
        properties=dict(self))

    # If we are in a transaction and the current entity needs an
    # automatically assigned ID, tell the transaction where to put that.
    transaction = self.dataset().connection().transaction()
    if transaction and self.key().is_partial():
      transaction.add_auto_id_entity(self)

    if isinstance(key_pb, datastore_pb.Key):
      updated_key = Key.from_protobuf(key_pb)
      # Update the path (which may have been altered).
      key = self.key().path(updated_key.path())
      self.key(key)

    return self

  def delete(self):
    """Delete the entity in the Cloud Datastore.

    .. note::
      This is based entirely off of the :class:`gcloud.datastore.key.Key` set
      on the entity. Whatever is stored remotely using the key on the entity
      will be deleted.
    """
    self.dataset().connection().delete_entity(
        dataset_id=self.dataset().id(), key_pb=self.key().to_protobuf())

  def __repr__(self):
    # TODO: Make sure that this makes sense.
    # An entity should have a key all the time (even if it's partial).
    if self.key():
      return '<Entity%s %s>' % (self.key().path(), super(Entity, self).__repr__())
    else:
      return '<Entity %s>' % (super(Entity, self).__repr__())
