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
import logging
import random
import string
import sys
import threading
import time
import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Union,
)

from google.cloud import (
    bigquery,
)

import bigframes.exceptions as bfe
import bigframes.formatting_helpers as bf_formatting
from bigframes import clients
from bigframes.functions import _function_client, _utils, udf_def
from bigframes.functions import function as bq_functions
from bigframes.functions._utils import (
    _BIGFRAMES_FUNCTION_PREFIX,
    _BQ_FUNCTION_NAME_SEPERATOR,
    _GCF_FUNCTION_NAME_SEPERATOR,
)

if TYPE_CHECKING:
    from bigframes.session import anonymous_dataset


_DEFAULT_FUNCTION_MEMORY_MIB = 1024


logger = logging.getLogger(__name__)


class FunctionSession:
    """Session to manage bigframes functions."""

    def __init__(
        self,
        functions_client: _function_client.FunctionClient,
        dataset_manager: anonymous_dataset.AnonymousDatasetManager,
        default_connection: str,
        location: str,
        session_id: str,
        manage_connections: bool,
    ):
        self._temp_cloud_functions: set[str] = set()
        self._temp_remote_functions: set[bigquery.RoutineReference] = set()

        # Lock to synchronize the update of the session artifacts
        self._artifacts_lock = threading.Lock()

        self._deployed_routines: set[bytes] = set()
        self._deploying_routines: set[bytes] = set()

        self._function_client: _function_client.FunctionClient = functions_client
        self._dataset_manager: anonymous_dataset.AnonymousDatasetManager = (
            dataset_manager
        )
        self._default_connection: str = default_connection
        self._location: str = location
        self._session_id: str = session_id
        self._manage_connections: bool = manage_connections

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def default_dataset(self) -> bigquery.DatasetReference:
        # We defer this as a property since this can actually take a query to determine
        # which dataset it is.
        return self._dataset_manager.dataset

    def _resolve_dataset_reference(
        self,
        dataset: Optional[str],
    ) -> bigquery.DatasetReference:
        """
        Resolves the dataset reference for the bigframes function.
        """
        return (
            bigquery.DatasetReference.from_string(
                dataset, default_project=self.default_dataset.project
            )
            if dataset
            else self.default_dataset
        )

    def _resolve_routine_reference(
        self,
        function_name: str,
        dataset: Optional[bigquery.DatasetReference] = None,
    ) -> bigquery.RoutineReference:
        """Resolves the routine reference for a BQ routine."""
        dataset_ref = dataset if dataset else self.default_dataset
        return dataset_ref.routine(function_name)

    def _resolve_bigquery_connection_id(
        self,
        dataset_ref: bigquery.DatasetReference,
        bigquery_connection: Optional[str] = None,
    ) -> str:
        """Resolves BigQuery connection id."""
        if not bigquery_connection:
            bigquery_connection = self._default_connection

        bigquery_connection = clients.get_canonical_bq_connection_id(
            bigquery_connection,
            default_project=dataset_ref.project,
            default_location=self._location,
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
        if bq_connection_location.casefold() != self._location.casefold():
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "The location does not match BigQuery connection location: "
                f"{self._location}.",
            )
        return bq_connection_id

    def _add_temp_cloud_function(self, gcf_path: str):
        with self._artifacts_lock:
            self._temp_cloud_functions.add(gcf_path)

    def _add_temp_remote_function(self, bqrf_routine: bigquery.RoutineReference):
        with self._artifacts_lock:
            self._temp_remote_functions.add(bqrf_routine)

    def _deploy_managed_function(
        self,
        config: udf_def.ManagedFunctionConfig,
        name: str,
        temp: bool,
        dataset: Optional[bigquery.DatasetReference] = None,
    ) -> udf_def.BigqueryUdf:
        routine_ref = self._resolve_routine_reference(name, dataset=dataset)
        if temp:
            self._add_temp_remote_function(routine_ref)
        self._function_client.provision_bq_managed_function(
            routine_ref=routine_ref, config=config
        )
        return udf_def.BigqueryUdf(
            routine_ref=routine_ref,
            signature=config.signature,
        )

    def _deploy_udf(
        self,
        bq_udf: udf_def.PythonUdf,
    ) -> udf_def.BigqueryUdf:
        """Deploys a UDF to BigQuery if not already deployed."""
        udf_hash = bq_udf.stable_hash()

        config = bq_udf.to_managed_function_config()
        bq_function_name = get_managed_function_name(config, self.session_id)
        routine_ref = self._resolve_routine_reference(bq_function_name)
        while True:
            with self._artifacts_lock:
                if udf_hash in self._deployed_routines:
                    return udf_def.BigqueryUdf(
                        routine_ref=routine_ref,
                        signature=bq_udf.signature,
                    )

                if udf_hash not in self._deploying_routines:
                    self._deploying_routines.add(udf_hash)
                    break

            time.sleep(0.1)
        try:
            self._function_client.provision_bq_managed_function(
                routine_ref=routine_ref, config=config
            )
        except Exception:
            with self._artifacts_lock:
                self._deploying_routines.discard(udf_hash)
            raise
        self._add_temp_remote_function(routine_ref)
        with self._artifacts_lock:
            self._deploying_routines.discard(udf_hash)
            self._deployed_routines.add(udf_hash)
        return udf_def.BigqueryUdf(
            routine_ref=routine_ref,
            signature=bq_udf.signature,
        )

    def clean_up(self):
        """Delete function artifacts in the current session."""
        with self._artifacts_lock:
            for bqrf_routine in self._temp_remote_functions:
                self._function_client.delete_routine(bqrf_routine)
            for gcf_name in self._temp_cloud_functions:
                self._function_client.delete_cloud_function(gcf_name)

            self._temp_remote_functions.clear()
            self._temp_cloud_functions.clear()

    # Inspired by @udf decorator implemented in ibis-bigquery package
    # https://github.com/ibis-project/ibis-bigquery/blob/main/ibis_bigquery/udf/__init__.py
    # which has moved as @js to the ibis package
    # https://github.com/ibis-project/ibis/blob/master/ibis/backends/bigquery/udf/__init__.py
    def remote_function(
        self,
        *,
        input_types: Union[None, type, Sequence[type]] = None,
        output_type: Optional[type] = None,
        dataset: Optional[str] = None,
        bigquery_connection: Optional[str] = None,
        reuse: bool = True,
        name: Optional[str] = None,
        packages: Optional[Sequence[str]] = None,
        cloud_function_service_account: str,
        cloud_function_kms_key_name: Optional[str] = None,
        cloud_function_docker_repository: Optional[str] = None,
        max_batching_rows: Optional[int] = None,
        cloud_function_timeout: Optional[int] = 600,
        cloud_function_max_instances: Optional[int] = None,
        cloud_function_vpc_connector: Optional[str] = None,
        cloud_function_vpc_connector_egress_settings: Optional[
            Literal["all", "private-ranges-only", "unspecified"]
        ] = None,
        cloud_function_memory_mib: Optional[int] = None,
        cloud_function_cpus: Optional[float] = None,
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
            cloud_function_vpc_connector_egress_settings (str, Optional):
                Egress settings for the VPC connector, controlling what outbound
                traffic is routed through the VPC connector.
                Options are: `all`, `private-ranges-only`, or `unspecified`.
                If not specified, `private-ranges-only` is used by default.
                See for more details
                https://cloud.google.com/run/docs/configuring/vpc-connectors#egress-job.
            cloud_function_memory_mib (int, Optional):
                The amounts of memory (in mebibytes) to allocate for the cloud
                function (2nd gen) created. This also dictates a corresponding
                amount of allocated CPU for the function. By default a memory of
                1024 MiB is set for the cloud functions created to support
                BigQuery DataFrames remote function. If you want to let the
                default memory of cloud functions be allocated, pass `None`. See
                for more details
                https://cloud.google.com/functions/docs/configuring/memory.
            cloud_function_cpus (float, Optional):
                The number of cpus to allocate for the cloud
                function (2nd gen) created.
                https://docs.cloud.google.com/run/docs/configuring/services/cpu.
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
        # If the user forces the cloud function service argument to None, throw
        # an exception
        if cloud_function_service_account is None:
            raise ValueError(
                'You must provide a user managed cloud_function_service_account, or "default" if you would like to let the default service account be used.'
            )

        # BQ remote function must be persisted, for which we need a dataset.
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#:~:text=You%20cannot%20create%20temporary%20remote%20functions.
        dataset_ref = self._resolve_dataset_reference(dataset)
        # A connection is required for BQ remote function.
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#create_a_remote_function
        bq_connection_id = self._resolve_bigquery_connection_id(
            dataset_ref, bigquery_connection
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

        # A VPC connector is required to specify VPC egress settings.
        if (
            cloud_function_vpc_connector_egress_settings is not None
            and cloud_function_vpc_connector is None
        ):
            raise bf_formatting.create_exception_with_feedback_link(
                ValueError,
                "cloud_function_vpc_connector must be specified before cloud_function_vpc_connector_egress_settings.",
            )

        if cloud_function_ingress_settings is None:
            cloud_function_ingress_settings = "internal-only"
            msg = bfe.format_message(
                "The `cloud_function_ingress_settings` is being set to 'internal-only' by default."
            )
            warnings.warn(msg, category=UserWarning, stacklevel=2)

        def wrapper(func):
            nonlocal input_types, output_type

            ### Step 1: Validate inputs and package into cloud run function, remote function defs. ###
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

            py_sig = _resolve_signature(
                inspect.signature(func, **signature_kwargs),
                input_types,
                output_type,
            )

            udf_sig = udf_def.UdfSignature.from_py_signature(
                py_sig
            ).to_remote_function_compatible()

            full_package_requirements = _utils.get_updated_package_requirements(
                packages or [], udf_sig.is_row_processor
            )
            memory_mib = cloud_function_memory_mib or _DEFAULT_FUNCTION_MEMORY_MIB

            # assumption is most bigframes functions are cpu bound, single-threaded and many won't release GIL
            # therefore, want to allocate a worker for each cpu, and allow a concurrent request per worker
            expected_milli_cpus = (
                int(cloud_function_cpus * 1000)
                if (cloud_function_cpus is not None)
                else _infer_milli_cpus_from_memory(memory_mib)
            )
            workers = -(
                expected_milli_cpus // -1000
            )  # ceil(cpus) without invoking floats
            threads = 4  # (per worker)
            # max concurrency==1 for vcpus < 1 hard limit from cloud run
            concurrency = (workers * threads) if (expected_milli_cpus >= 1000) else 1

            ### Step 1: Create resources or fetch existing matching resources. ###
            cloud_func_spec = udf_def.CloudRunFunctionConfig(
                code=udf_def.CodeDef.from_func(func, full_package_requirements),
                signature=udf_sig,
                timeout_seconds=cloud_function_timeout,
                max_instance_count=cloud_function_max_instances,
                vpc_connector=cloud_function_vpc_connector,
                vpc_connector_egress_settings=cloud_function_vpc_connector_egress_settings
                or "private-ranges-only",
                memory_mib=memory_mib,
                cpus=cloud_function_cpus,
                ingress_settings=cloud_function_ingress_settings,
                workers=workers,
                threads=threads,
                concurrency=concurrency,
                kms_key_name=cloud_function_kms_key_name,
                docker_repository=cloud_function_docker_repository,
                cloud_build_service_account=cloud_build_service_account,
                cloud_run_service_account=(
                    None
                    if (cloud_function_service_account == "default")
                    else cloud_function_service_account
                ),
            )
            uniq_suffix = None
            if not reuse:
                uniq_suffix = "".join(
                    random.choices(string.ascii_lowercase + string.digits, k=4)
                )
            cf_name = get_cloud_function_name(
                cloud_func_spec,
                # only session scope a temp unnamed function
                session_id=self.session_id if (name is None) else None,
                uniq_suffix=uniq_suffix,
            )
            if not name:
                self._add_temp_cloud_function(cf_name)

            # Create remote function that points at the cloud function
            cf_endpoint = None
            if reuse is not None:
                cf_endpoint = self._function_client.get_cloud_function_endpoint(cf_name)

            # If the endpoint is empty, the function might exist but the URL propagation is pending.
            # Running create_cloud_function will handle AlreadyExists and retry endpoint fetching.
            if not cf_endpoint:
                cf_endpoint = self._function_client.create_cloud_function(
                    cf_name, cloud_func_spec
                )
            else:
                logger.info(f"Cloud function {cf_name} already exists.")

            remote_function_config = udf_def.RemoteFunctionConfig(
                endpoint=cf_endpoint,
                connection_id=bq_connection_id,
                max_batching_rows=max_batching_rows or 1000,
                signature=udf_sig,
                bq_metadata=udf_sig.protocol_metadata,
            )
            remote_function_name = name or get_bigframes_function_name(
                remote_function_config,
                session_id=self.session_id,
                uniq_suffix=uniq_suffix,
            )
            routine_ref = self._resolve_routine_reference(
                remote_function_name, dataset=dataset_ref
            )
            if not name:
                self._add_temp_remote_function(routine_ref)

            self._function_client.create_bq_remote_function(
                udf_def=remote_function_config,
                routine_ref=routine_ref,
                maybe_reuse=reuse,
                try_create_connection=self._manage_connections,
            )

            udf_definition = udf_def.BigqueryUdf(
                routine_ref=routine_ref,
                signature=udf_sig,
            )
            decorator = functools.wraps(func)
            if udf_sig.is_row_processor:
                msg = bfe.format_message("input_types=Series is in preview.")
                warnings.warn(msg, stacklevel=1, category=bfe.PreviewWarning)

            cf_full_path = (
                self._function_client.get_cloud_function_fully_qualified_name(cf_name)
            )
            return decorator(
                bq_functions.BigqueryCallableRoutine(
                    udf_definition,
                    self._function_client._bq_client,
                    cloud_function_ref=cf_full_path,
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
        input_types: type | Sequence[type] | None = None,
        output_type: type | None = None,
        dataset: str | None = None,
        bigquery_connection: str | None = None,
        name: str | None = None,
        packages: Sequence[str] | None = None,
        max_batching_rows: int | None = None,
        container_cpu: Optional[float] = None,
        container_memory: Optional[str] = None,
        *,
        _force_deploy: bool = False,
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
            max_batching_rows (int, Optional):
                The maximum number of rows in each batch. If you specify
                max_batching_rows, BigQuery determines the number of rows in a
                batch, up to the max_batching_rows limit. If max_batching_rows
                is not specified, the number of rows to batch is determined
                automatically.
            container_cpu (float, Optional):
                The CPU limits for containers that run Python UDFs. By default,
                the CPU allocated is 0.33 vCPU. See details at
                https://cloud.google.com/bigquery/docs/user-defined-functions-python#configure-container-limits.
            container_memory (str, Optional):
                The memory limits for containers that run Python UDFs. By
                default, the memory allocated to each container instance is
                512 MiB. See details at
                https://cloud.google.com/bigquery/docs/user-defined-functions-python#configure-container-limits.
        """

        warnings.warn("udf is in preview.", category=bfe.PreviewWarning, stacklevel=5)
        # BQ managed function must be persisted, for which we need a dataset.
        dataset_ref = self._resolve_dataset_reference(dataset)

        # A connection is optional for BQ managed function.
        bq_connection_id = (
            self._resolve_bigquery_connection_id(dataset_ref, bigquery_connection)
            if bigquery_connection
            else None
        )

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
            py_sig = _resolve_signature(py_sig, input_types, output_type)

            # The function will actually be receiving a pandas Series, but allow
            # both BigQuery DataFrames and pandas object types for compatibility.
            udf_sig = udf_def.UdfSignature.from_py_signature(py_sig)

            code_def = udf_def.CodeDef.from_func(func, package_requirements=packages)
            requirements = udf_def.RuntimeRequirements(
                container_cpu=container_cpu,
                container_memory=container_memory,
                bq_connection_id=bq_connection_id,
                max_batching_rows=max_batching_rows,
                packages=tuple(packages) if packages else (),
            )
            if udf_sig.is_row_processor:
                msg = bfe.format_message("input_types=Series is in preview.")
                warnings.warn(msg, stacklevel=1, category=bfe.PreviewWarning)

            if (
                not name and not dataset and not _force_deploy
            ):  # session-owned resource - deferred deployment
                udf_definition = udf_def.PythonUdf(
                    signature=udf_sig,
                    code=code_def,
                    requirements=requirements,
                )
                return bq_functions.UdfRoutine(func=func, _udf_def=udf_definition)
            else:  # deploy immediately
                config = udf_def.ManagedFunctionConfig(
                    code=code_def,
                    signature=udf_sig,
                    max_batching_rows=max_batching_rows,
                    container_cpu=container_cpu,
                    container_memory=container_memory,
                    bq_connection_id=bq_connection_id,
                    capture_references=False,
                )
                function_name = name or get_managed_function_name(
                    config, self.session_id
                )
                rf_def = self._deploy_managed_function(
                    config,
                    name=function_name,
                    temp=(name is None),
                    dataset=dataset_ref,
                )
                return bq_functions.BigqueryCallableRoutine(
                    rf_def,
                    self._function_client._bq_client,
                    local_func=func,
                    is_managed=True,
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
        return self.udf(_force_deploy=True, **kwargs)(func)


def _resolve_signature(
    py_sig: inspect.Signature,
    input_types: Union[None, type, Sequence[type]] = None,
    output_type: Optional[type] = None,
) -> inspect.Signature:
    if input_types is not None:
        if not isinstance(input_types, collections.abc.Sequence):
            input_types = [input_types]
        if _utils.has_conflict_input_type(py_sig, input_types):
            msg = bfe.format_message(
                "Conflicting input types detected, using the one from the decorator."
            )
            warnings.warn(msg, category=bfe.FunctionConflictTypeHintWarning)
        py_sig = py_sig.replace(
            parameters=[
                par.replace(annotation=itype)
                for par, itype in zip(py_sig.parameters.values(), input_types)
            ]
        )
    if output_type:
        if _utils.has_conflict_output_type(py_sig, output_type):
            msg = bfe.format_message(
                "Conflicting return type detected, using the one from the decorator."
            )
            warnings.warn(msg, category=bfe.FunctionConflictTypeHintWarning)
        py_sig = py_sig.replace(return_annotation=output_type)

    return py_sig


def get_cloud_function_name(
    function_def: udf_def.CloudRunFunctionConfig, session_id=None, uniq_suffix=False
):
    """
    Get a name for the cloud function for the given user defined function.

    If make_unique is True, append a random suffix to the name.
    """
    parts = [_BIGFRAMES_FUNCTION_PREFIX]
    if session_id:
        parts.append(session_id)
    parts.append(function_def.stable_hash().hex())
    if uniq_suffix:
        parts.append(uniq_suffix)
    return _GCF_FUNCTION_NAME_SEPERATOR.join(parts)


def get_bigframes_function_name(
    function: udf_def.RemoteFunctionConfig, session_id, uniq_suffix=None
):
    """Get a name for the bigframes function for the given user defined function."""
    parts = [_BIGFRAMES_FUNCTION_PREFIX, session_id, function.stable_hash().hex()]
    if uniq_suffix:
        parts.append(uniq_suffix)
    return _BQ_FUNCTION_NAME_SEPERATOR.join(parts)


def get_managed_function_name(
    function_def: udf_def.ManagedFunctionConfig,
    session_id: str | None = None,
):
    """Get a name for the bigframes managed function for the given user defined function."""
    parts = [_BIGFRAMES_FUNCTION_PREFIX]
    if session_id:
        parts.append(session_id)
    parts.append(function_def.stable_hash().hex())
    return _BQ_FUNCTION_NAME_SEPERATOR.join(parts)


def _infer_milli_cpus_from_memory(memory_mib: int) -> int:
    # observed values, not formally documented by cloud run functions
    if memory_mib < 128:
        raise ValueError("Cloud run supports at minimum 128MiB per instance")
    elif memory_mib == 128:
        return 83
    elif memory_mib <= 256:
        return 167
    elif memory_mib <= 512:
        return 333
    elif memory_mib <= 1024:
        return 583
    elif memory_mib <= 2048:
        return 1000
    elif memory_mib <= 8192:
        return 2000
    elif memory_mib <= 16384:
        return 4000
    elif memory_mib <= 32768:
        return 8000
    else:
        raise ValueError("Cloud run supports at most 32768MiB per instance")
