class Zone(object):

  def __init__(self, connection=None, creation_time=None, description=None,
               dns_name=None, id=None, kind=None, name=None,
               name_servers=None):
    self.connection = connection
    self.creation_time = creation_time
    self.description = description
    self.dns_name = dns_name
    self.id = id
    self.kind = kind
    self.name = name
    self.name_servers = name_servers

  @classmethod
  def from_dict(cls, zone_dict, connection=None):

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

  def delete(self):
    return self.connection.delete_zone(self)

  def get(self):
    return self.connection.get_zone(self)
