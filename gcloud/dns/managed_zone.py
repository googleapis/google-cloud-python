class ManagedZone(object):

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

  @property
  def path(self):
    """The URL path to this managed zone."""

    if not self.connection.project_name:
      raise ValueError('Cannot determine path without project name.')

    return self.connection.project_name + '/managedZones/'

  @classmethod
  def from_dict(cls, managed_zone_dict, connection=None):

    return cls(connection=connection,
               creationTime=managed_zone_dict['creationTime'],
               description=managed_zone_dict['description'],
               dnsName=managed_zone_dict['dnsName'],
               id=managed_zone_dict['id'],
               kind=managed_zone_dict['kind'], name=managed_zone_dict['name'],
               nameServers=managed_zone_dict['nameServers'])

  def delete(self):
    return self.connection.delete_managed_zone(self)

  def get(self):
    return self.connection.get_managed_zone(self)
