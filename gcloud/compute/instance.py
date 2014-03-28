class Instance(object):

  def __init__(self, connection=None, name=None, zone=None):
    self.connection = connection
    self.name = name
    self.zone = zone

  @classmethod
  def from_dict(cls, instance_dict, connection=None):
    """Construct a new bucket from a dictionary of data from Cloud Storage.

    :type bucket_dict: dict
    :param bucket_dict: The dictionary of data to construct a bucket from.

    :rtype: :class:`Bucket`
    :returns: A bucket constructed from the data provided.
    """

    return cls(connection=connection, name=instance_dict['name'],
               zone=instance_dict['zone'].split('/').pop())

  @property
  def path(self):
    """The URL path to this instances."""

    if not self.name:
      raise ValueError('Cannot determine path without instance zone and name.')

    return ('projects/%s/zones/%s/instances/%s/' %
            (self.connection.project_name, self.zone, self.name))

  def reset(self):
    return self.connection.reset_instance(self)
