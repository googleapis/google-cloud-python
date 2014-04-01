from gcloud import connection
from gcloud.dns.record import Record
from gcloud.dns.zone import Zone


class Connection(connection.JsonConnection):
  """A connection to Google Cloud DNS via the JSON REST API.

  See :class:`gcloud.connection.JsonConnection` for a full list of parameters.
  :class:`Connection` differs only in needing a project name
  (which you specify when creating a project in the Cloud Console).
  """

  API_VERSION = 'v1beta1'
  """The version of the API, used in building the API call's URL."""

  API_URL_TEMPLATE = ('{api_base_url}/dns/{api_version}/projects/{path}')
  """A template used to craft the URL pointing toward a particular API call."""

  _EMPTY = object()
  """A pointer to represent an empty value for default arguments."""

  def __init__(self, project=None, *args, **kwargs):
    """
    :type project: string
    :param project: The project name to connect to.
    """

    super(Connection, self).__init__(*args, **kwargs)

    self.project = project

  def new_zone(self, zone):
    """Factory method for creating a new (unsaved) zone object.

    :type zone: string or :class:`gcloud.dns.zone.Zone`
    :param zone: A name of a zone or an existing Zone object.
    """

    if isinstance(zone, Zone):
      return zone

    # Support Python 2 and 3.
    try:
      string_type = basestring
    except NameError:
      string_type = str

    if isinstance(zone, string_type):
      return Zone(connection=self, name=zone)

  def create_zone(self, zone, dns_name, description):
    """Create a new zone.

    :type zone: string or :class:`gcloud.dns.zone.Zone`
    :param zone: The zone name (or zone object) to create.

    :rtype: :class:`gcloud.dns.zone.Zone`
    :returns: The newly created zone.
    """

    zone = self.new_zone(zone)
    response = self.api_request(method='POST', path=zone.path,
                                data={'name': zone.name, 'dnsName': dns_name,
                                      'description': description})
    return Zone.from_dict(response, connection=self)

  def delete_zone(self, zone, force=False):
    """Delete a zone.

    You can use this method to delete a zone by name,
    or to delete a zone object::

      >>> from gcloud import dns
      >>> connection = dns.get_connection(project, email, key_path)
      >>> connection.delete_zone('my-zone')
      True

    You can also delete pass in the zone object::

      >>> zone = connection.get_zone('other-zone')
      >>> connection.delete_zone(zone)
      True

    :type zone: string or :class:`gcloud.dns.zone.Zone`
    :param zone: The zone name (or zone object) to create.

    :type force: bool
    :param full: If True, deletes the zones's recordss then deletes it.

    :rtype: bool
    :returns: True if the zone was deleted.
    """

    zone = self.new_zone(zone)

    if force:
      rrsets = self.get_records(zone)
      for rrset in rrsets['rrsets']:
        record = Record.from_dict(rrset)
        if record.type != 'NS' and record.type != 'SOA':
          zone.remove_record(record)
      zone.save()

    self.api_request(method='DELETE', path=zone.path + zone.name)
    return True

  def get_zone(self, zone):
    """Get a zone by name.

    :type zone: string
    :param zone: The name of the zone to get.

    :rtype: :class:`gcloud.dns.zone.Zone`
    :returns: The zone matching the name provided.
    """

    zone = self.new_zone(zone)
    response = self.api_request(method='GET', path=zone.path)
    return Zone.from_dict(response['managedZones'][0], connection=self)

  def get_records(self, zone):
    """Get a list of resource records on a zone.

    :type zone: string or :class:`gcloud.dns.zone.Zone`
    :param zone: The zone name (or zone object) to get records from.
    """

    zone = self.new_zone(zone)
    return self.api_request(method='GET', path=zone.path + zone.name +
                            '/rrsets')

  def save_change(self, zone, change):
    """Save a set of changes to a zone.

    :type zone: string or :class:`gcloud.dns.zone.Zone`
    :param zone: The zone name (or zone object) to save to.

    :type change: dict
    :param dict: A dict with the addition and deletion lists of records.
    """

    zone = self.new_zone(zone)
    return self.api_request(method='POST', path=zone.path + zone.name +
                            '/changes', data=change)
