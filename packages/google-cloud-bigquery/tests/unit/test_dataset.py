# Copyright 2015 Google LLC
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
from unittest import mock

from google.cloud.bigquery.routine.routine import Routine, RoutineReference
import pytest
from google.cloud.bigquery.dataset import (
    AccessEntry,
    Condition,
    Dataset,
    DatasetReference,
    Table,
    TableReference,
)


class TestAccessEntry(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        return AccessEntry

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        entry = self._make_one("OWNER", "userByEmail", "phred@example.com")
        self.assertEqual(entry.role, "OWNER")
        self.assertEqual(entry.entity_type, "userByEmail")
        self.assertEqual(entry.entity_id, "phred@example.com")

    def test_ctor_view_success(self):
        role = None
        entity_type = "view"
        entity_id = object()
        entry = self._make_one(role, entity_type, entity_id)
        self.assertEqual(entry.role, role)
        self.assertEqual(entry.entity_type, entity_type)
        self.assertEqual(entry.entity_id, entity_id)

    def test_ctor_routine_success(self):
        role = None
        entity_type = "routine"
        entity_id = object()
        entry = self._make_one(role, entity_type, entity_id)
        self.assertEqual(entry.role, role)
        self.assertEqual(entry.entity_type, entity_type)
        self.assertEqual(entry.entity_id, entity_id)

    def test___eq___role_mismatch(self):
        entry = self._make_one("OWNER", "userByEmail", "phred@example.com")
        other = self._make_one("WRITER", "userByEmail", "phred@example.com")
        self.assertNotEqual(entry, other)

    def test___eq___entity_type_mismatch(self):
        entry = self._make_one("OWNER", "userByEmail", "phred@example.com")
        other = self._make_one("OWNER", "groupByEmail", "phred@example.com")
        self.assertNotEqual(entry, other)

    def test___eq___entity_id_mismatch(self):
        entry = self._make_one("OWNER", "userByEmail", "phred@example.com")
        other = self._make_one("OWNER", "userByEmail", "bharney@example.com")
        self.assertNotEqual(entry, other)

    def test___eq___hit(self):
        entry = self._make_one("OWNER", "userByEmail", "phred@example.com")
        other = self._make_one("OWNER", "userByEmail", "phred@example.com")
        self.assertEqual(entry, other)

    def test__eq___type_mismatch(self):
        entry = self._make_one("OWNER", "userByEmail", "silly@example.com")
        self.assertNotEqual(entry, object())
        self.assertEqual(entry, mock.ANY)

    def test___hash__set_equality(self):
        entry1 = self._make_one("OWNER", "userByEmail", "silly@example.com")
        entry2 = self._make_one("OWNER", "userByEmail", "phred@example.com")
        set_one = {entry1, entry2}
        set_two = {entry1, entry2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        entry1 = self._make_one("OWNER", "userByEmail", "silly@example.com")
        entry2 = self._make_one("OWNER", "userByEmail", "phred@example.com")
        set_one = {entry1}
        set_two = {entry2}
        self.assertNotEqual(set_one, set_two)

    def test_to_api_repr(self):
        entry = self._make_one("OWNER", "userByEmail", "salmon@example.com")
        resource = entry.to_api_repr()
        exp_resource = {"role": "OWNER", "userByEmail": "salmon@example.com"}
        self.assertEqual(resource, exp_resource)

    def test_to_api_repr_view(self):
        view = {
            "projectId": "my-project",
            "datasetId": "my_dataset",
            "tableId": "my_table",
        }
        entry = self._make_one(None, "view", view)
        resource = entry.to_api_repr()
        exp_resource = {"view": view, "role": None}
        self.assertEqual(resource, exp_resource)

    def test_to_api_repr_routine(self):
        routine = {
            "projectId": "my-project",
            "datasetId": "my_dataset",
            "routineId": "my_routine",
        }

        entry = self._make_one(None, "routine", routine)
        resource = entry.to_api_repr()
        exp_resource = {"routine": routine, "role": None}
        self.assertEqual(resource, exp_resource)

    def test_to_api_repr_dataset(self):
        dataset = {
            "dataset": {"projectId": "my-project", "datasetId": "my_dataset"},
            "target_types": "VIEWS",
        }
        entry = self._make_one(None, "dataset", dataset)
        resource = entry.to_api_repr()
        exp_resource = {"dataset": dataset, "role": None}
        self.assertEqual(resource, exp_resource)

    def test_from_api_repr(self):
        resource = {"role": "OWNER", "userByEmail": "salmon@example.com"}
        entry = self._get_target_class().from_api_repr(resource)
        self.assertEqual(entry.role, "OWNER")
        self.assertEqual(entry.entity_type, "userByEmail")
        self.assertEqual(entry.entity_id, "salmon@example.com")

    def test_from_api_repr_w_unknown_entity_type(self):
        resource = {"role": "READER", "unknown": "UNKNOWN"}
        entry = self._get_target_class().from_api_repr(resource)
        self.assertEqual(entry.role, "READER")
        self.assertEqual(entry.entity_type, "unknown")
        self.assertEqual(entry.entity_id, "UNKNOWN")
        exp_resource = entry.to_api_repr()
        self.assertEqual(resource, exp_resource)

    def test_from_api_repr_wo_role(self):
        resource = {
            "view": {
                "projectId": "my-project",
                "datasetId": "my_dataset",
                "tableId": "my_table",
            }
        }
        entry = self._get_target_class().from_api_repr(resource)
        exp_entry = self._make_one(
            role=None,
            entity_type="view",
            entity_id=resource["view"],
        )
        self.assertEqual(entry, exp_entry)

    def test_to_api_repr_w_extra_properties(self):
        resource = {
            "role": "READER",
            "userByEmail": "salmon@example.com",
        }
        entry = self._get_target_class().from_api_repr(resource)
        entry._properties["specialGroup"] = resource["specialGroup"] = "projectReaders"
        exp_resource = entry.to_api_repr()
        self.assertEqual(resource, exp_resource)

    def test_from_api_repr_entries_w_extra_keys(self):
        resource = {
            "role": "READER",
            "specialGroup": "projectReaders",
            "userByEmail": "salmon@example.com",
        }
        with self.assertRaises(ValueError):
            self._get_target_class().from_api_repr(resource)

    def test_view_getter_setter(self):
        view = {
            "projectId": "my_project",
            "datasetId": "my_dataset",
            "tableId": "my_table",
        }
        view_ref = TableReference.from_api_repr(view)
        entry = self._make_one(None)
        entry.view = view
        resource = entry.to_api_repr()
        exp_resource = {"view": view, "role": None}
        self.assertEqual(entry.view, view_ref)
        self.assertEqual(resource, exp_resource)

    def test_view_getter_setter_none(self):
        entry = self._make_one(None)
        self.assertEqual(entry.view, None)

    def test_view_getter_setter_string(self):
        project = "my_project"
        dataset = "my_dataset"
        table = "my_table"
        view = {
            "projectId": project,
            "datasetId": dataset,
            "tableId": table,
        }
        entry = self._make_one(None)
        entry.view = f"{project}.{dataset}.{table}"
        resource = entry.to_api_repr()
        exp_resource = {"view": view, "role": None}
        self.assertEqual(resource, exp_resource)

    def test_view_getter_setter_table(self):
        project = "my_project"
        dataset = "my_dataset"
        table = "my_table"
        view = {
            "projectId": project,
            "datasetId": dataset,
            "tableId": table,
        }
        view_ref = Table.from_string(f"{project}.{dataset}.{table}")
        entry = self._make_one(None)
        entry.view = view_ref
        resource = entry.to_api_repr()
        exp_resource = {"view": view, "role": None}
        self.assertEqual(resource, exp_resource)

    def test_view_getter_setter_table_ref(self):
        project = "my_project"
        dataset = "my_dataset"
        table = "my_table"
        view = {
            "projectId": project,
            "datasetId": dataset,
            "tableId": table,
        }
        view_ref = TableReference.from_string(f"{project}.{dataset}.{table}")
        entry = self._make_one(None)
        entry.view = view_ref
        resource = entry.to_api_repr()
        exp_resource = {"view": view, "role": None}
        self.assertEqual(resource, exp_resource)

    def test_view_getter_setter_incorrect_role(self):
        view = {
            "projectId": "my_project",
            "datasetId": "my_dataset",
            "tableId": "my_table",
        }
        view_ref = TableReference.from_api_repr(view)
        entry = self._make_one("READER")
        with self.assertRaises(ValueError):
            entry.view = view_ref

    def test_dataset_getter_setter(self):
        dataset = {"projectId": "my-project", "datasetId": "my_dataset"}
        entry = self._make_one(None)
        entry.dataset = dataset
        resource = entry.to_api_repr()
        exp_resource = {
            "dataset": {"dataset": dataset, "targetTypes": None},
            "role": None,
        }
        dataset_ref = DatasetReference.from_api_repr(dataset)
        prop = entry.dataset
        self.assertEqual(resource, exp_resource)
        self.assertEqual(prop, dataset_ref)

    def test_dataset_getter_setter_none(self):
        entry = self._make_one(None)
        self.assertEqual(entry.dataset, None)

    def test_dataset_getter_setter_string(self):
        project = "my-project"
        dataset_id = "my_dataset"
        dataset = {
            "projectId": project,
            "datasetId": dataset_id,
        }
        entry = self._make_one(None)
        string_ref = f"{project}.{dataset_id}"
        entry.dataset = string_ref
        resource = entry.to_api_repr()
        exp_resource = {
            "dataset": {"dataset": dataset, "targetTypes": None},
            "role": None,
        }
        self.assertEqual(resource, exp_resource)

    def test_dataset_getter_setter_dataset_ref(self):
        project = "my-project"
        dataset_id = "my_dataset"
        dataset_ref = DatasetReference(project, dataset_id)
        entry = self._make_one(None)
        entry.dataset = dataset_ref
        resource = entry.to_api_repr()
        exp_resource = {
            "dataset": {"dataset": dataset_ref, "targetTypes": None},
            "role": None,
        }
        self.assertEqual(resource, exp_resource)

    def test_dataset_getter_setter_dataset(self):
        project = "my-project"
        dataset_id = "my_dataset"
        dataset_repr = {
            "projectId": project,
            "datasetId": dataset_id,
        }
        dataset = Dataset(f"{project}.{dataset_id}")
        entry = self._make_one(None)
        entry.dataset = dataset
        resource = entry.to_api_repr()
        exp_resource = {
            "role": None,
            "dataset": {"dataset": dataset_repr, "targetTypes": None},
        }
        self.assertEqual(resource, exp_resource)

    def test_dataset_getter_setter_incorrect_role(self):
        dataset = {"dataset": {"projectId": "my-project", "datasetId": "my_dataset"}}
        entry = self._make_one("READER")
        with self.assertRaises(ValueError):
            entry.dataset = dataset

    def test_routine_getter_setter(self):
        routine = {
            "projectId": "my-project",
            "datasetId": "my_dataset",
            "routineId": "my_routine",
        }
        entry = self._make_one(None)
        entry.routine = routine
        resource = entry.to_api_repr()
        exp_resource = {"routine": routine, "role": None}
        self.assertEqual(resource, exp_resource)

    def test_routine_getter_setter_none(self):
        entry = self._make_one(None)
        self.assertEqual(entry.routine, None)

    def test_routine_getter_setter_string(self):
        project = "my-project"
        dataset_id = "my_dataset"
        routine_id = "my_routine"
        routine = {
            "projectId": project,
            "datasetId": dataset_id,
            "routineId": routine_id,
        }
        entry = self._make_one(None)
        entry.routine = f"{project}.{dataset_id}.{routine_id}"
        resource = entry.to_api_repr()
        exp_resource = {
            "routine": routine,
            "role": None,
        }
        self.assertEqual(resource, exp_resource)

    def test_routine_getter_setter_routine_ref(self):
        routine = {
            "projectId": "my-project",
            "datasetId": "my_dataset",
            "routineId": "my_routine",
        }
        entry = self._make_one(None)
        entry.routine = RoutineReference.from_api_repr(routine)
        resource = entry.to_api_repr()
        exp_resource = {
            "routine": routine,
            "role": None,
        }
        self.assertEqual(resource, exp_resource)

    def test_routine_getter_setter_routine(self):
        routine = {
            "projectId": "my-project",
            "datasetId": "my_dataset",
            "routineId": "my_routine",
        }
        routine_ref = RoutineReference.from_api_repr(routine)
        entry = self._make_one(None)
        entry.routine = Routine(routine_ref)
        resource = entry.to_api_repr()
        exp_resource = {
            "routine": routine,
            "role": None,
        }
        self.assertEqual(entry.routine, routine_ref)
        self.assertEqual(resource, exp_resource)

    def test_routine_getter_setter_incorrect_role(self):
        routine = {
            "projectId": "my-project",
            "datasetId": "my_dataset",
            "routineId": "my_routine",
        }
        entry = self._make_one("READER")
        with self.assertRaises(ValueError):
            entry.routine = routine

    def test_group_by_email_getter_setter(self):
        email = "cloud-developer-relations@google.com"
        entry = self._make_one(None)
        entry.group_by_email = email
        resource = entry.to_api_repr()
        exp_resource = {"groupByEmail": email, "role": None}
        self.assertEqual(entry.group_by_email, email)
        self.assertEqual(resource, exp_resource)

    def test_group_by_email_getter_setter_none(self):
        entry = self._make_one(None)
        self.assertEqual(entry.group_by_email, None)

    def test_user_by_email_getter_setter(self):
        email = "cloud-developer-relations@google.com"
        entry = self._make_one(None)
        entry.user_by_email = email
        resource = entry.to_api_repr()
        exp_resource = {"userByEmail": email, "role": None}
        self.assertEqual(entry.user_by_email, email)
        self.assertEqual(resource, exp_resource)

    def test_user_by_email_getter_setter_none(self):
        entry = self._make_one(None)
        self.assertEqual(entry.user_by_email, None)

    def test_domain_setter(self):
        domain = "my_domain"
        entry = self._make_one(None)
        entry.domain = domain
        resource = entry.to_api_repr()
        exp_resource = {"domain": domain, "role": None}
        self.assertEqual(entry.domain, domain)
        self.assertEqual(resource, exp_resource)

    def test_domain_getter_setter_none(self):
        entry = self._make_one(None)
        self.assertEqual(entry.domain, None)

    def test_special_group_getter_setter(self):
        special_group = "my_special_group"
        entry = self._make_one(None)
        entry.special_group = special_group
        resource = entry.to_api_repr()
        exp_resource = {"specialGroup": special_group, "role": None}
        self.assertEqual(entry.special_group, special_group)
        self.assertEqual(resource, exp_resource)

    def test_special_group_getter_setter_none(self):
        entry = self._make_one(None)
        self.assertEqual(entry.special_group, None)

    def test_role_getter_setter(self):
        role = "READER"
        entry = self._make_one(None)
        entry.role = role
        resource = entry.to_api_repr()
        exp_resource = {"role": role}
        self.assertEqual(resource, exp_resource)

    def test_role_getter_setter_none(self):
        entry = self._make_one(None)
        self.assertEqual(entry.role, None)

    def test_dataset_target_types_getter_setter(self):
        target_types = ["VIEWS"]
        entry = self._make_one(None)
        entry.dataset_target_types = target_types
        self.assertEqual(entry.dataset_target_types, target_types)

    def test_dataset_target_types_getter_setter_none(self):
        entry = self._make_one(None)
        self.assertEqual(entry.dataset_target_types, None)

    def test_dataset_target_types_getter_setter_w_dataset(self):
        dataset = {"projectId": "my-project", "datasetId": "my_dataset"}
        target_types = ["VIEWS"]
        entry = self._make_one(None)
        entry.dataset = dataset
        entry.dataset_target_types = target_types
        self.assertEqual(entry.dataset_target_types, target_types)


class TestDatasetReference(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.dataset import DatasetReference

        return DatasetReference

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        dataset_ref = self._make_one("some-project-1", "dataset_1")
        self.assertEqual(dataset_ref.project, "some-project-1")
        self.assertEqual(dataset_ref.dataset_id, "dataset_1")

    def test_ctor_bad_args(self):
        with self.assertRaises(ValueError):
            self._make_one(1, "d")
        with self.assertRaises(ValueError):
            self._make_one("p", 2)

    def test_table(self):
        dataset_ref = self._make_one("some-project-1", "dataset_1")
        table_ref = dataset_ref.table("table_1")
        self.assertEqual(table_ref.dataset_id, "dataset_1")
        self.assertEqual(table_ref.project, "some-project-1")
        self.assertEqual(table_ref.table_id, "table_1")

    def test_model(self):
        dataset_ref = self._make_one("some-project-1", "dataset_1")
        model_ref = dataset_ref.model("model_1")
        self.assertEqual(model_ref.project, "some-project-1")
        self.assertEqual(model_ref.dataset_id, "dataset_1")
        self.assertEqual(model_ref.model_id, "model_1")

    def test_routine(self):
        dataset_ref = self._make_one("some-project-1", "dataset_1")
        routine_ref = dataset_ref.routine("routine_1")
        self.assertEqual(routine_ref.project, "some-project-1")
        self.assertEqual(routine_ref.dataset_id, "dataset_1")
        self.assertEqual(routine_ref.routine_id, "routine_1")

    def test_to_api_repr(self):
        dataset = self._make_one("project_1", "dataset_1")

        resource = dataset.to_api_repr()

        self.assertEqual(resource, {"projectId": "project_1", "datasetId": "dataset_1"})

    def test_from_api_repr(self):
        cls = self._get_target_class()
        expected = self._make_one("project_1", "dataset_1")

        got = cls.from_api_repr({"projectId": "project_1", "datasetId": "dataset_1"})

        self.assertEqual(expected, got)

    def test_from_string(self):
        cls = self._get_target_class()
        got = cls.from_string("string-project.string_dataset")
        self.assertEqual(got.project, "string-project")
        self.assertEqual(got.dataset_id, "string_dataset")

    def test_from_string_w_prefix(self):
        cls = self._get_target_class()
        got = cls.from_string("google.com:string-project.string_dataset")
        self.assertEqual(got.project, "google.com:string-project")
        self.assertEqual(got.dataset_id, "string_dataset")

    def test_from_string_legacy_string(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("string-project:string_dataset")

    def test_from_string_w_incorrect_prefix(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("google.com.string-project.dataset_id")

    def test_from_string_w_prefix_and_too_many_parts(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("google.com:string-project.dataset_id.table_id")

    def test_from_string_not_fully_qualified(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("string_dataset")
        with self.assertRaises(ValueError):
            cls.from_string("a.b.c")

    def test_from_string_with_default_project(self):
        cls = self._get_target_class()
        got = cls.from_string("string_dataset", default_project="default-project")
        self.assertEqual(got.project, "default-project")
        self.assertEqual(got.dataset_id, "string_dataset")

    def test_from_string_ignores_default_project(self):
        cls = self._get_target_class()
        got = cls.from_string(
            "string-project.string_dataset", default_project="default-project"
        )
        self.assertEqual(got.project, "string-project")
        self.assertEqual(got.dataset_id, "string_dataset")

    def test___eq___wrong_type(self):
        dataset = self._make_one("project_1", "dataset_1")
        other = object()
        self.assertNotEqual(dataset, other)
        self.assertEqual(dataset, mock.ANY)

    def test___eq___project_mismatch(self):
        dataset = self._make_one("project_1", "dataset_1")
        other = self._make_one("project_2", "dataset_1")
        self.assertNotEqual(dataset, other)

    def test___eq___dataset_mismatch(self):
        dataset = self._make_one("project_1", "dataset_1")
        other = self._make_one("project_1", "dataset_2")
        self.assertNotEqual(dataset, other)

    def test___eq___equality(self):
        dataset = self._make_one("project_1", "dataset_1")
        other = self._make_one("project_1", "dataset_1")
        self.assertEqual(dataset, other)

    def test___hash__set_equality(self):
        dataset1 = self._make_one("project_1", "dataset_1")
        dataset2 = self._make_one("project_1", "dataset_2")
        set_one = {dataset1, dataset2}
        set_two = {dataset1, dataset2}
        self.assertEqual(set_one, set_two)

    def test___hash__not_equals(self):
        dataset1 = self._make_one("project_1", "dataset_1")
        dataset2 = self._make_one("project_1", "dataset_2")
        set_one = {dataset1}
        set_two = {dataset2}
        self.assertNotEqual(set_one, set_two)

    def test___repr__(self):
        dataset = self._make_one("project1", "dataset1")
        expected = "DatasetReference('project1', 'dataset1')"
        self.assertEqual(repr(dataset), expected)

    def test___str__(self):
        dataset = self._make_one("project1", "dataset1")
        self.assertEqual(str(dataset), "project1.dataset1")


class TestDataset(unittest.TestCase):
    from google.cloud.bigquery.dataset import DatasetReference

    PROJECT = "project"
    DS_ID = "dataset-id"
    DS_REF = DatasetReference(PROJECT, DS_ID)
    KMS_KEY_NAME = "projects/1/locations/us/keyRings/1/cryptoKeys/1"
    DEFAULT_STORAGE_LOCATION_URI = "gs://test-bucket/test-path"
    PARAMETERS = {"key": "value"}
    API_REPR = {
        "datasetReference": {"projectId": "project", "datasetId": "dataset-id"},
        "labels": {},
        "externalCatalogDatasetOptions": {
            "defaultStorageLocationUri": DEFAULT_STORAGE_LOCATION_URI,
            "parameters": PARAMETERS,
        },
    }

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
        self.WHEN = datetime.datetime.utcfromtimestamp(self.WHEN_TS).replace(tzinfo=UTC)
        self.ETAG = "ETAG"
        self.DS_FULL_ID = "%s:%s" % (self.PROJECT, self.DS_ID)
        self.RESOURCE_URL = "http://example.com/path/to/resource"

    def _make_resource(self):
        self._setUpConstants()
        USER_EMAIL = "phred@example.com"
        GROUP_EMAIL = "group-name@lists.example.com"
        return {
            "creationTime": self.WHEN_TS * 1000,
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
            "etag": self.ETAG,
            "id": self.DS_FULL_ID,
            "lastModifiedTime": self.WHEN_TS * 1000,
            "location": "US",
            "selfLink": self.RESOURCE_URL,
            "defaultTableExpirationMs": 3600,
            "storageBillingModel": "LOGICAL",
            "access": [
                {"role": "OWNER", "userByEmail": USER_EMAIL},
                {"role": "OWNER", "groupByEmail": GROUP_EMAIL},
                {"role": "WRITER", "specialGroup": "projectWriters"},
                {"role": "READER", "specialGroup": "projectReaders"},
            ],
            "defaultEncryptionConfiguration": {"kmsKeyName": self.KMS_KEY_NAME},
        }

    def _verify_access_entry(self, access_entries, resource):
        r_entries = []
        for r_entry in resource["access"]:
            role = r_entry.pop("role")
            for entity_type, entity_id in sorted(r_entry.items()):
                r_entries.append(
                    {"role": role, "entity_type": entity_type, "entity_id": entity_id}
                )

        self.assertEqual(len(access_entries), len(r_entries))
        for a_entry, r_entry in zip(access_entries, r_entries):
            self.assertEqual(a_entry.role, r_entry["role"])
            self.assertEqual(a_entry.entity_type, r_entry["entity_type"])
            self.assertEqual(a_entry.entity_id, r_entry["entity_id"])

    def _verify_readonly_resource_properties(self, dataset, resource):
        self.assertEqual(dataset.project, self.PROJECT)
        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.reference.project, self.PROJECT)
        self.assertEqual(dataset.reference.dataset_id, self.DS_ID)

        if "creationTime" in resource:
            self.assertEqual(dataset.created, self.WHEN)
        else:
            self.assertIsNone(dataset.created)
        if "etag" in resource:
            self.assertEqual(dataset.etag, self.ETAG)
        else:
            self.assertIsNone(dataset.etag)
        if "lastModifiedTime" in resource:
            self.assertEqual(dataset.modified, self.WHEN)
        else:
            self.assertIsNone(dataset.modified)
        if "selfLink" in resource:
            self.assertEqual(dataset.self_link, self.RESOURCE_URL)
        else:
            self.assertIsNone(dataset.self_link)

    def _verify_resource_properties(self, dataset, resource):
        self._verify_readonly_resource_properties(dataset, resource)

        if "defaultTableExpirationMs" in resource:
            self.assertEqual(
                dataset.default_table_expiration_ms,
                int(resource.get("defaultTableExpirationMs")),
            )
        else:
            self.assertIsNone(dataset.default_table_expiration_ms)
        self.assertEqual(dataset.description, resource.get("description"))
        self.assertEqual(dataset.friendly_name, resource.get("friendlyName"))
        self.assertEqual(dataset.location, resource.get("location"))
        self.assertEqual(
            dataset.is_case_insensitive, resource.get("isCaseInsensitive") or False
        )
        if "defaultEncryptionConfiguration" in resource:
            self.assertEqual(
                dataset.default_encryption_configuration.kms_key_name,
                resource.get("defaultEncryptionConfiguration")["kmsKeyName"],
            )
        else:
            self.assertIsNone(dataset.default_encryption_configuration)
        if "storageBillingModel" in resource:
            self.assertEqual(
                dataset.storage_billing_model, resource.get("storageBillingModel")
            )
        else:
            self.assertIsNone(dataset.storage_billing_model)
        if "access" in resource:
            self._verify_access_entry(dataset.access_entries, resource)
        else:
            self.assertEqual(dataset.access_entries, [])

    def test_ctor_defaults(self):
        dataset = self._make_one(self.DS_REF)
        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, self.PROJECT)
        self.assertEqual(
            dataset.path, "/projects/%s/datasets/%s" % (self.PROJECT, self.DS_ID)
        )
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
        self.assertEqual(dataset.is_case_insensitive, False)

    def test_ctor_string(self):
        dataset = self._make_one("some-project.some_dset")
        self.assertEqual(dataset.project, "some-project")
        self.assertEqual(dataset.dataset_id, "some_dset")

    def test_ctor_string_wo_project_id(self):
        with pytest.raises(ValueError):
            # Project ID is missing.
            self._make_one("some_dset")

    def test_ctor_explicit(self):
        from google.cloud.bigquery.dataset import DatasetReference, AccessEntry

        phred = AccessEntry("OWNER", "userByEmail", "phred@example.com")
        bharney = AccessEntry("OWNER", "userByEmail", "bharney@example.com")
        entries = [phred, bharney]
        OTHER_PROJECT = "foo-bar-123"
        dataset = self._make_one(DatasetReference(OTHER_PROJECT, self.DS_ID))
        dataset.access_entries = entries
        self.assertEqual(dataset.dataset_id, self.DS_ID)
        self.assertEqual(dataset.project, OTHER_PROJECT)
        self.assertEqual(
            dataset.path, "/projects/%s/datasets/%s" % (OTHER_PROJECT, self.DS_ID)
        )
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
        self.assertEqual(dataset.is_case_insensitive, False)

    def test_access_entries_setter_non_list(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(TypeError):
            dataset.access_entries = object()

    def test_access_entries_setter_invalid_field(self):
        from google.cloud.bigquery.dataset import AccessEntry

        dataset = self._make_one(self.DS_REF)
        phred = AccessEntry("OWNER", "userByEmail", "phred@example.com")
        with self.assertRaises(ValueError):
            dataset.access_entries = [phred, object()]

    def test_access_entries_setter(self):
        from google.cloud.bigquery.dataset import AccessEntry

        dataset = self._make_one(self.DS_REF)
        phred = AccessEntry("OWNER", "userByEmail", "phred@example.com")
        bharney = AccessEntry("OWNER", "userByEmail", "bharney@example.com")
        dataset.access_entries = [phred, bharney]
        self.assertEqual(dataset.access_entries, [phred, bharney])

    def test_default_partition_expiration_ms(self):
        dataset = self._make_one("proj.dset")
        assert dataset.default_partition_expiration_ms is None
        dataset.default_partition_expiration_ms = 12345
        assert dataset.default_partition_expiration_ms == 12345
        dataset.default_partition_expiration_ms = None
        assert dataset.default_partition_expiration_ms is None

    def test_default_table_expiration_ms_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.default_table_expiration_ms = "bogus"

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
        dataset.description = "DESCRIPTION"
        self.assertEqual(dataset.description, "DESCRIPTION")

    def test_friendly_name_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.friendly_name = 12345

    def test_friendly_name_setter(self):
        dataset = self._make_one(self.DS_REF)
        dataset.friendly_name = "FRIENDLY"
        self.assertEqual(dataset.friendly_name, "FRIENDLY")

    def test_location_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.location = 12345

    def test_location_setter(self):
        dataset = self._make_one(self.DS_REF)
        dataset.location = "LOCATION"
        self.assertEqual(dataset.location, "LOCATION")

    def test_resource_tags_update_in_place(self):
        dataset = self._make_one(self.DS_REF)
        tags = dataset.resource_tags
        tags["123456789012/foo"] = "bar"  # update in place
        self.assertEqual(dataset.resource_tags, {"123456789012/foo": "bar"})

    def test_resource_tags_setter(self):
        dataset = self._make_one(self.DS_REF)
        dataset.resource_tags = {"123456789012/foo": "bar"}
        self.assertEqual(dataset.resource_tags, {"123456789012/foo": "bar"})

    def test_resource_tags_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.resource_tags = "invalid"
        with self.assertRaises(ValueError):
            dataset.resource_tags = 123

    def test_resource_tags_getter_missing_value(self):
        dataset = self._make_one(self.DS_REF)
        self.assertEqual(dataset.resource_tags, {})

    def test_labels_update_in_place(self):
        dataset = self._make_one(self.DS_REF)
        del dataset._properties["labels"]  # don't start w/ existing dict
        labels = dataset.labels
        labels["foo"] = "bar"  # update in place
        self.assertEqual(dataset.labels, {"foo": "bar"})

    def test_labels_setter(self):
        dataset = self._make_one(self.DS_REF)
        dataset.labels = {"color": "green"}
        self.assertEqual(dataset.labels, {"color": "green"})

    def test_labels_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.labels = None

    def test_labels_getter_missing_value(self):
        dataset = self._make_one(self.DS_REF)
        self.assertEqual(dataset.labels, {})

    def test_is_case_insensitive_setter_bad_value(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError):
            dataset.is_case_insensitive = 0

    def test_is_case_insensitive_setter_true(self):
        dataset = self._make_one(self.DS_REF)
        dataset.is_case_insensitive = True
        self.assertEqual(dataset.is_case_insensitive, True)

    def test_is_case_insensitive_setter_none(self):
        dataset = self._make_one(self.DS_REF)
        dataset.is_case_insensitive = None
        self.assertEqual(dataset.is_case_insensitive, False)

    def test_is_case_insensitive_setter_false(self):
        dataset = self._make_one(self.DS_REF)
        dataset.is_case_insensitive = False
        self.assertEqual(dataset.is_case_insensitive, False)

    def test_from_api_repr_missing_identity(self):
        self._setUpConstants()
        RESOURCE = {}
        klass = self._get_target_class()
        with self.assertRaises(KeyError):
            klass.from_api_repr(RESOURCE)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        RESOURCE = {
            "id": "%s:%s" % (self.PROJECT, self.DS_ID),
            "datasetReference": {"projectId": self.PROJECT, "datasetId": self.DS_ID},
        }
        klass = self._get_target_class()
        dataset = klass.from_api_repr(RESOURCE)
        self._verify_resource_properties(dataset, RESOURCE)

    def test_from_api_repr_w_properties(self):
        RESOURCE = self._make_resource()
        klass = self._get_target_class()
        dataset = klass.from_api_repr(RESOURCE)
        self._verify_resource_properties(dataset, RESOURCE)

    def test_to_api_repr_w_custom_field(self):
        dataset = self._make_one(self.DS_REF)
        dataset._properties["newAlphaProperty"] = "unreleased property"
        resource = dataset.to_api_repr()

        exp_resource = {
            "datasetReference": self.DS_REF.to_api_repr(),
            "labels": {},
            "newAlphaProperty": "unreleased property",
        }
        self.assertEqual(resource, exp_resource)

    def test_default_encryption_configuration_setter(self):
        from google.cloud.bigquery.encryption_configuration import (
            EncryptionConfiguration,
        )

        dataset = self._make_one(self.DS_REF)
        encryption_configuration = EncryptionConfiguration(
            kms_key_name=self.KMS_KEY_NAME
        )
        dataset.default_encryption_configuration = encryption_configuration
        self.assertEqual(
            dataset.default_encryption_configuration.kms_key_name, self.KMS_KEY_NAME
        )
        dataset.default_encryption_configuration = None
        self.assertIsNone(dataset.default_encryption_configuration)

    def test_storage_billing_model_setter(self):
        dataset = self._make_one(self.DS_REF)
        dataset.storage_billing_model = "PHYSICAL"
        self.assertEqual(dataset.storage_billing_model, "PHYSICAL")

    def test_storage_billing_model_setter_with_none(self):
        dataset = self._make_one(self.DS_REF)
        dataset.storage_billing_model = None
        self.assertIsNone(dataset.storage_billing_model)

    def test_storage_billing_model_setter_with_invalid_type(self):
        dataset = self._make_one(self.DS_REF)
        with self.assertRaises(ValueError) as raises:
            dataset.storage_billing_model = object()

        self.assertIn("storage_billing_model", str(raises.exception))

    def test_from_string(self):
        cls = self._get_target_class()
        got = cls.from_string("string-project.string_dataset")
        self.assertEqual(got.project, "string-project")
        self.assertEqual(got.dataset_id, "string_dataset")

    def test_from_string_legacy_string(self):
        cls = self._get_target_class()
        with self.assertRaises(ValueError):
            cls.from_string("string-project:string_dataset")

    def test__build_resource_w_custom_field(self):
        dataset = self._make_one(self.DS_REF)
        dataset._properties["newAlphaProperty"] = "unreleased property"
        resource = dataset._build_resource(["newAlphaProperty"])

        exp_resource = {"newAlphaProperty": "unreleased property"}
        self.assertEqual(resource, exp_resource)

    def test__build_resource_w_custom_field_not_in__properties(self):
        dataset = self._make_one(self.DS_REF)
        dataset.bad = "value"
        with self.assertRaises(ValueError):
            dataset._build_resource(["bad"])

    def test_table(self):
        from google.cloud.bigquery.table import TableReference

        dataset = self._make_one(self.DS_REF)
        table = dataset.table("table_id")
        self.assertIsInstance(table, TableReference)
        self.assertEqual(table.table_id, "table_id")
        self.assertEqual(table.dataset_id, self.DS_ID)
        self.assertEqual(table.project, self.PROJECT)

    def test___repr__(self):
        from google.cloud.bigquery.dataset import DatasetReference

        dataset = self._make_one(DatasetReference("project1", "dataset1"))
        expected = "Dataset(DatasetReference('project1', 'dataset1'))"
        self.assertEqual(repr(dataset), expected)

    def test_external_catalog_dataset_options_setter(self):
        # GIVEN the parameters DEFAULT_STORAGE_LOCATION_URI and PARAMETERS
        # WHEN an ExternalCatalogDatasetOptions obj is created
        #     and added to a dataset.
        # THEN the api representation of the dataset will match API_REPR

        from google.cloud.bigquery.external_config import ExternalCatalogDatasetOptions

        dataset = self._make_one(self.DS_REF)

        ecdo_obj = ExternalCatalogDatasetOptions(
            default_storage_location_uri=self.DEFAULT_STORAGE_LOCATION_URI,
            parameters=self.PARAMETERS,
        )
        dataset.external_catalog_dataset_options = ecdo_obj

        result = dataset.to_api_repr()
        expected = self.API_REPR
        assert result == expected

    def test_external_catalog_dataset_options_getter_prop_exists(self):
        # GIVEN default dataset PLUS an ExternalCatalogDatasetOptions
        # THEN confirm that the api_repr of the ExternalCatalogDatasetsOptions
        #     matches the api_repr of the external_catalog_dataset_options attribute.

        from google.cloud.bigquery.external_config import ExternalCatalogDatasetOptions

        dataset = self._make_one(self.DS_REF)
        ecdo_obj = ExternalCatalogDatasetOptions(
            default_storage_location_uri=self.DEFAULT_STORAGE_LOCATION_URI,
            parameters=self.PARAMETERS,
        )
        dataset.external_catalog_dataset_options = ecdo_obj
        result = dataset.external_catalog_dataset_options.to_api_repr()
        expected = ecdo_obj.to_api_repr()
        assert result == expected

    def test_external_catalog_dataset_options_getter_prop_is_none(self):
        # GIVEN only a default dataset
        # THEN confirm that external_catalog_dataset_options is None

        dataset = self._make_one(self.DS_REF)
        expected = None
        result = dataset.external_catalog_dataset_options
        assert result == expected

    def test_external_catalog_dataset_options_from_api_repr(self):
        # GIVEN default dataset including an ExternalCatalogDatasetOptions
        # THEN confirm that the api_repr of the ExternalCatalogDatasetsOptions
        #     on a dataset object created via from_api_repr matches the api_repr
        #     of the "externalCatalogDatasetOptions" key.

        api_repr = self.API_REPR
        klass = self._get_target_class()
        dataset = klass.from_api_repr(api_repr)

        result = dataset.external_catalog_dataset_options.to_api_repr()
        expected = api_repr["externalCatalogDatasetOptions"]
        assert result == expected

    def test_external_catalog_dataset_options_to_api_repr(self):
        # GIVEN a dataset api_repr including an ExternalCatalogDatasetOptions key
        # THEN confirm that the api_repr of that key from a dataset object created
        #     via the to_api_repr() method matches the value of the key
        #     used to create the dataset object

        api_repr = self.API_REPR
        klass = self._get_target_class()
        dataset = klass.from_api_repr(api_repr)

        result = dataset.to_api_repr()["externalCatalogDatasetOptions"]
        expected = api_repr["externalCatalogDatasetOptions"]
        assert result == expected


class TestDatasetListItem(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.dataset import DatasetListItem

        return DatasetListItem

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        project = "test-project"
        dataset_id = "test_dataset"
        resource = {
            "kind": "bigquery#dataset",
            "id": "{}:{}".format(project, dataset_id),
            "datasetReference": {"projectId": project, "datasetId": dataset_id},
            "friendlyName": "Data of the Test",
            "labels": {"some-stuff": "this-is-a-label"},
        }

        dataset = self._make_one(resource)
        self.assertEqual(dataset.project, project)
        self.assertEqual(dataset.dataset_id, dataset_id)
        self.assertEqual(dataset.full_dataset_id, "{}:{}".format(project, dataset_id))
        self.assertEqual(dataset.reference.project, project)
        self.assertEqual(dataset.reference.dataset_id, dataset_id)
        self.assertEqual(dataset.friendly_name, "Data of the Test")
        self.assertEqual(dataset.labels["some-stuff"], "this-is-a-label")

    def test_ctor_missing_properties(self):
        resource = {
            "datasetReference": {"projectId": "testproject", "datasetId": "testdataset"}
        }
        dataset = self._make_one(resource)
        self.assertEqual(dataset.project, "testproject")
        self.assertEqual(dataset.dataset_id, "testdataset")
        self.assertIsNone(dataset.full_dataset_id)
        self.assertIsNone(dataset.friendly_name)
        self.assertEqual(dataset.labels, {})

    def test_ctor_wo_project(self):
        resource = {"datasetReference": {"datasetId": "testdataset"}}
        with self.assertRaises(ValueError):
            self._make_one(resource)

    def test_ctor_wo_dataset(self):
        resource = {"datasetReference": {"projectId": "testproject"}}
        with self.assertRaises(ValueError):
            self._make_one(resource)

    def test_ctor_wo_reference(self):
        with self.assertRaises(ValueError):
            self._make_one({})

    def test_labels_update_in_place(self):
        resource = {
            "datasetReference": {"projectId": "testproject", "datasetId": "testdataset"}
        }
        dataset = self._make_one(resource)
        labels = dataset.labels
        labels["foo"] = "bar"  # update in place
        self.assertEqual(dataset.labels, {"foo": "bar"})

    def test_table(self):
        from google.cloud.bigquery.table import TableReference

        project = "test-project"
        dataset_id = "test_dataset"
        resource = {"datasetReference": {"projectId": project, "datasetId": dataset_id}}
        dataset = self._make_one(resource)
        table = dataset.table("table_id")
        self.assertIsInstance(table, TableReference)
        self.assertEqual(table.table_id, "table_id")
        self.assertEqual(table.dataset_id, dataset_id)
        self.assertEqual(table.project, project)


class TestCondition:
    EXPRESSION = 'resource.name.startsWith("projects/my-project/instances/")'
    TITLE = "Instance Access"
    DESCRIPTION = "Access to instances in my-project"

    @pytest.fixture
    def condition_instance(self):
        """Provides a Condition instance for tests."""
        return Condition(
            expression=self.EXPRESSION,
            title=self.TITLE,
            description=self.DESCRIPTION,
        )

    @pytest.fixture
    def condition_api_repr(self):
        """Provides the API representation for the test Condition."""
        return {
            "expression": self.EXPRESSION,
            "title": self.TITLE,
            "description": self.DESCRIPTION,
        }

    # --- Basic Functionality Tests ---

    def test_constructor_and_getters_full(self, condition_instance):
        """Test initialization with all arguments and subsequent attribute access."""
        assert condition_instance.expression == self.EXPRESSION
        assert condition_instance.title == self.TITLE
        assert condition_instance.description == self.DESCRIPTION

    def test_constructor_and_getters_minimal(self):
        """Test initialization with only the required expression."""
        condition = Condition(expression=self.EXPRESSION)
        assert condition.expression == self.EXPRESSION
        assert condition.title is None
        assert condition.description is None

    def test_setters(self, condition_instance):
        """Test setting attributes after initialization."""
        new_title = "New Title"
        new_desc = "New Description"
        new_expr = "request.time < timestamp('2024-01-01T00:00:00Z')"

        condition_instance.title = new_title
        assert condition_instance.title == new_title

        condition_instance.description = new_desc
        assert condition_instance.description == new_desc

        condition_instance.expression = new_expr
        assert condition_instance.expression == new_expr

        # Test setting title and description to empty strings
        condition_instance.title = ""
        assert condition_instance.title == ""

        condition_instance.description = ""
        assert condition_instance.description == ""

        # Test setting optional fields back to None
        condition_instance.title = None
        assert condition_instance.title is None
        condition_instance.description = None
        assert condition_instance.description is None

    # --- API Representation Tests ---

    def test_to_api_repr_full(self, condition_instance, condition_api_repr):
        """Test converting a fully populated Condition to API representation."""
        api_repr = condition_instance.to_api_repr()
        assert api_repr == condition_api_repr

    def test_to_api_repr_minimal(self):
        """Test converting a minimally populated Condition to API representation."""
        condition = Condition(expression=self.EXPRESSION)
        expected_api_repr = {
            "expression": self.EXPRESSION,
            "title": None,
            "description": None,
        }
        api_repr = condition.to_api_repr()
        assert api_repr == expected_api_repr

    def test_from_api_repr_full(self, condition_api_repr):
        """Test creating a Condition from a full API representation."""
        condition = Condition.from_api_repr(condition_api_repr)
        assert condition.expression == self.EXPRESSION
        assert condition.title == self.TITLE
        assert condition.description == self.DESCRIPTION

    def test_from_api_repr_minimal(self):
        """Test creating a Condition from a minimal API representation."""
        minimal_repr = {"expression": self.EXPRESSION}
        condition = Condition.from_api_repr(minimal_repr)
        assert condition.expression == self.EXPRESSION
        assert condition.title is None
        assert condition.description is None

    def test_from_api_repr_with_extra_fields(self):
        """Test creating a Condition from an API repr with unexpected fields."""
        api_repr = {
            "expression": self.EXPRESSION,
            "title": self.TITLE,
            "unexpected_field": "some_value",
        }
        condition = Condition.from_api_repr(api_repr)
        assert condition.expression == self.EXPRESSION
        assert condition.title == self.TITLE
        assert condition.description is None
        # Check that the extra field didn't get added to internal properties
        assert "unexpected_field" not in condition._properties

    #     # --- Validation Tests ---

    @pytest.mark.parametrize(
        "kwargs, error_msg",
        [
            ({"expression": None}, "Pass a non-empty string for expression"),  # type: ignore
            ({"expression": ""}, "expression cannot be an empty string"),
            ({"expression": 123}, "Pass a non-empty string for expression"),  # type: ignore
            ({"expression": EXPRESSION, "title": 123}, "Pass a string for title, or None"),  # type: ignore
            ({"expression": EXPRESSION, "description": False}, "Pass a string for description, or None"),  # type: ignore
        ],
    )
    def test_validation_init(self, kwargs, error_msg):
        """Test validation during __init__."""
        with pytest.raises(ValueError, match=error_msg):
            Condition(**kwargs)

    @pytest.mark.parametrize(
        "attribute, value, error_msg",
        [
            ("expression", None, "Pass a non-empty string for expression"),  # type: ignore
            ("expression", "", "expression cannot be an empty string"),
            ("expression", 123, "Pass a non-empty string for expression"),  # type: ignore
            ("title", 123, "Pass a string for title, or None"),  # type: ignore
            ("description", [], "Pass a string for description, or None"),  # type: ignore
        ],
    )
    def test_validation_setters(self, condition_instance, attribute, value, error_msg):
        """Test validation via setters."""
        with pytest.raises(ValueError, match=error_msg):
            setattr(condition_instance, attribute, value)

    def test_validation_expression_required_from_api(self):
        """Test ValueError is raised if expression is missing in from_api_repr."""
        api_repr = {"title": self.TITLE}
        with pytest.raises(
            ValueError, match="API representation missing required 'expression' field."
        ):
            Condition.from_api_repr(api_repr)
