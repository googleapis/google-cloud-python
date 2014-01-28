class Dataset(object):
  """A dataset in the Cloud Datastore.

  This class acts as an abstraction of a single dataset
  in the Cloud Datastore.

  A dataset is analogous to a database
  in relational database world,
  and corresponds to a single project
  using the Cloud Datastore.

  Typically, you would only have one of these per connection
  however it didn't seem right to collapse the functionality
  of a connection and a dataset together into a single class.

  Datasets (like :class:`gcloud.datastore.query.Query`)
  are immutable.
  That is, you cannot change the ID and connection
  references.
  If you need to modify the connection or ID,
  it's recommended to construct a new :class:`Dataset`.

  :type id: string
  :param id: The ID of the dataset (your project ID)

  :type connection: :class:`gcloud.datastore.connection.Connection`
  :param connection: The connection to use for executing API calls.
  """

  def __init__(self, id, connection=None):
    self._connection = connection
    self._id = id

  def connection(self):
    """Get the current connection.

      >>> dataset = Dataset('dataset-id', connection=conn)
      >>> dataset.connection()
      <Connection object>

    :rtype: :class:`gcloud.datastore.connection.Connection`
    :returns: Returns the current connection.
    """

    return self._connection

  def id(self):
    """Get the current dataset ID.

      >>> dataset = Dataset('dataset-id', connection=conn)
      >>> dataset.id()
      'dataset-id'

    :rtype: string
    :returns: The current dataset ID.
    """

    return self._id

  def query(self, *args, **kwargs):
    from gcloud.datastore.query import Query
    kwargs['dataset'] = self
    return Query(*args, **kwargs)

  def entity(self, kind):
    from gcloud.datastore.entity import Entity
    return Entity(dataset=self, kind=kind)

  def transaction(self, *args, **kwargs):
    from gcloud.datastore.transaction import Transaction
    kwargs['dataset'] = self
    return Transaction(*args, **kwargs)

  def get_entity(self, key):
    """
    Retrieves an entity from the dataset, along with all of its attributes.

    :type key: :class:`gcloud.datastore.key.Key`
    :param item_name: The name of the item to retrieve.

    :rtype: :class:`gcloud.datastore.entity.Entity` or ``None``
    :return: The requested entity, or ``None`` if there was no match found.
    """
    entities = self.get_entities([key])
    if entities:
      return entities[0]

  def get_entities(self, keys):
    # This import is here to avoid circular references.
    from gcloud.datastore.entity import Entity

    entity_pbs = self.connection().lookup(dataset_id=self.id(),
        key_pbs=[k.to_protobuf() for k in keys])

    entities = []
    for entity_pb in entity_pbs:
      entities.append(Entity.from_protobuf(entity_pb, dataset=self))
    return entities
