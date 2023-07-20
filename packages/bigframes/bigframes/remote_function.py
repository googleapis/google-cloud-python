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
import time
import typing

if typing.TYPE_CHECKING:
    from bigframes.session import Session

import cloudpickle
import google.api_core.exceptions
from google.cloud import bigquery, bigquery_connection_v1, functions_v2
from ibis.backends.bigquery.compiler import compiles
from ibis.backends.bigquery.datatypes import BigQueryType
from ibis.expr.datatypes.core import dtype as python_type_to_bigquery_type
import ibis.expr.operations as ops
import ibis.expr.rules as rlz

# TODO(shobs): Change the min log level to INFO after the development stabilizes
# before June 2023
logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s][%(asctime)s][%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Protocol version 4 is available in python version 3.4 and above
# https://docs.python.org/3/library/pickle.html#data-stream-format
_pickle_protocol_version = 4

# Input and output python types supported by BigQuery DataFrames remote functions.
# TODO(shobs): Extend the support to all types supported by BQ remote functions
# https://cloud.google.com/bigquery/docs/remote-functions#limitations
_supported_io_types = set((bool, float, int, str))


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


def _get_hash(def_):
    "Get hash of a function."
    def_repr = cloudpickle.dumps(def_, protocol=_pickle_protocol_version)
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
        )


def get_cloud_function_name(def_, uniq_suffix=None):
    """Get the name of the cloud function."""
    cf_name = _get_hash(def_)
    cf_name = f"bigframes-{cf_name}"  # for identification
    if uniq_suffix:
        cf_name = f"{cf_name}-{uniq_suffix}"
    return cf_name


