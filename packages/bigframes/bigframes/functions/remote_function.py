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

import collections.abc
import hashlib
import inspect
import logging
import os
import random
import shutil
import string
import sys
import tempfile
from typing import (
    Any,
    cast,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    TYPE_CHECKING,
    Union,
)
import warnings

import ibis
import numpy
import pandas
import pyarrow
import requests

if TYPE_CHECKING:
    from bigframes.session import Session

import bigframes_vendored.ibis.backends.bigquery.datatypes as third_party_ibis_bqtypes
import cloudpickle
import google.api_core.exceptions
import google.api_core.retry
from google.cloud import (
    bigquery,
    bigquery_connection_v1,
    functions_v2,
    resourcemanager_v3,
)
import google.iam.v1
from ibis.expr.datatypes.core import DataType as IbisDataType

from bigframes import clients
import bigframes.constants as constants
import bigframes.core.compile.ibis_types
import bigframes.functions.remote_function_template

logger = logging.getLogger(__name__)

# Protocol version 4 is available in python version 3.4 and above
# https://docs.python.org/3/library/pickle.html#data-stream-format
_pickle_protocol_version = 4


def get_remote_function_locations(bq_location):
    """Get BQ location and cloud functions region given a BQ client."""
    # TODO(shobs, b/274647164): Find the best way to determine default location.
    # For now let's assume that if no BQ location is set in the client then it
    # defaults to US multi region
    bq_location = bq_location.lower() if bq_location else "us"

    # Cloud function should be in the same region as the bigquery remote function
    cloud_function_region = bq_location

    # BigQuery has multi region but cloud functions does not.
    # Any region in the multi region that supports cloud functions should work
    # https://cloud.google.com/functions/docs/locations
    if bq_location == "us":
        cloud_function_region = "us-central1"
    elif bq_location == "eu":
        cloud_function_region = "europe-west1"

    return bq_location, cloud_function_region


def _get_hash(def_, package_requirements=None):
    "Get hash (32 digits alphanumeric) of a function."
    def_repr = cloudpickle.dumps(def_, protocol=_pickle_protocol_version)
    if package_requirements:
        for p in sorted(package_requirements):
            def_repr += p.encode()
    return hashlib.md5(def_repr).hexdigest()


def _get_updated_package_requirements(package_requirements, is_row_processor):
    requirements = [f"cloudpickle=={cloudpickle.__version__}"]
    if is_row_processor:
        # bigframes remote function will send an entire row of data as json,
        # which would be converted to a pandas series and processed
        # Ensure numpy versions match to avoid unpickling problems. See
        # internal issue b/347934471.
        requirements.append(f"numpy=={numpy.__version__}")
        requirements.append(f"pandas=={pandas.__version__}")
        requirements.append(f"pyarrow=={pyarrow.__version__}")

    if package_requirements:
        requirements.extend(package_requirements)

    requirements = sorted(requirements)
    return requirements


def routine_ref_to_string_for_query(routine_ref: bigquery.RoutineReference) -> str:
    return f"`{routine_ref.project}.{routine_ref.dataset_id}`.{routine_ref.routine_id}"


class IbisSignature(NamedTuple):
    parameter_names: List[str]
    input_types: List[Optional[IbisDataType]]
    output_type: IbisDataType


def get_cloud_function_name(
    def_, uniq_suffix=None, package_requirements=None, is_row_processor=False
):
    "Get a name for the cloud function for the given user defined function."

    # Augment user package requirements with any internal package
    # requirements
    package_requirements = _get_updated_package_requirements(
        package_requirements, is_row_processor
    )

    cf_name = _get_hash(def_, package_requirements)
    cf_name = f"bigframes-{cf_name}"  # for identification
    if uniq_suffix:
        cf_name = f"{cf_name}-{uniq_suffix}"
    return cf_name, package_requirements


def get_remote_function_name(def_, uniq_suffix=None, package_requirements=None):
    "Get a name for the BQ remote function for the given user defined function."
    bq_rf_name = _get_hash(def_, package_requirements)
    bq_rf_name = f"bigframes_{bq_rf_name}"  # for identification
    if uniq_suffix:
        bq_rf_name = f"{bq_rf_name}_{uniq_suffix}"
    return bq_rf_name


