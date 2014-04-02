import json

from gcloud import connection
from gcloud.dns.zone import Zone


class Connection(connection.JsonConnection):
  API_VERSION = 'v1beta1'
  """The version of the API, used in building the API call's URL."""

  API_URL_TEMPLATE = ('{api_base_url}/dns/{api_version}/projects/{path}')
  """A template used to craft the URL pointing toward a particular API call."""

  _EMPTY = object()
  """A pointer to represent an empty value for default arguments."""

  def __init__(self, project_id=None, *args, **kwargs):

    super(Connection, self).__init__(*args, **kwargs)

    self.project_id = project_id

  def create_zone(self, data):
    zone = self.new_zone(data['name'])
    response = self.api_request(method='POST', path=zone.path,
                                data=data)
    return Zone.from_dict(response, connection=self)

  def delete_zone(self, zone):
    zone = self.new_zone(zone)
    self.api_request(method='DELETE', path=zone.path +
                     zone.name)
    return True

  def get_zone(self, zone):
    zone = self.new_zone(zone)
    response = self.api_request(method='GET', path=zone.path)
    return Zone.from_dict(response['managedZones'][0],
                          connection=self)

  def list_zones(self):
    zone = self.new_zone('test')
    response = self.api_request(method='GET', path=zone.path)
    print json.dumps(response, indent=2)

  def new_zone(self, zone):
    if isinstance(zone, Zone):
      return zone

    # Support Python 2 and 3.
    try:
      string_type = basestring
    except NameError:
      string_type = str

    if isinstance(zone, string_type):
      return Zone(connection=self, name=zone)

  def create_changes(self, zone, data):
    zone = self.new_zone(zone)
    self.api_request(method='POST', path=zone.path + zone.name + '/changes',
                     data=data)
    return True
