import json
import urllib

from gcloud import connection
from gcloud.dns import exceptions
from gcloud.dns.project import Project
from gcloud.dns.managed_zone import ManagedZone


class Connection(connection.Connection):

  API_BASE_URL = 'https://www.googleapis.com'
  """The base of the API call URL."""

  API_VERSION = 'v1beta1'
  """The version of the API, used in building the API call's URL."""

  API_URL_TEMPLATE = ('{api_base_url}/dns/{api_version}/projects/{path}')
  """A template used to craft the URL pointing toward a particular API call."""

  _EMPTY = object()
  """A pointer to represent an empty value for default arguments."""

  def __init__(self, project_name=None, *args, **kwargs):

    super(Connection, self).__init__(*args, **kwargs)

    self.project_name = project_name

  def build_api_url(self, path, query_params=None, api_base_url=None,
                    api_version=None):

    url = self.API_URL_TEMPLATE.format(
        api_base_url=(api_base_url or self.API_BASE_URL),
        api_version=(api_version or self.API_VERSION),
        path=path)

    query_params = query_params or {}
    query_params.update({'project': self.project_name})
    url += '?' + urllib.urlencode(query_params)

    return url

  def make_request(self, method, url, data=None, content_type=None,
                   headers=None):

    headers = headers or {}
    headers['Accept-Encoding'] = 'gzip'

    if data:
      content_length = len(str(data))
    else:
      content_length = 0

    headers['Content-Length'] = content_length

    if content_type:
      headers['Content-Type'] = content_type

    return self.http.request(uri=url, method=method, headers=headers,
                             body=data)

  def api_request(self, method, path=None, query_params=None,
                  data=None, content_type=None,
                  api_base_url=None, api_version=None,
                  expect_json=True):

    url = self.build_api_url(path=path, query_params=query_params,
                             api_base_url=api_base_url,
                             api_version=api_version)
    print url
    # Making the executive decision that any dictionary
    # data will be sent properly as JSON.
    if data and isinstance(data, dict):
      data = json.dumps(data)
      content_type = 'application/json'

    response, content = self.make_request(
        method=method, url=url, data=data, content_type=content_type)

    # TODO: Add better error handling.
    if response.status == 404:
      raise exceptions.NotFoundError(response, content)
    elif not 200 <= response.status < 300:
      raise exceptions.ConnectionError(response, content)

    if content and expect_json:
      # TODO: Better checking on this header for JSON.
      content_type = response.get('content-type', '')
      if not content_type.startswith('application/json'):
        raise TypeError('Expected JSON, got %s' % content_type)
      return json.loads(content)

    return content

  def get_project(self, project):
    project = self.new_project(project)
    response = self.api_request(method='GET', path=project.path)
    return Project.from_dict(response, connection=self)

  def new_project(self, project):
    if isinstance(project, Project):
      return project

    # Support Python 2 and 3.
    try:
      string_type = basestring
    except NameError:
      string_type = str

    if isinstance(project, string_type):
      return Project(connection=self)

  def create_managed_zone(self, data):
    managed_zone = self.new_managed_zone(data['name'])
    response = self.api_request(method='POST', path=managed_zone.path,
                                data=data)
    return ManagedZone.from_dict(response, connection=self)

  def delete_managed_zone(self, managed_zone):
    managed_zone = self.new_managed_zone(managed_zone)
    self.api_request(method='DELETE', path=managed_zone.path +
                     managed_zone.name)
    return True

  def get_managed_zone(self, managed_zone):
    managed_zone = self.new_managed_zone(managed_zone)
    response = self.api_request(method='GET', path=managed_zone.path)
    return ManagedZone.from_dict(response['managedZones'][0],
                                 connection=self)

  def list_managed_zones(self):
    managed_zone = self.new_managed_zone('test')
    response = self.api_request(method='GET', path=managed_zone.path)
    print json.dumps(response, indent=2)

  def new_managed_zone(self, managed_zone):
    if isinstance(managed_zone, ManagedZone):
      return managed_zone

    # Support Python 2 and 3.
    try:
      string_type = basestring
    except NameError:
      string_type = str

    if isinstance(managed_zone, string_type):
      return ManagedZone(connection=self, name=managed_zone)
