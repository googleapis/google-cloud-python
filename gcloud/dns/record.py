class Record(object):
  """A class representing a Resource Record Set on Cloud DNS.

  :type name: string
  :param name: The name of the record, for example 'www.example.com.'.

  :type data: list
  :param data: A list of the textual representation of Resource Records.

  :type ttl: int
  :param ttl: The record's time to live.

  :type type: string
  :param string: The type of DNS record.
  """

  def __init__(self, name=None, data=[], ttl=None, type=None):
    self.name = name
    self.data = data
    self.ttl = ttl
    self.type = type

  @classmethod
  def from_dict(cls, record_dict):
    """Construct a new record from a dictionary of data from Cloud DNS.

    :type record_dict: dict
    :param record_dict: The dictionary of data to construct a record from.

    :rtype: :class:`Record`
    :returns: A record constructed from the data provided.
    """

    return cls(name=record_dict['name'], data=record_dict['rrdatas'],
               ttl=record_dict['ttl'], type=record_dict['type'])

  def __str__(self):
    """Format the record when printed.

    :rtype: string
    :returns: A formated record string.
    """

    record = ('{name} {ttl} IN {type} {data}')
    return record.format(name=self.name, ttl=self.ttl, type=self.type,
                         data=self.data)

  def add_data(self, data):
    """Add to the list of resource record data for the record.

    :type data: string
    :param data: The textual representation of a resourse record.
    """

    self.data.append(data)

  def to_dict(self):
    """Format the record into a dict compatible with Cloud DNS.

    :rtype: dict
    :returns: A Cloud DNS dict representation of a record.
    """

    return {'name': self.name, 'rrdatas': self.data, 'ttl': self.ttl,
            'type': self.type}
