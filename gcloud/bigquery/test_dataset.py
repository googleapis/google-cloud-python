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


class TestDataset(unittest2.TestCase):
    PROJECT = 'project'
    DS_NAME = 'dataset-name'

    def _getTargetClass(self):
        from gcloud.bigquery.dataset import Dataset
        return Dataset

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _makeResource(self):
        import datetime
        import pytz
        self.WHEN_TS = 1437767599.006
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(
            tzinfo=pytz.UTC)
        self.ETAG = 'ETAG'
        self.DS_ID = '%s:%s' % (self.PROJECT, self.DS_NAME)
        self.RESOURCE_URL = 'http://example.com/path/to/resource'
        return {
            'creationTime': self.WHEN_TS * 1000,
            'datasetReference':
                {'projectId': self.PROJECT, 'datasetId': self.DS_NAME},
            'etag': 'ETAG',
            'id': self.DS_ID,
            'lastModifiedTime': self.WHEN_TS * 1000,
            'location': 'US',
            'selfLink': self.RESOURCE_URL,
        }

    def _verifyResourceProperties(self, dataset, resource):
        self.assertEqual(dataset.created, self.WHEN)
        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.etag, self.ETAG)
        self.assertEqual(dataset.modified, self.WHEN)
        self.assertEqual(dataset.self_link, self.RESOURCE_URL)

        self.assertEqual(dataset.default_table_expiration_ms,
                         resource.get('defaultTableExpirationMs'))
        self.assertEqual(dataset.description, resource.get('description'))
        self.assertEqual(dataset.friendly_name, resource.get('friendlyName'))
        self.assertEqual(dataset.location, resource.get('location'))

    def test_ctor(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        self.assertEqual(dataset.name, self.DS_NAME)
        self.assertTrue(dataset._client is client)
        self.assertEqual(dataset.project, client.project)
        self.assertEqual(
            dataset.path,
            '/projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME))

        self.assertEqual(dataset.created, None)
        self.assertEqual(dataset.dataset_id, None)
        self.assertEqual(dataset.etag, None)
        self.assertEqual(dataset.modified, None)
        self.assertEqual(dataset.self_link, None)

        self.assertEqual(dataset.default_table_expiration_ms, None)
        self.assertEqual(dataset.description, None)
        self.assertEqual(dataset.friendly_name, None)
        self.assertEqual(dataset.location, None)

    def test_default_table_expiration_ms_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        with self.assertRaises(ValueError):
            dataset.default_table_expiration_ms = 'bogus'

    def test_default_table_expiration_ms_setter(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        dataset.default_table_expiration_ms = 12345
        self.assertEqual(dataset.default_table_expiration_ms, 12345)

    def test_description_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        with self.assertRaises(ValueError):
            dataset.description = 12345

    def test_description_setter(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        dataset.description = 'DESCRIPTION'
        self.assertEqual(dataset.description, 'DESCRIPTION')

    def test_friendly_name_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        with self.assertRaises(ValueError):
            dataset.friendly_name = 12345

    def test_friendly_name_setter(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        dataset.friendly_name = 'FRIENDLY'
        self.assertEqual(dataset.friendly_name, 'FRIENDLY')

    def test_location_setter_bad_value(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        with self.assertRaises(ValueError):
            dataset.location = 12345

    def test_location_setter(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        dataset.location = 'LOCATION'
        self.assertEqual(dataset.location, 'LOCATION')

    def test_create_w_bound_client(self):
        PATH = 'projects/%s/datasets' % self.PROJECT
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT)

        dataset.create()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'datasetReference':
                {'projectId': self.PROJECT, 'datasetId': self.DS_NAME},
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_create_w_alternate_client(self):
        PATH = 'projects/%s/datasets' % self.PROJECT
        DESCRIPTION = 'DESCRIPTION'
        TITLE = 'TITLE'
        RESOURCE = self._makeResource()
        RESOURCE['description'] = DESCRIPTION
        RESOURCE['friendlyName'] = TITLE
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT1)
        dataset.friendly_name = TITLE
        dataset.description = DESCRIPTION

        dataset.create(client=CLIENT2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'datasetReference':
                {'projectId': self.PROJECT, 'datasetId': self.DS_NAME},
            'description': DESCRIPTION,
            'friendlyName': TITLE,
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        conn = _Connection()
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT)

        self.assertFalse(dataset.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_exists_hit_w_alternate_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT1)

        self.assertTrue(dataset.exists(client=CLIENT2))

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_reload_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT)

        dataset.reload()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        RESOURCE = self._makeResource()
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT1)

        dataset.reload(client=CLIENT2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_patch_w_invalid_expiration(self):
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT)

        with self.assertRaises(ValueError):
            dataset.patch(default_table_expiration_ms='BOGUS')

    def test_patch_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        DESCRIPTION = 'DESCRIPTION'
        TITLE = 'TITLE'
        RESOURCE = self._makeResource()
        RESOURCE['description'] = DESCRIPTION
        RESOURCE['friendlyName'] = TITLE
        conn = _Connection(RESOURCE)
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT)

        dataset.patch(description=DESCRIPTION, friendly_name=TITLE)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        SENT = {
            'description': DESCRIPTION,
            'friendlyName': TITLE,
        }
        self.assertEqual(req['data'], SENT)
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_patch_w_alternate_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        DEF_TABLE_EXP = 12345
        LOCATION = 'EU'
        RESOURCE = self._makeResource()
        RESOURCE['defaultTableExpirationMs'] = DEF_TABLE_EXP
        RESOURCE['location'] = LOCATION
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT1)

        dataset.patch(client=CLIENT2,
                      default_table_expiration_ms=DEF_TABLE_EXP,
                      location=LOCATION)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'PATCH')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'defaultTableExpirationMs': DEF_TABLE_EXP,
            'location': LOCATION,
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_update_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        DESCRIPTION = 'DESCRIPTION'
        TITLE = 'TITLE'
        RESOURCE = self._makeResource()
        RESOURCE['description'] = DESCRIPTION
        RESOURCE['friendlyName'] = TITLE
        conn = _Connection(RESOURCE)
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT)
        dataset.description = DESCRIPTION
        dataset.friendly_name = TITLE

        dataset.update()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'PUT')
        SENT = {
            'datasetReference':
                {'projectId': self.PROJECT, 'datasetId': self.DS_NAME},
            'description': DESCRIPTION,
            'friendlyName': TITLE,
        }
        self.assertEqual(req['data'], SENT)
        self.assertEqual(req['path'], '/%s' % PATH)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_update_w_alternate_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        DEF_TABLE_EXP = 12345
        LOCATION = 'EU'
        RESOURCE = self._makeResource()
        RESOURCE['defaultTableExpirationMs'] = 12345
        RESOURCE['location'] = LOCATION
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection(RESOURCE)
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT1)
        dataset.default_table_expiration_ms = DEF_TABLE_EXP
        dataset.location = LOCATION

        dataset.update(client=CLIENT2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'PUT')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'datasetReference':
                {'projectId': self.PROJECT, 'datasetId': self.DS_NAME},
            'defaultTableExpirationMs': 12345,
            'location': 'EU',
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_delete_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        conn = _Connection({})
        CLIENT = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT)

        dataset.delete()

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_delete_w_alternate_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        conn1 = _Connection()
        CLIENT1 = _Client(project=self.PROJECT, connection=conn1)
        conn2 = _Connection({})
        CLIENT2 = _Client(project=self.PROJECT, connection=conn2)
        dataset = self._makeOne(self.DS_NAME, client=CLIENT1)

        dataset.delete(client=CLIENT2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'DELETE')
        self.assertEqual(req['path'], '/%s' % PATH)


class _Client(object):

    def __init__(self, project='project', connection=None):
        self.project = project
        self.connection = connection


class _Connection(object):

    def __init__(self, *responses):
        self._responses = responses
        self._requested = []

    def api_request(self, **kw):
        from gcloud.exceptions import NotFound
        self._requested.append(kw)

        try:
            response, self._responses = self._responses[0], self._responses[1:]
        except:
            raise NotFound('miss')
        else:
            return response
