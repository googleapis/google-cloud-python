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

import concurrent
import copy
import http
import textwrap
import types

import freezegun
from google.api_core import exceptions
import google.api_core.retry
import mock
import requests

from google.cloud.bigquery.client import _LIST_ROWS_FROM_QUERY_RESULTS_FIELDS
import google.cloud.bigquery.query
from google.cloud.bigquery.table import _EmptyRowIterator

from ..helpers import make_connection

from .helpers import _Base
from .helpers import _make_client


class TestQueryJob(_Base):
    JOB_TYPE = "query"
    QUERY = "select count(*) from persons"
    DESTINATION_TABLE = "destination_table"

    @staticmethod
    def _get_target_class():
        from google.cloud.bigquery.job import QueryJob

        return QueryJob

    def _make_resource(self, started=False, ended=False, location="US"):
        resource = super(TestQueryJob, self)._make_resource(
            started, ended, location=location
        )
        config = resource["configuration"]["query"]
        config["query"] = self.QUERY
        return resource

    def _verifyBooleanResourceProperties(self, job, config):

        if "allowLargeResults" in config:
            self.assertEqual(job.allow_large_results, config["allowLargeResults"])
        else:
            self.assertIsNone(job.allow_large_results)
        if "flattenResults" in config:
            self.assertEqual(job.flatten_results, config["flattenResults"])
        else:
            self.assertIsNone(job.flatten_results)
        if "useQueryCache" in config:
            self.assertEqual(job.use_query_cache, config["useQueryCache"])
        else:
            self.assertIsNone(job.use_query_cache)
        if "useLegacySql" in config:
            self.assertEqual(job.use_legacy_sql, config["useLegacySql"])
        else:
            self.assertIsNone(job.use_legacy_sql)

    def _verifyIntegerResourceProperties(self, job, config):
        if "maximumBillingTier" in config:
            self.assertEqual(job.maximum_billing_tier, config["maximumBillingTier"])
        else:
            self.assertIsNone(job.maximum_billing_tier)
        if "maximumBytesBilled" in config:
            self.assertEqual(
                str(job.maximum_bytes_billed), config["maximumBytesBilled"]
            )
            self.assertIsInstance(job.maximum_bytes_billed, int)
        else:
            self.assertIsNone(job.maximum_bytes_billed)

    def _verify_udf_resources(self, job, config):
        udf_resources = config.get("userDefinedFunctionResources", ())
        self.assertEqual(len(job.udf_resources), len(udf_resources))
        for found, expected in zip(job.udf_resources, udf_resources):
            if "resourceUri" in expected:
                self.assertEqual(found.udf_type, "resourceUri")
                self.assertEqual(found.value, expected["resourceUri"])
            else:
                self.assertEqual(found.udf_type, "inlineCode")
                self.assertEqual(found.value, expected["inlineCode"])

    def _verifyQueryParameters(self, job, config):
        query_parameters = config.get("queryParameters", ())
        self.assertEqual(len(job.query_parameters), len(query_parameters))
        for found, expected in zip(job.query_parameters, query_parameters):
            self.assertEqual(found.to_api_repr(), expected)

    def _verify_table_definitions(self, job, config):
        table_defs = config.get("tableDefinitions")
        if job.table_definitions is None:
            self.assertIsNone(table_defs)
        else:
            self.assertEqual(len(job.table_definitions), len(table_defs))
            for found_key, found_ec in job.table_definitions.items():
                expected_ec = table_defs.get(found_key)
                self.assertIsNotNone(expected_ec)
                self.assertEqual(found_ec.to_api_repr(), expected_ec)

    def _verify_dml_stats_resource_properties(self, job, resource):
        query_stats = resource.get("statistics", {}).get("query", {})

        if "dmlStats" in query_stats:
            resource_dml_stats = query_stats["dmlStats"]
            job_dml_stats = job.dml_stats
            assert str(job_dml_stats.inserted_row_count) == resource_dml_stats.get(
                "insertedRowCount", "0"
            )
            assert str(job_dml_stats.updated_row_count) == resource_dml_stats.get(
                "updatedRowCount", "0"
            )
            assert str(job_dml_stats.deleted_row_count) == resource_dml_stats.get(
                "deletedRowCount", "0"
            )
        else:
            assert job.dml_stats is None

    def _verify_transaction_info_resource_properties(self, job, resource):
        resource_stats = resource.get("statistics", {})

        if "transactionInfo" in resource_stats:
            resource_transaction_info = resource_stats["transactionInfo"]
            job_transaction_info = job.transaction_info
            assert job_transaction_info.transaction_id == resource_transaction_info.get(
                "transactionId"
            )
        else:
            assert job.transaction_info is None

    def _verify_configuration_properties(self, job, configuration):
        if "dryRun" in configuration:
            self.assertEqual(job.dry_run, configuration["dryRun"])
        else:
            self.assertIsNone(job.dry_run)

    def _verifyResourceProperties(self, job, resource):
        self._verifyReadonlyResourceProperties(job, resource)
        self._verify_dml_stats_resource_properties(job, resource)
        self._verify_transaction_info_resource_properties(job, resource)

        configuration = resource.get("configuration", {})
        self._verify_configuration_properties(job, configuration)

        query_config = resource.get("configuration", {}).get("query")
        self._verifyBooleanResourceProperties(job, query_config)
        self._verifyIntegerResourceProperties(job, query_config)
        self._verify_udf_resources(job, query_config)
        self._verifyQueryParameters(job, query_config)
        self._verify_table_definitions(job, query_config)

        self.assertEqual(job.query, query_config["query"])

        if "createDisposition" in query_config:
            self.assertEqual(job.create_disposition, query_config["createDisposition"])
        else:
            self.assertIsNone(job.create_disposition)

        if "defaultDataset" in query_config:
            ds_ref = job.default_dataset
            ds_ref = {"projectId": ds_ref.project, "datasetId": ds_ref.dataset_id}
            self.assertEqual(ds_ref, query_config["defaultDataset"])
        else:
            self.assertIsNone(job.default_dataset)

        if "destinationTable" in query_config:
            table = job.destination
            tb_ref = {
                "projectId": table.project,
                "datasetId": table.dataset_id,
                "tableId": table.table_id,
            }
            self.assertEqual(tb_ref, query_config["destinationTable"])
        else:
            self.assertIsNone(job.destination)

        if "priority" in query_config:
            self.assertEqual(job.priority, query_config["priority"])
        else:
            self.assertIsNone(job.priority)

        if "writeDisposition" in query_config:
            self.assertEqual(job.write_disposition, query_config["writeDisposition"])
        else:
            self.assertIsNone(job.write_disposition)

        if "destinationEncryptionConfiguration" in query_config:
            self.assertIsNotNone(job.destination_encryption_configuration)
            self.assertEqual(
                job.destination_encryption_configuration.kms_key_name,
                query_config["destinationEncryptionConfiguration"]["kmsKeyName"],
            )
        else:
            self.assertIsNone(job.destination_encryption_configuration)

        if "schemaUpdateOptions" in query_config:
            self.assertEqual(
                job.schema_update_options, query_config["schemaUpdateOptions"]
            )
        else:
            self.assertIsNone(job.schema_update_options)

    def test_ctor_defaults(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.query, self.QUERY)
        self.assertIs(job._client, client)
        self.assertEqual(job.job_type, self.JOB_TYPE)
        self.assertEqual(job.path, "/projects/%s/jobs/%s" % (self.PROJECT, self.JOB_ID))

        self._verifyInitialReadonlyProperties(job)

        self.assertFalse(job.use_legacy_sql)

        # set/read from resource['configuration']['query']
        self.assertIsNone(job.allow_large_results)
        self.assertIsNone(job.create_disposition)
        self.assertIsNone(job.default_dataset)
        self.assertIsNone(job.destination)
        self.assertIsNone(job.dml_stats)
        self.assertIsNone(job.flatten_results)
        self.assertIsNone(job.priority)
        self.assertIsNone(job.use_query_cache)
        self.assertIsNone(job.dry_run)
        self.assertIsNone(job.write_disposition)
        self.assertIsNone(job.maximum_billing_tier)
        self.assertIsNone(job.maximum_bytes_billed)
        self.assertIsNone(job.table_definitions)
        self.assertIsNone(job.destination_encryption_configuration)
        self.assertIsNone(job.range_partitioning)
        self.assertIsNone(job.time_partitioning)
        self.assertIsNone(job.clustering_fields)
        self.assertIsNone(job.schema_update_options)

    def test_ctor_w_udf_resources(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import UDFResource

        RESOURCE_URI = "gs://some-bucket/js/lib.js"
        udf_resources = [UDFResource("resourceUri", RESOURCE_URI)]
        client = _make_client(project=self.PROJECT)
        config = QueryJobConfig()
        config.udf_resources = udf_resources
        job = self._make_one(self.JOB_ID, self.QUERY, client, job_config=config)
        self.assertEqual(job.udf_resources, udf_resources)

    def test_ctor_w_query_parameters(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", "INT64", 123)]
        client = _make_client(project=self.PROJECT)
        config = QueryJobConfig(query_parameters=query_parameters)
        job = self._make_one(self.JOB_ID, self.QUERY, client, job_config=config)
        self.assertEqual(job.query_parameters, query_parameters)

    def test_from_api_repr_bare(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            "id": self.JOB_ID,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "configuration": {"query": {"query": self.QUERY}},
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)
        self.assertEqual(len(job.connection_properties), 0)
        self.assertIsNone(job.create_session)

    def test_from_api_repr_with_encryption(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            "id": self.JOB_ID,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "configuration": {
                "query": {
                    "query": self.QUERY,
                    "destinationEncryptionConfiguration": {
                        "kmsKeyName": self.KMS_KEY_NAME
                    },
                }
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_with_dml_stats(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            "id": self.JOB_ID,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "configuration": {"query": {"query": self.QUERY}},
            "statistics": {
                "query": {
                    "dmlStats": {"insertedRowCount": "15", "updatedRowCount": "2"},
                },
            },
        }
        klass = self._get_target_class()

        job = klass.from_api_repr(RESOURCE, client=client)

        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_with_transaction_info(self):
        self._setUpConstants()
        client = _make_client(project=self.PROJECT)
        RESOURCE = {
            "id": self.JOB_ID,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "configuration": {"query": {"query": self.QUERY}},
            "statistics": {"transactionInfo": {"transactionId": "1a2b-3c4d"}},
        }
        klass = self._get_target_class()

        job = klass.from_api_repr(RESOURCE, client=client)

        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_from_api_repr_w_properties(self):
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import SchemaUpdateOption
        from google.cloud.bigquery.job import WriteDisposition

        client = _make_client(project=self.PROJECT)
        RESOURCE = self._make_resource()
        query_config = RESOURCE["configuration"]["query"]
        query_config["createDisposition"] = CreateDisposition.CREATE_IF_NEEDED
        query_config["writeDisposition"] = WriteDisposition.WRITE_TRUNCATE
        query_config["destinationTable"] = {
            "projectId": self.PROJECT,
            "datasetId": self.DS_ID,
            "tableId": self.DESTINATION_TABLE,
        }
        query_config["schemaUpdateOptions"] = [SchemaUpdateOption.ALLOW_FIELD_ADDITION]
        klass = self._get_target_class()
        job = klass.from_api_repr(RESOURCE, client=client)
        self.assertIs(job._client, client)
        self._verifyResourceProperties(job, RESOURCE)

    def test_cancelled(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        job._properties["status"] = {
            "state": "DONE",
            "errorResult": {"reason": "stopped"},
        }

        self.assertTrue(job.cancelled())

    def test__done_or_raise_w_timeout(self):
        client = _make_client(project=self.PROJECT)
        resource = self._make_resource(ended=False)
        job = self._get_target_class().from_api_repr(resource, client)

        with mock.patch.object(
            client, "_get_query_results"
        ) as fake_get_results, mock.patch.object(job, "reload") as fake_reload:
            job._done_or_raise(timeout=42)

        fake_get_results.assert_called_once()
        call_args = fake_get_results.call_args
        self.assertEqual(call_args.kwargs.get("timeout"), 42)

        call_args = fake_reload.call_args
        self.assertEqual(call_args.kwargs.get("timeout"), 42)

    def test__done_or_raise_w_timeout_and_longer_internal_api_timeout(self):
        client = _make_client(project=self.PROJECT)
        resource = self._make_resource(ended=False)
        job = self._get_target_class().from_api_repr(resource, client)
        job._done_timeout = 8.8

        with mock.patch.object(
            client, "_get_query_results"
        ) as fake_get_results, mock.patch.object(job, "reload") as fake_reload:
            job._done_or_raise(timeout=5.5)

        # The expected timeout used is simply the given timeout, as the latter
        # is shorter than the job's internal done timeout.
        expected_timeout = 5.5

        fake_get_results.assert_called_once()
        call_args = fake_get_results.call_args
        self.assertAlmostEqual(call_args.kwargs.get("timeout"), expected_timeout)

        call_args = fake_reload.call_args
        self.assertAlmostEqual(call_args.kwargs.get("timeout"), expected_timeout)

    def test__done_or_raise_w_query_results_error_reload_ok(self):
        client = _make_client(project=self.PROJECT)
        bad_request_error = exceptions.BadRequest("Error in query")
        client._get_query_results = mock.Mock(side_effect=bad_request_error)

        resource = self._make_resource(ended=False)
        job = self._get_target_class().from_api_repr(resource, client)
        job._exception = None

        def fake_reload(self, *args, **kwargs):
            self._properties["status"]["state"] = "DONE"
            self.set_exception(copy.copy(bad_request_error))

        fake_reload_method = types.MethodType(fake_reload, job)

        with mock.patch.object(job, "reload", new=fake_reload_method):
            job._done_or_raise()

        assert isinstance(job._exception, exceptions.BadRequest)

    def test__done_or_raise_w_query_results_error_reload_error(self):
        client = _make_client(project=self.PROJECT)
        bad_request_error = exceptions.BadRequest("Error in query")
        client._get_query_results = mock.Mock(side_effect=bad_request_error)

        resource = self._make_resource(ended=False)
        job = self._get_target_class().from_api_repr(resource, client)
        reload_error = exceptions.DataLoss("Oops, sorry!")
        job.reload = mock.Mock(side_effect=reload_error)
        job._exception = None

        job._done_or_raise()

        assert job._exception is bad_request_error

    def test__done_or_raise_w_job_query_results_ok_reload_error(self):
        client = _make_client(project=self.PROJECT)
        query_results = google.cloud.bigquery.query._QueryResults(
            properties={
                "jobComplete": True,
                "jobReference": {"projectId": self.PROJECT, "jobId": "12345"},
            }
        )
        client._get_query_results = mock.Mock(return_value=query_results)

        resource = self._make_resource(ended=False)
        job = self._get_target_class().from_api_repr(resource, client)
        retry_error = exceptions.RetryError("Too many retries", cause=TimeoutError)
        job.reload = mock.Mock(side_effect=retry_error)
        job._exception = None

        job._done_or_raise()

        assert job._exception is retry_error

    def test_query_plan(self):
        from google.cloud._helpers import _RFC3339_MICROS
        from google.cloud.bigquery.job import QueryPlanEntry
        from google.cloud.bigquery.job import QueryPlanEntryStep

        plan_entries = [
            {
                "name": "NAME",
                "id": "1234",
                "inputStages": ["88", "101"],
                "startMs": "1522540800000",
                "endMs": "1522540804000",
                "parallelInputs": "1000",
                "completedParallelInputs": "5",
                "waitMsAvg": "33",
                "waitMsMax": "400",
                "waitRatioAvg": 2.71828,
                "waitRatioMax": 3.14159,
                "readMsAvg": "45",
                "readMsMax": "90",
                "readRatioAvg": 1.41421,
                "readRatioMax": 1.73205,
                "computeMsAvg": "55",
                "computeMsMax": "99",
                "computeRatioAvg": 0.69315,
                "computeRatioMax": 1.09861,
                "writeMsAvg": "203",
                "writeMsMax": "340",
                "writeRatioAvg": 3.32193,
                "writeRatioMax": 2.30258,
                "recordsRead": "100",
                "recordsWritten": "1",
                "status": "STATUS",
                "shuffleOutputBytes": "1024",
                "shuffleOutputBytesSpilled": "1",
                "steps": [{"kind": "KIND", "substeps": ["SUBSTEP1", "SUBSTEP2"]}],
            }
        ]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.query_plan, [])

        statistics = job._properties["statistics"] = {}
        self.assertEqual(job.query_plan, [])

        query_stats = statistics["query"] = {}
        self.assertEqual(job.query_plan, [])

        query_stats["queryPlan"] = plan_entries

        self.assertEqual(len(job.query_plan), len(plan_entries))
        for found, expected in zip(job.query_plan, plan_entries):
            self.assertIsInstance(found, QueryPlanEntry)
            self.assertEqual(found.name, expected["name"])
            self.assertEqual(found.entry_id, expected["id"])
            self.assertEqual(len(found.input_stages), len(expected["inputStages"]))
            for f_id in found.input_stages:
                self.assertIn(f_id, [int(e) for e in expected["inputStages"]])
            self.assertEqual(
                found.start.strftime(_RFC3339_MICROS), "2018-04-01T00:00:00.000000Z"
            )
            self.assertEqual(
                found.end.strftime(_RFC3339_MICROS), "2018-04-01T00:00:04.000000Z"
            )
            self.assertEqual(found.parallel_inputs, int(expected["parallelInputs"]))
            self.assertEqual(
                found.completed_parallel_inputs,
                int(expected["completedParallelInputs"]),
            )
            self.assertEqual(found.wait_ms_avg, int(expected["waitMsAvg"]))
            self.assertEqual(found.wait_ms_max, int(expected["waitMsMax"]))
            self.assertEqual(found.wait_ratio_avg, expected["waitRatioAvg"])
            self.assertEqual(found.wait_ratio_max, expected["waitRatioMax"])
            self.assertEqual(found.read_ms_avg, int(expected["readMsAvg"]))
            self.assertEqual(found.read_ms_max, int(expected["readMsMax"]))
            self.assertEqual(found.read_ratio_avg, expected["readRatioAvg"])
            self.assertEqual(found.read_ratio_max, expected["readRatioMax"])
            self.assertEqual(found.compute_ms_avg, int(expected["computeMsAvg"]))
            self.assertEqual(found.compute_ms_max, int(expected["computeMsMax"]))
            self.assertEqual(found.compute_ratio_avg, expected["computeRatioAvg"])
            self.assertEqual(found.compute_ratio_max, expected["computeRatioMax"])
            self.assertEqual(found.write_ms_avg, int(expected["writeMsAvg"]))
            self.assertEqual(found.write_ms_max, int(expected["writeMsMax"]))
            self.assertEqual(found.write_ratio_avg, expected["writeRatioAvg"])
            self.assertEqual(found.write_ratio_max, expected["writeRatioMax"])
            self.assertEqual(found.records_read, int(expected["recordsRead"]))
            self.assertEqual(found.records_written, int(expected["recordsWritten"]))
            self.assertEqual(found.status, expected["status"])
            self.assertEqual(
                found.shuffle_output_bytes, int(expected["shuffleOutputBytes"])
            )
            self.assertEqual(
                found.shuffle_output_bytes_spilled,
                int(expected["shuffleOutputBytesSpilled"]),
            )

            self.assertEqual(len(found.steps), len(expected["steps"]))
            for f_step, e_step in zip(found.steps, expected["steps"]):
                self.assertIsInstance(f_step, QueryPlanEntryStep)
                self.assertEqual(f_step.kind, e_step["kind"])
                self.assertEqual(f_step.substeps, e_step["substeps"])

    def test_total_bytes_processed(self):
        total_bytes = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.total_bytes_processed)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.total_bytes_processed)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.total_bytes_processed)

        query_stats["totalBytesProcessed"] = str(total_bytes)
        self.assertEqual(job.total_bytes_processed, total_bytes)

    def test_total_bytes_billed(self):
        total_bytes = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.total_bytes_billed)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.total_bytes_billed)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.total_bytes_billed)

        query_stats["totalBytesBilled"] = str(total_bytes)
        self.assertEqual(job.total_bytes_billed, total_bytes)

    def test_billing_tier(self):
        billing_tier = 1
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.billing_tier)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.billing_tier)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.billing_tier)

        query_stats["billingTier"] = billing_tier
        self.assertEqual(job.billing_tier, billing_tier)

    def test_cache_hit(self):
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.cache_hit)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.cache_hit)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.cache_hit)

        query_stats["cacheHit"] = True
        self.assertTrue(job.cache_hit)

    def test_ddl_operation_performed(self):
        op = "SKIP"
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.ddl_operation_performed)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.ddl_operation_performed)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.ddl_operation_performed)

        query_stats["ddlOperationPerformed"] = op
        self.assertEqual(job.ddl_operation_performed, op)

    def test_ddl_target_routine(self):
        from google.cloud.bigquery.routine import RoutineReference

        ref_routine = {
            "projectId": self.PROJECT,
            "datasetId": "ddl_ds",
            "routineId": "targetroutine",
        }
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.ddl_target_routine)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.ddl_target_routine)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.ddl_target_routine)

        query_stats["ddlTargetRoutine"] = ref_routine
        self.assertIsInstance(job.ddl_target_routine, RoutineReference)
        self.assertEqual(job.ddl_target_routine.routine_id, "targetroutine")
        self.assertEqual(job.ddl_target_routine.dataset_id, "ddl_ds")
        self.assertEqual(job.ddl_target_routine.project, self.PROJECT)

    def test_ddl_target_table(self):
        from google.cloud.bigquery.table import TableReference

        ref_table = {
            "projectId": self.PROJECT,
            "datasetId": "ddl_ds",
            "tableId": "targettable",
        }
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.ddl_target_table)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.ddl_target_table)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.ddl_target_table)

        query_stats["ddlTargetTable"] = ref_table
        self.assertIsInstance(job.ddl_target_table, TableReference)
        self.assertEqual(job.ddl_target_table.table_id, "targettable")
        self.assertEqual(job.ddl_target_table.dataset_id, "ddl_ds")
        self.assertEqual(job.ddl_target_table.project, self.PROJECT)

    def test_num_dml_affected_rows(self):
        num_rows = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.num_dml_affected_rows)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.num_dml_affected_rows)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.num_dml_affected_rows)

        query_stats["numDmlAffectedRows"] = str(num_rows)
        self.assertEqual(job.num_dml_affected_rows, num_rows)

    def test_slot_millis(self):
        millis = 1234
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.slot_millis)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.slot_millis)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.slot_millis)

        query_stats["totalSlotMs"] = millis
        self.assertEqual(job.slot_millis, millis)

    def test_statement_type(self):
        statement_type = "SELECT"
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.statement_type)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.statement_type)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.statement_type)

        query_stats["statementType"] = statement_type
        self.assertEqual(job.statement_type, statement_type)

    def test_referenced_tables(self):
        from google.cloud.bigquery.table import TableReference

        ref_tables_resource = [
            {"projectId": self.PROJECT, "datasetId": "dataset", "tableId": "local1"},
            {"projectId": self.PROJECT, "datasetId": "dataset", "tableId": "local2"},
            {
                "projectId": "other-project-123",
                "datasetId": "other-dataset",
                "tableId": "other-table",
            },
        ]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.referenced_tables, [])

        statistics = job._properties["statistics"] = {}
        self.assertEqual(job.referenced_tables, [])

        query_stats = statistics["query"] = {}
        self.assertEqual(job.referenced_tables, [])

        query_stats["referencedTables"] = ref_tables_resource

        local1, local2, remote = job.referenced_tables

        self.assertIsInstance(local1, TableReference)
        self.assertEqual(local1.table_id, "local1")
        self.assertEqual(local1.dataset_id, "dataset")
        self.assertEqual(local1.project, self.PROJECT)

        self.assertIsInstance(local2, TableReference)
        self.assertEqual(local2.table_id, "local2")
        self.assertEqual(local2.dataset_id, "dataset")
        self.assertEqual(local2.project, self.PROJECT)

        self.assertIsInstance(remote, TableReference)
        self.assertEqual(remote.table_id, "other-table")
        self.assertEqual(remote.dataset_id, "other-dataset")
        self.assertEqual(remote.project, "other-project-123")

    def test_timeline(self):
        timeline_resource = [
            {
                "elapsedMs": 1,
                "activeUnits": 22,
                "pendingUnits": 33,
                "completedUnits": 44,
                "totalSlotMs": 101,
            }
        ]

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.timeline, [])

        statistics = job._properties["statistics"] = {}
        self.assertEqual(job.timeline, [])

        query_stats = statistics["query"] = {}
        self.assertEqual(job.timeline, [])

        query_stats["timeline"] = timeline_resource

        self.assertEqual(len(job.timeline), len(timeline_resource))
        self.assertEqual(job.timeline[0].elapsed_ms, 1)
        self.assertEqual(job.timeline[0].active_units, 22)
        self.assertEqual(job.timeline[0].pending_units, 33)
        self.assertEqual(job.timeline[0].completed_units, 44)
        self.assertEqual(job.timeline[0].slot_millis, 101)

    def test_undeclared_query_parameters(self):
        from google.cloud.bigquery.query import ArrayQueryParameter
        from google.cloud.bigquery.query import ScalarQueryParameter
        from google.cloud.bigquery.query import StructQueryParameter

        undeclared = [
            {
                "name": "my_scalar",
                "parameterType": {"type": "STRING"},
                "parameterValue": {"value": "value"},
            },
            {
                "name": "my_array",
                "parameterType": {"type": "ARRAY", "arrayType": {"type": "INT64"}},
                "parameterValue": {
                    "arrayValues": [{"value": "1066"}, {"value": "1745"}]
                },
            },
            {
                "name": "my_struct",
                "parameterType": {
                    "type": "STRUCT",
                    "structTypes": [{"name": "count", "type": {"type": "INT64"}}],
                },
                "parameterValue": {"structValues": {"count": {"value": "123"}}},
            },
        ]
        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertEqual(job.undeclared_query_parameters, [])

        statistics = job._properties["statistics"] = {}
        self.assertEqual(job.undeclared_query_parameters, [])

        query_stats = statistics["query"] = {}
        self.assertEqual(job.undeclared_query_parameters, [])

        query_stats["undeclaredQueryParameters"] = undeclared

        scalar, array, struct = job.undeclared_query_parameters

        self.assertIsInstance(scalar, ScalarQueryParameter)
        self.assertEqual(scalar.name, "my_scalar")
        self.assertEqual(scalar.type_, "STRING")
        self.assertEqual(scalar.value, "value")

        self.assertIsInstance(array, ArrayQueryParameter)
        self.assertEqual(array.name, "my_array")
        self.assertEqual(array.array_type, "INT64")
        self.assertEqual(array.values, [1066, 1745])

        self.assertIsInstance(struct, StructQueryParameter)
        self.assertEqual(struct.name, "my_struct")
        self.assertEqual(struct.struct_types, {"count": "INT64"})
        self.assertEqual(struct.struct_values, {"count": 123})

    def test_estimated_bytes_processed(self):
        est_bytes = 123456

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        self.assertIsNone(job.estimated_bytes_processed)

        statistics = job._properties["statistics"] = {}
        self.assertIsNone(job.estimated_bytes_processed)

        query_stats = statistics["query"] = {}
        self.assertIsNone(job.estimated_bytes_processed)

        query_stats["estimatedBytesProcessed"] = str(est_bytes)
        self.assertEqual(job.estimated_bytes_processed, est_bytes)

    def test_bi_engine_stats(self):
        from google.cloud.bigquery.job.query import BiEngineStats

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        assert job.bi_engine_stats is None

        statistics = job._properties["statistics"] = {}
        assert job.bi_engine_stats is None

        query_stats = statistics["query"] = {}
        assert job.bi_engine_stats is None

        query_stats["biEngineStatistics"] = {"biEngineMode": "FULL"}
        assert isinstance(job.bi_engine_stats, BiEngineStats)
        assert job.bi_engine_stats.mode == "FULL"

    def test_dml_stats(self):
        from google.cloud.bigquery.job.query import DmlStats

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        assert job.dml_stats is None

        statistics = job._properties["statistics"] = {}
        assert job.dml_stats is None

        query_stats = statistics["query"] = {}
        assert job.dml_stats is None

        query_stats["dmlStats"] = {"insertedRowCount": "35"}
        assert isinstance(job.dml_stats, DmlStats)
        assert job.dml_stats.inserted_row_count == 35

    def test_result(self):
        from google.cloud.bigquery.table import RowIterator

        query_resource = {
            "jobComplete": False,
            "jobReference": {
                "projectId": self.PROJECT,
                "jobId": self.JOB_ID,
                "location": "EU",
            },
        }
        query_resource_done = {
            "jobComplete": True,
            "jobReference": {
                "projectId": self.PROJECT,
                "jobId": self.JOB_ID,
                "location": "EU",
            },
            "schema": {"fields": [{"name": "col1", "type": "STRING"}]},
            "totalRows": "2",
        }
        job_resource = self._make_resource(started=True, location="EU")
        job_resource_done = self._make_resource(started=True, ended=True, location="EU")
        job_resource_done["configuration"]["query"]["destinationTable"] = {
            "projectId": "dest-project",
            "datasetId": "dest_dataset",
            "tableId": "dest_table",
        }
        query_page_resource = {
            # Explicitly set totalRows to be different from the initial
            # response to test update during iteration.
            "totalRows": "1",
            "pageToken": None,
            "rows": [{"f": [{"v": "abc"}]}],
        }
        conn = make_connection(
            query_resource, query_resource_done, job_resource_done, query_page_resource
        )
        client = _make_client(self.PROJECT, connection=conn)
        job = self._get_target_class().from_api_repr(job_resource, client)

        result = job.result()

        self.assertIsInstance(result, RowIterator)
        self.assertEqual(result.total_rows, 2)
        rows = list(result)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].col1, "abc")
        # Test that the total_rows property has changed during iteration, based
        # on the response from tabledata.list.
        self.assertEqual(result.total_rows, 1)

        query_results_path = f"/projects/{self.PROJECT}/queries/{self.JOB_ID}"
        query_results_call = mock.call(
            method="GET",
            path=query_results_path,
            query_params={"maxResults": 0, "location": "EU"},
            timeout=None,
        )
        reload_call = mock.call(
            method="GET",
            path=f"/projects/{self.PROJECT}/jobs/{self.JOB_ID}",
            query_params={"location": "EU"},
            timeout=None,
        )
        query_page_call = mock.call(
            method="GET",
            path=query_results_path,
            query_params={
                "fields": _LIST_ROWS_FROM_QUERY_RESULTS_FIELDS,
                "location": "EU",
                "formatOptions.useInt64Timestamp": True,
            },
            timeout=None,
        )
        conn.api_request.assert_has_calls(
            [query_results_call, query_results_call, reload_call, query_page_call]
        )

    def test_result_dry_run(self):
        job_resource = self._make_resource(started=True, location="EU")
        job_resource["configuration"]["dryRun"] = True
        conn = make_connection()
        client = _make_client(self.PROJECT, connection=conn)
        job = self._get_target_class().from_api_repr(job_resource, client)

        result = job.result()

        calls = conn.api_request.mock_calls
        self.assertIsInstance(result, _EmptyRowIterator)
        self.assertEqual(calls, [])

    def test_result_with_done_job_calls_get_query_results(self):
        query_resource_done = {
            "jobComplete": True,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "schema": {"fields": [{"name": "col1", "type": "STRING"}]},
            "totalRows": "1",
        }
        job_resource = self._make_resource(started=True, ended=True, location="EU")
        job_resource["configuration"]["query"]["destinationTable"] = {
            "projectId": "dest-project",
            "datasetId": "dest_dataset",
            "tableId": "dest_table",
        }
        results_page_resource = {
            "totalRows": "1",
            "pageToken": None,
            "rows": [{"f": [{"v": "abc"}]}],
        }
        conn = make_connection(query_resource_done, results_page_resource)
        client = _make_client(self.PROJECT, connection=conn)
        job = self._get_target_class().from_api_repr(job_resource, client)

        result = job.result()

        rows = list(result)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].col1, "abc")

        query_results_path = f"/projects/{self.PROJECT}/queries/{self.JOB_ID}"
        query_results_call = mock.call(
            method="GET",
            path=query_results_path,
            query_params={"maxResults": 0, "location": "EU"},
            timeout=None,
        )
        query_results_page_call = mock.call(
            method="GET",
            path=query_results_path,
            query_params={
                "fields": _LIST_ROWS_FROM_QUERY_RESULTS_FIELDS,
                "location": "EU",
                "formatOptions.useInt64Timestamp": True,
            },
            timeout=None,
        )
        conn.api_request.assert_has_calls([query_results_call, query_results_page_call])

    def test_result_with_max_results(self):
        from google.cloud.bigquery.table import RowIterator

        query_resource = {
            "jobComplete": True,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "schema": {"fields": [{"name": "col1", "type": "STRING"}]},
            "totalRows": "5",
        }
        query_page_resource = {
            "totalRows": "5",
            "pageToken": None,
            "rows": [
                {"f": [{"v": "abc"}]},
                {"f": [{"v": "def"}]},
                {"f": [{"v": "ghi"}]},
            ],
        }
        connection = make_connection(query_resource, query_page_resource)
        client = _make_client(self.PROJECT, connection=connection)
        resource = self._make_resource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)

        max_results = 3

        result = job.result(max_results=max_results)

        self.assertIsInstance(result, RowIterator)
        self.assertEqual(result.total_rows, 5)

        rows = list(result)

        self.assertEqual(len(rows), 3)
        self.assertEqual(len(connection.api_request.call_args_list), 2)
        query_page_request = connection.api_request.call_args_list[1]
        self.assertEqual(
            query_page_request[1]["query_params"]["maxResults"], max_results
        )

    def test_result_w_retry(self):
        from google.cloud.bigquery.table import RowIterator

        query_resource = {
            "jobComplete": False,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
        }
        query_resource_done = {
            "jobComplete": True,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "schema": {"fields": [{"name": "col1", "type": "STRING"}]},
            "totalRows": "2",
        }
        job_resource = self._make_resource(started=True, location="asia-northeast1")
        job_resource_done = self._make_resource(
            started=True, ended=True, location="asia-northeast1"
        )
        job_resource_done["configuration"]["query"]["destinationTable"] = {
            "projectId": "dest-project",
            "datasetId": "dest_dataset",
            "tableId": "dest_table",
        }

        connection = make_connection(
            exceptions.NotFound("not normally retriable"),
            query_resource,
            exceptions.NotFound("not normally retriable"),
            query_resource_done,
            exceptions.NotFound("not normally retriable"),
            job_resource_done,
        )
        client = _make_client(self.PROJECT, connection=connection)
        job = self._get_target_class().from_api_repr(job_resource, client)

        custom_predicate = mock.Mock()
        custom_predicate.return_value = True
        custom_retry = google.api_core.retry.Retry(
            initial=0.001,
            maximum=0.001,
            multiplier=1.0,
            deadline=0.1,
            predicate=custom_predicate,
        )

        self.assertIsInstance(job.result(retry=custom_retry), RowIterator)
        query_results_call = mock.call(
            method="GET",
            path=f"/projects/{self.PROJECT}/queries/{self.JOB_ID}",
            query_params={"maxResults": 0, "location": "asia-northeast1"},
            timeout=None,
        )
        reload_call = mock.call(
            method="GET",
            path=f"/projects/{self.PROJECT}/jobs/{self.JOB_ID}",
            query_params={"location": "asia-northeast1"},
            timeout=None,
        )

        connection.api_request.assert_has_calls(
            [query_results_call, query_results_call, reload_call]
        )

    def test_result_w_empty_schema(self):
        from google.cloud.bigquery.table import _EmptyRowIterator

        # Destination table may have no schema for some DDL and DML queries.
        query_resource = {
            "jobComplete": True,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "schema": {"fields": []},
        }
        connection = make_connection(query_resource, query_resource)
        client = _make_client(self.PROJECT, connection=connection)
        resource = self._make_resource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)

        result = job.result()

        self.assertIsInstance(result, _EmptyRowIterator)
        self.assertEqual(list(result), [])

    def test_result_invokes_begins(self):
        begun_resource = self._make_resource()
        incomplete_resource = {
            "jobComplete": False,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "schema": {"fields": [{"name": "col1", "type": "STRING"}]},
        }
        query_resource = copy.deepcopy(incomplete_resource)
        query_resource["jobComplete"] = True
        done_resource = copy.deepcopy(begun_resource)
        done_resource["status"] = {"state": "DONE"}
        connection = make_connection(
            begun_resource,
            incomplete_resource,
            query_resource,
            done_resource,
            query_resource,
        )
        client = _make_client(project=self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        job.result()

        self.assertEqual(len(connection.api_request.call_args_list), 4)
        begin_request = connection.api_request.call_args_list[0]
        query_request = connection.api_request.call_args_list[2]
        reload_request = connection.api_request.call_args_list[3]
        self.assertEqual(begin_request[1]["method"], "POST")
        self.assertEqual(query_request[1]["method"], "GET")
        self.assertEqual(reload_request[1]["method"], "GET")

    def test_result_w_timeout(self):
        import google.cloud.bigquery.client

        begun_resource = self._make_resource()
        query_resource = {
            "jobComplete": True,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "schema": {"fields": [{"name": "col1", "type": "STRING"}]},
        }
        done_resource = copy.deepcopy(begun_resource)
        done_resource["status"] = {"state": "DONE"}
        connection = make_connection(begun_resource, query_resource, done_resource)
        client = _make_client(project=self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        with freezegun.freeze_time("1970-01-01 00:00:00", tick=False):
            job.result(timeout=1.0)

        self.assertEqual(len(connection.api_request.call_args_list), 3)
        begin_request = connection.api_request.call_args_list[0]
        query_request = connection.api_request.call_args_list[1]
        reload_request = connection.api_request.call_args_list[2]
        self.assertEqual(begin_request[1]["method"], "POST")
        self.assertEqual(query_request[1]["method"], "GET")
        self.assertEqual(
            query_request[1]["path"],
            "/projects/{}/queries/{}".format(self.PROJECT, self.JOB_ID),
        )
        self.assertEqual(query_request[1]["query_params"]["timeoutMs"], 900)
        self.assertEqual(
            query_request[1]["timeout"],
            google.cloud.bigquery.client._MIN_GET_QUERY_RESULTS_TIMEOUT,
        )
        self.assertEqual(reload_request[1]["method"], "GET")

    def test_result_w_page_size(self):
        # Arrange
        query_results_resource = {
            "jobComplete": True,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "schema": {"fields": [{"name": "col1", "type": "STRING"}]},
            "totalRows": "4",
        }
        job_resource = self._make_resource(started=True, ended=True, location="US")
        q_config = job_resource["configuration"]["query"]
        q_config["destinationTable"] = {
            "projectId": self.PROJECT,
            "datasetId": self.DS_ID,
            "tableId": self.TABLE_ID,
        }
        query_page_resource = {
            "totalRows": 4,
            "pageToken": "some-page-token",
            "rows": [
                {"f": [{"v": "row1"}]},
                {"f": [{"v": "row2"}]},
                {"f": [{"v": "row3"}]},
            ],
        }
        query_page_resource_2 = {"totalRows": 4, "rows": [{"f": [{"v": "row4"}]}]}
        conn = make_connection(
            query_results_resource, query_page_resource, query_page_resource_2
        )
        client = _make_client(self.PROJECT, connection=conn)
        job = self._get_target_class().from_api_repr(job_resource, client)

        # Act
        result = job.result(page_size=3)

        # Assert
        actual_rows = list(result)
        self.assertEqual(len(actual_rows), 4)

        query_results_path = f"/projects/{self.PROJECT}/queries/{self.JOB_ID}"
        query_page_1_call = mock.call(
            method="GET",
            path=query_results_path,
            query_params={
                "maxResults": 3,
                "fields": _LIST_ROWS_FROM_QUERY_RESULTS_FIELDS,
                "location": "US",
                "formatOptions.useInt64Timestamp": True,
            },
            timeout=None,
        )
        query_page_2_call = mock.call(
            method="GET",
            path=query_results_path,
            query_params={
                "pageToken": "some-page-token",
                "maxResults": 3,
                "fields": _LIST_ROWS_FROM_QUERY_RESULTS_FIELDS,
                "location": "US",
                "formatOptions.useInt64Timestamp": True,
            },
            timeout=None,
        )
        conn.api_request.assert_has_calls([query_page_1_call, query_page_2_call])

    def test_result_with_start_index(self):
        from google.cloud.bigquery.table import RowIterator

        query_resource = {
            "jobComplete": True,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "schema": {"fields": [{"name": "col1", "type": "STRING"}]},
            "totalRows": "5",
        }
        tabledata_resource = {
            "totalRows": "5",
            "pageToken": None,
            "rows": [
                {"f": [{"v": "abc"}]},
                {"f": [{"v": "def"}]},
                {"f": [{"v": "ghi"}]},
                {"f": [{"v": "jkl"}]},
            ],
        }
        connection = make_connection(query_resource, tabledata_resource)
        client = _make_client(self.PROJECT, connection=connection)
        resource = self._make_resource(ended=True)
        job = self._get_target_class().from_api_repr(resource, client)

        start_index = 1

        result = job.result(start_index=start_index)

        self.assertIsInstance(result, RowIterator)
        self.assertEqual(result.total_rows, 5)

        rows = list(result)

        self.assertEqual(len(rows), 4)
        self.assertEqual(len(connection.api_request.call_args_list), 2)
        tabledata_list_request = connection.api_request.call_args_list[1]
        self.assertEqual(
            tabledata_list_request[1]["query_params"]["startIndex"], start_index
        )

    def test_result_error(self):
        from google.cloud import exceptions

        query = textwrap.dedent(
            """
            SELECT foo, bar
            FROM table_baz
            WHERE foo == bar"""
        )

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, query, client)
        error_result = {
            "debugInfo": "DEBUG",
            "location": "LOCATION",
            "message": "MESSAGE",
            "reason": "invalid",
        }
        job._properties["status"] = {
            "errorResult": error_result,
            "errors": [error_result],
            "state": "DONE",
        }
        job._query_results = google.cloud.bigquery.query._QueryResults.from_api_repr(
            {"jobComplete": True, "jobReference": job._properties["jobReference"]}
        )
        job._set_future_result()

        with self.assertRaises(exceptions.GoogleCloudError) as exc_info:
            job.result()

        self.assertIsInstance(exc_info.exception, exceptions.GoogleCloudError)
        self.assertEqual(exc_info.exception.code, http.client.BAD_REQUEST)

        exc_job_instance = getattr(exc_info.exception, "query_job", None)
        self.assertIs(exc_job_instance, job)

        # Query text could contain sensitive information, so it must not be
        # included in logs / exception representation.
        full_text = str(exc_info.exception)
        assert job.job_id in full_text
        assert "Query Job SQL Follows" not in full_text

        # It is useful to have query text available, so it is provided in a
        # debug_message property.
        debug_message = exc_info.exception.debug_message
        assert "Query Job SQL Follows" in debug_message
        for i, line in enumerate(query.splitlines(), start=1):
            expected_line = "{}:{}".format(i, line)
            assert expected_line in debug_message

    def test_result_transport_timeout_error(self):
        query = textwrap.dedent(
            """
            SELECT foo, bar
            FROM table_baz
            WHERE foo == bar"""
        )

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, query, client)
        call_api_patch = mock.patch(
            "google.cloud.bigquery.client.Client._call_api",
            autospec=True,
            side_effect=requests.exceptions.Timeout("Server response took too long."),
        )

        # Make sure that timeout errors get rebranded to concurrent futures timeout.
        with call_api_patch, self.assertRaises(concurrent.futures.TimeoutError):
            job.result(timeout=1)

    def test_no_schema(self):
        client = _make_client(project=self.PROJECT)
        resource = {}
        klass = self._get_target_class()
        job = klass.from_api_repr(resource, client=client)
        assert job.schema is None

    def test_schema(self):
        client = _make_client(project=self.PROJECT)
        resource = {
            "statistics": {
                "query": {
                    "schema": {
                        "fields": [
                            {"mode": "NULLABLE", "name": "bool_col", "type": "BOOLEAN"},
                            {
                                "mode": "NULLABLE",
                                "name": "string_col",
                                "type": "STRING",
                            },
                            {
                                "mode": "NULLABLE",
                                "name": "timestamp_col",
                                "type": "TIMESTAMP",
                            },
                        ]
                    },
                },
            },
        }
        klass = self._get_target_class()
        job = klass.from_api_repr(resource, client=client)
        assert len(job.schema) == 3
        assert job.schema[0].field_type == "BOOLEAN"
        assert job.schema[1].field_type == "STRING"
        assert job.schema[2].field_type == "TIMESTAMP"

    def test__begin_error(self):
        from google.cloud import exceptions

        query = textwrap.dedent(
            """
            SELECT foo, bar
            FROM table_baz
            WHERE foo == bar"""
        )

        client = _make_client(project=self.PROJECT)
        job = self._make_one(self.JOB_ID, query, client)
        call_api_patch = mock.patch(
            "google.cloud.bigquery.client.Client._call_api",
            autospec=True,
            side_effect=exceptions.BadRequest("Syntax error in SQL query"),
        )

        with call_api_patch, self.assertRaises(exceptions.GoogleCloudError) as exc_info:
            job.result()

        self.assertIsInstance(exc_info.exception, exceptions.GoogleCloudError)
        self.assertEqual(exc_info.exception.code, http.client.BAD_REQUEST)

        exc_job_instance = getattr(exc_info.exception, "query_job", None)
        self.assertIs(exc_job_instance, job)

        # Query text could contain sensitive information, so it must not be
        # included in logs / exception representation.
        full_text = str(exc_info.exception)
        assert job.job_id in full_text
        assert "Query Job SQL Follows" not in full_text

        # It is useful to have query text available, so it is provided in a
        # debug_message property.
        debug_message = exc_info.exception.debug_message
        assert "Query Job SQL Follows" in debug_message
        for i, line in enumerate(query.splitlines(), start=1):
            expected_line = "{}:{}".format(i, line)
            assert expected_line in debug_message

    def test__begin_w_timeout(self):
        PATH = "/projects/%s/jobs" % (self.PROJECT,)
        RESOURCE = self._make_resource()

        conn = make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job._begin(timeout=7.5)

        final_attributes.assert_called_with({"path": PATH}, client, job)

        conn.api_request.assert_called_once_with(
            method="POST",
            path=PATH,
            data={
                "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
                "configuration": {
                    "query": {"query": self.QUERY, "useLegacySql": False}
                },
            },
            timeout=7.5,
        )

    def test_begin_w_bound_client(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = "/projects/%s/jobs" % (self.PROJECT,)
        DS_ID = "DATASET"
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE["statistics"]["creationTime"]
        del RESOURCE["etag"]
        del RESOURCE["selfLink"]
        del RESOURCE["user_email"]
        conn = make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)

        config = QueryJobConfig()
        config.default_dataset = DatasetReference(self.PROJECT, DS_ID)
        job = self._make_one(self.JOB_ID, self.QUERY, client, job_config=config)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job._begin()

        final_attributes.assert_called_with({"path": PATH}, client, job)

        self.assertIsNone(job.default_dataset)
        self.assertEqual(job.udf_resources, [])
        conn.api_request.assert_called_once_with(
            method="POST",
            path=PATH,
            data={
                "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
                "configuration": {
                    "query": {
                        "query": self.QUERY,
                        "useLegacySql": False,
                        "defaultDataset": {
                            "projectId": self.PROJECT,
                            "datasetId": DS_ID,
                        },
                    }
                },
            },
            timeout=None,
        )
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_alternate_client(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import CreateDisposition
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.job import QueryPriority
        from google.cloud.bigquery.job import SchemaUpdateOption
        from google.cloud.bigquery.job import WriteDisposition

        PATH = "/projects/%s/jobs" % (self.PROJECT,)
        TABLE = "TABLE"
        DS_ID = "DATASET"
        RESOURCE = self._make_resource(ended=True)
        QUERY_CONFIGURATION = {
            "query": self.QUERY,
            "allowLargeResults": True,
            "createDisposition": CreateDisposition.CREATE_NEVER,
            "defaultDataset": {"projectId": self.PROJECT, "datasetId": DS_ID},
            "destinationTable": {
                "projectId": self.PROJECT,
                "datasetId": DS_ID,
                "tableId": TABLE,
            },
            "flattenResults": True,
            "priority": QueryPriority.INTERACTIVE,
            "useQueryCache": True,
            "useLegacySql": True,
            "writeDisposition": WriteDisposition.WRITE_TRUNCATE,
            "maximumBillingTier": 4,
            "maximumBytesBilled": "123456",
            "schemaUpdateOptions": [SchemaUpdateOption.ALLOW_FIELD_RELAXATION],
        }
        RESOURCE["configuration"]["query"] = QUERY_CONFIGURATION
        RESOURCE["configuration"]["dryRun"] = True
        conn1 = make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = make_connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        dataset_ref = DatasetReference(self.PROJECT, DS_ID)
        table_ref = dataset_ref.table(TABLE)

        config = QueryJobConfig()
        config.allow_large_results = True
        config.create_disposition = CreateDisposition.CREATE_NEVER
        config.default_dataset = dataset_ref
        config.destination = table_ref
        config.dry_run = True
        config.flatten_results = True
        config.maximum_billing_tier = 4
        config.priority = QueryPriority.INTERACTIVE
        config.use_legacy_sql = True
        config.use_query_cache = True
        config.write_disposition = WriteDisposition.WRITE_TRUNCATE
        config.maximum_bytes_billed = 123456
        config.schema_update_options = [SchemaUpdateOption.ALLOW_FIELD_RELAXATION]
        job = self._make_one(self.JOB_ID, self.QUERY, client1, job_config=config)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job._begin(client=client2)

        final_attributes.assert_called_with({"path": PATH}, client2, job)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method="POST",
            path=PATH,
            data={
                "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
                "configuration": {"dryRun": True, "query": QUERY_CONFIGURATION},
            },
            timeout=None,
        )
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_udf(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import UDFResource

        RESOURCE_URI = "gs://some-bucket/js/lib.js"
        INLINE_UDF_CODE = 'var someCode = "here";'
        PATH = "/projects/%s/jobs" % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE["statistics"]["creationTime"]
        del RESOURCE["etag"]
        del RESOURCE["selfLink"]
        del RESOURCE["user_email"]
        RESOURCE["configuration"]["query"]["userDefinedFunctionResources"] = [
            {"resourceUri": RESOURCE_URI},
            {"inlineCode": INLINE_UDF_CODE},
        ]
        conn = make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        udf_resources = [
            UDFResource("resourceUri", RESOURCE_URI),
            UDFResource("inlineCode", INLINE_UDF_CODE),
        ]
        config = QueryJobConfig()
        config.udf_resources = udf_resources
        config.use_legacy_sql = True
        job = self._make_one(self.JOB_ID, self.QUERY, client, job_config=config)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job._begin()

        final_attributes.assert_called_with({"path": PATH}, client, job)

        self.assertEqual(job.udf_resources, udf_resources)
        conn.api_request.assert_called_once_with(
            method="POST",
            path=PATH,
            data={
                "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
                "configuration": {
                    "query": {
                        "query": self.QUERY,
                        "useLegacySql": True,
                        "userDefinedFunctionResources": [
                            {"resourceUri": RESOURCE_URI},
                            {"inlineCode": INLINE_UDF_CODE},
                        ],
                    }
                },
            },
            timeout=None,
        )
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_named_query_parameter(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter("foo", "INT64", 123)]
        PATH = "/projects/%s/jobs" % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE["statistics"]["creationTime"]
        del RESOURCE["etag"]
        del RESOURCE["selfLink"]
        del RESOURCE["user_email"]
        config = RESOURCE["configuration"]["query"]
        config["parameterMode"] = "NAMED"
        config["queryParameters"] = [
            {
                "name": "foo",
                "parameterType": {"type": "INT64"},
                "parameterValue": {"value": "123"},
            }
        ]
        conn = make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        jconfig = QueryJobConfig()
        jconfig.query_parameters = query_parameters
        job = self._make_one(self.JOB_ID, self.QUERY, client, job_config=jconfig)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job._begin()

        final_attributes.assert_called_with({"path": PATH}, client, job)

        self.assertEqual(job.query_parameters, query_parameters)
        conn.api_request.assert_called_once_with(
            method="POST",
            path=PATH,
            data={
                "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
                "configuration": {
                    "query": {
                        "query": self.QUERY,
                        "useLegacySql": False,
                        "parameterMode": "NAMED",
                        "queryParameters": config["queryParameters"],
                    }
                },
            },
            timeout=None,
        )
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_positional_query_parameter(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.query import ScalarQueryParameter

        query_parameters = [ScalarQueryParameter.positional("INT64", 123)]
        PATH = "/projects/%s/jobs" % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE["statistics"]["creationTime"]
        del RESOURCE["etag"]
        del RESOURCE["selfLink"]
        del RESOURCE["user_email"]
        config = RESOURCE["configuration"]["query"]
        config["parameterMode"] = "POSITIONAL"
        config["queryParameters"] = [
            {"parameterType": {"type": "INT64"}, "parameterValue": {"value": "123"}}
        ]
        conn = make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        jconfig = QueryJobConfig()
        jconfig.query_parameters = query_parameters
        job = self._make_one(self.JOB_ID, self.QUERY, client, job_config=jconfig)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job._begin()

        final_attributes.assert_called_with({"path": PATH}, client, job)

        self.assertEqual(job.query_parameters, query_parameters)
        conn.api_request.assert_called_once_with(
            method="POST",
            path=PATH,
            data={
                "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
                "configuration": {
                    "query": {
                        "query": self.QUERY,
                        "useLegacySql": False,
                        "parameterMode": "POSITIONAL",
                        "queryParameters": config["queryParameters"],
                    }
                },
            },
            timeout=None,
        )
        self._verifyResourceProperties(job, RESOURCE)

    def test_begin_w_table_defs(self):
        from google.cloud.bigquery.job import QueryJobConfig
        from google.cloud.bigquery.external_config import ExternalConfig
        from google.cloud.bigquery.external_config import BigtableColumn
        from google.cloud.bigquery.external_config import BigtableColumnFamily

        PATH = "/projects/%s/jobs" % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE["statistics"]["creationTime"]
        del RESOURCE["etag"]
        del RESOURCE["selfLink"]
        del RESOURCE["user_email"]

        bt_config = ExternalConfig("BIGTABLE")
        bt_config.ignore_unknown_values = True
        bt_config.options.read_rowkey_as_string = True
        cf = BigtableColumnFamily()
        cf.family_id = "cf"
        col = BigtableColumn()
        col.field_name = "fn"
        cf.columns = [col]
        bt_config.options.column_families = [cf]
        BT_CONFIG_RESOURCE = {
            "sourceFormat": "BIGTABLE",
            "ignoreUnknownValues": True,
            "bigtableOptions": {
                "readRowkeyAsString": True,
                "columnFamilies": [
                    {"familyId": "cf", "columns": [{"fieldName": "fn"}]}
                ],
            },
        }
        CSV_CONFIG_RESOURCE = {
            "sourceFormat": "CSV",
            "maxBadRecords": 8,
            "csvOptions": {"allowJaggedRows": True},
        }
        csv_config = ExternalConfig("CSV")
        csv_config.max_bad_records = 8
        csv_config.options.allow_jagged_rows = True
        bt_table = "bigtable-table"
        csv_table = "csv-table"
        RESOURCE["configuration"]["query"]["tableDefinitions"] = {
            bt_table: BT_CONFIG_RESOURCE,
            csv_table: CSV_CONFIG_RESOURCE,
        }
        want_resource = copy.deepcopy(RESOURCE)
        conn = make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        config = QueryJobConfig()
        config.table_definitions = {bt_table: bt_config, csv_table: csv_config}
        config.use_legacy_sql = True
        job = self._make_one(self.JOB_ID, self.QUERY, client, job_config=config)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job._begin()

        final_attributes.assert_called_with({"path": PATH}, client, job)

        conn.api_request.assert_called_once_with(
            method="POST",
            path=PATH,
            data={
                "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
                "configuration": {
                    "query": {
                        "query": self.QUERY,
                        "useLegacySql": True,
                        "tableDefinitions": {
                            bt_table: BT_CONFIG_RESOURCE,
                            csv_table: CSV_CONFIG_RESOURCE,
                        },
                    }
                },
            },
            timeout=None,
        )
        self._verifyResourceProperties(job, want_resource)

    def test_dry_run_query(self):
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = "/projects/%s/jobs" % (self.PROJECT,)
        RESOURCE = self._make_resource()
        # Ensure None for missing server-set props
        del RESOURCE["statistics"]["creationTime"]
        del RESOURCE["etag"]
        del RESOURCE["selfLink"]
        del RESOURCE["user_email"]
        RESOURCE["configuration"]["dryRun"] = True
        conn = make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        config = QueryJobConfig()
        config.dry_run = True
        job = self._make_one(self.JOB_ID, self.QUERY, client, job_config=config)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job._begin()

        final_attributes.assert_called_with({"path": PATH}, client, job)
        self.assertEqual(job.udf_resources, [])
        conn.api_request.assert_called_once_with(
            method="POST",
            path=PATH,
            data={
                "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
                "configuration": {
                    "query": {"query": self.QUERY, "useLegacySql": False},
                    "dryRun": True,
                },
            },
            timeout=None,
        )
        self._verifyResourceProperties(job, RESOURCE)

    def test_exists_miss_w_bound_client(self):
        PATH = "/projects/%s/jobs/%s" % (self.PROJECT, self.JOB_ID)
        conn = make_connection()
        client = _make_client(project=self.PROJECT, connection=conn)
        job = self._make_one(self.JOB_ID, self.QUERY, client)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            self.assertFalse(job.exists())

        final_attributes.assert_called_with({"path": PATH}, client, job)

        conn.api_request.assert_called_once_with(
            method="GET", path=PATH, query_params={"fields": "id"}, timeout=None
        )

    def test_exists_hit_w_alternate_client(self):
        PATH = "/projects/%s/jobs/%s" % (self.PROJECT, self.JOB_ID)
        conn1 = make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = make_connection({})
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        job = self._make_one(self.JOB_ID, self.QUERY, client1)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            self.assertTrue(job.exists(client=client2))

        final_attributes.assert_called_with({"path": PATH}, client2, job)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method="GET", path=PATH, query_params={"fields": "id"}, timeout=None
        )

    def test_reload_w_bound_client(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = "/projects/%s/jobs/%s" % (self.PROJECT, self.JOB_ID)
        DS_ID = "DATASET"
        DEST_TABLE = "dest_table"
        RESOURCE = self._make_resource()
        conn = make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        dataset_ref = DatasetReference(self.PROJECT, DS_ID)
        table_ref = dataset_ref.table(DEST_TABLE)
        config = QueryJobConfig()
        config.destination = table_ref
        job = self._make_one(self.JOB_ID, None, client, job_config=config)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job.reload()

        final_attributes.assert_called_with({"path": PATH}, client, job)

        self.assertNotEqual(job.destination, table_ref)

        conn.api_request.assert_called_once_with(
            method="GET", path=PATH, query_params={}, timeout=None
        )
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_alternate_client(self):
        PATH = "/projects/%s/jobs/%s" % (self.PROJECT, self.JOB_ID)
        DS_ID = "DATASET"
        DEST_TABLE = "dest_table"
        RESOURCE = self._make_resource()
        q_config = RESOURCE["configuration"]["query"]
        q_config["destinationTable"] = {
            "projectId": self.PROJECT,
            "datasetId": DS_ID,
            "tableId": DEST_TABLE,
        }
        conn1 = make_connection()
        client1 = _make_client(project=self.PROJECT, connection=conn1)
        conn2 = make_connection(RESOURCE)
        client2 = _make_client(project=self.PROJECT, connection=conn2)
        job = self._make_one(self.JOB_ID, self.QUERY, client1)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job.reload(client=client2)

        final_attributes.assert_called_with({"path": PATH}, client2, job)

        conn1.api_request.assert_not_called()
        conn2.api_request.assert_called_once_with(
            method="GET", path=PATH, query_params={}, timeout=None
        )
        self._verifyResourceProperties(job, RESOURCE)

    def test_reload_w_timeout(self):
        from google.cloud.bigquery.dataset import DatasetReference
        from google.cloud.bigquery.job import QueryJobConfig

        PATH = "/projects/%s/jobs/%s" % (self.PROJECT, self.JOB_ID)
        DS_ID = "DATASET"
        DEST_TABLE = "dest_table"
        RESOURCE = self._make_resource()
        conn = make_connection(RESOURCE)
        client = _make_client(project=self.PROJECT, connection=conn)
        dataset_ref = DatasetReference(self.PROJECT, DS_ID)
        table_ref = dataset_ref.table(DEST_TABLE)
        config = QueryJobConfig()
        config.destination = table_ref
        job = self._make_one(self.JOB_ID, None, client, job_config=config)
        with mock.patch(
            "google.cloud.bigquery.opentelemetry_tracing._get_final_span_attributes"
        ) as final_attributes:
            job.reload(timeout=4.2)

        final_attributes.assert_called_with({"path": PATH}, client, job)

        self.assertNotEqual(job.destination, table_ref)

        conn.api_request.assert_called_once_with(
            method="GET", path=PATH, query_params={}, timeout=4.2
        )

    def test_iter(self):
        begun_resource = self._make_resource()
        query_resource = {
            "jobComplete": True,
            "jobReference": {"projectId": self.PROJECT, "jobId": self.JOB_ID},
            "totalRows": "0",
            "schema": {"fields": [{"name": "col1", "type": "STRING"}]},
        }
        done_resource = copy.deepcopy(begun_resource)
        done_resource["status"] = {"state": "DONE"}
        connection = make_connection(begun_resource, query_resource, done_resource)
        client = _make_client(project=self.PROJECT, connection=connection)
        job = self._make_one(self.JOB_ID, self.QUERY, client)

        self.assertIsInstance(iter(job), types.GeneratorType)