def get_remote_function_name(def_, uniq_suffix=None):
    """Get the name for the BQ remote function."""
    bq_rf_name = _get_hash(def_)
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
        bq_location,
        bq_dataset,
        bq_client,
        bq_connection_client,
        bq_connection_id,
    ):
        self._gcp_project_id = gcp_project_id
        self._cloud_function_region = cloud_function_region
        self._bq_location = bq_location
        self._bq_dataset = bq_dataset
        self._bq_client = bq_client
        self._bq_connection_client = bq_connection_client
        self._bq_connection_id = bq_connection_id

    def create_bq_remote_function(
        self, input_args, input_types, output_type, endpoint, bq_function_name
    ):
        """Create a BigQuery remote function given the artifacts of a user defined
        function and the http endpoint of a corresponding cloud function."""
        # TODO(shobs): The below command to enable BigQuery Connection API needs
        # to be automated. Disabling for now since most target users would not
        # have the privilege to enable API in a project.
        # log("Making sure BigQuery Connection API is enabled")
        # if os.system("gcloud services enable bigqueryconnection.googleapis.com"):
        #    raise ValueError("Failed to enable BigQuery Connection API")

        # If the intended connection does not exist then create it
        if self.check_bq_connection_exists():
            logger.info(f"Connector {self._bq_connection_id} already exists")
        else:
            connection_name, service_account_id = self.create_bq_connection()
            logger.info(
                f"Created BQ connection {connection_name} with service account id: {service_account_id}"
            )

            # Set up access on the newly created BQ connection
            # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#grant_permission_on_function
            # We would explicitly wait for 60+ seconds for the IAM binding to take effect
            command_iam = (
                f"gcloud projects add-iam-policy-binding {self._gcp_project_id}"
                + f' --member="serviceAccount:{service_account_id}"'
                + ' --role="roles/run.invoker"'
            )
            logger.info(f"Setting up IAM binding on the BQ connection: {command_iam}")
            _run_system_command(command_iam)

            logger.info(
                f"Waiting {self._iam_wait_seconds} seconds for IAM to take effect.."
            )
            time.sleep(self._iam_wait_seconds)

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
      endpoint = "{endpoint}"
    )"""
        logger.info(f"Creating BQ remote function: {create_function_ddl}")
        query_job = self._bq_client.query(create_function_ddl)  # Make an API request.
        query_job.result()  # Wait for the job to complete.
        logger.info(f"Created remote function {query_job.ddl_target_routine}")

    def get_remote_function_fully_qualified_name(self, name):
        "Get the fully qualilfied name for a BQ remote function."
        return "{}.{}.{}".format(self._gcp_project_id, self._bq_dataset, name)

    def get_cloud_function_fully_qualified_name(self, name):
        "Get the fully qualilfied name for a cloud function."
        return "projects/{}/locations/{}/functions/{}".format(
            self._gcp_project_id, self._cloud_function_region, name
        )

    def get_cloud_function_endpoint(self, name):
        """Get the http endpoint of a cloud function if it exists."""
        client = functions_v2.FunctionServiceClient()
        fully_qualified_name = self.get_cloud_function_fully_qualified_name(name)
        try:
            response = client.get_function(name=fully_qualified_name)
            return response.service_config.uri
        except google.api_core.exceptions.NotFound:
            pass
        return None

    def create_bq_connection(self):
        """Create the BigQuery Connection and returns corresponding service account id."""
        client = self._bq_connection_client
        connection = bigquery_connection_v1.Connection(
            cloud_resource=bigquery_connection_v1.CloudResourceProperties()
        )
        request = bigquery_connection_v1.CreateConnectionRequest(
            parent=client.common_location_path(self._gcp_project_id, self._bq_location),
            connection_id=self._bq_connection_id,
            connection=connection,
        )
        connection = client.create_connection(request)
        return connection.name, connection.cloud_resource.service_account_id

    def check_bq_connection_exists(self):
        """Check if the BigQuery Connection exists."""
        client = self._bq_connection_client
        request = bigquery_connection_v1.GetConnectionRequest(
            name=client.connection_path(
                self._gcp_project_id, self._bq_location, self._bq_connection_id
            )
        )

        try:
            client.get_connection(request=request)
            return True
        except google.api_core.exceptions.NotFound:
            pass
        return False

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
          print("[debug] received json request: " + str(request_json))
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

    def generate_cloud_function_code(self, def_, dir):
        """Generate the cloud function code for a given user defined function."""

        # requirements.txt
        requirements = ["cloudpickle >= 2.1.0"]
        requirements_txt = os.path.join(dir, "requirements.txt")
        with open(requirements_txt, "w") as f:
            f.write("\n".join(requirements))

        # main.py
        entry_point = self.generate_cloud_function_main_code(def_, dir)
        return entry_point

    def create_cloud_function(self, def_, cf_name):
        """Create a cloud function from the given user defined function."""

        # Build and deploy folder structure containing cloud function
        with tempfile.TemporaryDirectory() as dir:
            entry_point = self.generate_cloud_function_code(def_, dir)

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

            # deploy/redeploy the cloud function
            # TODO(shobs): Figure out a way to skip this step if a cloud function
            # already exists with the same name and source code
            command = (
                "gcloud functions deploy"
                + f" {cf_name} --gen2"
                + f" --runtime={python_version}"
                + f" --project={self._gcp_project_id}"
                + f" --region={self._cloud_function_region}"
                + f" --source={dir}"
                + f" --entry-point={entry_point}"
                + " --trigger-http"
            )

            # If the cloud function is being created for the first time, then let's
            # make it not allow unauthenticated calls. If it was previously created
            # then this invocation will update it, in which case do not touch that
            # aspect and let the previous policy hold. The reason we do this is to
            # avoid an IAM permission needed to update the invocation policy.
            # For example, when a cloud function is being created for the first
            # time, i.e.
            # $ gcloud functions deploy python-foo-http --gen2 --runtime=python310
            #       --region=us-central1
            #       --source=/source/code/dir
            #       --entry-point=foo_http
            #       --trigger-http
            #       --no-allow-unauthenticated
            # It works. When an invocation of the same command is done for the
            # second time, it may run into an error like:
            # ERROR: (gcloud.functions.deploy) PERMISSION_DENIED: Permission
            # 'run.services.setIamPolicy' denied on resource
            # 'projects/my_project/locations/us-central1/services/python-foo-http' (or resource may not exist)
            # But when --no-allow-unauthenticated is omitted then it goes through.
            # It suggests that in the second invocation the command is trying to set
            # the IAM policy of the service, and the user running BigQuery
            # DataFrame may not have privilege to do so, so better avoid this
            # if we can.
            if self.get_cloud_function_endpoint(cf_name):
                logger.info(f"Updating existing cloud function: {command}")
            else:
                command = f"{command} --no-allow-unauthenticated"
                logger.info(f"Creating new cloud function: {command}")

            _run_system_command(command)

        # Fetch the endpoint of the just created function
        endpoint = self.get_cloud_function_endpoint(cf_name)
        if not endpoint:
            raise ValueError("Couldn't fetch the http endpoint")

        logger.info(
            f"Successfully created cloud function {cf_name} with uri ({endpoint})"
        )
        return endpoint

    def provision_bq_remote_function(
        self, def_, input_types, output_type, uniq_suffix=None
    ):
        """Provision a BigQuery remote function."""
        # Derive the name of the underlying cloud function and first create
        # it if it does not exist
        cloud_function_name = get_cloud_function_name(def_, uniq_suffix)
        cf_endpoint = self.get_cloud_function_endpoint(cloud_function_name)
        if not cf_endpoint:
            self.check_cloud_function_tools_and_permissions()
            cf_endpoint = self.create_cloud_function(def_, cloud_function_name)
        else:
            logger.info(f"Cloud function {cloud_function_name} already exists.")

        # Derive the name of the remote function and create/replace it if needed
        remote_function_name = get_remote_function_name(def_, uniq_suffix)
        rf_endpoint, rf_conn = self.get_remote_function_specs(remote_function_name)
        if rf_endpoint != cf_endpoint or rf_conn != self._bq_connection_id:
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
        return (http_endpoint, bq_connection)

    def check_cloud_function_tools_and_permissions(self):
        """Check if the necessary tools and permissions are in place for creating remote function"""
        # gcloud CLI comes with bq CLI and they are required for creating google
        # cloud function and BigQuery remote function respectively
        if not shutil.which("gcloud"):
            raise ValueError(
                "gcloud tool not installed, install it from https://cloud.google.com/sdk/docs/install"
            )

        # TODO(shobs): Check for permissions too
        # I (shobs) tried the following method
        # $ gcloud asset search-all-iam-policies \
        #   --format=json \
        #   --scope=projects/{gcp_project_id} \
        #   --query='policy.role.permissions:cloudfunctions.functions.create'
        # as a proxy to all the privilges necessary to create cloud function
        # https://cloud.google.com/functions/docs/reference/iam/roles#cloudfunctions.developer
        # but that itself required the runner to have the permission to enable
        # `cloudasset.googleapis.com`


# Inspired by @udf decorator implemented in ibis-bigquery package
# https://github.com/ibis-project/ibis-bigquery/blob/main/ibis_bigquery/udf/__init__.py
# which has moved as @js to the ibis package
# https://github.com/ibis-project/ibis/blob/master/ibis/backends/bigquery/udf/__init__.py
def remote_function(
    input_types: typing.Sequence[type],
    output_type: type,
    session: typing.Optional[Session] = None,
    bigquery_client: typing.Optional[bigquery.Client] = None,
    bigquery_connection_client: typing.Optional[
        bigquery_connection_v1.ConnectionServiceClient
    ] = None,
    dataset: typing.Optional[str] = None,
    bigquery_connection: typing.Optional[str] = None,
    reuse: bool = True,
):
    """Decorator to turn a user defined function into a BigQuery remote function.

    .. deprecated:: 0.0.1
       Use :func:`bigframes.pandas.remote_function` instead.

    Args:
        input_types : list(type).
            List of input data types in the user defined function.
        output_type : type.
            Data type of the output in the user defined function.
        session : bigframes.Session, Optional
            BigQuery DataFrames session to use for getting default project,
            dataset and BigQuery connection.
        bigquery_client : google.cloud.bigquery.Client, Optional
            Client to use for BigQuery operations. If this param is not provided
            then bigquery client from the session would be used.
        bigquery_connection_client : google.cloud.bigquery_connection_v1.ConnectionServiceClient, Optional
            Client to use for BigQuery connection operations. If this param is
            not provided then bigquery connection client from the session would
            be used.
        dataset : str, Optional.
            Dataset to use to create a BigQuery function. It should be in
            `<project_id>.<dataset_name>` or `<dataset_name>` format. If this
            param is not provided then session dataset id would be used.
        bigquery_connection : str, Optional.
            Name of the BigQuery connection. If this param is not provided then
            the bigquery connection from the session would be used. If it is pre
            created in the same location as the `bigquery_client.location` then
            it would be used, otherwise it would be created dynamically using
            the `bigquery_connection_client` assuming the user has necessary
            priviliges.
        reuse : bool, Optional.
            Reuse the remote function if already exists.
            `True` by default, which will result in reusing an existing remote
            function (if any) that was previously created for the same udf.
            Setting it to false would force creating a unique remote function.
            If the required remote function does not exist then it would be
            created irrespective of this param.

    Notes:
        Please make sure following is setup before using this API:

        1. Have the below APIs enabled for your project:
              a. BigQuery Connection API
              b. Cloud Functions API
              c. Cloud Run API
              d. Cloud Build API
              e. Artifact Registry API
              f. Cloud Resource Manager API

           This can be done from the cloud console (change PROJECT_ID to yours):
              https://console.cloud.google.com/apis/enableflow?apiid=bigqueryconnection.googleapis.com,cloudfunctions.googleapis.com,run.googleapis.com,cloudbuild.googleapis.com,artifactregistry.googleapis.com,cloudresourcemanager.googleapis.com&project=PROJECT_ID
           Or from the gcloud CLI:
              $ gcloud services enable bigqueryconnection.googleapis.com cloudfunctions.googleapis.com run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com cloudresourcemanager.googleapis.com

        2. Have following IAM roles enabled for you:
              a. BigQuery Data Editor (roles/bigquery.dataEditor)
              b. BigQuery Connection Admin (roles/bigquery.connectionAdmin)
              c. Cloud Functions Developer (roles/cloudfunctions.developer)
              d. Service Account User (roles/iam.serviceAccountUser)
              e. Storage Object Viewer (roles/storage.objectViewer)
              f. Project IAM Admin (roles/resourcemanager.projectIamAdmin)
                 (Only required if the bigquery connection being used is not pre-created and is created dynamically with user credentials.)

        3. Either the user has setIamPolicy privilege on the project, or a BigQuery connection is pre-created with necessary IAM role set:
              a. To create a connection, follow https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#create_a_connection
              b. To set up IAM, follow https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#grant_permission_on_function
           Alternatively, the IAM could also be setup via the gcloud CLI:
              $ gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:CONNECTION_SERVICE_ACCOUNT_ID" --role="roles/run.invoker"

    """

    # A BigQuery client is required to perform BQ operations
    if not bigquery_client:
        if session:
            bigquery_client = session.bqclient
    if not bigquery_client:
        raise ValueError(
            "A bigquery client must be provided, either directly or via session"
        )

    # A BigQuery connection client is required to perform BQ connection operations
    if not bigquery_connection_client:
        if session:
            bigquery_connection_client = session.bqconnectionclient
    if not bigquery_connection_client:
        raise ValueError(
            "A bigquery connection client must be provided, either directly or via session"
        )

    # BQ remote function must be persisted, for which we need a dataset
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#:~:text=You%20cannot%20create%20temporary%20remote%20functions.
    if dataset:
        dataset_ref = bigquery.DatasetReference.from_string(
            dataset, default_project=bigquery_client.project
        )
        gcp_project_id = dataset_ref.project
        bq_dataset = dataset_ref.dataset_id
    else:
        gcp_project_id = bigquery_client.project
        if session:
            bq_dataset = session._session_dataset_id
    if not gcp_project_id:
        raise ValueError("Project must be provided, either directly or via session")
    if not bq_dataset:
        raise ValueError("Dataset must be provided, either directly or via session")

    bq_location, cloud_function_region = get_remote_function_locations(
        bigquery_client.location
    )

    # A connection is required for BQ remote function
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#create_a_remote_function
    if not bigquery_connection and session:
        bigquery_connection = session._remote_udf_connection  # type: ignore
    if not bigquery_connection:
        raise ValueError(
            "BigQuery connection must be provided, either directly or via session"
        )

    uniq_suffix = None
    if not reuse:
        uniq_suffix = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=8)
        )

    def wrapper(f):
        if not callable(f):
            raise TypeError("f must be callable, got {}".format(f))

        signature = inspect.signature(f)
        parameter_names = signature.parameters.keys()

        # Check supported python datatypes and convert to ibis datatypes
        type_error_message_format = (
            "type {{}} not supported, supported types are {}.".format(
                ", ".join([type_.__name__ for type_ in _supported_io_types])
            )
        )
        for type_ in input_types:
            assert type_ in _supported_io_types, type_error_message_format.format(type_)
        assert output_type in _supported_io_types, type_error_message_format.format(
            output_type
        )
        input_types_ibis = [
            python_type_to_bigquery_type(type_) for type_ in input_types
        ]
        output_type_ibis = python_type_to_bigquery_type(output_type)

        rf_node_fields = {
            name: rlz.value(type)
            for name, type in zip(parameter_names, input_types_ibis)
        }

        try:
            rf_node_fields["output_type"] = rlz.shape_like(
                "args", dtype=output_type_ibis
            )
        except TypeError:
            rf_node_fields["output_dtype"] = property(lambda _: output_type_ibis)
            rf_node_fields["output_shape"] = rlz.shape_like("args")

        remote_function_client = RemoteFunctionClient(
            gcp_project_id,
            cloud_function_region,
            bq_location,
            bq_dataset,
            bigquery_client,
            bigquery_connection_client,
            bigquery_connection,
        )
        rf_name, cf_name = remote_function_client.provision_bq_remote_function(
            f, input_types_ibis, output_type_ibis, uniq_suffix
        )
        rf_fully_qualified_name = f"`{gcp_project_id}.{bq_dataset}`.{rf_name}"
        rf_node = type(rf_fully_qualified_name, (ops.ValueOp,), rf_node_fields)

        @compiles(rf_node)
        def compiles_rf_node(t, op):
            return "{}({})".format(
                rf_node.__name__, ", ".join(map(t.translate, op.args))
            )

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            node = rf_node(*args, **kwargs)
            return node.to_expr()

        wrapped.__signature__ = signature
        wrapped.bigframes_remote_function = (
            remote_function_client.get_remote_function_fully_qualified_name(rf_name)
        )
        wrapped.bigframes_cloud_function = (
            remote_function_client.get_cloud_function_fully_qualified_name(cf_name)
        )
        return wrapped

    return wrapper