class RemoteFunctionClient:
    # Wait time (in seconds) for an IAM binding to take effect after creation
    _iam_wait_seconds = 120

    def __init__(
        self,
        gcp_project_id,
        cloud_function_region,
        cloud_functions_client,
        bq_location,
        bq_dataset,
        bq_client,
        bq_connection_id,
        bq_connection_manager,
        cloud_function_service_account,
        cloud_function_kms_key_name,
        cloud_function_docker_repository,
        *,
        session: Session,
    ):
        self._gcp_project_id = gcp_project_id
        self._cloud_function_region = cloud_function_region
        self._cloud_functions_client = cloud_functions_client
        self._bq_location = bq_location
        self._bq_dataset = bq_dataset
        self._bq_client = bq_client
        self._bq_connection_id = bq_connection_id
        self._bq_connection_manager = bq_connection_manager
        self._cloud_function_service_account = cloud_function_service_account
        self._cloud_function_kms_key_name = cloud_function_kms_key_name
        self._cloud_function_docker_repository = cloud_function_docker_repository
        self._session = session

    def create_bq_remote_function(
        self,
        input_args,
        input_types,
        output_type,
        endpoint,
        bq_function_name,
        max_batching_rows,
    ):
        """Create a BigQuery remote function given the artifacts of a user defined
        function and the http endpoint of a corresponding cloud function."""
        if self._bq_connection_manager:
            self._bq_connection_manager.create_bq_connection(
                self._gcp_project_id,
                self._bq_location,
                self._bq_connection_id,
                "run.invoker",
            )

        # Create BQ function
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#create_a_remote_function_2
        bq_function_args = []
        bq_function_return_type = output_type

        # We are expecting the input type annotations to be 1:1 with the input args
        for name, type_ in zip(input_args, input_types):
            bq_function_args.append(f"{name} {type_}")

        remote_function_options = {
            "endpoint": endpoint,
            "max_batching_rows": max_batching_rows,
        }

        remote_function_options_str = ", ".join(
            [
                f'{key}="{val}"' if isinstance(val, str) else f"{key}={val}"
                for key, val in remote_function_options.items()
                if val is not None
            ]
        )

        create_function_ddl = f"""
            CREATE OR REPLACE FUNCTION `{self._gcp_project_id}.{self._bq_dataset}`.{bq_function_name}({','.join(bq_function_args)})
            RETURNS {bq_function_return_type}
            REMOTE WITH CONNECTION `{self._gcp_project_id}.{self._bq_location}.{self._bq_connection_id}`
            OPTIONS ({remote_function_options_str})"""

        logger.info(f"Creating BQ remote function: {create_function_ddl}")

        # Make sure the dataset exists. I.e. if it doesn't exist, go ahead and
        # create it
        dataset = bigquery.Dataset(
            bigquery.DatasetReference.from_string(
                self._bq_dataset, default_project=self._gcp_project_id
            )
        )
        dataset.location = self._bq_location
        try:
            # This check does not require bigquery.datasets.create IAM
            # permission. So, if the data set already exists, then user can work
            # without having that permission.
            self._bq_client.get_dataset(dataset)
        except google.api_core.exceptions.NotFound:
            # This requires bigquery.datasets.create IAM permission
            self._bq_client.create_dataset(dataset, exists_ok=True)

        # TODO(swast): plumb through the original, user-facing api_name.
        _, query_job = self._session._start_query(create_function_ddl)
        logger.info(f"Created remote function {query_job.ddl_target_routine}")

    def get_cloud_function_fully_qualified_parent(self):
        "Get the fully qualilfied parent for a cloud function."
        return self._cloud_functions_client.common_location_path(
            self._gcp_project_id, self._cloud_function_region
        )

    def get_cloud_function_fully_qualified_name(self, name):
        "Get the fully qualilfied name for a cloud function."
        return self._cloud_functions_client.function_path(
            self._gcp_project_id, self._cloud_function_region, name
        )

    def get_cloud_function_endpoint(self, name):
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

    def generate_cloud_function_code(
        self,
        def_,
        directory,
        *,
        input_types: Tuple[str],
        output_type: str,
        package_requirements=None,
        is_row_processor=False,
    ):
        """Generate the cloud function code for a given user defined function.

        Args:
            input_types (tuple[str]):
                Types of the input arguments in BigQuery SQL data type names.
            output_type (str):
                Types of the output scalar as a BigQuery SQL data type name.
        """

        # requirements.txt
        if package_requirements:
            requirements_txt = os.path.join(directory, "requirements.txt")
            with open(requirements_txt, "w") as f:
                f.write("\n".join(package_requirements))

        # main.py
        entry_point = bigframes.functions.remote_function_template.generate_cloud_function_main_code(
            def_,
            directory,
            input_types=input_types,
            output_type=output_type,
            is_row_processor=is_row_processor,
        )
        return entry_point

    def create_cloud_function(
        self,
        def_,
        cf_name,
        *,
        input_types: Tuple[str],
        output_type: str,
        package_requirements=None,
        timeout_seconds=600,
        max_instance_count=None,
        is_row_processor=False,
        vpc_connector=None,
        memory_mib=1024,
    ):
        """Create a cloud function from the given user defined function.

        Args:
            input_types (tuple[str]):
                Types of the input arguments in BigQuery SQL data type names.
            output_type (str):
                Types of the output scalar as a BigQuery SQL data type name.
        """

        # Build and deploy folder structure containing cloud function
        with tempfile.TemporaryDirectory() as directory:
            entry_point = self.generate_cloud_function_code(
                def_,
                directory,
                package_requirements=package_requirements,
                input_types=input_types,
                output_type=output_type,
                is_row_processor=is_row_processor,
            )
            archive_path = shutil.make_archive(directory, "zip", directory)

            # We are creating cloud function source code from the currently running
            # python version. Use the same version to deploy. This is necessary
            # because cloudpickle serialization done in one python version and
            # deserialization done in another python version doesn't work.
            # TODO(shobs): Figure out how to achieve version compatibility, specially
            # when pickle (internally used by cloudpickle) guarantees that:
            # https://docs.python.org/3/library/pickle.html#:~:text=The%20pickle%20serialization%20format%20is,unique%20breaking%20change%20language%20boundary.
            python_version = "python{}{}".format(
                sys.version_info.major, sys.version_info.minor
            )

            # Determine an upload URL for user code
            upload_url_request = functions_v2.GenerateUploadUrlRequest(
                kms_key_name=self._cloud_function_kms_key_name
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
                    raise RuntimeError(
                        "Failed to upload user code. code={}, reason={}, text={}".format(
                            response.status_code, response.reason, response.text
                        )
                    )

            # Deploy Cloud Function
            create_function_request = functions_v2.CreateFunctionRequest()
            create_function_request.parent = (
                self.get_cloud_function_fully_qualified_parent()
            )
            create_function_request.function_id = cf_name
            function = functions_v2.Function()
            function.name = self.get_cloud_function_fully_qualified_name(cf_name)
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
            function.build_config.docker_repository = (
                self._cloud_function_docker_repository
            )
            function.service_config = functions_v2.ServiceConfig()
            if memory_mib is not None:
                function.service_config.available_memory = f"{memory_mib}Mi"
            if timeout_seconds is not None:
                if timeout_seconds > 1200:
                    raise ValueError(
                        "BigQuery remote function can wait only up to 20 minutes"
                        ", see for more details "
                        "https://cloud.google.com/bigquery/quotas#remote_function_limits."
                    )
                function.service_config.timeout_seconds = timeout_seconds
            if max_instance_count is not None:
                function.service_config.max_instance_count = max_instance_count
            if vpc_connector is not None:
                function.service_config.vpc_connector = vpc_connector
            function.service_config.service_account_email = (
                self._cloud_function_service_account
            )
            function.kms_key_name = self._cloud_function_kms_key_name
            create_function_request.function = function

            # Create the cloud function and wait for it to be ready to use
            try:
                operation = self._cloud_functions_client.create_function(
                    request=create_function_request
                )
                operation.result()

                # Cleanup
                os.remove(archive_path)
            except google.api_core.exceptions.AlreadyExists:
                # If a cloud function with the same name already exists, let's
                # update it
                update_function_request = functions_v2.UpdateFunctionRequest()
                update_function_request.function = function
                operation = self._cloud_functions_client.update_function(
                    request=update_function_request
                )
                operation.result()

        # Fetch the endpoint of the just created function
        endpoint = self.get_cloud_function_endpoint(cf_name)
        if not endpoint:
            raise ValueError(
                f"Couldn't fetch the http endpoint. {constants.FEEDBACK_LINK}"
            )

        logger.info(
            f"Successfully created cloud function {cf_name} with uri ({endpoint})"
        )
        return endpoint

    def provision_bq_remote_function(
        self,
        def_,
        input_types,
        output_type,
        reuse,
        name,
        package_requirements,
        max_batching_rows,
        cloud_function_timeout,
        cloud_function_max_instance_count,
        is_row_processor,
        cloud_function_vpc_connector,
        cloud_function_memory_mib,
    ):
        """Provision a BigQuery remote function."""
        # If reuse of any existing function with the same name (indicated by the
        # same hash of its source code) is not intended, then attach a unique
        # suffix to the intended function name to make it unique.
        uniq_suffix = None
        if not reuse:
            uniq_suffix = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=8)
            )

        # Derive the name of the cloud function underlying the intended BQ
        # remote function, also collect updated package requirements as
        # determined in the name resolution
        cloud_function_name, package_requirements = get_cloud_function_name(
            def_, uniq_suffix, package_requirements, is_row_processor
        )
        cf_endpoint = self.get_cloud_function_endpoint(cloud_function_name)

        # Create the cloud function if it does not exist
        if not cf_endpoint:
            cf_endpoint = self.create_cloud_function(
                def_,
                cloud_function_name,
                input_types=input_types,
                output_type=output_type,
                package_requirements=package_requirements,
                timeout_seconds=cloud_function_timeout,
                max_instance_count=cloud_function_max_instance_count,
                is_row_processor=is_row_processor,
                vpc_connector=cloud_function_vpc_connector,
                memory_mib=cloud_function_memory_mib,
            )
        else:
            logger.info(f"Cloud function {cloud_function_name} already exists.")

        # Derive the name of the remote function
        remote_function_name = name
        if not remote_function_name:
            remote_function_name = get_remote_function_name(
                def_, uniq_suffix, package_requirements
            )
        rf_endpoint, rf_conn = self.get_remote_function_specs(remote_function_name)

        # Create the BQ remote function in following circumstances:
        # 1. It does not exist
        # 2. It exists but the existing remote function has different
        #    configuration than intended
        if not rf_endpoint or (
            rf_endpoint != cf_endpoint or rf_conn != self._bq_connection_id
        ):
            input_args = inspect.getargs(def_.__code__).args
            if len(input_args) != len(input_types):
                raise ValueError(
                    "Exactly one type should be provided for every input arg."
                )
            self.create_bq_remote_function(
                input_args,
                input_types,
                output_type,
                cf_endpoint,
                remote_function_name,
                max_batching_rows,
            )
        else:
            logger.info(f"Remote function {remote_function_name} already exists.")

        return remote_function_name, cloud_function_name

    def get_remote_function_specs(self, remote_function_name):
        """Check whether a remote function already exists for the udf."""
        http_endpoint = None
        bq_connection = None
        routines = self._bq_client.list_routines(
            f"{self._gcp_project_id}.{self._bq_dataset}"
        )
        try:
            for routine in routines:
                if routine.reference.routine_id == remote_function_name:
                    # TODO(shobs): Use first class properties when they are available
                    # https://github.com/googleapis/python-bigquery/issues/1552
                    rf_options = routine._properties.get("remoteFunctionOptions")
                    if rf_options:
                        http_endpoint = rf_options.get("endpoint")
                        bq_connection = rf_options.get("connection")
                        if bq_connection:
                            bq_connection = os.path.basename(bq_connection)
                    break
        except google.api_core.exceptions.NotFound:
            # The dataset might not exist, in which case the http_endpoint doesn't, either.
            # Note: list_routines doesn't make an API request until we iterate on the response object.
            pass
        return (http_endpoint, bq_connection)


