# Copyright 2023 Google LLC
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


from __future__ import annotations

import logging
import os
import re
import shutil
import tempfile
import textwrap
import types
import warnings
from typing import Any, cast

import google.api_core.exceptions
import google.api_core.retry
import requests
from google.cloud import bigquery, functions_v2

import bigframes.exceptions as bfe
import bigframes.formatting_helpers as bf_formatting
import bigframes.functions.function_template as bff_template
import bigframes.functions.udf_def as udf_def
from bigframes.functions import _utils

logger = logging.getLogger(__name__)

# https://cloud.google.com/sdk/gcloud/reference/functions/deploy#--ingress-settings
_INGRESS_SETTINGS_MAP = types.MappingProxyType(
    {
        "all": functions_v2.ServiceConfig.IngressSettings.ALLOW_ALL,
        "internal-only": functions_v2.ServiceConfig.IngressSettings.ALLOW_INTERNAL_ONLY,
        "internal-and-gclb": functions_v2.ServiceConfig.IngressSettings.ALLOW_INTERNAL_AND_GCLB,
    }
)

# https://cloud.google.com/functions/docs/reference/rest/v2/projects.locations.functions#vpconnectoregresssettings
_VPC_EGRESS_SETTINGS_MAP = types.MappingProxyType(
    {
        "all": functions_v2.ServiceConfig.VpcConnectorEgressSettings.ALL_TRAFFIC,
        "private-ranges-only": functions_v2.ServiceConfig.VpcConnectorEgressSettings.PRIVATE_RANGES_ONLY,
        "unspecified": functions_v2.ServiceConfig.VpcConnectorEgressSettings.VPC_CONNECTOR_EGRESS_SETTINGS_UNSPECIFIED,
    }
)

# BQ managed functions (@udf) currently only support Python 3.11.
_MANAGED_FUNC_PYTHON_VERSION = "python-3.11"


