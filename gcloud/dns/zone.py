# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Define API ManagedZones."""
import six

from gcloud._helpers import _rfc3339_to_datetime
from gcloud.exceptions import NotFound
from gcloud.dns.changes import Changes
from gcloud.dns.resource_record_set import ResourceRecordSet


class ManagedZone(object):
    """ManagedZones are containers for DNS resource records.

    See:
    https://cloud.google.com/dns/api/v1/managedZones

    :type name: string
    :param name: the name of the zone

    :type dns_name: string or :class:`NoneType`
    :param dns_name: the DNS name of the zone.  If not passed, then calls
                     to :meth:`create` will fail.

    :type client: :class:`gcloud.dns.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the zone (which requires a project).

    :type description: string or :class:`NoneType`
    :param description: the description for the zone.  If not passed, defaults
                        to the value of 'dns_name'.
    """

    def __init__(self, name, dns_name=None, client=None, description=None):
        self.name = name
        self.dns_name = dns_name
        self._client = client
        self._properties = {}
        if description is None:
            description = dns_name
        self.description = description

    @classmethod
    def from_api_repr(cls, resource, client):
        """Factory:  construct a zone given its API representation

        :type resource: dict
        :param resource: zone resource representation returned from the API

        :type client: :class:`gcloud.dns.client.Client`
        :param client: Client which holds credentials and project
                       configuration for the zone.

        :rtype: :class:`gcloud.dns.zone.ManagedZone`
        :returns: Zone parsed from ``resource``.
        """
        name = resource.get('name')
        dns_name = resource.get('dnsName')
        if name is None or dns_name is None:
            raise KeyError('Resource lacks required identity information:'
                           '["name"]["dnsName"]')
        zone = cls(name, dns_name, client=client)
        zone._set_properties(resource)
        return zone

    @property
    def project(self):
        """Project bound to the zone.

        :rtype: string
        :returns: the project (derived from the client).
        """
        return self._client.project

    @property
    def path(self):
        """URL path for the zone's APIs.

        :rtype: string
        :returns: the path based on project and dataste name.
        """
        return '/projects/%s/managedZones/%s' % (self.project, self.name)

    @property
    def created(self):
        """Datetime at which the zone was created.

        :rtype: ``datetime.datetime``, or ``NoneType``
        :returns: the creation time (None until set from the server).
        """
        return self._properties.get('creationTime')

    @property
    def name_servers(self):
        """Datetime at which the zone was created.

        :rtype: list of strings, or ``NoneType``.
        :returns: the assigned name servers (None until set from the server).
        """
        return self._properties.get('nameServers')

    @property
    def zone_id(self):
        """ID for the zone resource.

        :rtype: string, or ``NoneType``
        :returns: the ID (None until set from the server).
        """
        return self._properties.get('id')

    @property
    def description(self):
        """Description of the zone.

        :rtype: string, or ``NoneType``
        :returns: The description as set by the user, or None (the default).
        """
        return self._properties.get('description')

    @description.setter
    def description(self, value):
        """Update description of the zone.

        :type value: string, or ``NoneType``
        :param value: new description

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['description'] = value

    @property
    def name_server_set(self):
        """Named set of DNS name servers that all host the same ManagedZones.

        Most users will leave this blank.

        See:
        https://cloud.google.com/dns/api/v1/managedZones#nameServerSet

        :rtype: string, or ``NoneType``
        :returns: The name as set by the user, or None (the default).
        """
        return self._properties.get('nameServerSet')

    @name_server_set.setter
    def name_server_set(self, value):
        """Update named set of DNS name servers.

        :type value: string, or ``NoneType``
        :param value: new title

        :raises: ValueError for invalid value types.
        """
        if not isinstance(value, six.string_types) and value is not None:
            raise ValueError("Pass a string, or None")
        self._properties['nameServerSet'] = value

    def resource_record_set(self, name, record_type, ttl, rrdatas):
        """Construct a resource record set bound to this zone.

        :type name: string
        :param name: Name of the record set.

        :type record_type: string
        :param record_type: RR type

        :type ttl: integer
        :param ttl: TTL for the RR, in seconds

        :type rrdatas: list of string
        :param rrdatas: resource data for the RR

        :rtype: :class:`gcloud.dns.resource_record_set.ResourceRecordSet`
        :returns: a new ``ResourceRecordSet`` instance
        """
        return ResourceRecordSet(name, record_type, ttl, rrdatas, zone=self)

    def changes(self):
        """Construct a change set bound to this zone.

        :rtype: :class:`gcloud.dns.changes.Changes`
        :returns: a new ``Changes`` instance
        """
        return Changes(zone=self)

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.dns.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current zone.

        :rtype: :class:`gcloud.dns.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def _set_properties(self, api_response):
        """Update properties from resource in body of ``api_response``

        :type api_response: httplib2.Response
        :param api_response: response returned from an API call
        """
        self._properties.clear()
        cleaned = api_response.copy()
        self.dns_name = cleaned.pop('dnsName', None)
        if 'creationTime' in cleaned:
            cleaned['creationTime'] = _rfc3339_to_datetime(
                cleaned['creationTime'])
        self._properties.update(cleaned)

    def _build_resource(self):
        """Generate a resource for ``create`` or ``update``."""
        resource = {
            'name': self.name,
        }

        if self.dns_name is not None:
            resource['dnsName'] = self.dns_name

        if self.description is not None:
            resource['description'] = self.description

        if self.name_server_set is not None:
            resource['nameServerSet'] = self.name_server_set

        return resource

    def create(self, client=None):
        """API call:  create the zone via a PUT request

        See:
        https://cloud.google.com/dns/api/v1/managedZones/create

        :type client: :class:`gcloud.dns.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current zone.
        """
        client = self._require_client(client)
        path = '/projects/%s/managedZones' % (self.project,)
        api_response = client.connection.api_request(
            method='POST', path=path, data=self._build_resource())
        self._set_properties(api_response)

    def exists(self, client=None):
        """API call:  test for the existence of the zone via a GET request

        See
        https://cloud.google.com/dns/api/v1/managedZones/get

        :type client: :class:`gcloud.dns.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current zone.

        :rtype: bool
        :returns: Boolean indicating existence of the managed zone.
        """
        client = self._require_client(client)

        try:
            client.connection.api_request(method='GET', path=self.path,
                                          query_params={'fields': 'id'})
        except NotFound:
            return False
        else:
            return True

    def reload(self, client=None):
        """API call:  refresh zone properties via a GET request

        See
        https://cloud.google.com/dns/api/v1/managedZones/get

        :type client: :class:`gcloud.dns.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current zone.
        """
        client = self._require_client(client)

        api_response = client.connection.api_request(
            method='GET', path=self.path)
        self._set_properties(api_response)

    def delete(self, client=None):
        """API call:  delete the zone via a DELETE request

        See:
        https://cloud.google.com/dns/api/v1/managedZones/delete

        :type client: :class:`gcloud.dns.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current zone.
        """
        client = self._require_client(client)
        client.connection.api_request(method='DELETE', path=self.path)

    def list_resource_record_sets(self, max_results=None, page_token=None,
                                  client=None):
        """List resource record sets for this zone.

        See:
        https://cloud.google.com/dns/api/v1/resourceRecordSets/list

        :type max_results: int
        :param max_results: maximum number of zones to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of zones. If
                           not passed, the API will return the first page of
                           zones.

        :type client: :class:`gcloud.dns.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current zone.

        :rtype: tuple, (list, str)
        :returns: list of
                  :class:`gcloud.dns.resource_record_set.ResourceRecordSet`,
                  plus a "next page token" string:  if the token is not None,
                  indicates that more zones can be retrieved with another
                  call (pass that value as ``page_token``).
        """
        params = {}

        if max_results is not None:
            params['maxResults'] = max_results

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/managedZones/%s/rrsets' % (
            self.project, self.name)
        client = self._require_client(client)
        conn = client.connection
        resp = conn.api_request(method='GET', path=path, query_params=params)
        zones = [ResourceRecordSet.from_api_repr(resource, self)
                 for resource in resp['rrsets']]
        return zones, resp.get('nextPageToken')

    def list_changes(self, max_results=None, page_token=None, client=None):
        """List change sets for this zone.

        See:
        https://cloud.google.com/dns/api/v1/resourceRecordSets/list

        :type max_results: int
        :param max_results: maximum number of zones to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of zones. If
                           not passed, the API will return the first page of
                           zones.

        :type client: :class:`gcloud.dns.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current zone.

        :rtype: tuple, (list, str)
        :returns: list of
                  :class:`gcloud.dns.resource_record_set.ResourceRecordSet`,
                  plus a "next page token" string:  if the token is not None,
                  indicates that more zones can be retrieved with another
                  call (pass that value as ``page_token``).
        """
        params = {}

        if max_results is not None:
            params['maxResults'] = max_results

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/managedZones/%s/changes' % (
            self.project, self.name)
        client = self._require_client(client)
        conn = client.connection
        resp = conn.api_request(method='GET', path=path, query_params=params)
        zones = [Changes.from_api_repr(resource, self)
                 for resource in resp['changes']]
        return zones, resp.get('nextPageToken')
