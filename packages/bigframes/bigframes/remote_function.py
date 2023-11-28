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

import functools
import hashlib
import inspect
import logging
import os
import random
import shutil
import string
import subprocess
import sys
import tempfile
import textwrap
from typing import List, NamedTuple, Optional, Sequence, TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from bigframes.session import Session

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
from ibis.backends.bigquery.compiler import compiles
from ibis.backends.bigquery.datatypes import BigQueryType
from ibis.expr.datatypes.core import DataType as IbisDataType
from ibis.expr.datatypes.core import dtype as python_type_to_bigquery_type
import ibis.expr.operations as ops
import ibis.expr.rules as rlz

from bigframes import clients
import bigframes.constants as constants

logger = logging.getLogger(__name__)

# Protocol version 4 is available in python version 3.4 and above
# https://docs.python.org/3/library/pickle.html#data-stream-format
_pickle_protocol_version = 4

# Input and output types supported by BigQuery DataFrames remote functions.
# TODO(shobs): Extend the support to all types supported by BQ remote functions
# https://cloud.google.com/bigquery/docs/remote-functions#limitations
SUPPORTED_IO_PYTHON_TYPES = {bool, float, int, str}
SUPPORTED_IO_BIGQUERY_TYPEKINDS = {
    "BOOLEAN",
    "BOOL",
    "FLOAT",
    "FLOAT64",
    "INT64",
    "INTEGER",
    "STRING",
}


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