class UnsupportedTypeError(ValueError):
    def __init__(self, type_, supported_types):
        self.type = type_
        self.supported_types = supported_types


def ibis_signature_from_python_signature(
    signature: inspect.Signature,
    input_types: Sequence[type],
    output_type: type,
) -> IbisSignature:

    return IbisSignature(
        parameter_names=list(signature.parameters.keys()),
        input_types=[
            bigframes.core.compile.ibis_types.ibis_type_from_python_type(t)
            for t in input_types
        ],
        output_type=bigframes.core.compile.ibis_types.ibis_type_from_python_type(
            output_type
        ),
    )


class ReturnTypeMissingError(ValueError):
    pass


# TODO: Move this to compile folder
def ibis_signature_from_routine(routine: bigquery.Routine) -> IbisSignature:
    if not routine.return_type:
        raise ReturnTypeMissingError

    return IbisSignature(
        parameter_names=[arg.name for arg in routine.arguments],
        input_types=[
            bigframes.core.compile.ibis_types.ibis_type_from_type_kind(
                arg.data_type.type_kind
            )
            if arg.data_type
            else None
            for arg in routine.arguments
        ],
        output_type=bigframes.core.compile.ibis_types.ibis_type_from_type_kind(
            routine.return_type.type_kind
        ),
    )