class FunctionClient:
    # TODO(b/392707725): Convert all necessary parameters for cloud function
    # deployment into method parameters.
    def __init__(
        self,
        gcp_project_id: str,
        bq_location: str,
        bq_client: bigquery.Client,
        bq_connection_manager,
        cloud_functions_client: functions_v2.FunctionServiceClient,
        publisher,
    ):
        self._gcp_project_id = gcp_project_id
        self._bq_location = bq_location
        self._bq_client = bq_client
        self._bq_connection_manager = bq_connection_manager
        self._publisher = publisher
        self._cloud_functions_client = cloud_functions_client

        self._cf_location = _utils.gcf_location_from_bq_location(bq_location)

    @property
    def cloudfunctions_region(self) -> str:
        return self._cf_location

    def _create_bq_connection(
        self,
        connection_id: str,
        bq_project_id: str,
    ) -> None:
        self._bq_connection_manager.create_bq_connection(
            bq_project_id,
            self._bq_location,
            connection_id,
            "run.invoker",
        )

    def _ensure_dataset_exists(self, dataset_ref: bigquery.DatasetReference) -> None:
        # Make sure the dataset exists, i.e. if it doesn't exist, go ahead and
        # create it.
        try:
            # This check does not require bigquery.datasets.create IAM
            # permission. So, if the data set already exists, then user can work
            # without having that permission.
            self._bq_client.get_dataset(dataset_ref)
        except google.api_core.exceptions.NotFound:
            # This requires bigquery.datasets.create IAM permission.
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = self._bq_location
            self._bq_client.create_dataset(dataset, exists_ok=True)

    def _create_bq_function(self, create_function_ddl: str) -> None:
        # TODO(swast): plumb through the original, user-facing api_name.
        import bigframes.session._io.bigquery

        _, query_job = bigframes.session._io.bigquery.start_query_with_job(
            self._bq_client,
            create_function_ddl,
            job_config=bigquery.QueryJobConfig(),
            location=self._bq_location,
            project=None,
            timeout=None,
            metrics=None,
            publisher=self._publisher,
        )
        logger.info(f"Created bigframes function {query_job.ddl_target_routine}")

    def _format_function_options(self, function_options: dict) -> str:
        def format_val(val):
            if isinstance(val, str):
                return f"'{val}'"
            if isinstance(val, (list, tuple)):
                return str(list(val))
            return str(val)

        return ", ".join(
            [
                f"{key}={format_val(val)}"
                for key, val in function_options.items()
                if val is not None
            ]
        )

    def create_bq_remote_function(
        self,
        routine_ref: bigquery.RoutineReference,
        udf_def: udf_def.RemoteFunctionConfig,
        maybe_reuse: bool,
        try_create_connection: bool,
    ):
        """Create a BigQuery remote function given the artifacts of a user defined
        function and the http endpoint of a corresponding cloud function."""

        if maybe_reuse:
            existing_rf_spec = self.get_remote_function_specs(routine_ref)
            if existing_rf_spec and existing_rf_spec == udf_def:
                logger.info(f"Remote function {str(routine_ref)} already exists.")
                return

        if try_create_connection:
            self._create_bq_connection(udf_def.connection_id, routine_ref.project)

        # Create BQ function
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#create_a_remote_function_2

        remote_function_options = {
            "endpoint": udf_def.endpoint,
            "max_batching_rows": udf_def.max_batching_rows,
        }

        if udf_def.bq_metadata:
            # We are using the description field to store this structured
            # bigframes specific metadata for the lack of a better option
            remote_function_options["description"] = udf_def.bq_metadata

        remote_function_options_str = self._format_function_options(
            remote_function_options
        )

        import bigframes.core.sql
        import bigframes.core.utils

        # removes anything that isn't letter, number or underscore
        _validate_routine_name(routine_ref.routine_id)
        bq_function_name_escaped = bigframes.core.sql.identifier(routine_ref.routine_id)
        create_function_ddl = f"""
            CREATE OR REPLACE FUNCTION `{routine_ref.project}.{routine_ref.dataset_id}`.{bq_function_name_escaped}({udf_def.signature.to_sql_input_signature()})
            RETURNS {udf_def.signature.with_devirtualize().output.sql_type}
            REMOTE WITH CONNECTION `{routine_ref.project}.{self._bq_location}.{udf_def.connection_id}`
            OPTIONS ({remote_function_options_str})"""

        logger.info(f"Creating BQ remote function: {create_function_ddl}")

        self._ensure_dataset_exists(
            bigquery.DatasetReference(routine_ref.project, routine_ref.dataset_id)
        )
        self._create_bq_function(create_function_ddl)

    def provision_bq_managed_function(
        self,
        routine_ref: bigquery.RoutineReference,
        config: udf_def.ManagedFunctionConfig,
    ):
        """Create a BigQuery managed function."""

        # TODO(b/406283812): Expose the capability to pass down
        # capture_references=True in the public udf API.
        if (
            config.capture_references
            and (python_version := _utils.get_python_version())
            != _MANAGED_FUNC_PYTHON_VERSION
        ):
            raise bf_formatting.create_exception_with_feedback_link(
                NotImplementedError,
                f"Capturing references for udf is currently supported only in Python version {_MANAGED_FUNC_PYTHON_VERSION}, you are running {python_version}.",
            )

        # Create BQ managed function.
        bq_function_args = config.signature.to_sql_input_signature()
        bq_function_return_type = config.signature.with_devirtualize().output.sql_type

        managed_function_options: dict[str, Any] = {
            "runtime_version": _MANAGED_FUNC_PYTHON_VERSION,
            "entry_point": "bigframes_handler",
        }
        if config.max_batching_rows:
            managed_function_options["max_batching_rows"] = config.max_batching_rows
        if config.container_cpu:
            managed_function_options["container_cpu"] = config.container_cpu
        if config.container_memory:
            managed_function_options["container_memory"] = config.container_memory

        # Augment user package requirements with any internal package
        # requirements.
        packages = _utils.get_updated_package_requirements(
            config.code.package_requirements or [],
            config.signature.is_row_processor,
            config.capture_references,
            ignore_package_version=True,
        )
        if packages:
            managed_function_options["packages"] = packages
        managed_function_options_str = self._format_function_options(
            managed_function_options
        )

        persistent_func_id = (
            f"`{routine_ref.project}.{routine_ref.dataset_id}.{routine_ref.routine_id}`"
        )

        with_connection_clause = (
            (
                f"WITH CONNECTION `{routine_ref.project}.{self._bq_location}.{config.bq_connection_id}`"
            )
            if config.bq_connection_id
            else ""
        )

        # Generate the complete Python code block for the managed Python UDF,
        # including the user's function, necessary imports, and the BigQuery
        # handler wrapper.
        python_code_block = bff_template.generate_managed_function_code(
            config.code, config.signature, config.capture_references
        )

        create_function_ddl = (
            textwrap.dedent(
                f"""
                CREATE OR REPLACE FUNCTION {persistent_func_id}({bq_function_args})
                RETURNS {bq_function_return_type}
                LANGUAGE python
                {with_connection_clause}
                OPTIONS ({managed_function_options_str})
                AS r'''
                __UDF_PLACE_HOLDER__
                '''
            """
            )
            .strip()
            .replace("__UDF_PLACE_HOLDER__", python_code_block)
        )

        self._ensure_dataset_exists(
            bigquery.DatasetReference(routine_ref.project, routine_ref.dataset_id)
        )
        self._create_bq_function(create_function_ddl)

    def get_cloud_function_fully_qualified_parent(self):
        "Get the fully qualilfied parent for a cloud function."
        return self._cloud_functions_client.common_location_path(
            self._gcp_project_id, self._cf_location
        )

    def get_cloud_function_fully_qualified_name(self, name):
        "Get the fully qualilfied name for a cloud function."
        return self._cloud_functions_client.function_path(
            self._gcp_project_id, self._cf_location, name
        )

    def get_cloud_function_endpoint(self, name) -> str | None:
        """Get the http endpoint of a cloud function if it exists."""
        fully_qualified_name = self.get_cloud_function_fully_qualified_name(name)
        try:
            response = self._cloud_functions_client.get_function(
                name=fully_qualified_name
            )
            return response.service_config.uri
        except google.api_core.exceptions.NotFound:
            pass
        return None

    def _generate_cloud_function_code(
        self,
        code_def: udf_def.CodeDef,
        directory,
        *,
        udf_signature: udf_def.UdfSignature,
    ):
        """Generate the cloud function code for a given user defined function."""

        # requirements.txt
        if code_def.package_requirements:
            requirements_txt = os.path.join(directory, "requirements.txt")
            with open(requirements_txt, "w") as f:
                f.write("\n".join(code_def.package_requirements))

        # main.py
        entry_point = bff_template.generate_cloud_function_main_code(
            code_def,
            directory,
            udf_signature=udf_signature,
        )
        return entry_point

    @google.api_core.retry.Retry(
        predicate=google.api_core.retry.if_exception_type(ValueError),
        initial=1.0,
        maximum=10.0,
        multiplier=2.0,
        deadline=300.0,  # Wait up to 5 minutes for propagation
    )
    def _get_cloud_function_endpoint_with_retry(self, name):
        endpoint = self.get_cloud_function_endpoint(name)
        if not endpoint:
            # Raising ValueError triggers the retry predicate
            raise ValueError(f"Endpoint for {name} not yet available.")
        return endpoint

    def create_cloud_function(
        self,
        name: str,
        func_def: udf_def.CloudRunFunctionConfig,
    ) -> str:
        """Create a cloud function from the given user defined function."""

        config = func_def

        # Build and deploy folder structure containing cloud function
        with tempfile.TemporaryDirectory() as scratch_dir:
            # Keep the generated sources in a subdirectory so the archive can be
            # written inside the 0700 TemporaryDirectory. shutil.make_archive
            # appends ".zip" to base_name, so archiving `directory` into itself
            # would leave a world-readable copy of the (pickled) user code as a
            # sibling of the temp dir that also survives the cleanup.
            directory = os.path.join(scratch_dir, "src")
            os.mkdir(directory)
            entry_point = self._generate_cloud_function_code(
                config.code,
                directory,
                udf_signature=config.signature,
            )
            archive_path = shutil.make_archive(
                os.path.join(scratch_dir, "source"), "zip", directory
            )

            # We are creating cloud function source code from the currently running
            # python version. Use the same version to deploy. This is necessary
            # because cloudpickle serialization done in one python version and
            # deserialization done in another python version doesn't work.
            # TODO(shobs): Figure out how to achieve version compatibility, specially
            # when pickle (internally used by cloudpickle) guarantees that:
            # https://docs.python.org/3/library/pickle.html#:~:text=The%20pickle%20serialization%20format%20is,unique%20breaking%20change%20language%20boundary.
            python_version = _utils.get_python_version(is_compat=True)

            # Determine an upload URL for user code
            upload_url_request = functions_v2.GenerateUploadUrlRequest(
                kms_key_name=config.kms_key_name
            )
            upload_url_request.parent = self.get_cloud_function_fully_qualified_parent()
            upload_url_response = self._cloud_functions_client.generate_upload_url(
                request=upload_url_request
            )

            # Upload the code to GCS
            with open(archive_path, "rb") as f:
                response = requests.put(
                    upload_url_response.upload_url,
                    data=f,
                    headers={"content-type": "application/zip"},
                )
                if response.status_code != 200:
                    raise bf_formatting.create_exception_with_feedback_link(
                        RuntimeError,
                        f"Failed to upload user code. code={response.status_code}, reason={response.reason}, text={response.text}",
                    )

            # Deploy Cloud Function
            create_function_request = functions_v2.CreateFunctionRequest()
            create_function_request.parent = (
                self.get_cloud_function_fully_qualified_parent()
            )
            create_function_request.function_id = name
            function = functions_v2.Function()
            function.name = self.get_cloud_function_fully_qualified_name(name)
            function.build_config = functions_v2.BuildConfig()
            function.build_config.runtime = python_version
            function.build_config.entry_point = entry_point
            function.build_config.source = functions_v2.Source()
            function.build_config.source.storage_source = functions_v2.StorageSource()
            function.build_config.source.storage_source.bucket = (
                upload_url_response.storage_source.bucket
            )
            function.build_config.source.storage_source.object_ = (
                upload_url_response.storage_source.object_
            )
            if config.docker_repository is not None:
                function.build_config.docker_repository = config.docker_repository

            if config.cloud_build_service_account is not None:
                canonical_cloud_build_service_account = (
                    config.cloud_build_service_account
                    if "/" in config.cloud_build_service_account
                    else f"projects/{self._gcp_project_id}/serviceAccounts/{config.cloud_build_service_account}"
                )
                function.build_config.service_account = (
                    canonical_cloud_build_service_account
                )

            function.service_config = functions_v2.ServiceConfig()
            if config.memory_mib is not None:
                function.service_config.available_memory = f"{config.memory_mib}Mi"
            if config.cpus is not None:
                function.service_config.available_cpu = str(config.cpus)
            if config.timeout_seconds is not None:
                if config.timeout_seconds > 1200:
                    raise bf_formatting.create_exception_with_feedback_link(
                        ValueError,
                        "BigQuery remote function can wait only up to 20 minutes"
                        ", see for more details "
                        "https://cloud.google.com/bigquery/quotas#remote_function_limits.",
                    )
                function.service_config.timeout_seconds = config.timeout_seconds
            if config.max_instance_count is not None:
                function.service_config.max_instance_count = config.max_instance_count
            if config.vpc_connector is not None:
                function.service_config.vpc_connector = config.vpc_connector
                vpc_connector_egress_settings = config.vpc_connector_egress_settings
                if config.vpc_connector_egress_settings is None:
                    msg = bfe.format_message(
                        "The 'vpc_connector_egress_settings' was not specified. Defaulting to 'private-ranges-only'.",
                    )
                    warnings.warn(msg, category=UserWarning)
                    vpc_connector_egress_settings = "private-ranges-only"
                if config.vpc_connector_egress_settings not in _VPC_EGRESS_SETTINGS_MAP:
                    raise bf_formatting.create_exception_with_feedback_link(
                        ValueError,
                        f"'{config.vpc_connector_egress_settings}' is not one of the supported vpc egress settings values: {list(_VPC_EGRESS_SETTINGS_MAP)}",
                    )
                function.service_config.vpc_connector_egress_settings = cast(
                    functions_v2.ServiceConfig.VpcConnectorEgressSettings,
                    _VPC_EGRESS_SETTINGS_MAP[vpc_connector_egress_settings],
                )
            if config.cloud_run_service_account:
                function.service_config.service_account_email = (
                    config.cloud_run_service_account
                )
            if config.concurrency:
                function.service_config.max_instance_request_concurrency = (
                    config.concurrency
                )

            # Functions framework use environment variables to pass config to gunicorn
            # See https://github.com/GoogleCloudPlatform/functions-framework-python/issues/241
            # Code: https://github.com/GoogleCloudPlatform/functions-framework-python/blob/v3.10.1/src/functions_framework/_http/gunicorn.py#L37-L43
            env_vars = {}
            if config.workers:
                env_vars["WORKERS"] = str(config.workers)
            if config.threads:
                env_vars["THREADS"] = str(config.threads)
            if env_vars:
                function.service_config.environment_variables = env_vars

            if config.ingress_settings not in _INGRESS_SETTINGS_MAP:
                raise bf_formatting.create_exception_with_feedback_link(
                    ValueError,
                    f"'{config.ingress_settings}' not one of the supported ingress settings values: {list(_INGRESS_SETTINGS_MAP)}",
                )
            function.service_config.ingress_settings = cast(
                functions_v2.ServiceConfig.IngressSettings,
                _INGRESS_SETTINGS_MAP[config.ingress_settings],
            )
            if config.kms_key_name:
                function.kms_key_name = config.kms_key_name
            create_function_request.function = function

            # Create the cloud function and wait for it to be ready to use
            endpoint = None
            try:
                operation = self._cloud_functions_client.create_function(
                    request=create_function_request
                )
                # operation.result() returns the Function object upon completion
                function_obj = operation.result()
                endpoint = function_obj.service_config.uri

                # Cleanup
                os.remove(archive_path)
            except google.api_core.exceptions.AlreadyExists:
                # b/437124912: The most likely scenario is that
                # `create_function` had a retry due to a network issue. The
                # retried request then fails because the first call actually
                # succeeded, but we didn't get the successful response back.
                #
                # Since the function name was randomly chosen to avoid
                # conflicts, we know the AlreadyExist can only happen because
                # we created it. This error is safe to ignore.
                pass

        # Fetch the endpoint with retries if it wasn't returned by the operation
        if not endpoint:
            try:
                endpoint = self._get_cloud_function_endpoint_with_retry(name)
            except Exception as e:
                raise bf_formatting.create_exception_with_feedback_link(
                    ValueError, f"Couldn't fetch the http endpoint: {e}"
                )

        logger.info(f"Successfully created cloud function {name} with uri ({endpoint})")
        return endpoint

    def get_remote_function_specs(
        self, remote_function_name: bigquery.RoutineReference
    ) -> udf_def.RemoteFunctionConfig | None:
        """Check whether a remote function already exists for the udf."""
        try:
            routine = self._bq_client.get_routine(str(remote_function_name))
            if routine.reference == remote_function_name:
                try:
                    return udf_def.RemoteFunctionConfig.from_bq_routine(routine)
                except udf_def.ReturnTypeMissingError:
                    # The remote function exists, but it's missing a return type.
                    # Something is wrong with the function, so we should replace it.
                    return None
        except google.api_core.exceptions.NotFound:
            # The dataset might not exist, in which case the remote function doesn't, either.
            # Note: list_routines doesn't make an API request until we iterate on the response object.
            pass
        return None

    def delete_routine(self, routine_name: bigquery.RoutineReference) -> None:
        self._bq_client.delete_routine(str(routine_name), not_found_ok=True)

    def delete_cloud_function(self, cloud_function_name: str) -> None:
        try:
            self._cloud_functions_client.delete_function(
                name=self.get_cloud_function_fully_qualified_name(cloud_function_name)
            )
        except google.api_core.exceptions.NotFound:
            # The dataset might not exist, in which case the remote function doesn't, either.
            pass


def _validate_routine_name(name: str) -> None:
    """Validate that the given name is a valid BigQuery routine name."""
    # Routine IDs can contain only letters (a-z, A-Z), numbers (0-9), or underscores (_)
    # must also start with a letter or underscore only
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
        raise ValueError(
            "Routine ID can contain only letters (a-z, A-Z), numbers (0-9), or underscores (_)"
        )
