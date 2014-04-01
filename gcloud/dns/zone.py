class Zone(object):

  def __init__(self, connection=None, creationTime=None, description=None,
               dnsName=None, id=None, kind=None, name=None, nameServers=None):
    self.connection = connection
    self.creationTime = creationTime
    self.description = description
    self.dnsName = dnsName
    self.id = id
    self.kind = kind
    self.name = name
    self.nameServers = nameServers

  @classmethod
  def from_dict(cls, zone_dict, connection=None):

    return cls(connection=connection,
               creationTime=zone_dict['creationTime'],
               description=zone_dict['description'],
               dnsName=zone_dict['dnsName'],
               id=zone_dict['id'],
               kind=zone_dict['kind'], name=zone_dict['name'],
               nameServers=zone_dict['nameServers'])

  @property
  def path(self):
    """The URL path to this zone."""

    if not self.connection.project_id:
      raise ValueError('Cannot determine path without project name.')

    return self.connection.project_id + '/managedZones/'

  def delete(self):
    return self.connection.delete_zone(self)

  def get(self):
    return self.connection.get_zone(self)
