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
import functools
import inspect
import sys
import threading
from typing import (
    Any,
    cast,
    Dict,
    get_origin,
    Literal,
    Mapping,
    Optional,
    Sequence,
    TYPE_CHECKING,
    Union,
)
import warnings

import google.api_core.exceptions
from google.cloud import (
    bigquery,
    bigquery_connection_v1,
    functions_v2,
    resourcemanager_v3,
)

from bigframes import clients
import bigframes.exceptions as bfe
import bigframes.formatting_helpers as bf_formatting
from bigframes.functions import function as bq_functions
from bigframes.functions import udf_def

if TYPE_CHECKING:
    from bigframes.session import Session

import pandas

from bigframes.functions import _function_client, _utils


class FunctionSession:
    """Session to manage bigframes functions."""

    def __init__(self):
        # Session level mapping of function artifacts
        self._temp_artifacts: Dict[str, str] = dict()

        # Lock to synchronize the update of the session artifacts
        self._artifacts_lock = threading.Lock()

    def _resolve_session(self, session: Optional[Session]) -> Session:
        """Resolves the BigFrames session."""
        import bigframes.pandas as bpd
        import bigframes.session

        # Using the global session if none is provided.
        return cast(bigframes.session.Session, session or bpd.get_global_session())

    def _resolve_bigquery_client(
        self, session: Session, bigquery_client: Optional[bigquery.Client]
    ) -> bigquery.Client:
        """Resolves the BigQuery client."""
        if not bigquery_client:
            bigquery_client = session.bqclient
        if not bigquery_client:
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "A bigquery client must be provided, either directly or via "
                "session.",
            )
        return bigquery_client

    def _resolve_bigquery_connection_client(
        self,
        session: Session,
        bigquery_connection_client: Optional[
            bigquery_connection_v1.ConnectionServiceClient
        ],
    ) -> bigquery_connection_v1.ConnectionServiceClient:
        """Resolves the BigQuery connection client."""
        if not bigquery_connection_client:
            bigquery_connection_client = session.bqconnectionclient
        if not bigquery_connection_client:
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "A bigquery connection client must be provided, either "
                "directly or via session.",
            )
        return bigquery_connection_client

    def _resolve_resource_manager_client(
        self,
        session: Session,
        resource_manager_client: Optional[resourcemanager_v3.ProjectsClient],
    ) -> resourcemanager_v3.ProjectsClient:
        """Resolves the resource manager client."""
        if not resource_manager_client:
            resource_manager_client = session.resourcemanagerclient
        if not resource_manager_client:
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "A resource manager client must be provided, either directly "
                "or via session.",
            )
        return resource_manager_client

    def _resolve_dataset_reference(
        self,
        session: Session,
        bigquery_client: bigquery.Client,
        dataset: Optional[str],
    ) -> bigquery.DatasetReference:
        """Resolves the dataset reference for the bigframes function."""
        if dataset:
            dataset_ref = bigquery.DatasetReference.from_string(
                dataset, default_project=bigquery_client.project
            )
        else:
            dataset_ref = session._anonymous_dataset
        return dataset_ref

    def _resolve_cloud_functions_client(
        self,
        session: Session,
        cloud_functions_client: Optional[functions_v2.FunctionServiceClient],
    ) -> Optional[functions_v2.FunctionServiceClient]:
        """Resolves the Cloud Functions client."""
        if not cloud_functions_client:
            cloud_functions_client = session.cloudfunctionsclient
        if not cloud_functions_client:
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "A cloud functions client must be provided, either directly "
                "or via session.",
            )
        return cloud_functions_client

    def _resolve_bigquery_connection_id(
        self,
        session: Session,
        dataset_ref: bigquery.DatasetReference,
        bq_location: str,
        bigquery_connection: Optional[str] = None,
    ) -> str:
        """Resolves BigQuery connection id."""
        if not bigquery_connection:
            bigquery_connection = session._bq_connection  # type: ignore

        bigquery_connection = clients.get_canonical_bq_connection_id(
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
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "The project_id does not match BigQuery connection "
                f"gcp_project_id: {dataset_ref.project}.",
            )
        if bq_connection_location.casefold() != bq_location.casefold():
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "The location does not match BigQuery connection location: "
                f"{bq_location}.",
            )
        return bq_connection_id

    def _update_temp_artifacts(self, bqrf_routine: str, gcf_path: str):
        """Update function artifacts in the current session."""
        with self._artifacts_lock:
            self._temp_artifacts[bqrf_routine] = gcf_path

    def clean_up(
        self,
        bqclient: bigquery.Client,
        gcfclient: functions_v2.FunctionServiceClient,
        session_id: str,
    ):
        """Delete function artifacts in the current session."""
        with self._artifacts_lock:
            for bqrf_routine, gcf_path in self._temp_artifacts.items():
                # Let's accept the possibility that the function may have been
                # deleted directly by the user
                bqclient.delete_routine(bqrf_routine, not_found_ok=True)

                if gcf_path:
                    # Let's accept the possibility that the cloud function may
                    # have been deleted directly by the user
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
        *,
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
        cloud_function_service_account: str,
        cloud_function_kms_key_name: Optional[str] = None,
        cloud_function_docker_repository: Optional[str] = None,
        max_batching_rows: Optional[int] = 1000,
        cloud_function_timeout: Optional[int] = 600,
        cloud_function_max_instances: Optional[int] = None,
        cloud_function_vpc_connector: Optional[str] = None,
        cloud_function_memory_mib: Optional[int] = 1024,
        cloud_function_ingress_settings: Literal[
            "all", "internal-only", "internal-and-gclb"
        ] = "internal-only",
        cloud_build_service_account: Optional[str] = None,
    ):
        """Decorator to turn a user defined function into a BigQuery remote function.

        .. deprecated:: 0.0.1
        This is an internal method. Please use :func:`bigframes.pandas.remote_function` instead.

        .. warning::
            To use remote functions with Bigframes 2.0 and onwards, please (preferred)
            set an explicit user-managed ``cloud_function_service_account`` or (discouraged)
            set ``cloud_function_service_account`` to use the Compute Engine service account
            by setting it to `"default"`.
            See, https://cloud.google.com/functions/docs/securing/function-identity.

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
            input_types (type or sequence(type), Optional):
                For scalar user defined function it should be the input type or
                sequence of input types. The supported scalar input types are
                `bool`, `bytes`, `float`, `int`, `str`. For row processing user
                defined function (i.e. functions that receive a single input
                representing a row in form of a Series), type `Series` should be
                specified.
            output_type (type, Optional):
                Data type of the output in the user defined function. If the
                user defined function returns an array, then `list[type]` should
                be specified. The supported output types are `bool`, `bytes`,
                `float`, `int`, `str`, `list[bool]`, `list[float]`, `list[int]`
                and `list[str]`.
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
            cloud_function_service_account (str):
                Service account to use for the cloud functions. If "default" provided then
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
                function. Options are: `all`, `internal-only`, or `internal-and-gclb`.
                If no setting is provided, `internal-only` will be used by default.
                See for more details
                https://cloud.google.com/functions/docs/networking/network-settings#ingress_settings.
            cloud_build_service_account (str, Optional):
                Service account in the fully qualified format
                `projects/PROJECT_ID/serviceAccounts/SERVICE_ACCOUNT_EMAIL`, or
                just the SERVICE_ACCOUNT_EMAIL. The latter would be interpreted
                as belonging to the BigQuery DataFrames session project. This is
                to be used by Cloud Build to build the function source code into
                a deployable artifact. If not provided, the default Cloud Build
                service account is used. See
                https://cloud.google.com/build/docs/cloud-build-service-account
                for more details.
        """
        # Some defaults may be used from the session if not provided otherwise.
        session = self._resolve_session(session)

        # If the user forces the cloud function service argument to None, throw
        # an exception
        if cloud_function_service_account is None:
            raise ValueError(
                'You must provide a user managed cloud_function_service_account, or "default" if you would like to let the default service account be used.'
            )

        # A BigQuery client is required to perform BQ operations.
        bigquery_client = self._resolve_bigquery_client(session, bigquery_client)

        # A BigQuery connection client is required for BQ connection operations.
        bigquery_connection_client = self._resolve_bigquery_connection_client(
            session, bigquery_connection_client
        )

        # A resource manager client is required to get/set IAM operations.
        resource_manager_client = self._resolve_resource_manager_client(
            session, resource_manager_client
        )

        # BQ remote function must be persisted, for which we need a dataset.
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#:~:text=You%20cannot%20create%20temporary%20remote%20functions.
        dataset_ref = self._resolve_dataset_reference(session, bigquery_client, dataset)

        # A cloud functions client is required for cloud functions operations.
        cloud_functions_client = self._resolve_cloud_functions_client(
            session, cloud_functions_client
        )

        bq_location, cloud_function_region = _utils.get_remote_function_locations(
            bigquery_client.location
        )

        # A connection is required for BQ remote function.
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#create_a_remote_function
        bq_connection_id = self._resolve_bigquery_connection_id(
            session, dataset_ref, bq_location, bigquery_connection
        )

        # If any CMEK is intended then check that a docker repository is also specified.
        if (
            cloud_function_kms_key_name is not None
            and cloud_function_docker_repository is None
        ):
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "cloud_function_docker_repository must be specified with cloud_function_kms_key_name."
                " For more details see https://cloud.google.com/functions/docs/securing/cmek#before_you_begin.",
            )

        if cloud_function_ingress_settings is None:
            cloud_function_ingress_settings = "internal-only"
            msg = bfe.format_message(
                "The `cloud_function_ingress_settings` is being set to 'internal-only' by default."
            )
            warnings.warn(msg, category=UserWarning, stacklevel=2)

        bq_connection_manager = session.bqconnectionmanager

        def wrapper(func):
            nonlocal input_types, output_type

            if not callable(func):
                raise bf_formatting.create_exception_with_feedback_link(
                    TypeError, f"func must be a callable, got {func}"
                )

            if sys.version_info >= (3, 10):
                # Add `eval_str = True` so that deferred annotations are turned into their
                # corresponding type objects. Need Python 3.10 for eval_str parameter.
                # https://docs.python.org/3/library/inspect.html#inspect.signature
                signature_kwargs: Mapping[str, Any] = {"eval_str": True}
            else:
                signature_kwargs = {}  # type: ignore

            py_sig = inspect.signature(
                func,
                **signature_kwargs,
            )
            if input_types is not None:
                if not isinstance(input_types, collections.abc.Sequence):
                    input_types = [input_types]
                py_sig = py_sig.replace(
                    parameters=[
                        par.replace(annotation=itype)
                        for par, itype in zip(py_sig.parameters.values(), input_types)
                    ]
                )
            if output_type:
                py_sig = py_sig.replace(return_annotation=output_type)

            # Try to get input types via type annotations.

            # The function will actually be receiving a pandas Series, but allow both
            # BigQuery DataFrames and pandas object types for compatibility.
            # The function will actually be receiving a pandas Series, but allow
            # both BigQuery DataFrames and pandas object types for compatibility.
            is_row_processor = False
            if new_sig := _convert_row_processor_sig(py_sig):
                py_sig = new_sig
                is_row_processor = True

            remote_function_client = _function_client.FunctionClient(
                dataset_ref.project,
                bq_location,
                dataset_ref.dataset_id,
                bigquery_client,
                bq_connection_id,
                bq_connection_manager,
                cloud_function_region,
                cloud_functions_client,
                None
                if cloud_function_service_account == "default"
                else cloud_function_service_account,
                cloud_function_kms_key_name,
                cloud_function_docker_repository,
                cloud_build_service_account=cloud_build_service_account,
                session=session,  # type: ignore
            )

            # resolve the output type that can be supported in the bigframes,
            # ibis, BQ remote functions and cloud functions integration.
            bqrf_metadata = None
            post_process_routine = None
            if get_origin(py_sig.return_annotation) is list:
                # TODO(b/284515241): remove this special handling to support
                # array output types once BQ remote functions support ARRAY.
                # Until then, use json serialized strings at the cloud function
                # and BQ level, and parse that to the intended output type at
                # the bigframes level.
                bqrf_metadata = _utils.get_bigframes_metadata(
                    python_output_type=py_sig.return_annotation
                )
                post_process_routine = _utils._build_unnest_post_routine(
                    py_sig.return_annotation
                )
                py_sig = py_sig.replace(return_annotation=str)

            udf_sig = udf_def.UdfSignature.from_py_signature(py_sig)

            (
                rf_name,
                cf_name,
                created_new,
            ) = remote_function_client.provision_bq_remote_function(
                func,
                input_types=udf_sig.sql_input_types,
                output_type=udf_sig.sql_output_type,
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
                bq_metadata=bqrf_metadata,
            )

            bigframes_cloud_function = (
                remote_function_client.get_cloud_function_fully_qualified_name(cf_name)
            )
            bigframes_bigquery_function = (
                remote_function_client.get_remote_function_fully_qualilfied_name(
                    rf_name
                )
            )

            # If a new remote function was created, update the cloud artifacts
            # created in the session. This would be used to clean up any
            # resources in the session. Note that we need to do this only for
            # the case where an explicit name was not provided by the user and
            # we used an internal name. For the cases where the user provided an
            # explicit name, we are assuming that the user wants to persist them
            # with that name and would directly manage their lifecycle.
            if created_new and (not name):
                self._update_temp_artifacts(
                    bigframes_bigquery_function, bigframes_cloud_function
                )

            udf_definition = udf_def.BigqueryUdf(
                routine_ref=bigquery.RoutineReference.from_string(
                    bigframes_bigquery_function
                ),
                signature=udf_sig,
            )
            decorator = functools.wraps(func)
            if is_row_processor:
                return decorator(
                    bq_functions.BigqueryCallableRowRoutine(
                        udf_definition,
                        session,
                        post_routine=post_process_routine,
                        cloud_function_ref=bigframes_cloud_function,
                        local_func=func,
                        is_managed=False,
                    )
                )
            else:
                return decorator(
                    bq_functions.BigqueryCallableRoutine(
                        udf_definition,
                        session,
                        post_routine=post_process_routine,
                        cloud_function_ref=bigframes_cloud_function,
                        local_func=func,
                        is_managed=False,
                    )
                )

        return wrapper

    def deploy_remote_function(
        self,
        func,
        **kwargs,
    ):
        """Orchestrates the creation of a BigQuery remote function that deploys immediately.

        This method ensures that the remote function is created and available for
        use in BigQuery as soon as this call is made.

        Args:
            kwargs:
                All arguments are passed directly to
                :meth:`~bigframes.session.Session.remote_function`.  Please see
                its docstring for parameter details.

        Returns:
            A wrapped remote function, usable in
            :meth:`~bigframes.series.Series.apply`.
        """
        # TODO(tswast): If we update remote_function to defer deployment, update
        # this method to deploy immediately.
        return self.remote_function(**kwargs)(func)

    def udf(
        self,
        input_types: Union[None, type, Sequence[type]] = None,
        output_type: Optional[type] = None,
        session: Optional[Session] = None,
        bigquery_client: Optional[bigquery.Client] = None,
        dataset: Optional[str] = None,
        bigquery_connection: Optional[str] = None,
        name: Optional[str] = None,
        packages: Optional[Sequence[str]] = None,
    ):
        """Decorator to turn a Python user defined function (udf) into a
        BigQuery managed function.

        .. note::
            This feature is in preview. The code in the udf must be
            (1) self-contained, i.e. it must not contain any
            references to an import or variable defined outside the function
            body, and
            (2) Python 3.11 compatible, as that is the environment
            in which the code is executed in the cloud.

        .. note::
            Please have following IAM roles enabled for you:

            * BigQuery Data Editor (roles/bigquery.dataEditor)

        Args:
            input_types (type or sequence(type), Optional):
                For scalar user defined function it should be the input type or
                sequence of input types. The supported scalar input types are
                `bool`, `bytes`, `float`, `int`, `str`.
            output_type (type, Optional):
                Data type of the output in the user defined function. If the
                user defined function returns an array, then `list[type]` should
                be specified. The supported output types are `bool`, `bytes`,
                `float`, `int`, `str`, `list[bool]`, `list[float]`, `list[int]`
                and `list[str]`.
            session (bigframes.Session, Optional):
                BigQuery DataFrames session to use for getting default project,
                dataset and BigQuery connection.
            bigquery_client (google.cloud.bigquery.Client, Optional):
                Client to use for BigQuery operations. If this param is not
                provided, then bigquery client from the session would be used.
            dataset (str, Optional):
                Dataset in which to create a BigQuery managed function. It
                should be in `<project_id>.<dataset_name>` or `<dataset_name>`
                format. If this parameter is not provided then session dataset
                id is used.
            bigquery_connection (str, Optional):
                Name of the BigQuery connection. It is used to provide an
                identity to the serverless instances running the user code. It
                helps BigQuery manage and track the resources used by the udf.
                This connection is required for internet access and for
                interacting with other GCP services. To access GCP services, the
                appropriate IAM permissions must also be granted to the
                connection's Service Account. When it defaults to None, the udf
                will be created without any connection. A udf without a
                connection has no internet access and no access to other GCP
                services.
            name (str, Optional):
                Explicit name of the persisted BigQuery managed function. Use it
                with caution, because more than one users working in the same
                project and dataset could overwrite each other's managed
                functions if they use the same persistent name. When an explicit
                name is provided, any session specific clean up (
                ``bigframes.session.Session.close``/
                ``bigframes.pandas.close_session``/
                ``bigframes.pandas.reset_session``/
                ``bigframes.pandas.clean_up_by_session_id``) does not clean up
                the function, and leaves it for the user to manage the function
                directly.
            packages (str[], Optional):
                Explicit name of the external package dependencies. Each
                dependency is added to the `requirements.txt` as is, and can be
                of the form supported in
                https://pip.pypa.io/en/stable/reference/requirements-file-format/.
        """

        warnings.warn("udf is in preview.", category=bfe.PreviewWarning, stacklevel=5)

        # Some defaults may be used from the session if not provided otherwise.
        session = self._resolve_session(session)

        # A BigQuery client is required to perform BQ operations.
        bigquery_client = self._resolve_bigquery_client(session, bigquery_client)

        # BQ managed function must be persisted, for which we need a dataset.
        dataset_ref = self._resolve_dataset_reference(session, bigquery_client, dataset)

        bq_location, _ = _utils.get_remote_function_locations(bigquery_client.location)

        # A connection is optional for BQ managed function.
        bq_connection_id = (
            self._resolve_bigquery_connection_id(
                session, dataset_ref, bq_location, bigquery_connection
            )
            if bigquery_connection
            else None
        )

        bq_connection_manager = session.bqconnectionmanager

        # TODO(b/399129906): Write a method for the repeated part in the wrapper
        # for both managed function and remote function.
        def wrapper(func):
            nonlocal input_types, output_type

            if not callable(func):
                raise bf_formatting.create_exception_with_feedback_link(
                    TypeError, f"func must be a callable, got {func}"
                )

            if sys.version_info >= (3, 10):
                # Add `eval_str = True` so that deferred annotations are turned into their
                # corresponding type objects. Need Python 3.10 for eval_str parameter.
                # https://docs.python.org/3/library/inspect.html#inspect.signature
                signature_kwargs: Mapping[str, Any] = {"eval_str": True}
            else:
                signature_kwargs = {}  # type: ignore

            py_sig = inspect.signature(
                func,
                **signature_kwargs,
            )
            if input_types is not None:
                if not isinstance(input_types, collections.abc.Sequence):
                    input_types = [input_types]
                py_sig = py_sig.replace(
                    parameters=[
                        par.replace(annotation=itype)
                        for par, itype in zip(py_sig.parameters.values(), input_types)
                    ]
                )
            if output_type:
                py_sig = py_sig.replace(return_annotation=output_type)

            udf_sig = udf_def.UdfSignature.from_py_signature(py_sig)

            # The function will actually be receiving a pandas Series, but allow
            # both BigQuery DataFrames and pandas object types for compatibility.
            is_row_processor = False
            if new_sig := _convert_row_processor_sig(py_sig):
                py_sig = new_sig
                is_row_processor = True

            managed_function_client = _function_client.FunctionClient(
                dataset_ref.project,
                bq_location,
                dataset_ref.dataset_id,
                bigquery_client,
                bq_connection_id,
                bq_connection_manager,
                session=session,  # type: ignore
            )

            bq_function_name = managed_function_client.provision_bq_managed_function(
                func=func,
                input_types=udf_sig.sql_input_types,
                output_type=udf_sig.sql_output_type,
                name=name,
                packages=packages,
                is_row_processor=is_row_processor,
                bq_connection_id=bq_connection_id,
            )
            full_rf_name = (
                managed_function_client.get_remote_function_fully_qualilfied_name(
                    bq_function_name
                )
            )

            udf_definition = udf_def.BigqueryUdf(
                routine_ref=bigquery.RoutineReference.from_string(full_rf_name),
                signature=udf_sig,
            )

            if not name:
                self._update_temp_artifacts(full_rf_name, "")

            decorator = functools.wraps(func)
            if is_row_processor:
                return decorator(
                    bq_functions.BigqueryCallableRowRoutine(
                        udf_definition, session, local_func=func, is_managed=True
                    )
                )
            else:
                return decorator(
                    bq_functions.BigqueryCallableRoutine(
                        udf_definition,
                        session,
                        local_func=func,
                        is_managed=True,
                    )
                )

        return wrapper

    def deploy_udf(
        self,
        func,
        **kwargs,
    ):
        """Orchestrates the creation of a BigQuery UDF that deploys immediately.

        This method ensures that the UDF is created and available for
        use in BigQuery as soon as this call is made.

        Args:
            func:
                Function to deploy.
            kwargs:
                All arguments are passed directly to
                :meth:`~bigframes.session.Session.udf`.  Please see
                its docstring for parameter details.

        Returns:
            A wrapped Python user defined function, usable in
            :meth:`~bigframes.series.Series.apply`.
        """
        # TODO(tswast): If we update udf to defer deployment, update this method
        # to deploy immediately.
        return self.udf(**kwargs)(func)


def _convert_row_processor_sig(
    signature: inspect.Signature,
) -> Optional[inspect.Signature]:
    import bigframes.series as bf_series

    if len(signature.parameters) == 1:
        only_param = next(iter(signature.parameters.values()))
        param_type = only_param.annotation
        if (param_type == bf_series.Series) or (param_type == pandas.Series):
            msg = bfe.format_message("input_types=Series is in preview.")
            warnings.warn(msg, stacklevel=1, category=bfe.PreviewWarning)
            return signature.replace(parameters=[only_param.replace(annotation=str)])
    return None
