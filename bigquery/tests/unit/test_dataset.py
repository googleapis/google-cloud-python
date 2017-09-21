# Copyright 2015 Google Inc.
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

import unittest

import mock


class TestAccessEntry(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.dataset import AccessEntry

        return AccessEntry

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        entry = self._make_one('OWNER', 'userByEmail', 'phred@example.com')
        self.assertEqual(entry.role, 'OWNER')
        self.assertEqual(entry.entity_type, 'userByEmail')
        self.assertEqual(entry.entity_id, 'phred@example.com')

    def test_ctor_bad_entity_type(self):
        with self.assertRaises(ValueError):
            self._make_one(None, 'unknown', None)

    def test_ctor_view_with_role(self):
        role = 'READER'
        entity_type = 'view'
        with self.assertRaises(ValueError):
            self._make_one(role, entity_type, None)

    def test_ctor_view_success(self):
        role = None
        entity_type = 'view'
        entity_id = object()
        entry = self._make_one(role, entity_type, entity_id)
        self.assertEqual(entry.role, role)
        self.assertEqual(entry.entity_type, entity_type)
        self.assertEqual(entry.entity_id, entity_id)

    def test_ctor_nonview_without_role(self):
        role = None
        entity_type = 'userByEmail'
        with self.assertRaises(ValueError):
            self._make_one(role, entity_type, None)

    def test___eq___role_mismatch(self):
        entry = self._make_one('OWNER', 'userByEmail', 'phred@example.com')
        other = self._make_one('WRITER', 'userByEmail', 'phred@example.com')
        self.assertNotEqual(entry, other)

    def test___eq___entity_type_mismatch(self):
        entry = self._make_one('OWNER', 'userByEmail', 'phred@example.com')
        other = self._make_one('OWNER', 'groupByEmail', 'phred@example.com')
        self.assertNotEqual(entry, other)

    def test___eq___entity_id_mismatch(self):
        entry = self._make_one('OWNER', 'userByEmail', 'phred@example.com')
        other = self._make_one('OWNER', 'userByEmail', 'bharney@example.com')
        self.assertNotEqual(entry, other)

    def test___eq___hit(self):
        entry = self._make_one('OWNER', 'userByEmail', 'phred@example.com')
        other = self._make_one('OWNER', 'userByEmail', 'phred@example.com')
        self.assertEqual(entry, other)

    def test__eq___type_mismatch(self):
        entry = self._make_one('OWNER', 'userByEmail', 'silly@example.com')
        self.assertNotEqual(entry, object())
        self.assertEqual(entry, mock.ANY)


class TestDatasetReference(unittest.TestCase):

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.dataset import DatasetReference

        return DatasetReference

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        dataset_ref = self._make_one('some-project-1', 'dataset_1')
        self.assertEqual(dataset_ref.project, 'some-project-1')
        self.assertEqual(dataset_ref.dataset_id, 'dataset_1')

    def test_ctor_bad_args(self):
        with self.assertRaises(ValueError):
            self._make_one(1, 'd')
        with self.assertRaises(ValueError):
            self._make_one('p', 2)

    def test_table(self):
        dataset_ref = self._make_one('some-project-1', 'dataset_1')
        table_ref = dataset_ref.table('table_1')
        self.assertEqual(table_ref.dataset_id, 'dataset_1')
        self.assertEqual(table_ref.project, 'some-project-1')
        self.assertEqual(table_ref.table_id, 'table_1')

    def test_to_api_repr(self):
        dataset = self._make_one('project_1', 'dataset_1')

        resource = dataset.to_api_repr()

        self.assertEqual(
            resource,
            {
                'projectId': 'project_1',
                'datasetId': 'dataset_1',
            })

    def test_from_api_repr(self):
        from google.cloud.bigquery.dataset import DatasetReference
        expected = self._make_one('project_1', 'dataset_1')

        got = DatasetReference.from_api_repr(
            {
                'projectId': 'project_1',
                'datasetId': 'dataset_1',
            })

        self.assertEqual(expected, got)

    def test___eq___wrong_type(self):
        dataset = self._make_one('project_1', 'dataset_1')
        other = object()
        self.assertNotEqual(dataset, other)
        self.assertEqual(dataset, mock.ANY)

    def test___eq___project_mismatch(self):
        dataset = self._make_one('project_1', 'dataset_1')
        other = self._make_one('project_2', 'dataset_1')
        self.assertNotEqual(dataset, other)

    def test___eq___dataset_mismatch(self):
        dataset = self._make_one('project_1', 'dataset_1')
        other = self._make_one('project_1', 'dataset_2')
        self.assertNotEqual(dataset, other)

    def test___eq___equality(self):
        dataset = self._make_one('project_1', 'dataset_1')
        other = self._make_one('project_1', 'dataset_1')
        self.assertEqual(dataset, other)

    def test___hash__set_equality(self):
        dataset1 = self._make_one('project_1', 'dataset_1')
        dataset2 = self._make_one('project_1', 'dataset_2')
        set_one = {dataset1, dataset2}
        set_two = {dataset1, dataset2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        dataset1 = self._make_one('project_1', 'dataset_1')
        dataset2 = self._make_one('project_1', 'dataset_2')
        set_one = {dataset1}
        set_two = {dataset2}
        self.assertNotEqual(set_one, set_two)

    def test___repr__(self):
        dataset = self._make_one('project1', 'dataset1')
        expected = "DatasetReference('project1', 'dataset1')"
        self.assertEqual(repr(dataset), expected)


class TestDataset(unittest.TestCase):
    from google.cloud.bigquery.dataset import DatasetReference

    PROJECT = 'project'
    DS_ID = 'dataset-id'
    DS_REF = DatasetReference(PROJECT, DS_ID)

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.dataset import Dataset

        return Dataset

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def _setUpConstants(self):
        import datetime
        from google.cloud._helpers import UTC

        self.WHEN_TS = 1437767599.006
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(
            tzinfo=UTC)
        self.ETAG = 'ETAG'
        self.DS_FULL_ID = '%s:%s' % (self.PROJECT, self.DS_ID)
        self.RESOURCE_URL = 'http://example.com/path/to/resource'

    def _makeResource(self):
        self._setUpConstants()
        USER_EMAIL = 'phred@example.com'
        GROUP_EMAIL = 'group-name@lists.example.com'
        return {
            'creationTime': self.WHEN_TS * 1000,
            'datasetReference':
                {'projectId': self.PROJECT, 'datasetId': self.DS_ID},
            'etag': self.ETAG,
            'id': self.DS_FULL_ID,
            'lastModifiedTime': self.WHEN_TS * 1000,
            'location': 'US',
            'selfLink': self.RESOURCE_URL,
            'defaultTableExpirationMs': 3600,
            'access': [
                {'role': 'OWNER', 'userByEmail': USER_EMAIL},
                {'role': 'OWNER', 'groupByEmail': GROUP_EMAIL},
                {'role': 'WRITER', 'specialGroup': 'projectWriters'},
                {'role': 'READER', 'specialGroup': 'projectReaders'}],
        }

    def _verify_access_entry(self, access_entries, resource):
        r_entries = []
        for r_entry in resource['access']:
            role = r_entry.pop('role')
            for entity_type, entity_id in sorted(r_entry.items()):
                r_entries.append({
                    'role': role,
                    'entity_type': entity_type,
                    'entity_id': entity_id})

        self.assertEqual(len(access_entries), len(r_entries))
        for a_entry, r_entry in zip(access_entries, r_entries):
            self.assertEqual(a_entry.role, r_entry['role'])
            self.assertEqual(a_entry.entity_type, r_entry['entity_type'])
            self.assertEqual(a_entry.entity_id, r_entry['entity_id'])

    def _verify_readonly_resource_properties(self, dataset, resource):

        self.assertEqual(dataset.dataset_id, self.DS_ID)

        if 'creationTime' in resource:
            self.assertEqual(dataset.created, self.WHEN)
        else:
            self.assertIsNone(dataset.created)
        if 'etag' in resource:
            self.assertEqual(dataset.etag, self.ETAG)
        else:
            self.assertIsNone(dataset.etag)
        if 'lastModifiedTime' in resource:
            self.assertEqual(dataset.modified, self.WHEN)
        else:
            self.assertIsNone(dataset.modified)
        if 'selfLink' in resource:
            self.assertEqual(dataset.self_link, self.RESOURCE_URL)
        else:
            self.assertIsNone(dataset.self_link)

    def _verify_resource_properties(self, dataset, resource):

        self._verify_readonly_resource_properties(dataset, resource)

        if 'defaultTableExpirationMs' in resource:
            self.assertEqual(dataset.default_table_expiration_ms,
                             int(resource.get('defaultTableExpirationMs')))
        else:
            self.assertIsNone(dataset.default_table_expiration_ms)
        self.assertEqual(dataset.description, resource.get('description'))
        self.assertEqual(dataset.friendly_name, resource.get('friendlyName'))
        self.assertEqual(dataset.location, resource.get('location'))

        if 'access' in resource:
            self._verify_access_entry(dataset.access_entries, resource)
        else:
            self.assertEqual(dataset.access_entries, [])

    def test_ctor_defaults(self):
        dataset = self._make_one(self.DS_REF)
        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)
        self.assertEqual(
            dataset.path,
            '/projects/%s/datasets/%s' % (self.PROJECT, self.DS_ID))
        self.assertEqual(dataset.access_entries, [])

        self.assertIsNone(dataset.created)
        self.assertIsNone(dataset.full_dataset_id)
        self.assertIsNone(dataset.etag)
        self.assertIsNone(dataset.modified)
        self.assertIsNone(dataset.self_link)

        self.assertIsNone(dataset.default_table_expiration_ms)
        self.assertIsNone(dataset.description)
        self.assertIsNone(dataset.friendly_name)
        self.assertIsNone(dataset.location)

    def test_ctor_explicit(self):
        from google.cloud.bigquery.dataset import DatasetReference, AccessEntry

        phred = AccessEntry('OWNER', 'userByEmail', 'phred@example.com')
        bharney = AccessEntry('OWNER', 'userByEmail', 'bharney@example.com')
        entries = [phred, bharney]
        OTHER_PROJECT = 'foo-bar-123'
        dataset = self._make_one(DatasetReference(OTHER_PROJECT, self.DS_ID))
        dataset.access_entries = entries
        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, OTHER_PROJECT)
        self.assertEqual(
            dataset.path,
            '/projects/%s/datasets/%s' % (OTHER_PROJECT, self.DS_ID))
        self.assertEqual(dataset.access_entries, entries)

        self.assertIsNone(dataset.created)
        self.assertIsNone(dataset.full_dataset_id)
        self.assertIsNone(dataset.etag)
        self.assertIsNone(dataset.modified)
        self.assertIsNone(dataset.self_link)

        self.assertIsNone(dataset.default_table_expiration_ms)
        self.assertIsNone(dataset.description)
        self.assertIsNone(dataset.friendly_name)
        self.assertIsNone(dataset.location)

    def test_access_entries_setter_non_list(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(TypeError):
            dataset.access_entries = object()

    def test_access_entries_setter_invalid_field(self):
        from google.cloud.bigquery.dataset import AccessEntry

        dataset = self._make_one(self.DS_REF)
        phred = AccessEntry('OWNER', 'userByEmail', 'phred@example.com')
        with self.assertRaises(ValueError):
            dataset.access_entries = [phred, object()]

    def test_access_entries_setter(self):
        from google.cloud.bigquery.dataset import AccessEntry

        dataset = self._make_one(self.DS_REF)
        phred = AccessEntry('OWNER', 'userByEmail', 'phred@example.com')
        bharney = AccessEntry('OWNER', 'userByEmail', 'bharney@example.com')
        dataset.access_entries = [phred, bharney]
        self.assertEqual(dataset.access_entries, [phred, bharney])

    def test_default_table_expiration_ms_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.default_table_expiration_ms = 'bogus'

    def test_default_table_expiration_ms_setter(self):
        dataset = self._make_one(self.DS_REF)
        dataset.default_table_expiration_ms = 12345
        self.assertEqual(dataset.default_table_expiration_ms, 12345)

    def test_description_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.description = 12345

    def test_description_setter(self):
        dataset = self._make_one(self.DS_REF)
        dataset.description = 'DESCRIPTION'
        self.assertEqual(dataset.description, 'DESCRIPTION')

    def test_friendly_name_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.friendly_name = 12345

    def test_friendly_name_setter(self):
        dataset = self._make_one(self.DS_REF)
        dataset.friendly_name = 'FRIENDLY'
        self.assertEqual(dataset.friendly_name, 'FRIENDLY')

    def test_location_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.location = 12345

    def test_location_setter(self):
        dataset = self._make_one(self.DS_REF)
        dataset.location = 'LOCATION'
        self.assertEqual(dataset.location, 'LOCATION')

    def test_labels_setter(self):
        dataset = self._make_one(self.DS_REF)
        dataset.labels = {'color': 'green'}
        self.assertEqual(dataset.labels, {'color': 'green'})

    def test_labels_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.labels = None

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        RESOURCE = {
            'id': '%s:%s' % (self.PROJECT, self.DS_ID),
            'datasetReference': {
                'projectId': self.PROJECT,
                'datasetId': self.DS_ID,
            }
        }
        klass = self._get_target_class()
        dataset = klass.from_api_repr(RESOURCE)
        self._verify_resource_properties(dataset, RESOURCE)

    def test_from_api_repr_w_properties(self):
        RESOURCE = self._makeResource()
        klass = self._get_target_class()
        dataset = klass.from_api_repr(RESOURCE)
        self._verify_resource_properties(dataset, RESOURCE)

    def test__parse_access_entries_w_unknown_entity_type(self):
        ACCESS = [
            {'role': 'READER', 'unknown': 'UNKNOWN'},
        ]
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset._parse_access_entries(ACCESS)

    def test__parse_access_entries_w_extra_keys(self):
        USER_EMAIL = 'phred@example.com'
        ACCESS = [
            {
                'role': 'READER',
                'specialGroup': 'projectReaders',
                'userByEmail': USER_EMAIL,
            },
        ]
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset._parse_access_entries(ACCESS)

    def test_table(self):
        from google.cloud.bigquery.table import TableReference

        dataset = self._make_one(self.DS_REF)
        table = dataset.table('table_id')
        self.assertIsInstance(table, TableReference)
        self.assertEqual(table.table_id, 'table_id')
        self.assertEqual(table.dataset_id, self.DS_ID)
        self.assertEqual(table.project, self.PROJECT)
