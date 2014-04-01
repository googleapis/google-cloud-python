class Changes(object):

  def __init__(self, connection=None, additions=None, deletions=None, id=None,
               kind=None, status=None):
    self.connection = connection
    self.additions = additions
    self.deletions = deletions
    self.id = id
    self.kind = kind
    self.status = status
