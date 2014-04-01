from gcloud.dns.change import Change
from gcloud.dns.record import Record


class Zone(object):
  """A class representing a Managed Zone on Cloud DNS.

  :type connection: :class:`gcloud.dns.connection.Connection`
  :param connection: The connection to use when sending requests.

  :type creation_time: string
  :param connection_time: Time that this zone was created on the server.

  :type description: string
  :param data: A description of the zone.

  :type dns_name: string
  :param data: The DNS name of the zone.

  :type id: unsigned long
  :param data: Unique identifier defined by the server.

  :type kind: string
  :param data: Identifies what kind of resource.

  :type name_servers: list
  :param name_servers: List of virtual name servers of the zone.
  """

  def __init__(self, connection=None, creation_time=None,
               description=None, dns_name=None, id=None, kind=None, name=None,
               name_servers=None):
    self.additions = []
    self.connection = connection
    self.creation_time = creation_time
    self.deletions = []
    self.description = description
    self.dns_name = dns_name
    self.id = id
    self.kind = kind
    self.name = name
    self.name_servers = name_servers

  @classmethod
  def from_dict(cls, zone_dict, connection=None):
    """Construct a new zone from a dictionary of data from Cloud DNS.

    :type zone_dict: dict
    :param zone_dict: The dictionary of data to construct a record from.

    :rtype: :class:`Zone`
    :returns: A zone constructed from the data provided.
    """

    return cls(connection=connection,
               creation_time=zone_dict['creationTime'],
               description=zone_dict['description'],
               dns_name=zone_dict['dnsName'], id=zone_dict['id'],
               kind=zone_dict['kind'], name=zone_dict['name'],
               name_servers=zone_dict['nameServers'])

  @property
  def path(self):
    """The URL path to this zone."""

    if not self.connection.project:
      raise ValueError('Cannot determine path without project name.')

    return self.connection.project + '/managedZones/'

  def delete(self, force=False):
    """Delete this zone.

    The zone **must** be empty in order to delete it.

    If you want to delete a non-empty zone you can pass
    in a force parameter set to true.
    This will iterate through the zones's records and delete the related
    records, before deleting the zone.

    :type force: bool
    :param full: If True, deletes the zones's records then deletes it.
    """

    return self.connection.delete_zone(self.name, force=force)

  def save(self):
    """Commit all the additions and deletions of records on this zone.
    """

    change = Change(additions=self.additions, deletions=self.deletions)
    self.connection.save_change(self.name, change.to_dict())
    self.additions = []
    self.deletions = []
    return True

  def add_record(self, record):
    """Add a record to the dict of records to be added to the zone.

    :type record: dict or :class:`Record`
    :param record: A dict representation of a record to be added.
    """

    if isinstance(record, Record):
      record = record.to_dict()

    if isinstance(record, dict):
      self.additions.append(record)

    # Throw type error here.

  def remove_record(self, record):
    """Add a record to the dict of records to be deleted to the zone.

    :type record: dict or :class:`Record`
    :param record: A dict representation of a record to be deleted.
    """

    if isinstance(record, Record):
      record = record.to_dict()

    if isinstance(record, dict):
      self.deletions.append(record)

    # Throw type error here.

  def add_a(self, name, data, ttl):
    """ Shortcut method to add a A record to be added to the zone.
    :type name: string
    :param name: The name of the record, for example 'www.example.com.'.

    :type data: list
    :param data: A list of the textual representation of Resource Records.

    :type ttl: int
    :param ttl: The record's time to live.
    """

    record = Record(name, data, ttl, 'A')
    self.add_record(record)

  def add_aaaa(self, name, data, ttl):
    """ Shortcut method to add a AAAA record to be added to the zone.
    :type name: string
    :param name: The name of the record, for example 'www.example.com.'.

    :type data: list
    :param data: A list of the textual representation of Resource Records.

    :type ttl: int
    :param ttl: The record's time to live.
    """

    record = Record(name, data, ttl, 'AAAA')
    self.add_record(record)

  def add_cname(self, name, data, ttl):
    """ Shortcut method to add a CNAME record to be added to the zone.
    :type name: string
    :param name: The name of the record, for example 'www.example.com.'.

    :type data: list
    :param data: A list of the textual representation of Resource Records.

    :type ttl: int
    :param ttl: The record's time to live.
    """

    record = Record(name, data, ttl, 'CNAME')
    self.add_record(record)

  def add_mx(self, name, data, ttl):
    """ Shortcut method to add a MX record to be added to the zone.
    :type name: string
    :param name: The name of the record, for example 'www.example.com.'.

    :type data: list
    :param data: A list of the textual representation of Resource Records.

    :type ttl: int
    :param ttl: The record's time to live.
    """

    record = Record(name, data, ttl, 'MX')
    self.add_record(record)

  def add_ns(self, name, data, ttl):
    """ Shortcut method to add a NS record to be added to the zone.
    :type name: string
    :param name: The name of the record, for example 'www.example.com.'.

    :type data: list
    :param data: A list of the textual representation of Resource Records.

    :type ttl: int
    :param ttl: The record's time to live.
    """

    record = Record(name, data, ttl, 'NS')
    self.add_record(record)

  def add_ptr(self, name, data, ttl):
    """ Shortcut method to add a PTR record to be added to the zone.
    :type name: string
    :param name: The name of the record, for example 'www.example.com.'.

    :type data: list
    :param data: A list of the textual representation of Resource Records.

    :type ttl: int
    :param ttl: The record's time to live.
    """

    record = Record(name, data, ttl, 'PTR')
    self.add_record(record)

  def add_soa(self, name, data, ttl):
    """ Shortcut method to add a SOA record to be added to the zone.
    :type name: string
    :param name: The name of the record, for example 'www.example.com.'.

    :type data: list
    :param data: A list of the textual representation of Resource Records.

    :type ttl: int
    :param ttl: The record's time to live.
    """

    record = Record(name, data, ttl, 'SOA')
    self.add_record(record)

  def add_spf(self, name, data, ttl):
    """ Shortcut method to add a SRV record to be added to the zone.
    :type name: string
    :param name: The name of the record, for example 'www.example.com.'.

    :type data: list
    :param data: A list of the textual representation of Resource Records.

    :type ttl: int
    :param ttl: The record's time to live.
    """

    record = Record(name, data, ttl, 'SRV')
    self.add_record(record)

  def add_txt(self, name, data, ttl):
    """ Shortcut method to add a TXT record to be added to the zone.
    :type name: string
    :param name: The name of the record, for example 'www.example.com.'.

    :type data: list
    :param data: A list of the textual representation of Resource Records.

    :type ttl: int
    :param ttl: The record's time to live.
    """

    record = Record(name, data, ttl, 'TXT')
    self.add_record(record)