class DatasetMissingError(ValueError):
    pass


def get_routine_reference(
    routine_ref_str: str, bigquery_client: bigquery.Client, session: Optional[Session]
) -> bigquery.RoutineReference:
    try:
        # Handle cases "<project_id>.<dataset_name>.<routine_name>" and
        # "<dataset_name>.<routine_name>".
        return bigquery.RoutineReference.from_string(
            routine_ref_str,
            default_project=bigquery_client.project,
        )
    except ValueError:
        # Handle case of "<routine_name>".
        if not session:
            raise DatasetMissingError

        dataset_ref = bigquery.DatasetReference(
            bigquery_client.project, session._anonymous_dataset.dataset_id
        )
        return dataset_ref.routine(routine_ref_str)


# Inspired by @udf decorator implemented in ibis-bigquery package
# https://github.com/ibis-project/ibis-bigquery/blob/main/ibis_bigquery/udf/__init__.py
# which has moved as @js to the ibis package
# https://github.com/ibis-project/ibis/blob/master/ibis/backends/bigquery/udf/__init__.py
def remote_function(
    input_types: Union[None, type, Sequence[type]] = None,
    output_type: Optional[type] = None,
    session: Optional[Session] = None,
    bigquery_client: Optional[bigquery.Client] = None,
    bigquery_connection_client: Optional[
        bigquery_connection_v1.ConnectionServiceClient
    ] = None,
    cloud_functions_client: Optional[functions_v2.FunctionServiceClient] = None,
    resource_manager_client: Optional[resourcemanager_v3.ProjectsClient] = None,
    dataset: Optional[str] = None,
    bigquery_connection: Optional[str] = None,
    reuse: bool = True,
    name: Optional[str] = None,
    packages: Optional[Sequence[str]] = None,
    cloud_function_service_account: Optional[str] = None,
    cloud_function_kms_key_name: Optional[str] = None,
    cloud_function_docker_repository: Optional[str] = None,
    max_batching_rows: Optional[int] = 1000,
    cloud_function_timeout: Optional[int] = 600,
    cloud_function_max_instances: Optional[int] = None,
    cloud_function_vpc_connector: Optional[str] = None,
    cloud_function_memory_mib: Optional[int] = 1024,
):
    """Decorator to turn a user defined function into a BigQuery remote function.

    .. deprecated:: 0.0.1
       This is an internal method. Please use :func:`bigframes.pandas.remote_function` instead.

    .. note::
        Please make sure following is setup before using this API:

        1. Have the below APIs enabled for your project:

            * BigQuery Connection API
            * Cloud Functions API
            * Cloud Run API
            * Cloud Build API
            * Artifact Registry API
            * Cloud Resource Manager API

           This can be done from the cloud console (change `PROJECT_ID` to yours):
           https://console.cloud.google.com/apis/enableflow?apiid=bigqueryconnection.googleapis.com,cloudfunctions.googleapis.com,run.googleapis.com,cloudbuild.googleapis.com,artifactregistry.googleapis.com,cloudresourcemanager.googleapis.com&project=PROJECT_ID

           Or from the gcloud CLI:

           `$ gcloud services enable bigqueryconnection.googleapis.com cloudfunctions.googleapis.com run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com cloudresourcemanager.googleapis.com`

        2. Have following IAM roles enabled for you:

            * BigQuery Data Editor (roles/bigquery.dataEditor)
            * BigQuery Connection Admin (roles/bigquery.connectionAdmin)
            * Cloud Functions Developer (roles/cloudfunctions.developer)
            * Service Account User (roles/iam.serviceAccountUser) on the service account `PROJECT_NUMBER-compute@developer.gserviceaccount.com`
            * Storage Object Viewer (roles/storage.objectViewer)
            * Project IAM Admin (roles/resourcemanager.projectIamAdmin) (Only required if the bigquery connection being used is not pre-created and is created dynamically with user credentials.)

        3. Either the user has setIamPolicy privilege on the project, or a BigQuery connection is pre-created with necessary IAM role set:

            1. To create a connection, follow https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#create_a_connection
            2. To set up IAM, follow https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#grant_permission_on_function

               Alternatively, the IAM could also be setup via the gcloud CLI:

               `$ gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:CONNECTION_SERVICE_ACCOUNT_ID" --role="roles/run.invoker"`.

    Args:
        input_types (None, type, or sequence(type)):
            For scalar user defined function it should be the input type or
            sequence of input types. For row processing user defined function,
            type `Series` should be specified.
        output_type (Optional[type]):
            Data type of the output in the user defined function.
        session (bigframes.Session, Optional):
            BigQuery DataFrames session to use for getting default project,
            dataset and BigQuery connection.
        bigquery_client (google.cloud.bigquery.Client, Optional):
            Client to use for BigQuery operations. If this param is not provided
            then bigquery client from the session would be used.
        bigquery_connection_client (google.cloud.bigquery_connection_v1.ConnectionServiceClient, Optional):
            Client to use for BigQuery connection operations. If this param is
            not provided then bigquery connection client from the session would
            be used.
        cloud_functions_client (google.cloud.functions_v2.FunctionServiceClient, Optional):
            Client to use for cloud functions operations. If this param is not
            provided then the functions client from the session would be used.
        resource_manager_client (google.cloud.resourcemanager_v3.ProjectsClient, Optional):
            Client to use for cloud resource management operations, e.g. for
            getting and setting IAM roles on cloud resources. If this param is
            not provided then resource manager client from the session would be
            used.
        dataset (str, Optional.):
            Dataset in which to create a BigQuery remote function. It should be in
            `<project_id>.<dataset_name>` or `<dataset_name>` format. If this
            parameter is not provided then session dataset id is used.
        bigquery_connection (str, Optional):
            Name of the BigQuery connection in the form of `CONNECTION_ID` or
            `LOCATION.CONNECTION_ID` or `PROJECT_ID.LOCATION.CONNECTION_ID`.
            If this param is not provided then the bigquery connection from the session
            would be used. If it is pre created in the same location as the
            `bigquery_client.location` then it would be used, otherwise it is created
            dynamically using the `bigquery_connection_client` assuming the user has necessary
            priviliges. The PROJECT_ID should be the same as the BigQuery connection project.
        reuse (bool, Optional):
            Reuse the remote function if is already exists.
            `True` by default, which results in reusing an existing remote
            function and corresponding cloud function (if any) that was
            previously created for the same udf.
            Setting it to `False` forces the creation of a unique remote function.
            If the required remote function does not exist then it would be
            created irrespective of this param.
        name (str, Optional):
            Explicit name of the persisted BigQuery remote function. Use it with
            caution, because two users working in the same project and dataset
            could overwrite each other's remote functions if they use the same
            persistent name.
        packages (str[], Optional):
            Explicit name of the external package dependencies. Each dependency
            is added to the `requirements.txt` as is, and can be of the form
            supported in https://pip.pypa.io/en/stable/reference/requirements-file-format/.
        cloud_function_service_account (str, Optional):
            Service account to use for the cloud functions. If not provided then
            the default service account would be used. See
            https://cloud.google.com/functions/docs/securing/function-identity
            for more details. Please make sure the service account has the
            necessary IAM permissions configured as described in
            https://cloud.google.com/functions/docs/reference/iam/roles#additional-configuration.
        cloud_function_kms_key_name (str, Optional):
            Customer managed encryption key to protect cloud functions and
            related data at rest. This is of the format
            projects/PROJECT_ID/locations/LOCATION/keyRings/KEYRING/cryptoKeys/KEY.
            Read https://cloud.google.com/functions/docs/securing/cmek for
            more details including granting necessary service accounts
            access to the key.
        cloud_function_docker_repository (str, Optional):
            Docker repository created with the same encryption key as
            `cloud_function_kms_key_name` to store encrypted artifacts
            created to support the cloud function. This is of the format
            projects/PROJECT_ID/locations/LOCATION/repositories/REPOSITORY_NAME.
            For more details see
            https://cloud.google.com/functions/docs/securing/cmek#before_you_begin.
        max_batching_rows (int, Optional):
            The maximum number of rows to be batched for processing in the
            BQ remote function. Default value is 1000. A lower number can be
            passed to avoid timeouts in case the user code is too complex to
            process large number of rows fast enough. A higher number can be
            used to increase throughput in case the user code is fast enough.
            `None` can be passed to let BQ remote functions service apply
            default batching. See for more details
            https://cloud.google.com/bigquery/docs/remote-functions#limiting_number_of_rows_in_a_batch_request.
        cloud_function_timeout (int, Optional):
            The maximum amount of time (in seconds) BigQuery should wait for
            the cloud function to return a response. See for more details
            https://cloud.google.com/functions/docs/configuring/timeout.
            Please note that even though the cloud function (2nd gen) itself
            allows seeting up to 60 minutes of timeout, BigQuery remote
            function can wait only up to 20 minutes, see for more details
            https://cloud.google.com/bigquery/quotas#remote_function_limits.
            By default BigQuery DataFrames uses a 10 minute timeout. `None`
            can be passed to let the cloud functions default timeout take effect.
        cloud_function_max_instances (int, Optional):
            The maximumm instance count for the cloud function created. This
            can be used to control how many cloud function instances can be
            active at max at any given point of time. Lower setting can help
            control the spike in the billing. Higher setting can help
            support processing larger scale data. When not specified, cloud
            function's default setting applies. For more details see
            https://cloud.google.com/functions/docs/configuring/max-instances.
        cloud_function_vpc_connector (str, Optional):
            The VPC connector you would like to configure for your cloud
            function. This is useful if your code needs access to data or
            service(s) that are on a VPC network. See for more details
            https://cloud.google.com/functions/docs/networking/connecting-vpc.
        cloud_function_memory_mib (int, Optional):
            The amounts of memory (in mebibytes) to allocate for the cloud
            function (2nd gen) created. This also dictates a corresponding
            amount of allocated CPU for the function. By default a memory of
            1024 MiB is set for the cloud functions created to support
            BigQuery DataFrames remote function. If you want to let the
            default memory of cloud functions be allocated, pass `None`. See
            for more details
            https://cloud.google.com/functions/docs/configuring/memory.
    """
    # Some defaults may be used from the session if not provided otherwise
    import bigframes.exceptions as bf_exceptions
    import bigframes.pandas as bpd
    import bigframes.series as bf_series
    import bigframes.session

    session = cast(bigframes.session.Session, session or bpd.get_global_session())

    # A BigQuery client is required to perform BQ operations
    if not bigquery_client:
        bigquery_client = session.bqclient
    if not bigquery_client:
        raise ValueError(
            "A bigquery client must be provided, either directly or via session. "
            f"{constants.FEEDBACK_LINK}"
        )

    # A BigQuery connection client is required to perform BQ connection operations
    if not bigquery_connection_client:
        bigquery_connection_client = session.bqconnectionclient
    if not bigquery_connection_client:
        raise ValueError(
            "A bigquery connection client must be provided, either directly or via session. "
            f"{constants.FEEDBACK_LINK}"
        )

    # A cloud functions client is required to perform cloud functions operations
    if not cloud_functions_client:
        cloud_functions_client = session.cloudfunctionsclient
    if not cloud_functions_client:
        raise ValueError(
            "A cloud functions client must be provided, either directly or via session. "
            f"{constants.FEEDBACK_LINK}"
        )

    # A resource manager client is required to get/set IAM operations
    if not resource_manager_client:
        resource_manager_client = session.resourcemanagerclient
    if not resource_manager_client:
        raise ValueError(
            "A resource manager client must be provided, either directly or via session. "
            f"{constants.FEEDBACK_LINK}"
        )

    # BQ remote function must be persisted, for which we need a dataset
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#:~:text=You%20cannot%20create%20temporary%20remote%20functions.
    if dataset:
        dataset_ref = bigquery.DatasetReference.from_string(
            dataset, default_project=bigquery_client.project
        )
    else:
        dataset_ref = session._anonymous_dataset

    bq_location, cloud_function_region = get_remote_function_locations(
        bigquery_client.location
    )

    # A connection is required for BQ remote function
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#create_a_remote_function
    if not bigquery_connection:
        bigquery_connection = session._bq_connection  # type: ignore

    bigquery_connection = clients.resolve_full_bq_connection_name(
        bigquery_connection,
        default_project=dataset_ref.project,
        default_location=bq_location,
    )
    # Guaranteed to be the form of <project>.<location>.<connection_id>
    (
        gcp_project_id,
        bq_connection_location,
        bq_connection_id,
    ) = bigquery_connection.split(".")
    if gcp_project_id.casefold() != dataset_ref.project.casefold():
        raise ValueError(
            "The project_id does not match BigQuery connection gcp_project_id: "
            f"{dataset_ref.project}."
        )
    if bq_connection_location.casefold() != bq_location.casefold():
        raise ValueError(
            "The location does not match BigQuery connection location: "
            f"{bq_location}."
        )

    # If any CMEK is intended then check that a docker repository is also specified
    if (
        cloud_function_kms_key_name is not None
        and cloud_function_docker_repository is None
    ):
        raise ValueError(
            "cloud_function_docker_repository must be specified with cloud_function_kms_key_name."
            " For more details see https://cloud.google.com/functions/docs/securing/cmek#before_you_begin"
        )

    bq_connection_manager = None if session is None else session.bqconnectionmanager

    def wrapper(func):
        nonlocal input_types, output_type

        if not callable(func):
            raise TypeError("f must be callable, got {}".format(func))

        if sys.version_info >= (3, 10):
            # Add `eval_str = True` so that deferred annotations are turned into their
            # corresponding type objects. Need Python 3.10 for eval_str parameter.
            # https://docs.python.org/3/library/inspect.html#inspect.signature
            signature_kwargs: Mapping[str, Any] = {"eval_str": True}
        else:
            signature_kwargs = {}

        signature = inspect.signature(
            func,
            **signature_kwargs,
        )

        # Try to get input types via type annotations.
        if input_types is None:
            input_types = []
            for parameter in signature.parameters.values():
                if (param_type := parameter.annotation) is inspect.Signature.empty:
                    raise ValueError(
                        "'input_types' was not set and parameter "
                        f"'{parameter.name}' is missing a type annotation. "
                        "Types are required to use @remote_function."
                    )
                input_types.append(param_type)
        elif not isinstance(input_types, collections.abc.Sequence):
            input_types = [input_types]

        if output_type is None:
            if (output_type := signature.return_annotation) is inspect.Signature.empty:
                raise ValueError(
                    "'output_type' was not set and function is missing a "
                    "return type annotation. Types are required to use "
                    "@remote_function."
                )

        # The function will actually be receiving a pandas Series, but allow both
        # BigQuery DataFrames and pandas object types for compatibility.
        is_row_processor = False
        if len(input_types) == 1 and (
            (input_type := input_types[0]) == bf_series.Series
            or input_type == pandas.Series
        ):
            warnings.warn(
                "input_types=Series is in preview.",
                stacklevel=1,
                category=bf_exceptions.PreviewWarning,
            )

            # we will model the row as a json serialized string containing the data
            # and the metadata representing the row
            input_types = [str]
            is_row_processor = True
        elif isinstance(input_types, type):
            input_types = [input_types]

        # TODO(b/340898611): fix type error
        ibis_signature = ibis_signature_from_python_signature(
            signature, input_types, output_type  # type: ignore
        )

        remote_function_client = RemoteFunctionClient(
            dataset_ref.project,
            cloud_function_region,
            cloud_functions_client,
            bq_location,
            dataset_ref.dataset_id,
            bigquery_client,
            bq_connection_id,
            bq_connection_manager,
            cloud_function_service_account,
            cloud_function_kms_key_name,
            cloud_function_docker_repository,
            session=session,  # type: ignore
        )

        # In the unlikely case where the user is trying to re-deploy the same
        # function, cleanup the attributes we add below, first. This prevents
        # the pickle from having dependencies that might not otherwise be
        # present such as ibis or pandas.
        def try_delattr(attr):
            try:
                delattr(func, attr)
            except AttributeError:
                pass

        try_delattr("bigframes_cloud_function")
        try_delattr("bigframes_remote_function")
        try_delattr("output_dtype")
        try_delattr("ibis_node")

        rf_name, cf_name = remote_function_client.provision_bq_remote_function(
            func,
            input_types=tuple(
                third_party_ibis_bqtypes.BigQueryType.from_ibis(type_)
                for type_ in ibis_signature.input_types
            ),
            output_type=third_party_ibis_bqtypes.BigQueryType.from_ibis(
                ibis_signature.output_type
            ),
            reuse=reuse,
            name=name,
            package_requirements=packages,
            max_batching_rows=max_batching_rows,
            cloud_function_timeout=cloud_function_timeout,
            cloud_function_max_instance_count=cloud_function_max_instances,
            is_row_processor=is_row_processor,
            cloud_function_vpc_connector=cloud_function_vpc_connector,
            cloud_function_memory_mib=cloud_function_memory_mib,
        )

        # TODO: Move ibis logic to compiler step
        node = ibis.udf.scalar.builtin(
            func,
            name=rf_name,
            schema=f"{dataset_ref.project}.{dataset_ref.dataset_id}",
            signature=(ibis_signature.input_types, ibis_signature.output_type),
        )
        func.bigframes_cloud_function = (
            remote_function_client.get_cloud_function_fully_qualified_name(cf_name)
        )
        func.bigframes_remote_function = str(dataset_ref.routine(rf_name))  # type: ignore

        func.output_dtype = (
            bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(
                ibis_signature.output_type
            )
        )
        func.ibis_node = node
        return func

    return wrapper


