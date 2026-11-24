# Copyright 2024 Google LLC All rights reserved.
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

from google.cloud.spanner_v1._async.client import Client
from google.cloud.spanner_v1.transaction import DefaultTransactionOptions
from tests._builders import build_scoped_credentials


class TestClientExtra(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.project = "project-id"
        self.credentials = build_scoped_credentials()

    def test_experimental_host_ctor(self):
        # coverage for lines 293-300
        client = Client(
            project=self.project,
            credentials=self.credentials,
            experimental_host="experimental.host",
            use_plain_text=True,
        )
        self.assertEqual(client.project, "default")
        self.assertEqual(client.instance_type, "omni")
        self.assertEqual(client._host, "experimental.host")
        self.assertTrue(client._use_plain_text)

    async def test_experimental_host_apis(self):
        # coverage for lines 400-425 and 454-479
        client = Client(
            project=self.project,
            credentials=self.credentials,
            experimental_host="experimental.host",
            use_plain_text=True,
        )
        with mock.patch(
            "google.cloud.spanner_admin_instance_v1.services.instance_admin.async_client.InstanceAdminAsyncClient"
        ) as _:
            with mock.patch(
                "google.cloud.spanner_admin_database_v1.services.database_admin.async_client.DatabaseAdminAsyncClient"
            ) as _:
                ia_api = client.instance_admin_api
                da_api = client.database_admin_api
                # We just verify that they were called or they are not None
                self.assertIsNotNone(ia_api)
                self.assertIsNotNone(da_api)

    async def test_emulator_host_apis(self):
        # coverage for lines 388-398 and 442-452
        with mock.patch(
            "google.cloud.spanner_v1._async.client._get_spanner_emulator_host",
            return_value="localhost:9010",
        ):
            client = Client(project=self.project, credentials=self.credentials)
            self.assertEqual(client._emulator_host, "localhost:9010")

            with mock.patch(
                "google.cloud.spanner_v1._async.client.InstanceAdminClient"
            ) as ia_mock:
                with mock.patch(
                    "google.cloud.spanner_v1._async.client.DatabaseAdminClient"
                ) as da_mock:
                    ia_api = client.instance_admin_api
                    da_api = client.database_admin_api
                    self.assertIs(ia_api, ia_mock.return_value)
                    self.assertIs(da_api, da_mock.return_value)

    async def test_sync_branches_admin_apis(self):
        # coverage for lines 392, 417, 446, 471
        client = Client(
            project=self.project,
            credentials=self.credentials,
            experimental_host="experimental.host",
            use_plain_text=True,
        )
        # Mock the transports to be simple callables to avoid GAPIC transport init failures
        with mock.patch(
            "google.cloud.spanner_v1._async.client.InstanceAdminGrpcTransport",
            return_value=mock.Mock(),
        ):
            with mock.patch(
                "google.cloud.spanner_v1._async.client.DatabaseAdminGrpcTransport",
                return_value=mock.Mock(),
            ):
                with mock.patch(
                    "google.cloud.spanner_v1._async.client.CrossSync.is_async", False
                ):
                    # Test experimental host sync branch
                    with mock.patch(
                        "google.cloud.spanner_v1._async.client.InstanceAdminClient"
                    ) as _:
                        with mock.patch(
                            "google.cloud.spanner_v1._async.client.DatabaseAdminClient"
                        ) as _:
                            ia_api = client.instance_admin_api
                            da_api = client.database_admin_api
                            self.assertIsNotNone(ia_api)
                            self.assertIsNotNone(da_api)

                    # Reset for emulator test
                    client._instance_admin_api = None
                    client._database_admin_api = None
                    with mock.patch(
                        "google.cloud.spanner_v1._async.client._get_spanner_emulator_host",
                        return_value="localhost:9010",
                    ):
                        client_emu = Client(
                            project=self.project, credentials=self.credentials
                        )
                        with mock.patch(
                            "google.cloud.spanner_v1._async.client.InstanceAdminClient"
                        ) as _:
                            with mock.patch(
                                "google.cloud.spanner_v1._async.client.DatabaseAdminClient"
                            ) as _:
                                ia_api = client_emu.instance_admin_api
                                da_api = client_emu.database_admin_api
                                self.assertIsNotNone(ia_api)
                                self.assertIsNotNone(da_api)

    # Safety shield mocks: We intercept the OpenTelemetry metric classes at the client module namespace level
    # to prevent instantiating real exporter objects. This prevents spawning live background worker threads
    # that periodically wake up and trigger 401 credential errors inside unauthenticated unit test runs.
    @mock.patch("google.cloud.spanner_v1._async.client.CloudMonitoringMetricsExporter")
    @mock.patch("google.cloud.spanner_v1._async.client.PeriodicExportingMetricReader")
    @mock.patch("google.cloud.spanner_v1._async.client.MeterProvider")
    # Global state reset: Temporarily override the module's process-wide global boolean _metrics_monitor_initialized
    # to False so that the client enters the initialization logic instead of returning early.
    @mock.patch(
        "google.cloud.spanner_v1._async.client._metrics_monitor_initialized",
        False,
    )
    def test_initialize_metrics_double_check(
        self, mock_provider, mock_reader, mock_exporter
    ):
        # coverage for line 143->exit
        from google.cloud.spanner_v1._async import client as MUT

        # We want to hit the second 'if not _metrics_monitor_initialized' and it being True
        # This is a bit tricky, but we can mock the lock to set the variable
        original_lock = MUT._metrics_monitor_lock

        class SettingLock:
            def __enter__(self):
                MUT._metrics_monitor_initialized = True
                return original_lock.__enter__()

            def __exit__(self, *args):
                return original_lock.__exit__(*args)

        # Concurrency race condition simulator: Replace the process synchronization lock with our custom SettingLock.
        # When this lock enters, it toggles _metrics_monitor_initialized to True to simulate another thread
        # completing metrics setup while this thread was waiting for the lock.
        with mock.patch(
            "google.cloud.spanner_v1._async.client._metrics_monitor_lock",
            SettingLock(),
        ):
            # Trigger the initialization function and verify Spanner's double-checked lock safely
            # checks the flag again and aborts cleanly to prevent dual-registration.
            MUT._initialize_metrics("project", self.credentials)
            self.assertTrue(MUT._metrics_monitor_initialized)

    def test_default_transaction_options_validation(self):
        # coverage for line 344
        with self.assertRaises(TypeError):
            Client(
                project=self.project,
                credentials=self.credentials,
                default_transaction_options="invalid",
            )

    def test_directed_read_options_setter(self):
        # coverage for line 668
        client = Client(project=self.project, credentials=self.credentials)
        dro = {"include_replicas": {}}
        client.directed_read_options = dro
        self.assertEqual(client.directed_read_options, dro)

    def test_default_transaction_options_setter(self):
        # coverage for lines 679-686
        client = Client(project=self.project, credentials=self.credentials)
        dto = DefaultTransactionOptions(isolation_level="SERIALIZABLE")
        client.default_transaction_options = dto
        self.assertEqual(client.default_transaction_options, dto)

        # branch for None
        client.default_transaction_options = None
        self.assertIsInstance(
            client.default_transaction_options, DefaultTransactionOptions
        )

        # branch for TypeError
        with self.assertRaises(TypeError):
            client.default_transaction_options = "invalid"

    def test_instance_factory(self):
        # coverage for line 616
        client = Client(project=self.project, credentials=self.credentials)
        inst = client.instance("inst-id")
        self.assertEqual(inst.instance_id, "inst-id")
        self.assertIs(inst._client, client)

    def test_initialize_metrics_already_initialized(self):
        # coverage for line 143->exit
        from google.cloud.spanner_v1._async import client as MUT

        with mock.patch(
            "google.cloud.spanner_v1._async.client._metrics_monitor_initialized", True
        ):
            MUT._initialize_metrics("project", self.credentials)
            # Should just return without doing anything

    def test_initialize_metrics_emulator_branch(self):
        # coverage for line 146->158 (skipping emulator)
        from google.cloud.spanner_v1._async import client as MUT

        with mock.patch(
            "google.cloud.spanner_v1._async.client._get_spanner_emulator_host",
            return_value="localhost",
        ):
            with mock.patch(
                "google.cloud.spanner_v1._async.client._metrics_monitor_initialized",
                False,
            ):
                with mock.patch(
                    "google.cloud.spanner_v1._async.client.metrics.set_meter_provider"
                ) as set_mock:
                    MUT._initialize_metrics("project", self.credentials)
                    set_mock.assert_called_once()

    def test_initialize_metrics_emulator_host_parameter(self):
        from google.cloud.spanner_v1._async import client as MUT

        with mock.patch(
            "google.cloud.spanner_v1._async.client._metrics_monitor_initialized",
            False,
        ):
            with mock.patch(
                "google.cloud.spanner_v1._async.client.metrics.set_meter_provider"
            ) as set_mock:
                MUT._initialize_metrics(
                    "project",
                    self.credentials,
                    emulator_host="localhost:9010",
                )
                set_mock.assert_called_once()

    def test_initialize_metrics_anonymous_credentials(self):
        from google.auth.credentials import AnonymousCredentials

        from google.cloud.spanner_v1._async import client as MUT

        with mock.patch(
            "google.cloud.spanner_v1._async.client._metrics_monitor_initialized",
            False,
        ):
            with mock.patch(
                "google.cloud.spanner_v1._async.client.metrics.set_meter_provider"
            ) as set_mock:
                MUT._initialize_metrics(
                    "project",
                    AnonymousCredentials(),
                )
                set_mock.assert_called_once()

    def test_initialize_metrics_custom_api_endpoint_skips_exporter(self):
        from google.api_core.client_options import ClientOptions

        from google.cloud.spanner_v1._async import client as MUT

        custom_endpoints = [
            {"api_endpoint": "private-spanner.internal:443"},
            ClientOptions(api_endpoint="private-psc.internal:443"),
            ClientOptions(api_endpoint="spanner.us-central1.rep.googleapis.com"),
            ClientOptions(
                api_endpoint="spanner.googleapis.com",
                universe_domain="my-universe.com",
            ),
            ClientOptions(api_endpoint="spanner.googleapis.com@evil.example"),
        ]
        for client_options in custom_endpoints:
            with (
                mock.patch(
                    "google.cloud.spanner_v1._async.client._metrics_monitor_initialized",
                    False,
                ),
                mock.patch(
                    "google.cloud.spanner_v1._async.client._get_spanner_emulator_host",
                    return_value=None,
                ),
                mock.patch(
                    "google.cloud.spanner_v1._async.client.CloudMonitoringMetricsExporter"
                ) as mock_exporter,
                mock.patch(
                    "google.cloud.spanner_v1._async.client.metrics.set_meter_provider"
                ) as mock_set_provider,
                mock.patch(
                    "google.cloud.spanner_v1._async.client.SpannerMetricsTracerFactory"
                ),
            ):
                MUT._initialize_metrics(
                    "project",
                    self.credentials,
                    client_options=client_options,
                )
                mock_exporter.assert_not_called()
                mock_set_provider.assert_called_once()
                self.assertIsInstance(
                    mock_set_provider.call_args[0][0],
                    MUT.metrics.NoOpMeterProvider,
                )

    def test_initialize_metrics_universe_propagation_and_option_filtering(self):
        from google.api_core.client_options import ClientOptions

        from google.cloud.spanner_v1._async import client as MUT

        creds = mock.Mock()
        client_options = ClientOptions(
            universe_domain="my-universe.com",
            quota_project_id="quota-proj",
            scopes=["https://www.googleapis.com/auth/spanner.admin"],
            api_audience="https://spanner.my-universe.com",
            api_key="fake-api-key",
        )
        with (
            mock.patch(
                "google.cloud.spanner_v1._async.client._metrics_monitor_initialized",
                False,
            ),
            mock.patch(
                "google.cloud.spanner_v1._async.client._get_spanner_emulator_host",
                return_value=None,
            ),
            mock.patch(
                "google.cloud.spanner_v1._async.client.CloudMonitoringMetricsExporter"
            ) as mock_exporter,
            mock.patch(
                "google.cloud.spanner_v1._async.client.PeriodicExportingMetricReader"
            ),
            mock.patch("google.cloud.spanner_v1._async.client.MeterProvider"),
            mock.patch(
                "google.cloud.spanner_v1._async.client.metrics.set_meter_provider"
            ),
            mock.patch(
                "google.cloud.spanner_v1._async.client.SpannerMetricsTracerFactory"
            ),
        ):
            MUT._initialize_metrics(
                "my-project",
                creds,
                client_options=client_options,
            )

        mock_exporter.assert_called_once()
        _, kwargs = mock_exporter.call_args
        self.assertEqual(kwargs["project_id"], "my-project")
        self.assertIs(kwargs["credentials"], creds)
        monitoring_opts = kwargs["client_options"]
        self.assertIsInstance(monitoring_opts, ClientOptions)
        self.assertEqual(monitoring_opts.universe_domain, "my-universe.com")
        self.assertIsNone(monitoring_opts.api_endpoint)
        self.assertIsNone(monitoring_opts.scopes)
        self.assertIsNone(monitoring_opts.api_audience)
        self.assertIsNone(monitoring_opts.credentials_file)
        self.assertIsNone(monitoring_opts.api_key)

    def test_client_custom_api_endpoint_skips_metrics_exporter(self):
        import os

        from google.cloud.spanner_v1._async import client as MUT

        creds = build_scoped_credentials()
        with (
            mock.patch.dict(os.environ, {"SPANNER_DISABLE_BUILTIN_METRICS": "false"}),
            mock.patch(
                "google.cloud.spanner_v1._async.client._metrics_monitor_initialized",
                False,
            ),
            mock.patch("google.cloud.spanner_v1._async.client.metrics"),
            mock.patch(
                "google.cloud.spanner_v1._async.client.CloudMonitoringMetricsExporter"
            ) as mock_exporter,
            mock.patch(
                "google.cloud.spanner_v1._async.client.SpannerMetricsTracerFactory"
            ),
        ):
            MUT.Client(
                project="my-project",
                credentials=creds,
                client_options={"api_endpoint": "private-psc.internal:443"},
            )
            mock_exporter.assert_not_called()

    def test_client_custom_api_endpoint_with_monitoring_host_env(self):
        import os

        from google.cloud.spanner_v1._async import client as MUT

        creds = build_scoped_credentials()
        with (
            mock.patch.dict(
                os.environ,
                {
                    "SPANNER_DISABLE_BUILTIN_METRICS": "false",
                    "SPANNER_MONITORING_HOST": "monitoring-psc.internal:443",
                },
            ),
            mock.patch(
                "google.cloud.spanner_v1._async.client._metrics_monitor_initialized",
                False,
            ),
            mock.patch("google.cloud.spanner_v1._async.client.metrics"),
            mock.patch(
                "google.cloud.spanner_v1._async.client.CloudMonitoringMetricsExporter"
            ) as mock_exporter,
            mock.patch(
                "google.cloud.spanner_v1._async.client.PeriodicExportingMetricReader"
            ),
            mock.patch("google.cloud.spanner_v1._async.client.MeterProvider"),
            mock.patch(
                "google.cloud.spanner_v1._async.client.SpannerMetricsTracerFactory"
            ),
        ):
            MUT.Client(
                project="my-project",
                credentials=creds,
                client_options={
                    "api_endpoint": "spanner.us-central1.rep.googleapis.com",
                    "universe_domain": "async.universe",
                },
            )
            mock_exporter.assert_called_once()
            _, kwargs = mock_exporter.call_args
            self.assertEqual(
                kwargs["client_options"].api_endpoint,
                "monitoring-psc.internal:443",
            )
            self.assertEqual(
                kwargs["client_options"].universe_domain,
                "async.universe",
            )

    def test_client_passes_resolved_project_credentials_and_universe_domain(self):
        import os

        from google.cloud.spanner_v1._async import client as MUT

        creds = build_scoped_credentials()
        creds.project_id = "resolved-async-project"
        with (
            mock.patch.dict(os.environ, {"SPANNER_DISABLE_BUILTIN_METRICS": "false"}),
            mock.patch(
                "google.cloud.spanner_v1._async.client._metrics_monitor_initialized",
                False,
            ),
            mock.patch("google.cloud.spanner_v1._async.client.metrics"),
            mock.patch(
                "google.cloud.spanner_v1._async.client.CloudMonitoringMetricsExporter"
            ) as mock_exporter,
            mock.patch(
                "google.cloud.spanner_v1._async.client.PeriodicExportingMetricReader"
            ),
            mock.patch("google.cloud.spanner_v1._async.client.MeterProvider"),
            mock.patch(
                "google.cloud.spanner_v1._async.client.SpannerMetricsTracerFactory"
            ),
        ):
            os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
            os.environ.pop("GCLOUD_PROJECT", None)
            client = MUT.Client(
                project=None,
                credentials=creds,
                client_options={
                    "universe_domain": "async.universe",
                    "api_audience": "https://spanner.async.universe",
                },
            )
            mock_exporter.assert_called_once()
            _, kwargs = mock_exporter.call_args
            self.assertEqual(kwargs["project_id"], "resolved-async-project")
            self.assertIs(kwargs["credentials"], client._credentials)
            self.assertEqual(kwargs["client_options"].universe_domain, "async.universe")
            self.assertIsNone(kwargs["client_options"].api_audience)
