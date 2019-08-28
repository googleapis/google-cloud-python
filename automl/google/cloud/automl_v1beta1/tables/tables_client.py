# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A tables helper for the google.cloud.automl_v1beta1 AutoML API"""

import pkg_resources
import logging

from google.api_core.gapic_v1 import client_info
from google.api_core import exceptions
from google.cloud.automl_v1beta1 import gapic
from google.cloud.automl_v1beta1.proto import data_types_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-automl").version
_LOGGER = logging.getLogger(__name__)


class TablesClient(object):
    """
    AutoML Tables API helper.

    This is intended to simplify usage of the auto-generated python client,
    in particular for the `AutoML Tables product
    <https://cloud.google.com/automl-tables/>`_.
    """

    def __init__(
        self,
        project=None,
        region="us-central1",
        client=None,
        prediction_client=None,
        **kwargs
    ):
        """Constructor.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...

        Args:
            project (Optional[string]): The project all future calls will
                default to. Most methods take `project` as an optional
                parameter, and can override your choice of `project` supplied
                here.
            region (Optional[string]): The region all future calls will
                default to. Most methods take `region` as an optional
                parameter, and can override your choice of `region` supplied
                here. Note, only `us-central1` is supported to-date.
            transport (Union[~.AutoMlGrpcTransport, Callable[[~.Credentials, type], ~.AutoMlGrpcTransport]):
                A transport instance, responsible for actually making the API
                calls.  The default transport uses the gRPC protocol.  This
                argument may also be a callable which returns a transport
                instance. Callables will be sent the credentials as the first
                argument and the default transport class as the second
                argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        version = _GAPIC_LIBRARY_VERSION
        user_agent = "automl-tables-wrapper/{}".format(version)

        client_info_ = kwargs.get("client_info")
        if client_info_ is None:
            client_info_ = client_info.ClientInfo(
                user_agent=user_agent, gapic_version=version
            )
        else:
            client_info_.user_agent = user_agent
            client_info_.gapic_version = version

        if client is None:
            self.auto_ml_client = gapic.auto_ml_client.AutoMlClient(
                client_info=client_info_, **kwargs
            )
        else:
            self.auto_ml_client = client

        if prediction_client is None:
            self.prediction_client = gapic.prediction_service_client.PredictionServiceClient(
                client_info=client_info_, **kwargs
            )
        else:
            self.prediction_client = prediction_client

        self.project = project
        self.region = region

    def __lookup_by_display_name(self, object_type, items, display_name):
        relevant_items = [i for i in items if i.display_name == display_name]
        if len(relevant_items) == 0:
            raise exceptions.NotFound(
                "The {} with display_name='{}' was not found.".format(
                    object_type, display_name
                )
            )
        elif len(relevant_items) == 1:
            return relevant_items[0]
        else:
            raise ValueError(
                (
                    "Multiple {}s match display_name='{}': {}\n\n"
                    "Please use the `.name` (unique identifier) field instead"
                ).format(
                    object_type,
                    display_name,
                    ", ".join([str(i) for i in relevant_items]),
                )
            )

    def __location_path(self, project=None, region=None):
        if project is None:
            if self.project is None:
                raise ValueError(
                    "Either initialize your client with a value "
                    "for 'project', or provide 'project' as a "
                    "parameter for this method."
                )
            project = self.project

        if region is None:
            if self.region is None:
                raise ValueError(
                    "Either initialize your client with a value "
                    "for 'region', or provide 'region' as a "
                    "parameter for this method."
                )
            region = self.region

        return self.auto_ml_client.location_path(project, region)

    # the returned metadata object doesn't allow for updating fields, so
    # we need to manually copy user-updated fields over
    def __update_metadata(self, metadata, k, v):
        new_metadata = {}
        new_metadata["ml_use_column_spec_id"] = metadata.ml_use_column_spec_id
        new_metadata["weight_column_spec_id"] = metadata.weight_column_spec_id
        new_metadata["target_column_spec_id"] = metadata.target_column_spec_id
        new_metadata[k] = v

        return new_metadata

    def __dataset_from_args(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        if dataset is None and dataset_display_name is None and dataset_name is None:
            raise ValueError(
                "One of 'dataset', 'dataset_name' or "
                "'dataset_display_name' must be set."
            )
        # we prefer to make a live call here in the case that the
        # dataset object is out-of-date
        if dataset is not None:
            dataset_name = dataset.name

        return self.get_dataset(
            dataset_display_name=dataset_display_name,
            dataset_name=dataset_name,
            project=project,
            region=region,
            **kwargs
        )

    def __model_from_args(
        self,
        model=None,
        model_display_name=None,
        model_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        if model is None and model_display_name is None and model_name is None:
            raise ValueError(
                "One of 'model', 'model_name' or " "'model_display_name' must be set."
            )
        # we prefer to make a live call here in the case that the
        # model object is out-of-date
        if model is not None:
            model_name = model.name

        return self.get_model(
            model_display_name=model_display_name,
            model_name=model_name,
            project=project,
            region=region,
            **kwargs
        )

    def __dataset_name_from_args(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        if dataset is None and dataset_display_name is None and dataset_name is None:
            raise ValueError(
                "One of 'dataset', 'dataset_name' or "
                "'dataset_display_name' must be set."
            )

        if dataset_name is None:
            if dataset is None:
                dataset = self.get_dataset(
                    dataset_display_name=dataset_display_name,
                    project=project,
                    region=region,
                    **kwargs
                )

            dataset_name = dataset.name
        else:
            # we do this to force a NotFound error when needed
            self.get_dataset(
                dataset_name=dataset_name, project=project, region=region, **kwargs
            )
        return dataset_name

    def __table_spec_name_from_args(
        self,
        table_spec_index=0,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        dataset_name = self.__dataset_name_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )

        table_specs = [
            t for t in self.list_table_specs(dataset_name=dataset_name, **kwargs)
        ]

        table_spec_full_id = table_specs[table_spec_index].name
        return table_spec_full_id

    def __model_name_from_args(
        self,
        model=None,
        model_display_name=None,
        model_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        if model is None and model_display_name is None and model_name is None:
            raise ValueError(
                "One of 'model', 'model_name' or " "'model_display_name' must be set."
            )

        if model_name is None:
            if model is None:
                model = self.get_model(
                    model_display_name=model_display_name,
                    project=project,
                    region=region,
                    **kwargs
                )
            model_name = model.name
        else:
            # we do this to force a NotFound error when needed
            self.get_model(
                model_name=model_name, project=project, region=region, **kwargs
            )
        return model_name

    def __log_operation_info(self, message, op):
        name = "UNKNOWN"
        try:
            if (
                op is not None
                and op.operation is not None
                and op.operation.name is not None
            ):
                name = op.operation.name
        except AttributeError:
            pass
        _LOGGER.info(
            (
                "Operation '{}' is running in the background. The returned "
                "Operation '{}' can be used to query or block on the status "
                "of this operation. Ending your python session will _not_ "
                "cancel this operation. Read the documentation here:\n\n"
                "\thttps://googleapis.dev/python/google-api-core/latest/operation.html\n\n"
                "for more information on the Operation class."
            ).format(message, name)
        )
        return op

    def __column_spec_name_from_args(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        table_spec_name=None,
        table_spec_index=0,
        column_spec_name=None,
        column_spec_display_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        column_specs = self.list_column_specs(
            dataset=dataset,
            dataset_display_name=dataset_display_name,
            dataset_name=dataset_name,
            table_spec_name=table_spec_name,
            table_spec_index=table_spec_index,
            project=project,
            region=region,
            **kwargs
        )
        if column_spec_display_name is not None:
            column_specs = {s.display_name: s for s in column_specs}
            if column_specs.get(column_spec_display_name) is None:
                raise exceptions.NotFound(
                    "No column with "
                    + "column_spec_display_name: '{}' found".format(
                        column_spec_display_name
                    )
                )
            column_spec_name = column_specs[column_spec_display_name].name
        elif column_spec_name is not None:
            column_specs = {s.name: s for s in column_specs}
            if column_specs.get(column_spec_name) is None:
                raise exceptions.NotFound(
                    "No column with "
                    + "column_spec_name: '{}' found".format(column_spec_name)
                )
        else:
            raise ValueError(
                "Either supply 'column_spec_name' or "
                "'column_spec_display_name' for the column to update"
            )

        return column_spec_name

    def __type_code_to_value_type(self, type_code, value):
        if value is None:
            return {"null_value": 0}
        elif type_code == data_types_pb2.FLOAT64:
            return {"number_value": value}
        elif type_code == data_types_pb2.TIMESTAMP:
            return {"string_value": value}
        elif type_code == data_types_pb2.STRING:
            return {"string_value": value}
        elif type_code == data_types_pb2.ARRAY:
            return {"list_value": value}
        elif type_code == data_types_pb2.STRUCT:
            return {"struct_value": value}
        elif type_code == data_types_pb2.CATEGORY:
            return {"string_value": value}
        else:
            raise ValueError("Unknown type_code: {}".format(type_code))

    def list_datasets(self, project=None, region=None, **kwargs):
        """List all datasets in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> ds = client.list_datasets()
            >>>
            >>> for d in ds:
            ...     # do something
            ...     pass
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.automl_v1beta1.types.Dataset`
            instances.  You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        return self.auto_ml_client.list_datasets(
            self.__location_path(project=project, region=region), **kwargs
        )

    def get_dataset(
        self,
        project=None,
        region=None,
        dataset_name=None,
        dataset_display_name=None,
        **kwargs
    ):
        """Gets a single dataset in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> d = client.get_dataset(dataset_display_name='my_dataset')
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            dataset_name (Optional[string]):
                This is the fully-qualified name generated by the AutoML API
                for this dataset. This is not to be confused with the
                human-assigned `dataset_display_name` that is provided when
                creating a dataset. Either `dataset_name` or
                `dataset_display_name` must be provided.
            dataset_display_name (Optional[string]):
                This is the name you provided for the dataset when first
                creating it. Either `dataset_name` or `dataset_display_name`
                must be provided.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Dataset` instance if
            found, `None` otherwise.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        if dataset_name is None and dataset_display_name is None:
            raise ValueError(
                "One of 'dataset_name' or " "'dataset_display_name' must be set."
            )

        if dataset_name is not None:
            return self.auto_ml_client.get_dataset(dataset_name, **kwargs)

        return self.__lookup_by_display_name(
            "dataset",
            self.list_datasets(project, region, **kwargs),
            dataset_display_name,
        )

    def create_dataset(
        self, dataset_display_name, metadata={}, project=None, region=None, **kwargs
    ):
        """Create a dataset. Keep in mind, importing data is a separate step.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> d = client.create_dataset(dataset_display_name='my_dataset')
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            dataset_display_name (string):
                A human-readable name to refer to this dataset by.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Dataset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        return self.auto_ml_client.create_dataset(
            self.__location_path(project, region),
            {"display_name": dataset_display_name, "tables_dataset_metadata": metadata},
            **kwargs
        )

    def delete_dataset(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Deletes a dataset. This does not delete any models trained on
        this dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> op = client.delete_dataset(dataset_display_name='my_dataset')
            >>>
            >>> op.result() # blocks on delete request
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to
                delete.  This must be supplied if `dataset` or `dataset_name`
                are not supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                delete. This must be supplied if `dataset_display_name` or
                `dataset` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to delete. This must be
                supplied if `dataset_display_name` or `dataset_name` are not
                supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture`
            instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        try:
            dataset_name = self.__dataset_name_from_args(
                dataset=dataset,
                dataset_name=dataset_name,
                dataset_display_name=dataset_display_name,
                project=project,
                region=region,
                **kwargs
            )
        # delete is idempotent
        except exceptions.NotFound:
            return None

        op = self.auto_ml_client.delete_dataset(dataset_name, **kwargs)
        self.__log_operation_info("Delete dataset", op)
        return op

    def import_data(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        gcs_input_uris=None,
        bigquery_input_uri=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Imports data into a dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> d = client.create_dataset(dataset_display_name='my_dataset')
            >>>
            >>> client.import_data(dataset=d,
            ...     gcs_input_uris='gs://cloud-ml-tables-data/bank-marketing.csv')
            ...
            >>> def callback(operation_future):
            ...    result = operation_future.result()
            ...
            >>> response.add_done_callback(callback)
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to import
                data into. This must be supplied if `dataset` or `dataset_name`
                are not supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                import data into. This must be supplied if
                `dataset_display_name` or `dataset` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to import data into. This must
                be supplied if `dataset_display_name` or `dataset_name` are not
                supplied.
            gcs_input_uris (Optional[Union[string, Sequence[string]]]):
                Either a single `gs://..` prefixed URI, or a list of URIs
                referring to GCS-hosted CSV files containing the data to
                import. This must be supplied if `bigquery_input_uri` is not.
            bigquery_input_uri (Optional[string]):
                A URI pointing to the BigQuery table containing the data to
                import. This must be supplied if `gcs_input_uris` is not.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture`
            instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        dataset_name = self.__dataset_name_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )

        request = {}
        if gcs_input_uris is not None:
            if type(gcs_input_uris) != list:
                gcs_input_uris = [gcs_input_uris]
            request = {"gcs_source": {"input_uris": gcs_input_uris}}
        elif bigquery_input_uri is not None:
            request = {"bigquery_source": {"input_uri": bigquery_input_uri}}
        else:
            raise ValueError(
                "One of 'gcs_input_uris', or " "'bigquery_input_uri' must be set."
            )

        op = self.auto_ml_client.import_data(dataset_name, request, **kwargs)
        self.__log_operation_info("Data import", op)
        return op

    def export_data(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        gcs_output_uri_prefix=None,
        bigquery_output_uri=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Exports data from a dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> d = client.create_dataset(dataset_display_name='my_dataset')
            >>>
            >>> client.export_data(dataset=d,
            ...     gcs_output_uri_prefix='gs://cloud-ml-tables-data/bank-marketing.csv')
            ...
            >>> def callback(operation_future):
            ...    result = operation_future.result()
            ...
            >>> response.add_done_callback(callback)
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to export
                data from. This must be supplied if `dataset` or `dataset_name`
                are not supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                export data from. This must be supplied if
                `dataset_display_name` or `dataset` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to export data from. This must
                be supplied if `dataset_display_name` or `dataset_name` are not
                supplied.
            gcs_output_uri_prefix (Optional[Union[string, Sequence[string]]]):
                A single `gs://..` prefixed URI to export to. This must be
                supplied if `bigquery_output_uri` is not.
            bigquery_output_uri (Optional[string]):
                A URI pointing to the BigQuery table containing the data to
                export. This must be supplied if `gcs_output_uri_prefix` is not.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture`
            instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        dataset_name = self.__dataset_name_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )

        request = {}
        if gcs_output_uri_prefix is not None:
            request = {"gcs_destination": {"output_uri_prefix": gcs_output_uri_prefix}}
        elif bigquery_output_uri is not None:
            request = {"bigquery_destination": {"output_uri": bigquery_output_uri}}
        else:
            raise ValueError(
                "One of 'gcs_output_uri_prefix', or 'bigquery_output_uri' must be set."
            )

        op = self.auto_ml_client.export_data(dataset_name, request, **kwargs)
        self.__log_operation_info("Export data", op)
        return op

    def get_table_spec(self, table_spec_name, project=None, region=None, **kwargs):
        """Gets a single table spec in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> d = client.get_table_spec('my_table_spec')
            >>>

        Args:
            table_spec_name (string):
                This is the fully-qualified name generated by the AutoML API
                for this table spec.
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.TableSpec` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        return self.auto_ml_client.get_table_spec(table_spec_name, **kwargs)

    def list_table_specs(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Lists table specs.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> for s in client.list_table_specs(dataset_display_name='my_dataset')
            ...     # process the spec
            ...     pass
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to read
                specs from. This must be supplied if `dataset` or
                `dataset_name` are not supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to read
                specs from. This must be supplied if `dataset_display_name` or
                `dataset` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to read specs from. This must
                be supplied if `dataset_display_name` or `dataset_name` are not
                supplied.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of
            :class:`~google.cloud.automl_v1beta1.types.TableSpec` instances.
            You can also iterate over the pages of the response using its
            `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        dataset_name = self.__dataset_name_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )

        return self.auto_ml_client.list_table_specs(dataset_name, **kwargs)

    def get_column_spec(self, column_spec_name, project=None, region=None, **kwargs):
        """Gets a single column spec in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> d = client.get_column_spec('my_column_spec')
            >>>

        Args:
            column_spec_name (string):
                This is the fully-qualified name generated by the AutoML API
                for this column spec.
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.ColumnSpec` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        return self.auto_ml_client.get_column_spec(column_spec_name, **kwargs)

    def list_column_specs(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        table_spec_name=None,
        table_spec_index=0,
        project=None,
        region=None,
        **kwargs
    ):
        """Lists column specs.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> for s in client.list_column_specs(dataset_display_name='my_dataset')
            ...     # process the spec
            ...     pass
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            table_spec_name (Optional[string]):
                The AutoML-assigned name for the table whose specs you want to
                read. If not supplied, the client can determine this name from
                a source `Dataset` object.
            table_spec_index (Optional[int]):
                If no `table_spec_name` was provided, we use this index to
                determine which table to read column specs from.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to read
                specs from. If no `table_spec_name` is supplied, this will be
                used together with `table_spec_index` to infer the name of
                table to read specs from. This must be supplied if
                `table_spec_name`, `dataset` or `dataset_name` are not
                supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to read
                specs from. If no `table_spec_name` is supplied, this will be
                used together with `table_spec_index` to infer the name of
                table to read specs from. This must be supplied if
                `table_spec_name`, `dataset` or `dataset_display_name` are not
                supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to read specs from. If no
                `table_spec_name` is supplied, this will be used together with
                `table_spec_index` to infer the name of table to read specs
                from. This must be supplied if `table_spec_name`,
                `dataset_name` or `dataset_display_name` are not supplied.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of
            :class:`~google.cloud.automl_v1beta1.types.ColumnSpec` instances.
            You can also iterate over the pages of the response using its
            `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        if table_spec_name is None:
            table_specs = [
                t
                for t in self.list_table_specs(
                    dataset=dataset,
                    dataset_display_name=dataset_display_name,
                    dataset_name=dataset_name,
                    project=project,
                    region=region,
                    **kwargs
                )
            ]

            table_spec_name = table_specs[table_spec_index].name

        return self.auto_ml_client.list_column_specs(table_spec_name, **kwargs)

    def update_column_spec(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        table_spec_name=None,
        table_spec_index=0,
        column_spec_name=None,
        column_spec_display_name=None,
        type_code=None,
        nullable=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Updates a column's specs.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> client.update_column_specs(dataset_display_name='my_dataset',
            ...     column_spec_display_name='Outcome', type_code='CATEGORY')
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            column_spec_name (Optional[string]):
                The name AutoML-assigned name for the column you want to
                update.
            column_spec_display_name (Optional[string]):
                The human-readable name of the column you want to update. If
                this is supplied in place of `column_spec_name`, you also need
                to provide either a way to lookup the source dataset (using one
                of the `dataset*` kwargs), or the `table_spec_name` of the
                table this column belongs to.
            table_spec_name (Optional[string]):
                The AutoML-assigned name for the table whose specs you want to
                update. If not supplied, the client can determine this name
                from a source `Dataset` object.
            table_spec_index (Optional[int]):
                If no `table_spec_name` was provided, we use this index to
                determine which table to update column specs on.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to update
                specs on. If no `table_spec_name` is supplied, this will be
                used together with `table_spec_index` to infer the name of
                table to update specs on. This must be supplied if
                `table_spec_name`, `dataset` or `dataset_name` are not
                supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                update specs one. If no `table_spec_name` is supplied, this
                will be used together with `table_spec_index` to infer the name
                of table to update specs on. This must be supplied if
                `table_spec_name`, `dataset` or `dataset_display_name` are not
                supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to update specs on. If no
                `table_spec_name` is supplied, this will be used together with
                `table_spec_index` to infer the name of table to update specs
                on. This must be supplied if `table_spec_name`, `dataset_name`
                or `dataset_display_name` are not supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.ColumnSpec` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        column_spec_name = self.__column_spec_name_from_args(
            dataset=dataset,
            dataset_display_name=dataset_display_name,
            dataset_name=dataset_name,
            table_spec_name=table_spec_name,
            table_spec_index=table_spec_index,
            column_spec_name=column_spec_name,
            column_spec_display_name=column_spec_display_name,
            project=project,
            region=region,
            **kwargs
        )

        # type code must always be set
        if type_code is None:
            # this index is safe, we would have already thrown a NotFound
            # had the column_spec_name not existed
            type_code = {
                s.name: s
                for s in self.list_column_specs(
                    dataset=dataset,
                    dataset_display_name=dataset_display_name,
                    dataset_name=dataset_name,
                    table_spec_name=table_spec_name,
                    table_spec_index=table_spec_index,
                    project=project,
                    region=region,
                    **kwargs
                )
            }[column_spec_name].data_type.type_code

        data_type = {}
        if nullable is not None:
            data_type["nullable"] = nullable

        data_type["type_code"] = type_code

        request = {"name": column_spec_name, "data_type": data_type}

        return self.auto_ml_client.update_column_spec(request, **kwargs)

    def set_target_column(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        table_spec_name=None,
        table_spec_index=0,
        column_spec_name=None,
        column_spec_display_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Sets the target column for a given table.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> client.set_target_column(dataset_display_name='my_dataset',
            ...     column_spec_display_name='Income')
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            column_spec_name (Optional[string]):
                The name AutoML-assigned name for the column you want to set as
                the target column.
            column_spec_display_name (Optional[string]):
                The human-readable name of the column you want to set as the
                target column. If this is supplied in place of
                `column_spec_name`, you also need to provide either a way to
                lookup the source dataset (using one of the `dataset*` kwargs),
                or the `table_spec_name` of the table this column belongs to.
            table_spec_name (Optional[string]):
                The AutoML-assigned name for the table whose target column you
                want to set . If not supplied, the client can determine this
                name from a source `Dataset` object.
            table_spec_index (Optional[int]):
                If no `table_spec_name` or `column_spec_name` was provided, we
                use this index to determine which table to set the target
                column on.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to update
                the target column of. If no `table_spec_name` is supplied, this
                will be used together with `table_spec_index` to infer the name
                of table to update the target column of. This must be supplied
                if `table_spec_name`, `dataset` or `dataset_name` are not
                supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                update the target column of. If no `table_spec_name` is
                supplied, this will be used together with `table_spec_index` to
                infer the name of table to update the target column of. This
                must be supplied if `table_spec_name`, `dataset` or
                `dataset_display_name` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to update the target column of.
                If no `table_spec_name` is supplied, this will be used together
                with `table_spec_index` to infer the name of table to update
                the target column of. This must be supplied if
                `table_spec_name`, `dataset_name` or `dataset_display_name` are
                not supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Dataset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        column_spec_name = self.__column_spec_name_from_args(
            dataset=dataset,
            dataset_display_name=dataset_display_name,
            dataset_name=dataset_name,
            table_spec_name=table_spec_name,
            table_spec_index=table_spec_index,
            column_spec_name=column_spec_name,
            column_spec_display_name=column_spec_display_name,
            project=project,
            region=region,
            **kwargs
        )
        column_spec_id = column_spec_name.rsplit("/", 1)[-1]

        dataset = self.__dataset_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )
        metadata = dataset.tables_dataset_metadata
        metadata = self.__update_metadata(
            metadata, "target_column_spec_id", column_spec_id
        )

        request = {"name": dataset.name, "tables_dataset_metadata": metadata}

        return self.auto_ml_client.update_dataset(request, **kwargs)

    def set_time_column(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        table_spec_name=None,
        table_spec_index=0,
        column_spec_name=None,
        column_spec_display_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Sets the time column which designates which data will be of type
        timestamp and will be used for the timeseries data.
        This column must be of type timestamp.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> client.set_time_column(dataset_display_name='my_dataset',
            ...     column_spec_name='Unix Time')
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            column_spec_name (Optional[string]):
                The name AutoML-assigned name for the column you want to set as
                the time column.
            column_spec_display_name (Optional[string]):
                The human-readable name of the column you want to set as the
                time column. If this is supplied in place of
                `column_spec_name`, you also need to provide either a way to
                lookup the source dataset (using one of the `dataset*` kwargs),
                or the `table_spec_name` of the table this column belongs to.
            table_spec_name (Optional[string]):
                The AutoML-assigned name for the table whose time column
                you want to set . If not supplied, the client can determine
                this name from a source `Dataset` object.
            table_spec_index (Optional[int]):
                If no `table_spec_name` or `column_spec_name` was provided, we
                use this index to determine which table to set the time
                column on.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to update
                the time column of. If no `table_spec_name` is supplied,
                this will be used together with `table_spec_index` to infer the
                name of table to update the time column of. This must be
                supplied if `table_spec_name`, `dataset` or `dataset_name` are
                not supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                update the time column of. If no `table_spec_name` is
                supplied, this will be used together with `table_spec_index` to
                infer the name of table to update the time column of.
                This must be supplied if `table_spec_name`, `dataset` or
                `dataset_display_name` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to update the time column
                of.  If no `table_spec_name` is supplied, this will be used
                together with `table_spec_index` to infer the name of table to
                update the time column of. This must be supplied if
                `table_spec_name`, `dataset_name` or `dataset_display_name` are
                not supplied.
        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.TableSpec` instance.
        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        column_spec_name = self.__column_spec_name_from_args(
            dataset=dataset,
            dataset_display_name=dataset_display_name,
            dataset_name=dataset_name,
            table_spec_name=table_spec_name,
            table_spec_index=table_spec_index,
            column_spec_name=column_spec_name,
            column_spec_display_name=column_spec_display_name,
            project=project,
            region=region,
            **kwargs
        )
        column_spec_id = column_spec_name.rsplit("/", 1)[-1]

        dataset_name = self.__dataset_name_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )

        table_spec_full_id = self.__table_spec_name_from_args(
            dataset_name=dataset_name, **kwargs
        )

        my_table_spec = {
            "name": table_spec_full_id,
            "time_column_spec_id": column_spec_id,
        }

        return self.auto_ml_client.update_table_spec(my_table_spec, **kwargs)

    def clear_time_column(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Clears the time column which designates which data will be of type
        timestamp and will be used for the timeseries data.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> client.set_time_column(dataset_display_name='my_dataset')
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to update
                the time column of. If no `table_spec_name` is supplied,
                this will be used together with `table_spec_index` to infer the
                name of table to update the time column of. This must be
                supplied if `table_spec_name`, `dataset` or `dataset_name` are
                not supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                update the time column of. If no `table_spec_name` is
                supplied, this will be used together with `table_spec_index` to
                infer the name of table to update the time column of.
                This must be supplied if `table_spec_name`, `dataset` or
                `dataset_display_name` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to update the time column
                of.  If no `table_spec_name` is supplied, this will be used
                together with `table_spec_index` to infer the name of table to
                update the time column of. This must be supplied if
                `table_spec_name`, `dataset_name` or `dataset_display_name` are
                not supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.TableSpec` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        dataset_name = self.__dataset_name_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )

        table_spec_full_id = self.__table_spec_name_from_args(
            dataset_name=dataset_name, **kwargs
        )

        my_table_spec = {"name": table_spec_full_id, "time_column_spec_id": None}

        return self.auto_ml_client.update_table_spec(my_table_spec, **kwargs)

    def set_weight_column(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        table_spec_name=None,
        table_spec_index=0,
        column_spec_name=None,
        column_spec_display_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Sets the weight column for a given table.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> client.set_weight_column(dataset_display_name='my_dataset',
            ...     column_spec_display_name='Income')
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            column_spec_name (Optional[string]):
                The name AutoML-assigned name for the column you want to
                set as the weight column.
            column_spec_display_name (Optional[string]):
                The human-readable name of the column you want to set as the
                weight column. If this is supplied in place of
                `column_spec_name`, you also need to provide either a way to
                lookup the source dataset (using one of the `dataset*` kwargs),
                or the `table_spec_name` of the table this column belongs to.
            table_spec_name (Optional[string]):
                The AutoML-assigned name for the table whose weight column you
                want to set . If not supplied, the client can determine this
                name from a source `Dataset` object.
            table_spec_index (Optional[int]):
                If no `table_spec_name` or `column_spec_name` was provided, we
                use this index to determine which table to set the weight
                column on.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to update
                the weight column of. If no `table_spec_name` is supplied, this
                will be used together with `table_spec_index` to infer the name
                of table to update the weight column of. This must be supplied
                if `table_spec_name`, `dataset` or `dataset_name` are not
                supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                update the weight column of. If no `table_spec_name` is
                supplied, this will be used together with `table_spec_index` to
                infer the name of table to update the weight column of. This
                must be supplied if `table_spec_name`, `dataset` or
                `dataset_display_name` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to update the weight column of.
                If no `table_spec_name` is supplied, this will be used together
                with `table_spec_index` to infer the name of table to update
                the weight column of. This must be supplied if
                `table_spec_name`, `dataset_name` or `dataset_display_name` are
                not supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Dataset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        column_spec_name = self.__column_spec_name_from_args(
            dataset=dataset,
            dataset_display_name=dataset_display_name,
            dataset_name=dataset_name,
            table_spec_name=table_spec_name,
            table_spec_index=table_spec_index,
            column_spec_name=column_spec_name,
            column_spec_display_name=column_spec_display_name,
            project=project,
            region=region,
            **kwargs
        )
        column_spec_id = column_spec_name.rsplit("/", 1)[-1]

        dataset = self.__dataset_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )
        metadata = dataset.tables_dataset_metadata
        metadata = self.__update_metadata(
            metadata, "weight_column_spec_id", column_spec_id
        )

        request = {"name": dataset.name, "tables_dataset_metadata": metadata}

        return self.auto_ml_client.update_dataset(request, **kwargs)

    def clear_weight_column(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Clears the weight column for a given dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> client.clear_weight_column(dataset_display_name='my_dataset')
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to update
                the weight column of. If no `table_spec_name` is supplied, this
                will be used together with `table_spec_index` to infer the name
                of table to update the weight column of. This must be supplied
                if `table_spec_name`, `dataset` or `dataset_name` are not
                supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                update the weight column of. If no `table_spec_name` is
                supplied, this will be used together with `table_spec_index` to
                infer the name of table to update the weight column of. This
                must be supplied if `table_spec_name`, `dataset` or
                `dataset_display_name` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to update the weight column of.
                If no `table_spec_name` is supplied, this will be used together
                with `table_spec_index` to infer the name of table to update
                the weight column of. This must be supplied if
                `table_spec_name`, `dataset_name` or `dataset_display_name` are
                not supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Dataset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        dataset = self.__dataset_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )
        metadata = dataset.tables_dataset_metadata
        metadata = self.__update_metadata(metadata, "weight_column_spec_id", None)

        request = {"name": dataset.name, "tables_dataset_metadata": metadata}

        return self.auto_ml_client.update_dataset(request, **kwargs)

    def set_test_train_column(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        table_spec_name=None,
        table_spec_index=0,
        column_spec_name=None,
        column_spec_display_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Sets the test/train (ml_use) column which designates which data
        belongs to the test and train sets. This column must be categorical.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> client.set_test_train_column(dataset_display_name='my_dataset',
            ...     column_spec_display_name='TestSplit')
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            column_spec_name (Optional[string]):
                The name AutoML-assigned name for the column you want to set as
                the test/train column.
            column_spec_display_name (Optional[string]):
                The human-readable name of the column you want to set as the
                test/train column. If this is supplied in place of
                `column_spec_name`, you also need to provide either a way to
                lookup the source dataset (using one of the `dataset*` kwargs),
                or the `table_spec_name` of the table this column belongs to.
            table_spec_name (Optional[string]):
                The AutoML-assigned name for the table whose test/train column
                you want to set . If not supplied, the client can determine
                this name from a source `Dataset` object.
            table_spec_index (Optional[int]):
                If no `table_spec_name` or `column_spec_name` was provided, we
                use this index to determine which table to set the test/train
                column on.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to update
                the test/train column of. If no `table_spec_name` is supplied,
                this will be used together with `table_spec_index` to infer the
                name of table to update the test/train column of. This must be
                supplied if `table_spec_name`, `dataset` or `dataset_name` are
                not supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                update the test/train column of. If no `table_spec_name` is
                supplied, this will be used together with `table_spec_index` to
                infer the name of table to update the test/train column of.
                This must be supplied if `table_spec_name`, `dataset` or
                `dataset_display_name` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to update the test/train column
                of.  If no `table_spec_name` is supplied, this will be used
                together with `table_spec_index` to infer the name of table to
                update the test/train column of. This must be supplied if
                `table_spec_name`, `dataset_name` or `dataset_display_name` are
                not supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Dataset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        column_spec_name = self.__column_spec_name_from_args(
            dataset=dataset,
            dataset_display_name=dataset_display_name,
            dataset_name=dataset_name,
            table_spec_name=table_spec_name,
            table_spec_index=table_spec_index,
            column_spec_name=column_spec_name,
            column_spec_display_name=column_spec_display_name,
            project=project,
            region=region,
            **kwargs
        )
        column_spec_id = column_spec_name.rsplit("/", 1)[-1]

        dataset = self.__dataset_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )
        metadata = dataset.tables_dataset_metadata
        metadata = self.__update_metadata(
            metadata, "ml_use_column_spec_id", column_spec_id
        )

        request = {"name": dataset.name, "tables_dataset_metadata": metadata}

        return self.auto_ml_client.update_dataset(request, **kwargs)

    def clear_test_train_column(
        self,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Clears the test/train (ml_use) column which designates which data
        belongs to the test and train sets.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> client.clear_test_train_column(dataset_display_name='my_dataset')
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to update
                the test/train column of. If no `table_spec_name` is supplied,
                this will be used together with `table_spec_index` to infer the
                name of table to update the test/train column of. This must be
                supplied if `table_spec_name`, `dataset` or `dataset_name` are
                not supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to
                update the test/train column of. If no `table_spec_name` is
                supplied, this will be used together with `table_spec_index` to
                infer the name of table to update the test/train column of.
                This must be supplied if `table_spec_name`, `dataset` or
                `dataset_display_name` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to update the test/train column
                of.  If no `table_spec_name` is supplied, this will be used
                together with `table_spec_index` to infer the name of table to
                update the test/train column of. This must be supplied if
                `table_spec_name`, `dataset_name` or `dataset_display_name` are
                not supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Dataset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        dataset = self.__dataset_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )
        metadata = dataset.tables_dataset_metadata
        metadata = self.__update_metadata(metadata, "ml_use_column_spec_id", None)

        request = {"name": dataset.name, "tables_dataset_metadata": metadata}

        return self.auto_ml_client.update_dataset(request, **kwargs)

    def list_models(self, project=None, region=None, **kwargs):
        """List all models in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> ms = client.list_models()
            >>>
            >>> for m in ms:
            ...     # do something
            ...     pass
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.automl_v1beta1.types.Model`
            instances.  You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        return self.auto_ml_client.list_models(
            self.__location_path(project=project, region=region), **kwargs
        )

    def list_model_evaluations(
        self,
        project=None,
        region=None,
        model=None,
        model_display_name=None,
        model_name=None,
        **kwargs
    ):
        """List all model evaluations for a given model.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> ms = client.list_model_evaluations(model_display_name='my_model')
            >>>
            >>> for m in ms:
            ...     # do something
            ...     pass
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            model_display_name (Optional[string]):
                The human-readable name given to the model you want to list
                evaluations for.  This must be supplied if `model` or
                `model_name` are not supplied.
            model_name (Optional[string]):
                The AutoML-assigned name given to the model you want to list
                evaluations for. This must be supplied if `model_display_name`
                or `model` are not supplied.
            model (Optional[model]):
                The `model` instance you want to list evaluations for. This
                must be supplied if `model_display_name` or `model_name` are
                not supplied.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of
            :class:`~google.cloud.automl_v1beta1.types.ModelEvaluation`
            instances.  You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        model_name = self.__model_name_from_args(
            model=model,
            model_name=model_name,
            model_display_name=model_display_name,
            project=project,
            region=region,
            **kwargs
        )

        return self.auto_ml_client.list_model_evaluations(model_name, **kwargs)

    def create_model(
        self,
        model_display_name,
        dataset=None,
        dataset_display_name=None,
        dataset_name=None,
        train_budget_milli_node_hours=None,
        optimization_objective=None,
        project=None,
        region=None,
        model_metadata={},
        include_column_spec_names=None,
        exclude_column_spec_names=None,
        **kwargs
    ):
        """Create a model. This will train your model on the given dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> m = client.create_model('my_model', dataset_display_name='my_dataset')
            >>>
            >>> m.result() # blocks on result
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            model_display_name (string):
                A human-readable name to refer to this model by.
            train_budget_milli_node_hours (int):
                The amount of time (in thousandths of an hour) to spend
                training. This value must be between 1,000 and 72,000 inclusive
                (between 1 and 72 hours).
            optimization_objective (string):
                The metric AutoML tables should optimize for.
            dataset_display_name (Optional[string]):
                The human-readable name given to the dataset you want to train
                your model on. This must be supplied if `dataset` or
                `dataset_name` are not supplied.
            dataset_name (Optional[string]):
                The AutoML-assigned name given to the dataset you want to train
                your model on. This must be supplied if `dataset_display_name`
                or `dataset` are not supplied.
            dataset (Optional[Dataset]):
                The `Dataset` instance you want to train your model on. This
                must be supplied if `dataset_display_name` or `dataset_name`
                are not supplied.
            model_metadata (Optional[Dict]):
                Optional model metadata to supply to the client.
            include_column_spec_names(Optional[string]):
                The list of the names of the columns you want to include to train
                your model on.
            exclude_column_spec_names(Optional[string]):
                The list of the names of the columns you want to exclude and
                not train your model on.
        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture`
            instance.
        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        if (
            train_budget_milli_node_hours is None
            or train_budget_milli_node_hours < 1000
            or train_budget_milli_node_hours > 72000
        ):
            raise ValueError(
                "'train_budget_milli_node_hours' must be a "
                "value between 1,000 and 72,000 inclusive"
            )

        if exclude_column_spec_names not in [
            None,
            [],
        ] and include_column_spec_names not in [None, []]:
            raise ValueError(
                "Cannot set both "
                "'exclude_column_spec_names' and "
                "'include_column_spec_names'"
            )

        dataset_name = self.__dataset_name_from_args(
            dataset=dataset,
            dataset_name=dataset_name,
            dataset_display_name=dataset_display_name,
            project=project,
            region=region,
            **kwargs
        )

        model_metadata["train_budget_milli_node_hours"] = train_budget_milli_node_hours
        if optimization_objective is not None:
            model_metadata["optimization_objective"] = optimization_objective

        dataset_id = dataset_name.rsplit("/", 1)[-1]
        columns = [
            s
            for s in self.list_column_specs(
                dataset=dataset,
                dataset_name=dataset_name,
                dataset_display_name=dataset_display_name,
                **kwargs
            )
        ]

        final_columns = []
        if include_column_spec_names:
            for c in columns:
                if c.display_name in include_column_spec_names:
                    final_columns.append(c)

            model_metadata["input_feature_column_specs"] = final_columns
        elif exclude_column_spec_names:
            for a in columns:
                if a.display_name not in exclude_column_spec_names:
                    final_columns.append(a)

            model_metadata["input_feature_column_specs"] = final_columns

        request = {
            "display_name": model_display_name,
            "dataset_id": dataset_id,
            "tables_model_metadata": model_metadata,
        }

        op = self.auto_ml_client.create_model(
            self.__location_path(project=project, region=region), request, **kwargs
        )
        self.__log_operation_info("Model creation", op)
        return op

    def delete_model(
        self,
        model=None,
        model_display_name=None,
        model_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Deletes a model. Note this will not delete any datasets associated
        with this model.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> op = client.delete_model(model_display_name='my_model')
            >>>
            >>> op.result() # blocks on delete request
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            model_display_name (Optional[string]):
                The human-readable name given to the model you want to
                delete.  This must be supplied if `model` or `model_name`
                are not supplied.
            model_name (Optional[string]):
                The AutoML-assigned name given to the model you want to
                delete. This must be supplied if `model_display_name` or
                `model` are not supplied.
            model (Optional[model]):
                The `model` instance you want to delete. This must be
                supplied if `model_display_name` or `model_name` are not
                supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture`
            instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        try:
            model_name = self.__model_name_from_args(
                model=model,
                model_name=model_name,
                model_display_name=model_display_name,
                project=project,
                region=region,
                **kwargs
            )
        # delete is idempotent
        except exceptions.NotFound:
            return None

        op = self.auto_ml_client.delete_model(model_name, **kwargs)
        self.__log_operation_info("Delete model", op)
        return op

    def get_model_evaluation(
        self, model_evaluation_name, project=None, region=None, **kwargs
    ):
        """Gets a single evaluation model in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> d = client.get_model_evaluation('my_model_evaluation')
            >>>

        Args:
            model_evaluation_name (string):
                This is the fully-qualified name generated by the AutoML API
                for this model evaluation.
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.ModelEvaluation` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        return self.auto_ml_client.get_model_evaluation(model_evaluation_name, **kwargs)

    def get_model(
        self,
        project=None,
        region=None,
        model_name=None,
        model_display_name=None,
        **kwargs
    ):
        """Gets a single model in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> d = client.get_model(model_display_name='my_model')
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            model_name (Optional[string]):
                This is the fully-qualified name generated by the AutoML API
                for this model. This is not to be confused with the
                human-assigned `model_display_name` that is provided when
                creating a model. Either `model_name` or
                `model_display_name` must be provided.
            model_display_name (Optional[string]):
                This is the name you provided for the model when first
                creating it. Either `model_name` or `model_display_name`
                must be provided.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.Model` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        if model_name is None and model_display_name is None:
            raise ValueError(
                "One of 'model_name' or " "'model_display_name' must be set."
            )

        if model_name is not None:
            return self.auto_ml_client.get_model(model_name, **kwargs)

        return self.__lookup_by_display_name(
            "model", self.list_models(project, region, **kwargs), model_display_name
        )

    # TODO(jonathanskim): allow deployment from just model ID
    def deploy_model(
        self,
        model=None,
        model_name=None,
        model_display_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Deploys a model. This allows you make online predictions using the
        model you've deployed.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> op = client.deploy_model(model_display_name='my_model')
            >>>
            >>> op.result() # blocks on deploy request
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            model_display_name (Optional[string]):
                The human-readable name given to the model you want to
                deploy.  This must be supplied if `model` or `model_name`
                are not supplied.
            model_name (Optional[string]):
                The AutoML-assigned name given to the model you want to
                deploy. This must be supplied if `model_display_name` or
                `model` are not supplied.
            model (Optional[model]):
                The `model` instance you want to deploy. This must be
                supplied if `model_display_name` or `model_name` are not
                supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture`
            instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        model_name = self.__model_name_from_args(
            model=model,
            model_name=model_name,
            model_display_name=model_display_name,
            project=project,
            region=region,
            **kwargs
        )

        op = self.auto_ml_client.deploy_model(model_name, **kwargs)
        self.__log_operation_info("Deploy model", op)
        return op

    def undeploy_model(
        self,
        model=None,
        model_name=None,
        model_display_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Undeploys a model.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> op = client.undeploy_model(model_display_name='my_model')
            >>>
            >>> op.result() # blocks on undeploy request
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            model_display_name (Optional[string]):
                The human-readable name given to the model you want to
                undeploy.  This must be supplied if `model` or `model_name`
                are not supplied.
            model_name (Optional[string]):
                The AutoML-assigned name given to the model you want to
                undeploy. This must be supplied if `model_display_name` or
                `model` are not supplied.
            model (Optional[model]):
                The `model` instance you want to undeploy. This must be
                supplied if `model_display_name` or `model_name` are not
                supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture`
            instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        model_name = self.__model_name_from_args(
            model=model,
            model_name=model_name,
            model_display_name=model_display_name,
            project=project,
            region=region,
            **kwargs
        )

        op = self.auto_ml_client.undeploy_model(model_name, **kwargs)
        self.__log_operation_info("Undeploy model", op)
        return op

    ## TODO(lwander): support pandas DataFrame as input type
    def predict(
        self,
        inputs,
        model=None,
        model_name=None,
        model_display_name=None,
        project=None,
        region=None,
        **kwargs
    ):
        """Makes a prediction on a deployed model. This will fail if the model
        was not deployed.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> client.predict(inputs={'Age': 30, 'Income': 12, 'Category': 'A'}
            ...     model_display_name='my_model')
            ...
            >>> client.predict([30, 12, 'A'], model_display_name='my_model')
            >>>

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            inputs (Union[List[string], Dict[string, string]]):
                Either the sorted list of column values to predict with, or a
                key-value map of column display name to value to predict with.
            model_display_name (Optional[string]):
                The human-readable name given to the model you want to predict
                with.  This must be supplied if `model` or `model_name` are not
                supplied.
            model_name (Optional[string]):
                The AutoML-assigned name given to the model you want to predict
                with. This must be supplied if `model_display_name` or `model`
                are not supplied.
            model (Optional[model]):
                The `model` instance you want to predict with . This must be
                supplied if `model_display_name` or `model_name` are not
                supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types.PredictResponse`
            instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        model = self.__model_from_args(
            model=model,
            model_name=model_name,
            model_display_name=model_display_name,
            project=project,
            region=region,
            **kwargs
        )

        column_specs = model.tables_model_metadata.input_feature_column_specs
        if type(inputs) == dict:
            inputs = [inputs.get(c.display_name, None) for c in column_specs]

        if len(inputs) != len(column_specs):
            raise ValueError(
                (
                    "Dimension mismatch, the number of provided "
                    "inputs ({}) does not match that of the model "
                    "({})"
                ).format(len(inputs), len(column_specs))
            )

        values = []
        for i, c in zip(inputs, column_specs):
            value_type = self.__type_code_to_value_type(c.data_type.type_code, i)
            values.append(value_type)

        request = {"row": {"values": values}}

        return self.prediction_client.predict(model.name, request, **kwargs)

    def batch_predict(
        self,
        bigquery_input_uri=None,
        bigquery_output_uri=None,
        gcs_input_uris=None,
        gcs_output_uri_prefix=None,
        model=None,
        model_name=None,
        model_display_name=None,
        project=None,
        region=None,
        inputs=None,
        **kwargs
    ):
        """Makes a batch prediction on a model. This does _not_ require the
        model to be deployed.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> from google.oauth2 import service_account
            >>>
            >>> client = automl_v1beta1.TablesClient(
            ...     credentials=service_account.Credentials.from_service_account_file('~/.gcp/account.json')
            ...     project='my-project', region='us-central1')
            ...
            >>> client.batch_predict(
            ...     gcs_input_uris='gs://inputs/input.csv',
            ...     gcs_output_uri_prefix='gs://outputs/',
            ...     model_display_name='my_model'
            ...  ).result()
            ...

        Args:
            project (Optional[string]):
                If you have initialized the client with a value for `project`
                it will be used if this parameter is not supplied. Keep in
                mind, the service account this client was initialized with must
                have access to this project.
            region (Optional[string]):
                If you have initialized the client with a value for `region` it
                will be used if this parameter is not supplied.
            gcs_input_uris (Optional(Union[List[string], string]))
                Either a list of or a single GCS URI containing the data you
                want to predict off of.
            gcs_output_uri_prefix (Optional[string])
                The folder in GCS you want to write output to.
            bigquery_input_uri (Optional[string])
                The BigQuery table to input data from.
            bigquery_output_uri (Optional[string])
                The BigQuery table to output data to.
            model_display_name (Optional[string]):
                The human-readable name given to the model you want to predict
                with.  This must be supplied if `model` or `model_name` are not
                supplied.
            model_name (Optional[string]):
                The AutoML-assigned name given to the model you want to predict
                with. This must be supplied if `model_display_name` or `model`
                are not supplied.
            model (Optional[model]):
                The `model` instance you want to predict with . This must be
                supplied if `model_display_name` or `model_name` are not
                supplied.

        Returns:
            A :class:`~google.cloud.automl_v1beta1.types._OperationFuture`
            instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        model_name = self.__model_name_from_args(
            model=model,
            model_name=model_name,
            model_display_name=model_display_name,
            project=project,
            region=region,
            **kwargs
        )

        input_request = None
        if gcs_input_uris is not None:
            if type(gcs_input_uris) != list:
                gcs_input_uris = [gcs_input_uris]
            input_request = {"gcs_source": {"input_uris": gcs_input_uris}}
        elif bigquery_input_uri is not None:
            input_request = {"bigquery_source": {"input_uri": bigquery_input_uri}}
        else:
            raise ValueError(
                "One of 'gcs_input_uris'/'bigquery_input_uris' must" "be set"
            )

        output_request = None
        if gcs_output_uri_prefix is not None:
            output_request = {
                "gcs_destination": {"output_uri_prefix": gcs_output_uri_prefix}
            }
        elif bigquery_output_uri is not None:
            output_request = {
                "bigquery_destination": {"output_uri": bigquery_output_uri}
            }
        else:
            raise ValueError(
                "One of 'gcs_output_uri_prefix'/'bigquery_output_uri' must be set"
            )

        op = self.prediction_client.batch_predict(
            model_name, input_request, output_request, **kwargs
        )
        self.__log_operation_info("Batch predict", op)
        return op