def read_gbq_function(
    function_name: str,
    *,
    session: Session,
):
    """
    Read an existing BigQuery function and prepare it for use in future queries.
    """
    bigquery_client = session.bqclient
    ibis_client = session.ibis_client

    try:
        routine_ref = get_routine_reference(function_name, bigquery_client, session)
    except DatasetMissingError:
        raise ValueError(
            "Project and dataset must be provided, either directly or via session. "
            f"{constants.FEEDBACK_LINK}"
        )

    # Find the routine and get its arguments.
    try:
        routine = bigquery_client.get_routine(routine_ref)
    except google.api_core.exceptions.NotFound:
        raise ValueError(f"Unknown function '{routine_ref}'. {constants.FEEDBACK_LINK}")

    try:
        ibis_signature = ibis_signature_from_routine(routine)
    except ReturnTypeMissingError:
        raise ValueError(
            f"Function return type must be specified. {constants.FEEDBACK_LINK}"
        )
    except bigframes.core.compile.ibis_types.UnsupportedTypeError as e:
        raise ValueError(
            f"Type {e.type} not supported, supported types are {e.supported_types}. "
            f"{constants.FEEDBACK_LINK}"
        )

    # The name "args" conflicts with the Ibis operator, so we use
    # non-standard names for the arguments here.
    def func(*ignored_args, **ignored_kwargs):
        f"""Remote function {str(routine_ref)}."""
        nonlocal node  # type: ignore

        expr = node(*ignored_args, **ignored_kwargs)  # type: ignore
        return ibis_client.execute(expr)

    # TODO: Move ibis logic to compiler step

    func.__name__ = routine_ref.routine_id

    node = ibis.udf.scalar.builtin(
        func,
        name=routine_ref.routine_id,
        schema=f"{routine_ref.project}.{routine_ref.dataset_id}",
        signature=(ibis_signature.input_types, ibis_signature.output_type),
    )
    func.bigframes_remote_function = str(routine_ref)  # type: ignore
    func.output_dtype = bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(  # type: ignore
        ibis_signature.output_type
    )
    func.ibis_node = node  # type: ignore
    return func
