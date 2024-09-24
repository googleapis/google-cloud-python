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
import inspect
import sys
import threading
from typing import (
    Any,
    cast,
    Dict,
    Literal,
    Mapping,
    Optional,
    Sequence,
    TYPE_CHECKING,
    Union,
)
import warnings

import bigframes_vendored.constants as constants
import cloudpickle
import google.api_core.exceptions
from google.cloud import (
    bigquery,
    bigquery_connection_v1,
    functions_v2,
    resourcemanager_v3,
)

from bigframes import clients

if TYPE_CHECKING:
    from bigframes.session import Session

import bigframes_vendored.ibis.backends.bigquery.datatypes as third_party_ibis_bqtypes
import ibis
import pandas

from . import _remote_function_client as rf_client
from . import _utils


class RemoteFunctionSession:
    """Session to manage remote functions."""

    def __init__(self):
        # Session level mapping of remote function artifacts
        self._temp_artifacts: Dict[str, str] = dict()

        # Lock to synchronize the update of the session artifacts
        self._artifacts_lock = threading.Lock()

    def _update_temp_artifacts(self, bqrf_routine: str, gcf_path: str):
        """Update remote function artifacts in the current session."""
        with self._artifacts_lock:
            self._temp_artifacts[bqrf_routine] = gcf_path

    def clean_up(
        self,
        bqclient: bigquery.Client,
        gcfclient: functions_v2.FunctionServiceClient,
        session_id: str,
    ):
        """Delete remote function artifacts in the current session."""
        with self._artifacts_lock:
            for bqrf_routine, gcf_path in self._temp_artifacts.items():
                # Let's accept the possibility that the remote function may have
                # been deleted directly by the user
                bqclient.delete_routine(bqrf_routine, not_found_ok=True)

                # Let's accept the possibility that the cloud function may have
                # been deleted directly by the user
                try:
                    gcfclient.delete_function(name=gcf_path)
                except google.api_core.exceptions.NotFound:
                    pass

            self._temp_artifacts.clear()

    # Inspired by @udf decorator implemented in ibis-bigquery package
    # https://github.com/ibis-project/ibis-bigquery/blob/main/ibis_bigquery/udf/__init__.py
    # which has moved as @js to the ibis package
    # https://github.com/ibis-project/ibis/blob/master/ibis/backends/bigquery/udf/__init__.py
    def remote_function(
        self,
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
        cloud_function_ingress_settings: Literal[
            "all", "internal-only", "internal-and-gclb"
        ] = "all",
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
            dataset (str, Optional):
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
                Reuse the remote function if already exists.
                `True` by default, which will result in reusing an existing remote
                function and corresponding cloud function that was previously
                created (if any) for the same udf.
                Please note that for an unnamed (i.e. created without an explicit
                `name` argument) remote function, the BigQuery DataFrames
                session id is attached in the cloud artifacts names. So for the
                effective reuse across the sessions it is recommended to create
                the remote function with an explicit `name`.
                Setting it to `False` would force creating a unique remote function.
                If the required remote function does not exist then it would be
                created irrespective of this param.
            name (str, Optional):
                Explicit name of the persisted BigQuery remote function. Use it with
                caution, because two users working in the same project and dataset
                could overwrite each other's remote functions if they use the same
                persistent name. When an explicit name is provided, any session
                specific clean up (``bigframes.session.Session.close``/
                ``bigframes.pandas.close_session``/
                ``bigframes.pandas.reset_session``/
                ``bigframes.pandas.clean_up_by_session_id``) does not clean up
                the function, and leaves it for the user to manage the function
                and the associated cloud function directly.
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
            cloud_function_ingress_settings (str, Optional):
                Ingress settings controls dictating what traffic can reach the
                function. By default `all` will be used. It must be one of:
                `all`, `internal-only`, `internal-and-gclb`. See for more details
                https://cloud.google.com/functions/docs/networking/network-settings#ingress_settings.
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

        bq_location, cloud_function_region = _utils.get_remote_function_locations(
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

        bq_connection_manager = session.bqconnectionmanager

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
                signature_kwargs = {}  # type: ignore

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
                if (
                    output_type := signature.return_annotation
                ) is inspect.Signature.empty:
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
            ibis_signature = _utils.ibis_signature_from_python_signature(
                signature, input_types, output_type  # type: ignore
            )

            remote_function_client = rf_client.RemoteFunctionClient(
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

            # To respect the user code/environment let's use a copy of the
            # original udf, especially since we would be setting some properties
            # on it
            func = cloudpickle.loads(cloudpickle.dumps(func))

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
            try_delattr("input_dtypes")
            try_delattr("output_dtype")
            try_delattr("is_row_processor")
            try_delattr("ibis_node")

            (
                rf_name,
                cf_name,
                created_new,
            ) = remote_function_client.provision_bq_remote_function(
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
                cloud_function_ingress_settings=cloud_function_ingress_settings,
            )

            # TODO(shobs): Find a better way to support udfs with param named "name".
            # This causes an issue in the ibis compilation.
            func.__signature__ = inspect.signature(func).replace(  # type: ignore
                parameters=[
                    inspect.Parameter(
                        f"bigframes_{param.name}",
                        param.kind,
                    )
                    for param in inspect.signature(func).parameters.values()
                ]
            )

            # TODO: Move ibis logic to compiler step
            node = ibis.udf.scalar.builtin(
                func,
                name=rf_name,
                catalog=dataset_ref.project,
                database=dataset_ref.dataset_id,
                signature=(ibis_signature.input_types, ibis_signature.output_type),
            )
            func.bigframes_cloud_function = (
                remote_function_client.get_cloud_function_fully_qualified_name(cf_name)
            )
            func.bigframes_remote_function = (
                remote_function_client.get_remote_function_fully_qualilfied_name(
                    rf_name
                )
            )
            func.input_dtypes = tuple(
                [
                    bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(
                        input_type
                    )
                    for input_type in ibis_signature.input_types
                ]
            )
            func.output_dtype = (
                bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(
                    ibis_signature.output_type
                )
            )
            func.is_row_processor = is_row_processor
            func.ibis_node = node

            # If a new remote function was created, update the cloud artifacts
            # created in the session. This would be used to clean up any
            # resources in the session. Note that we need to do this only for
            # the case where an explicit name was not provided by the user and
            # we used an internal name. For the cases where the user provided an
            # explicit name, we are assuming that the user wants to persist them
            # with that name and would directly manage their lifecycle.
            if created_new and (not name):
                self._update_temp_artifacts(
                    func.bigframes_remote_function, func.bigframes_cloud_function
                )
            return func

        return wrapper
