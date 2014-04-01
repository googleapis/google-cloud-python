class Change(object):
  """A class representing a Change on Cloud DNS.

  :type additions: list
  :param name: A list of records slated to be added to a zone.

  :type deletions: list
  :param data: A list of records slated to be deleted to a zone.
  """

  def __init__(self, additions=None, deletions=None):
    self.additions = additions
    self.deletions = deletions

  def to_dict(self):
    """Format the change into a dict compatible with Cloud DNS.

    :rtype: dict
    :returns: A Cloud DNS dict representation of a change.
    """
    return {'additions': self.additions, 'deletions': self.deletions}
