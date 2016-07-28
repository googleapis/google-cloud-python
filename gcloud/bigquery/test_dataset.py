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


class TestAccessGrant(unittest2.TestCase):

    def _getTargetClass(self):
        from gcloud.bigquery.dataset import AccessGrant
        return AccessGrant

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def test_ctor_defaults(self):
        grant = self._makeOne('OWNER', 'userByEmail', 'phred@example.com')
        self.assertEqual(grant.role, 'OWNER')
        self.assertEqual(grant.entity_type, 'userByEmail')
        self.assertEqual(grant.entity_id, 'phred@example.com')

    def test_ctor_bad_entity_type(self):
        with self.assertRaises(ValueError):
            self._makeOne(None, 'unknown', None)

    def test_ctor_view_with_role(self):
        role = 'READER'
        entity_type = 'view'
        with self.assertRaises(ValueError):
            self._makeOne(role, entity_type, None)

    def test_ctor_view_success(self):
        role = None
        entity_type = 'view'
        entity_id = object()
        grant = self._makeOne(role, entity_type, entity_id)
        self.assertEqual(grant.role, role)
        self.assertEqual(grant.entity_type, entity_type)
        self.assertEqual(grant.entity_id, entity_id)

    def test_ctor_nonview_without_role(self):
        role = None
        entity_type = 'userByEmail'
        with self.assertRaises(ValueError):
            self._makeOne(role, entity_type, None)

    def test___eq___role_mismatch(self):
        grant = self._makeOne('OWNER', 'userByEmail', 'phred@example.com')
        other = self._makeOne('WRITER', 'userByEmail', 'phred@example.com')
        self.assertNotEqual(grant, other)

    def test___eq___entity_type_mismatch(self):
        grant = self._makeOne('OWNER', 'userByEmail', 'phred@example.com')
        other = self._makeOne('OWNER', 'groupByEmail', 'phred@example.com')
        self.assertNotEqual(grant, other)

    def test___eq___entity_id_mismatch(self):
        grant = self._makeOne('OWNER', 'userByEmail', 'phred@example.com')
        other = self._makeOne('OWNER', 'userByEmail', 'bharney@example.com')
        self.assertNotEqual(grant, other)

    def test___eq___hit(self):
        grant = self._makeOne('OWNER', 'userByEmail', 'phred@example.com')
        other = self._makeOne('OWNER', 'userByEmail', 'phred@example.com')
        self.assertEqual(grant, other)


