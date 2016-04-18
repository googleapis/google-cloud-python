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

"""Client for interacting with the Google Cloud DNS API."""


from gcloud.client import JSONClient
from gcloud.dns.connection import Connection
from gcloud.dns.zone import ManagedZone


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: string
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a zone.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def quotas(self):
        """Return DNS quots for the project associated with this client.

        See:
        https://cloud.google.com/dns/api/v1/projects/get

        :rtype: mapping
        :returns: keys for the mapping correspond to those of the ``quota``
                  sub-mapping of the project resource.
        """
        path = '/projects/%s' % (self.project,)
        resp = self.connection.api_request(method='GET', path=path)

        return dict([(key, int(value))
                     for key, value in resp['quota'].items() if key != 'kind'])

    def list_zones(self, max_results=None, page_token=None):
        """List zones for the project associated with this client.

        See:
        https://cloud.google.com/dns/api/v1/managedZones/list

        :type max_results: int
        :param max_results: maximum number of zones to return, If not
                            passed, defaults to a value set by the API.

        :type page_token: string
        :param page_token: opaque marker for the next "page" of zones. If
                           not passed, the API will return the first page of
                           zones.

        :rtype: tuple, (list, str)
        :returns: list of :class:`gcloud.dns.zone.ManagedZone`, plus a
                  "next page token" string:  if the token is not None,
                  indicates that more zones can be retrieved with another
                  call (pass that value as ``page_token``).
        """
        params = {}

        if max_results is not None:
            params['maxResults'] = max_results

        if page_token is not None:
            params['pageToken'] = page_token

        path = '/projects/%s/managedZones' % (self.project,)
        resp = self.connection.api_request(method='GET', path=path,
                                           query_params=params)
        zones = [ManagedZone.from_api_repr(resource, self)
                 for resource in resp['managedZones']]
        return zones, resp.get('nextPageToken')

    def zone(self, name, dns_name=None, description=None):
        """Construct a zone bound to this client.

        :type name: string
        :param name: Name of the zone.

        :type dns_name: string or :class:`NoneType`
        :param dns_name: DNS name of the zone.  If not passed, then calls
                         to :meth:`zone.create` will fail.

        :type description: string or :class:`NoneType`
        :param description: the description for the zone.  If not passed,
                            defaults to the value of 'dns_name'.

        :rtype: :class:`gcloud.dns.zone.ManagedZone`
        :returns: a new ``ManagedZone`` instance
        """
        return ManagedZone(name, dns_name, client=self,
                           description=description)