def _run_system_command(command):
    program = subprocess.Popen(
        [command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = program.communicate()
    exit_code = program.wait()
    if exit_code:
        raise RuntimeError(
            f"Command: {command}\nOutput: {stdout.decode()}\nError: {stderr.decode()}"
            f"{constants.FEEDBACK_LINK}"
        )


def routine_ref_to_string_for_query(routine_ref: bigquery.RoutineReference) -> str:
    return f"`{routine_ref.project}.{routine_ref.dataset_id}`.{routine_ref.routine_id}"


class IbisSignature(NamedTuple):
    parameter_names: List[str]
    input_types: List[Optional[IbisDataType]]
    output_type: IbisDataType


def get_cloud_function_name(def_, uniq_suffix=None, package_requirements=None):
    "Get a name for the cloud function for the given user defined function."
    cf_name = _get_hash(def_, package_requirements)
    cf_name = f"bigframes-{cf_name}"  # for identification
    if uniq_suffix:
        cf_name = f"{cf_name}-{uniq_suffix}"
    return cf_name


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
        bq_connection_client,
        bq_connection_id,
        cloud_resource_manager_client,
    ):
        self._gcp_project_id = gcp_project_id
        self._cloud_function_region = cloud_function_region
        self._cloud_functions_client = cloud_functions_client
        self._bq_location = bq_location
        self._bq_dataset = bq_dataset
        self._bq_client = bq_client
        self._bq_connection_id = bq_connection_id
        self._bq_connection_manager = clients.BqConnectionManager(
            bq_connection_client, cloud_resource_manager_client
        )

    def create_bq_remote_function(
        self, input_args, input_types, output_type, endpoint, bq_function_name
    ):
        """Create a BigQuery remote function given the artifacts of a user defined
        function and the http endpoint of a corresponding cloud function."""
        self._bq_connection_manager.create_bq_connection(
            self._gcp_project_id,
            self._bq_location,
            self._bq_connection_id,
            "run.invoker",
        )

        # Create BQ function
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#create_a_remote_function_2
        bq_function_args = []
        bq_function_return_type = BigQueryType.from_ibis(output_type)

        # We are expecting the input type annotations to be 1:1 with the input args
        for idx, name in enumerate(input_args):
            bq_function_args.append(
                f"{name} {BigQueryType.from_ibis(input_types[idx])}"
            )
        create_function_ddl = f"""
            CREATE OR REPLACE FUNCTION `{self._gcp_project_id}.{self._bq_dataset}`.{bq_function_name}({','.join(bq_function_args)})
            RETURNS {bq_function_return_type}
            REMOTE WITH CONNECTION `{self._gcp_project_id}.{self._bq_location}.{self._bq_connection_id}`
            OPTIONS (
              endpoint = "{endpoint}",
              max_batching_rows = 1000
            )"""

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

        # TODO: Use session._start_query() so we get progress bar
        query_job = self._bq_client.query(create_function_ddl)  # Make an API request.
        query_job.result()  # Wait for the job to complete.

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

    def generate_udf_code(self, def_, dir):
        """Generate serialized bytecode using cloudpickle given a udf."""
        udf_code_file_name = "udf.py"
        udf_bytecode_file_name = "udf.cloudpickle"

        # original code, only for debugging purpose
        udf_code = textwrap.dedent(inspect.getsource(def_))
        udf_code_file_path = os.path.join(dir, udf_code_file_name)
        with open(udf_code_file_path, "w") as f:
            f.write(udf_code)

        # serialized bytecode
        udf_bytecode_file_path = os.path.join(dir, udf_bytecode_file_name)
        with open(udf_bytecode_file_path, "wb") as f:
            cloudpickle.dump(def_, f, protocol=_pickle_protocol_version)

        return udf_code_file_name, udf_bytecode_file_name

    def generate_cloud_function_main_code(self, def_, dir):
        """Get main.py code for the cloud function for the given user defined function."""

        # Pickle the udf with all its dependencies
        udf_code_file, udf_bytecode_file = self.generate_udf_code(def_, dir)
        handler_func_name = "udf_http"

        # We want to build a cloud function that works for BQ remote functions,
        # where we receive `calls` in json which is a batch of rows from BQ SQL.
        # The number and the order of values in each row is expected to exactly
        # match to the number and order of arguments in the udf , e.g. if the udf is
        #   def foo(x: int, y: str):
        #     ...
        # then the http request body could look like
        # {
        #   ...
        #   "calls" : [
        #     [123, "hello"],
        #     [456, "world"]
        #   ]
        #   ...
        # }
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#input_format
        code_template = textwrap.dedent(
            """\
        import cloudpickle
        import json

        # original udf code is in {udf_code_file}
        # serialized udf code is in {udf_bytecode_file}
        with open("{udf_bytecode_file}", "rb") as f:
          udf = cloudpickle.load(f)

        def {handler_func_name}(request):
          request_json = request.get_json(silent=True)
          calls = request_json["calls"]
          replies = []
          for call in calls:
            reply = udf(*call)
            replies.append(reply)
          return_json = json.dumps({{"replies" : replies}})
          return return_json
        """
        )

        code = code_template.format(
            udf_code_file=udf_code_file,
            udf_bytecode_file=udf_bytecode_file,
            handler_func_name=handler_func_name,
        )

        main_py = os.path.join(dir, "main.py")
        with open(main_py, "w") as f:
            f.write(code)
        logger.debug(f"Wrote {os.path.abspath(main_py)}:\n{open(main_py).read()}")

        return handler_func_name

    def generate_cloud_function_code(self, def_, dir, package_requirements=None):
        """Generate the cloud function code for a given user defined function."""

        # requirements.txt
        requirements = ["cloudpickle >= 2.1.0"]
        if package_requirements:
            requirements.extend(package_requirements)
        requirements = sorted(requirements)
        requirements_txt = os.path.join(dir, "requirements.txt")
        with open(requirements_txt, "w") as f:
            f.write("\n".join(requirements))

        # main.py
        entry_point = self.generate_cloud_function_main_code(def_, dir)
        return entry_point

    def create_cloud_function(self, def_, cf_name, package_requirements=None):
        """Create a cloud function from the given user defined function."""

        # Build and deploy folder structure containing cloud function
        with tempfile.TemporaryDirectory() as dir:
            entry_point = self.generate_cloud_function_code(
                def_, dir, package_requirements
            )
            archive_path = shutil.make_archive(dir, "zip", dir)

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
            upload_url_request = functions_v2.GenerateUploadUrlRequest()
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
            function.service_config = functions_v2.ServiceConfig()
            function.service_config.available_memory = "1024M"
            function.service_config.timeout_seconds = 600
            create_function_request.function = function

            # Create the cloud function and wait for it to be ready to use
            operation = self._cloud_functions_client.create_function(
                request=create_function_request
            )
            operation.result()

            # Cleanup
            os.remove(archive_path)

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
        # remote function
        cloud_function_name = get_cloud_function_name(
            def_, uniq_suffix, package_requirements
        )
        cf_endpoint = self.get_cloud_function_endpoint(cloud_function_name)

        # Create the cloud function if it does not exist
        if not cf_endpoint:
            cf_endpoint = self.create_cloud_function(
                def_, cloud_function_name, package_requirements
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
                input_args, input_types, output_type, cf_endpoint, remote_function_name
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


def remote_function_node(
    routine_ref: bigquery.RoutineReference, ibis_signature: IbisSignature
):
    """Creates an Ibis node representing a remote function call."""

    fields = {
        name: rlz.value(type_) if type_ else rlz.any
        for name, type_ in zip(
            ibis_signature.parameter_names, ibis_signature.input_types
        )
    }

    try:
        fields["output_type"] = rlz.shape_like("args", dtype=ibis_signature.output_type)  # type: ignore
    except TypeError:
        fields["output_dtype"] = property(lambda _: ibis_signature.output_type)
        fields["output_shape"] = rlz.shape_like("args")

    node = type(routine_ref_to_string_for_query(routine_ref), (ops.ValueOp,), fields)  # type: ignore

    @compiles(node)
    def compile_node(t, op):
        return "{}({})".format(node.__name__, ", ".join(map(t.translate, op.args)))

    def f(*args, **kwargs):
        return node(*args, **kwargs).to_expr()

    f.bigframes_remote_function = str(routine_ref)  # type: ignore

    return f


class UnsupportedTypeError(ValueError):
    def __init__(self, type_, supported_types):
        self.type = type_
        self.supported_types = supported_types


def ibis_type_from_python_type(t: type) -> IbisDataType:
    if t not in SUPPORTED_IO_PYTHON_TYPES:
        raise UnsupportedTypeError(t, SUPPORTED_IO_PYTHON_TYPES)
    return python_type_to_bigquery_type(t)


def ibis_type_from_type_kind(tk: bigquery.StandardSqlTypeNames) -> IbisDataType:
    if tk not in SUPPORTED_IO_BIGQUERY_TYPEKINDS:
        raise UnsupportedTypeError(tk, SUPPORTED_IO_BIGQUERY_TYPEKINDS)
    return BigQueryType.to_ibis(tk)


def ibis_signature_from_python_signature(
    signature: inspect.Signature,
    input_types: Sequence[type],
    output_type: type,
) -> IbisSignature:
    return IbisSignature(
        parameter_names=list(signature.parameters.keys()),
        input_types=[ibis_type_from_python_type(t) for t in input_types],
        output_type=ibis_type_from_python_type(output_type),
    )


class ReturnTypeMissingError(ValueError):
    pass


def ibis_signature_from_routine(routine: bigquery.Routine) -> IbisSignature:
    if not routine.return_type:
        raise ReturnTypeMissingError

    return IbisSignature(
        parameter_names=[arg.name for arg in routine.arguments],
        input_types=[
            ibis_type_from_type_kind(arg.data_type.type_kind) if arg.data_type else None
            for arg in routine.arguments
        ],
        output_type=ibis_type_from_type_kind(routine.return_type.type_kind),
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
    input_types: Sequence[type],
    output_type: type,
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
        input_types list(type):
            List of input data types in the user defined function.
        output_type type:
            Data type of the output in the user defined function.
        session (bigframes.Session, Optional):
            BigQuery DataFrames session to use for getting default project,
            dataset and BigQuery connection.
        bigquery_client (google.cloud.bigquery.Client, Optional):
            Client to use for BigQuery operations. If this param is not provided
            then bigquery client from the session would be used.
        bigquery_connection_client (google.cloud.bigquery_connection_v1.ConnectionServiceClient, Optional):
            Client to use for cloud functions operations. If this param is not
            provided then functions client from the session would be used.
        cloud_functions_client (google.cloud.functions_v2.FunctionServiceClient, Optional):
            Client to use for BigQuery connection operations. If this param is
            not provided then bigquery connection client from the session would
            be used.
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

    """
    import bigframes.pandas as bpd

    session = session or bpd.get_global_session()

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

    bigquery_connection = clients.BqConnectionManager.resolve_full_connection_name(
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

    def wrapper(f):
        if not callable(f):
            raise TypeError("f must be callable, got {}".format(f))

        signature = inspect.signature(f)
        ibis_signature = ibis_signature_from_python_signature(
            signature, input_types, output_type
        )

        remote_function_client = RemoteFunctionClient(
            dataset_ref.project,
            cloud_function_region,
            cloud_functions_client,
            bq_location,
            dataset_ref.dataset_id,
            bigquery_client,
            bigquery_connection_client,
            bq_connection_id,
            resource_manager_client,
        )

        rf_name, cf_name = remote_function_client.provision_bq_remote_function(
            f,
            ibis_signature.input_types,
            ibis_signature.output_type,
            reuse,
            name,
            packages,
        )

        node = remote_function_node(dataset_ref.routine(rf_name), ibis_signature)

        node = functools.wraps(f)(node)
        node.__signature__ = signature
        node.bigframes_cloud_function = (
            remote_function_client.get_cloud_function_fully_qualified_name(cf_name)
        )

        return node

    return wrapper


def read_gbq_function(
    function_name: str,
    session: Optional[Session] = None,
    bigquery_client: Optional[bigquery.Client] = None,
):
    """
    Read an existing BigQuery function and prepare it for use in future queries.
    """

    # A BigQuery client is required to perform BQ operations
    if not bigquery_client and session:
        bigquery_client = session.bqclient
    if not bigquery_client:
        raise ValueError(
            "A bigquery client must be provided, either directly or via session. "
            f"{constants.FEEDBACK_LINK}"
        )

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
            "Function return type must be specified. {constants.FEEDBACK_LINK}"
        )
    except UnsupportedTypeError as e:
        raise ValueError(
            f"Type {e.type} not supported, supported types are {e.supported_types}. "
            f"{constants.FEEDBACK_LINK}"
        )

    return remote_function_node(routine_ref, ibis_signature)
