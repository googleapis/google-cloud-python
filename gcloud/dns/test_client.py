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

import unittest2


class TestClient(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.dns.client import Client
        return Client

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor(self):
        from gcloud.dns.connection import Connection
        PROJECT = 'PROJECT'
        creds = _Credentials()
        http = object()
        client = self._makeOne(project=PROJECT, credentials=creds, http=http)
        self.assertTrue(isinstance(client.connection, Connection))
        self.assertTrue(client.connection.credentials is creds)
        self.assertTrue(client.connection.http is http)

    def test_quotas_defaults(self):
        PROJECT = 'PROJECT'
        PATH = 'projects/%s' % PROJECT
        MANAGED_ZONES = 1234
        RRS_PER_RRSET = 23
        RRSETS_PER_ZONE = 345
        RRSET_ADDITIONS = 456
        RRSET_DELETIONS = 567
        TOTAL_SIZE = 67890
        DATA = {
            'quota': {
                'managedZones': str(MANAGED_ZONES),
                'resourceRecordsPerRrset': str(RRS_PER_RRSET),
                'rrsetsPerManagedZone': str(RRSETS_PER_ZONE),
                'rrsetAdditionsPerChange': str(RRSET_ADDITIONS),
                'rrsetDeletionsPerChange': str(RRSET_DELETIONS),
                'totalRrdataSizePerChange': str(TOTAL_SIZE),
            }
        }
        CONVERTED = dict([(key, int(value))
                          for key, value in DATA['quota'].items()])
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        quotas = client.quotas()

        self.assertEqual(quotas, CONVERTED)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_quotas_w_kind_key(self):
        PROJECT = 'PROJECT'
        PATH = 'projects/%s' % PROJECT
        MANAGED_ZONES = 1234
        RRS_PER_RRSET = 23
        RRSETS_PER_ZONE = 345
        RRSET_ADDITIONS = 456
        RRSET_DELETIONS = 567
        TOTAL_SIZE = 67890
        DATA = {
            'quota': {
                'managedZones': str(MANAGED_ZONES),
                'resourceRecordsPerRrset': str(RRS_PER_RRSET),
                'rrsetsPerManagedZone': str(RRSETS_PER_ZONE),
                'rrsetAdditionsPerChange': str(RRSET_ADDITIONS),
                'rrsetDeletionsPerChange': str(RRSET_DELETIONS),
                'totalRrdataSizePerChange': str(TOTAL_SIZE),
            }
        }
        CONVERTED = dict([(key, int(value))
                          for key, value in DATA['quota'].items()])
        WITH_KIND = {'quota': DATA['quota'].copy()}
        WITH_KIND['quota']['kind'] = 'dns#quota'
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(WITH_KIND)

        quotas = client.quotas()

        self.assertEqual(quotas, CONVERTED)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_zones_defaults(self):
        from gcloud.dns.zone import ManagedZone
        PROJECT = 'PROJECT'
        ID_1 = '123'
        ZONE_1 = 'zone_one'
        DNS_1 = 'one.example.com'
        ID_2 = '234'
        ZONE_2 = 'zone_two'
        DNS_2 = 'two.example.com'
        PATH = 'projects/%s/managedZones' % PROJECT
        TOKEN = 'TOKEN'
        DATA = {
            'nextPageToken': TOKEN,
            'managedZones': [
                {'kind': 'dns#managedZone',
                 'id': ID_1,
                 'name': ZONE_1,
                 'dnsName': DNS_1},
                {'kind': 'dns#managedZone',
                 'id': ID_2,
                 'name': ZONE_2,
                 'dnsName': DNS_2},
            ]
        }
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        zones, token = client.list_zones()

        self.assertEqual(len(zones), len(DATA['managedZones']))
        for found, expected in zip(zones, DATA['managedZones']):
            self.assertTrue(isinstance(found, ManagedZone))
            self.assertEqual(found.zone_id, expected['id'])
            self.assertEqual(found.name, expected['name'])
            self.assertEqual(found.dns_name, expected['dnsName'])
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_zones_explicit(self):
        from gcloud.dns.zone import ManagedZone
        PROJECT = 'PROJECT'
        ID_1 = '123'
        ZONE_1 = 'zone_one'
        DNS_1 = 'one.example.com'
        ID_2 = '234'
        ZONE_2 = 'zone_two'
        DNS_2 = 'two.example.com'
        PATH = 'projects/%s/managedZones' % PROJECT
        TOKEN = 'TOKEN'
        DATA = {
            'managedZones': [
                {'kind': 'dns#managedZone',
                 'id': ID_1,
                 'name': ZONE_1,
                 'dnsName': DNS_1},
                {'kind': 'dns#managedZone',
                 'id': ID_2,
                 'name': ZONE_2,
                 'dnsName': DNS_2},
            ]
        }
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        conn = client.connection = _Connection(DATA)

        zones, token = client.list_zones(max_results=3, page_token=TOKEN)

        self.assertEqual(len(zones), len(DATA['managedZones']))
        for found, expected in zip(zones, DATA['managedZones']):
            self.assertTrue(isinstance(found, ManagedZone))
            self.assertEqual(found.zone_id, expected['id'])
            self.assertEqual(found.name, expected['name'])
            self.assertEqual(found.dns_name, expected['dnsName'])
        self.assertEqual(token, None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'maxResults': 3, 'pageToken': TOKEN})

    def test_zone(self):
        from gcloud.dns.zone import ManagedZone
        PROJECT = 'PROJECT'
        ZONE_NAME = 'zone-name'
        DNS_NAME = 'test.example.com'
        creds = _Credentials()
        client = self._makeOne(PROJECT, creds)
        zone = client.zone(ZONE_NAME, DNS_NAME)
        self.assertTrue(isinstance(zone, ManagedZone))
        self.assertEqual(zone.name, ZONE_NAME)
        self.assertEqual(zone.dns_name, DNS_NAME)
        self.assertTrue(zone._client is client)

    def test_get_zone_miss(self):
        from gcloud.exceptions import NotFound

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        NONESUCH = 'nonesuch'
        URI = '/'.join([
            client.connection.API_BASE_URL,
            'dns',
            client.connection.API_VERSION,
            'projects',
            PROJECT,
            'managedZones',
            'nonesuch',
        ])
        http = client.connection._http = _Http(
            {'status': '404', 'content-type': 'application/json'},
            b'{}',
        )
        self.assertRaises(NotFound, client.get_zone, NONESUCH)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)

    def test_get_zone_hit(self):
        from gcloud.dns.zone import ManagedZone

        PROJECT = 'PROJECT'
        CREDENTIALS = _Credentials()
        client = self._makeOne(project=PROJECT, credentials=CREDENTIALS)

        ZONE_NAME = 'zone-name'
        ZONE_DNS_NAME = 'example.com.'
        URI = '/'.join([
            client.connection.API_BASE_URL,
            'dns',
            client.connection.API_VERSION,
            'projects',
            PROJECT,
            'managedZones',
            ZONE_NAME
        ])
        http = client.connection._http = _Http(
            {'status': '200', 'content-type': 'application/json'},
            '{{"name": "{0}", "dnsName": "{1}"}}'.format(
                ZONE_NAME, ZONE_DNS_NAME).encode('utf-8'),
        )

        zone = client.get_zone(ZONE_NAME)
        self.assertTrue(isinstance(zone, ManagedZone))
        self.assertEqual(zone.name, ZONE_NAME)
        self.assertEqual(zone.dns_name, ZONE_DNS_NAME)
        self.assertEqual(http._called_with['method'], 'GET')
        self.assertEqual(http._called_with['uri'], URI)


class _Credentials(object):

    _scopes = None

    @staticmethod
    def create_scoped_required():
        return True

    def create_scoped(self, scope):
        self._scopes = scope
        return self


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        self._requested.append(kw)
        response, self._responses = self._responses[0], self._responses[1:]
        return response


class _Http(object):

    _called_with = None

    def __init__(self, headers, content):
        from httplib2 import Response
        self._response = Response(headers)
        self._content = content

    def request(self, **kw):
        self._called_with = kw
        return self._response, self._content