class TestDataset(unittest2.TestCase):
    PROJECT = 'project'
    DS_NAME = 'dataset-name'

    def _getTargetClass(self):
        from gcloud.bigquery.dataset import Dataset
        return Dataset

    def _makeOne(self, *args, **kw):
        return self._getTargetClass()(*args, **kw)

    def _setUpConstants(self):
        import datetime
        from gcloud._helpers import UTC

        self.WHEN_TS = 1437767599.006
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(
            tzinfo=UTC)
        self.ETAG = 'ETAG'
        self.DS_ID = '%s:%s' % (self.PROJECT, self.DS_NAME)
        self.RESOURCE_URL = 'http://example.com/path/to/resource'

    def _makeResource(self):
        self._setUpConstants()
        USER_EMAIL = 'phred@example.com'
        GROUP_EMAIL = 'group-name@lists.example.com'
        return {
            'creationTime': self.WHEN_TS * 1000,
            'datasetReference':
                {'projectId': self.PROJECT, 'datasetId': self.DS_NAME},
            'etag': self.ETAG,
            'id': self.DS_ID,
            'lastModifiedTime': self.WHEN_TS * 1000,
            'location': 'US',
            'selfLink': self.RESOURCE_URL,
            'access': [
                {'role': 'OWNER', 'userByEmail': USER_EMAIL},
                {'role': 'OWNER', 'groupByEmail': GROUP_EMAIL},
                {'role': 'WRITER', 'specialGroup': 'projectWriters'},
                {'role': 'READER', 'specialGroup': 'projectReaders'}],
        }

    def _verifyAccessGrants(self, access_grants, resource):
        r_grants = []
        for r_grant in resource['access']:
            role = r_grant.pop('role')
            for entity_type, entity_id in sorted(r_grant.items()):
                r_grants.append({'role': role,
                                 'entity_type': entity_type,
                                 'entity_id': entity_id})

        self.assertEqual(len(access_grants), len(r_grants))
        for a_grant, r_grant in zip(access_grants, r_grants):
            self.assertEqual(a_grant.role, r_grant['role'])
            self.assertEqual(a_grant.entity_type, r_grant['entity_type'])
            self.assertEqual(a_grant.entity_id, r_grant['entity_id'])

    def _verifyReadonlyResourceProperties(self, dataset, resource):

        self.assertEqual(dataset.dataset_id, self.DS_ID)

        if 'creationTime' in resource:
            self.assertEqual(dataset.created, self.WHEN)
        else:
            self.assertEqual(dataset.created, None)
        if 'etag' in resource:
            self.assertEqual(dataset.etag, self.ETAG)
        else:
            self.assertEqual(dataset.etag, None)
        if 'lastModifiedTime' in resource:
            self.assertEqual(dataset.modified, self.WHEN)
        else:
            self.assertEqual(dataset.modified, None)
        if 'selfLink' in resource:
            self.assertEqual(dataset.self_link, self.RESOURCE_URL)
        else:
            self.assertEqual(dataset.self_link, None)

    def _verifyResourceProperties(self, dataset, resource):

        self._verifyReadonlyResourceProperties(dataset, resource)

        if 'defaultTableExpirationMs' in resource:
            self.assertEqual(dataset.default_table_expiration_ms,
                             int(resource.get('defaultTableExpirationMs')))
        else:
            self.assertEqual(dataset.default_table_expiration_ms, None)
        self.assertEqual(dataset.description, resource.get('description'))
        self.assertEqual(dataset.friendly_name, resource.get('friendlyName'))
        self.assertEqual(dataset.location, resource.get('location'))

        if 'access' in resource:
            self._verifyAccessGrants(dataset.access_grants, resource)
        else:
            self.assertEqual(dataset.access_grants, [])

    def test_ctor(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        self.assertEqual(dataset.name, self.DS_NAME)
        self.assertTrue(dataset._client is client)
        self.assertEqual(dataset.project, client.project)
        self.assertEqual(
            dataset.path,
            '/projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME))
        self.assertEqual(dataset.access_grants, [])

        self.assertEqual(dataset.created, None)
        self.assertEqual(dataset.dataset_id, None)
        self.assertEqual(dataset.etag, None)
        self.assertEqual(dataset.modified, None)
        self.assertEqual(dataset.self_link, None)

        self.assertEqual(dataset.default_table_expiration_ms, None)
        self.assertEqual(dataset.description, None)
        self.assertEqual(dataset.friendly_name, None)
        self.assertEqual(dataset.location, None)

    def test_access_roles_setter_non_list(self):
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        with self.assertRaises(TypeError):
            dataset.access_grants = object()

    def test_access_roles_setter_invalid_field(self):
        from gcloud.bigquery.dataset import AccessGrant
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        phred = AccessGrant('OWNER', 'userByEmail', 'phred@example.com')
        with self.assertRaises(ValueError):
            dataset.access_grants = [phred, object()]

    def test_access_roles_setter(self):
        from gcloud.bigquery.dataset import AccessGrant
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client)
        phred = AccessGrant('OWNER', 'userByEmail', 'phred@example.com')
        bharney = AccessGrant('OWNER', 'userByEmail', 'bharney@example.com')
        dataset.access_grants = [phred, bharney]
        self.assertEqual(dataset.access_grants, [phred, bharney])

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

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {}
        klass = self._getTargetClass()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE, client=client)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _Client(self.PROJECT)
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_NAME),
            'datasetReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
            }
        }
        klass = self._getTargetClass()
        dataset = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(dataset._client is client)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_from_api_repr_w_properties(self):
        client = _Client(self.PROJECT)
        RESOURCE = self._makeResource()
        klass = self._getTargetClass()
        dataset = klass.from_api_repr(RESOURCE, client=client)
        self.assertTrue(dataset._client is client)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test__parse_access_grants_w_unknown_entity_type(self):
        ACCESS = [
            {'role': 'READER', 'unknown': 'UNKNOWN'},
        ]
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client=client)
        with self.assertRaises(ValueError):
            dataset._parse_access_grants(ACCESS)

    def test__parse_access_grants_w_extra_keys(self):
        USER_EMAIL = 'phred@example.com'
        ACCESS = [
            {
                'role': 'READER',
                'specialGroup': 'projectReaders',
                'userByEmail': USER_EMAIL,
            },
        ]
        client = _Client(self.PROJECT)
        dataset = self._makeOne(self.DS_NAME, client=client)
        with self.assertRaises(ValueError):
            dataset._parse_access_grants(ACCESS)

    def test_create_w_bound_client(self):
        PATH = 'projects/%s/datasets' % self.PROJECT
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)

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
        from gcloud.bigquery.dataset import AccessGrant
        PATH = 'projects/%s/datasets' % self.PROJECT
        USER_EMAIL = 'phred@example.com'
        GROUP_EMAIL = 'group-name@lists.example.com'
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
        VIEW = {
            'projectId': 'my-proj',
            'datasetId': 'starry-skies',
            'tableId': 'northern-hemisphere',
        }
        dataset.access_grants = [
            AccessGrant('OWNER', 'userByEmail', USER_EMAIL),
            AccessGrant('OWNER', 'groupByEmail', GROUP_EMAIL),
            AccessGrant('READER', 'domain', 'foo.com'),
            AccessGrant('READER', 'specialGroup', 'projectReaders'),
            AccessGrant('WRITER', 'specialGroup', 'projectWriters'),
            AccessGrant(None, 'view', VIEW),
        ]

        dataset.create(client=CLIENT2)

        self.assertEqual(len(conn1._requested), 0)
        self.assertEqual(len(conn2._requested), 1)
        req = conn2._requested[0]
        self.assertEqual(req['method'], 'POST')
        self.assertEqual(req['path'], '/%s' % PATH)
        SENT = {
            'datasetReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_NAME,
            },
            'description': DESCRIPTION,
            'friendlyName': TITLE,
            'access': [
                {'role': 'OWNER', 'userByEmail': USER_EMAIL},
                {'role': 'OWNER', 'groupByEmail': GROUP_EMAIL},
                {'role': 'READER', 'domain': 'foo.com'},
                {'role': 'READER', 'specialGroup': 'projectReaders'},
                {'role': 'WRITER', 'specialGroup': 'projectWriters'},
                {'view': VIEW},
            ],
        }
        self.assertEqual(req['data'], SENT)
        self._verifyResourceProperties(dataset, RESOURCE)

    def test_create_w_missing_output_properties(self):
        # In the wild, the resource returned from 'dataset.create' sometimes
        # lacks 'creationTime' / 'lastModifiedTime'
        PATH = 'projects/%s/datasets' % (self.PROJECT,)
        RESOURCE = self._makeResource()
        del RESOURCE['creationTime']
        del RESOURCE['lastModifiedTime']
        self.WHEN = None
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)

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

    def test_exists_miss_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        conn = _Connection()
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)

        self.assertFalse(dataset.exists())

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'], {'fields': 'id'})

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
        self.assertEqual(req['query_params'], {'fields': 'id'})

    def test_reload_w_bound_client(self):
        PATH = 'projects/%s/datasets/%s' % (self.PROJECT, self.DS_NAME)
        RESOURCE = self._makeResource()
        conn = _Connection(RESOURCE)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)

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
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)

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
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)

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
        RESOURCE['defaultTableExpirationMs'] = str(DEF_TABLE_EXP)
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
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)
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
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)

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

    def test_list_tables_empty(self):
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)
        tables, token = dataset.list_tables()
        self.assertEqual(tables, [])
        self.assertEqual(token, None)
        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_NAME)
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_tables_defaults(self):
        from gcloud.bigquery.table import Table

        TABLE_1 = 'table_one'
        TABLE_2 = 'table_two'
        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_NAME)
        TOKEN = 'TOKEN'
        DATA = {
            'nextPageToken': TOKEN,
            'tables': [
                {'kind': 'bigquery#table',
                 'id': '%s:%s.%s' % (self.PROJECT, self.DS_NAME, TABLE_1),
                 'tableReference': {'tableId': TABLE_1,
                                    'datasetId': self.DS_NAME,
                                    'projectId': self.PROJECT},
                 'type': 'TABLE'},
                {'kind': 'bigquery#table',
                 'id': '%s:%s.%s' % (self.PROJECT, self.DS_NAME, TABLE_2),
                 'tableReference': {'tableId': TABLE_2,
                                    'datasetId': self.DS_NAME,
                                    'projectId': self.PROJECT},
                 'type': 'TABLE'},
            ]
        }

        conn = _Connection(DATA)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)

        tables, token = dataset.list_tables()

        self.assertEqual(len(tables), len(DATA['tables']))
        for found, expected in zip(tables, DATA['tables']):
            self.assertTrue(isinstance(found, Table))
            self.assertEqual(found.table_id, expected['id'])
            self.assertEqual(found.table_type, expected['type'])
        self.assertEqual(token, TOKEN)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)

    def test_list_tables_explicit(self):
        from gcloud.bigquery.table import Table

        TABLE_1 = 'table_one'
        TABLE_2 = 'table_two'
        PATH = 'projects/%s/datasets/%s/tables' % (self.PROJECT, self.DS_NAME)
        TOKEN = 'TOKEN'
        DATA = {
            'tables': [
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s.%s' % (self.PROJECT, self.DS_NAME, TABLE_1),
                 'tableReference': {'tableId': TABLE_1,
                                    'datasetId': self.DS_NAME,
                                    'projectId': self.PROJECT},
                 'type': 'TABLE'},
                {'kind': 'bigquery#dataset',
                 'id': '%s:%s.%s' % (self.PROJECT, self.DS_NAME, TABLE_2),
                 'tableReference': {'tableId': TABLE_2,
                                    'datasetId': self.DS_NAME,
                                    'projectId': self.PROJECT},
                 'type': 'TABLE'},
            ]
        }

        conn = _Connection(DATA)
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)

        tables, token = dataset.list_tables(max_results=3, page_token=TOKEN)

        self.assertEqual(len(tables), len(DATA['tables']))
        for found, expected in zip(tables, DATA['tables']):
            self.assertTrue(isinstance(found, Table))
            self.assertEqual(found.table_id, expected['id'])
            self.assertEqual(found.table_type, expected['type'])
        self.assertEqual(token, None)

        self.assertEqual(len(conn._requested), 1)
        req = conn._requested[0]
        self.assertEqual(req['method'], 'GET')
        self.assertEqual(req['path'], '/%s' % PATH)
        self.assertEqual(req['query_params'],
                         {'maxResults': 3, 'pageToken': TOKEN})

    def test_table_wo_schema(self):
        from gcloud.bigquery.table import Table
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)
        table = dataset.table('table_name')
        self.assertTrue(isinstance(table, Table))
        self.assertEqual(table.name, 'table_name')
        self.assertTrue(table._dataset is dataset)
        self.assertEqual(table.schema, [])

    def test_table_w_schema(self):
        from gcloud.bigquery.table import SchemaField
        from gcloud.bigquery.table import Table
        conn = _Connection({})
        client = _Client(project=self.PROJECT, connection=conn)
        dataset = self._makeOne(self.DS_NAME, client=client)
        full_name = SchemaField('full_name', 'STRING', mode='REQUIRED')
        age = SchemaField('age', 'INTEGER', mode='REQUIRED')
        table = dataset.table('table_name', schema=[full_name, age])
        self.assertTrue(isinstance(table, Table))
        self.assertEqual(table.name, 'table_name')
        self.assertTrue(table._dataset is dataset)
        self.assertEqual(table.schema, [full_name, age])


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
