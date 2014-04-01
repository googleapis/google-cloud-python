class Project(object):

  def __init__(self, connection=None, id=None, kind=None, number=None,
               quota=None):

    self.connection = connection
    self.id = id
    self.kind = kind
    self.number = number
    self.quota = quota

  @classmethod
  def from_dict(cls, project_dict, connection=None):

    return cls(connection=connection, id=project_dict['id'],
               kind=project_dict['kind'], number=project_dict['number'],
               quota=project_dict['quota'])

  @property
  def path(self):
    """The URL path to this instances."""

    if not self.connection.project_id:
      raise ValueError('Cannot determine path without project name.')

    return self.connection.project_id


  def get(self):
    return self.connection.get_project(self)
