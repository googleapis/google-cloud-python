# Copyright 2019 Google Inc. All Rights Reserved.
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

"""A helper for the google.cloud.automl_v1beta1 AutoML Tables API"""

from google.cloud.automl_v1beta1.proto import data_types_pb2

class ClientHelper(object):
    """
    AutoML Server API helper.

    This is intended to simplify usage of the auto-generated python client,
    in particular for the `AutoML Tables product
    <https://cloud.google.com/automl-tables/>`_.
    """
    def __init__(self, client=None, prediction_client=None, project=None,
            region='us-central1'):
        """Constructor.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
            ...     prediction_client=automl_v1beta1.PredictionServiceClient(),
            ...     project='my-project', region='us-central1')
            ...

        Args:
            client (Optional[google.cloud.automl.v1beta1.AutoMlClient]): An
                initialized AutoMLClient instance. This parameter is optional;
                however, if you expect to make CRUD operations on either
                models or datasets, this parameter needs to be set.
                Additionally, if you want to make online predictions without
                supplying a column schema, this client is during prediction.
            prediction_client (Optional[google.cloud.automl.v1beta1.PredictionServiceClient]):
                An initialized PredicitonServiceClient instance. This parameter
                is optional; however, if you expect to make predictions, this
                parameter needs to be set.
            project (Optional[string]): The project all future calls will
                default to. Most methods take `project` as an optional
                parameter, and can override your choice of `project` supplied
                here.
            region (Optional[string]): The reigon all future calls will
                default to. Most methods take `region` as an optional
                parameter, and can override your choice of `region` supplied
                here. Note, only `us-central1` is supported to-date.
        """
        self.client = client
        self.prediction_client = prediction_client
        self.project = project
        self.region = region

    def __location_path(self, project=None, region=None):
        if project is None:
            if self.project is None:
                raise ValueError('Either initialize your client with a value '
                        'for \'project\', or provide \'project\' as a '
                        'parameter for this method.')
            project = self.project

        if region is None:
            if self.region is None:
                raise ValueError('Either initialize your client with a value '
                        'for \'region\', or provide \'region\' as a '
                        'parameter for this method.')
            region = self.region

        return self.client.location_path(project, region)

    def __dataset_name_from_args(self, dataset=None, dataset_display_name=None,
            dataset_name=None, project=None, region=None):
        if (dataset is None
                and dataset_display_name is None
                and dataset_name is None):
            raise ValueError('One of \'dataset\', \'dataset_name\' or '
                    '\'dataset_display_name\' must be set.')

        if dataset_name is None:
            if dataset is None:
                dataset = self.get_dataset(
                        dataset_display_name=dataset_display_name,
                        project=project,
                        region=region
                )
            dataset_name = dataset.name
        return dataset_name

    def __model_name_from_args(self, model=None, model_display_name=None,
            model_name=None, project=None, region=None):
        if (model is None
                and model_display_name is None
                and model_name is None):
            raise ValueError('One of \'model\', \'model_name\' or '
                    '\'model_display_name\' must be set.')

        if model_name is None:
            if model is None:
                model = self.get_model(
                        model_display_name=dataset_display_name,
                        project=project,
                        region=region
                )
            model_name = model.name
        return model_name

    def __column_spec_name_from_args(self, dataset=None, dataset_display_name=None,
            dataset_name=None, table_spec_name=None, table_spec_index=0,
            column_spec_name=None, column_spec_display_name=None,
            project=None, region=None):
        if column_spec_name is None:
            if column_spec_display_name is None:
                raise ValueError('Either supply \'column_spec_name\' or '
                        '\'column_spec_display_name\' for the column to update')
            column_specs = {s.display_name: s for s in
                    self.list_column_specs(dataset=dataset,
                        dataset_display_name=dataset_display_name,
                        dataset_name=dataset_name,
                        table_spec_name=table_spec_name,
                        table_spec_index=table_spec_index,
                        project=project,
                        region=region)
            }
            column_spec_name = column_specs[column_spec_display_name].name
        return column_spec_name

    ## TODO(lwander): what other type codes are there?
    ## https://github.com/googleapis/google-cloud-python/blob/master/automl/google/cloud/automl_v1beta1/proto/data_types_pb2.py#L87-L92
    def __type_code_to_value_type(self, type_code):
        if type_code == data_types_pb2.FLOAT64:
            return 'number_value'
        if type_code == data_types_pb2.CATEGORY:
            return 'string_value'
        else:
            raise ValueError('Unknown type_code: {}'.format(type_code))

    def list_datasets(self, project=None, region=None):
        """List all datasets in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
        return self.client.list_datasets(
                    self.__location_path(project=project, region=region)
                )

    def get_dataset(self, project=None, region=None,
            dataset_name=None, dataset_display_name=None):
        """Gets a single dataset in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
            A :class:`~google.cloud.automl_v1beta1.types.Dataset` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                to a retryable error and retry attempts failed.
            ValueError: If required parameters are missing.
        """
        if dataset_name is None and dataset_display_name is None:
            raise ValueError('One of \'dataset_name\' or '
                    '\'dataset_display_name\' must be set.')

        if dataset_name is not None:
            return client.get_dataset(dataset_name)

        return next(d for d in self.list_datasets(project, region)
                if d.display_name == dataset_display_name)

    ## TODO(lwander): is metadata needed here?
    def create_dataset(self, dataset_display_name, metadata={}, project=None,
            region=None):
        """Create a dataset. Keep in mind, importing data is a separate step.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
        return self.client.create_dataset(
                    self.__location_path(project, region),
                    {
                        'display_name': dataset_display_name,
                        'tables_dataset_metadata': metadata
                    }
                )

    def delete_dataset(self, dataset=None, dataset_display_name=None,
            dataset_name=None, project=None, region=None):
        """Deletes a dataset. This does not delete any models trained on
        this dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
        dataset_name = self.__dataset_name_from_args(dataset=dataset,
                dataset_name=dataset_name,
                dataset_display_name=dataset_display_name,
                project=project,
                region=region)

        return self.client.delete_dataset(dataset_name)

    ## TODO(lwander): why multiple input GCS files? why not bq?
    def import_data(self, dataset=None, dataset_display_name=None,
            dataset_name=None, gcs_input_uris=None,
            bigquery_input_uri=None, project=None, region=None):
        """Imports data into a dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
        dataset_name = self.__dataset_name_from_args(dataset=dataset,
                dataset_name=dataset_name,
                dataset_display_name=dataset_display_name,
                project=project,
                region=region)

        request = {}
        if gcs_input_uris is not None:
            if type(gcs_input_uris) != list:
                gcs_input_uris = [gcs_input_uris]
            request = {
                    'gcs_source': {
                        'input_uris': gcs_input_uris
                    }
            }
        elif bigquery_input_uri is not None:
            request = {
                    'bigquery_source': {
                        'input_uri': bigquery_input_uri
                    }
            }
        else:
            raise ValueError('One of \'gcs_input_uris\', or '
                    '\'bigquery_input_uri\' must be set.')

        return self.client.import_data(dataset_name, request)

    def list_table_specs(self, dataset=None, dataset_display_name=None,
            dataset_name=None, project=None, region=None):
        """Lists table specs.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
        dataset_name = self.__dataset_name_from_args(dataset=dataset,
                dataset_name=dataset_name,
                dataset_display_name=dataset_display_name,
                project=project,
                region=region)

        return self.client.list_table_specs(dataset_name)

    def list_column_specs(self, dataset=None, dataset_display_name=None,
            dataset_name=None, table_spec_name=None, table_spec_index=0,
            project=None, region=None):
        """Lists column specs.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
            table_specs = [t for t in self.list_table_specs(dataset=dataset,
                    dataset_display_name=dataset_display_name,
                    dataset_name=dataset_name,
                    project=project,
                    region=region)]

            table_spec_name = table_specs[table_spec_index].name

        return self.client.list_column_specs(table_spec_name)

    def update_column_spec(self, dataset=None, dataset_display_name=None,
            dataset_name=None, table_spec_name=None, table_spec_index=0,
            column_spec_name=None, column_spec_display_name=None,
            type_code=None, nullable=None, project=None, region=None):
        """Updates a column's specs.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
                region=region
        )

        # type code must always be set
        if type_code is None:
            type_code = {s.name: s for s in self.list_column_specs(
                    dataset=dataset,
                    dataset_display_name=dataset_display_name,
                    dataset_name=dataset_name,
                    table_spec_name=table_spec_name,
                    table_spec_index=table_spec_index,
                    project=project,
                    region=region)
            }[column_spec_name].data_type.type_code

        data_type = {}
        if nullable is not None:
            data_type['nullable'] = nullable

        data_type['type_code'] = type_code

        request = {
                'name': column_spec_name,
                'data_type': data_type
        }

        return self.client.update_column_spec(request)

    def set_target_column(self, dataset=None, dataset_display_name=None,
            dataset_name=None, table_spec_name=None, table_spec_index=0,
            column_spec_name=None, column_spec_display_name=None,
            project=None, region=None):
        """Sets the target column for a given table.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
                region=region
        )
        column_spec_id = column_spec_name.rsplit('/', 1)[-1]

        dataset_name = self.__dataset_name_from_args(dataset=dataset,
                dataset_name=dataset_name,
                dataset_display_name=dataset_display_name,
                project=project,
                region=region)

        request = {
                'name': dataset_name,
                'tables_dataset_metadata': {
                    'target_column_spec_id': column_spec_id
                }
        }

        return self.client.update_dataset(request)

    def set_weight_column(self, dataset=None, dataset_display_name=None,
            dataset_name=None, table_spec_name=None, table_spec_index=0,
            column_spec_name=None, column_spec_display_name=None,
            project=None, region=None):
        """Sets the weight column for a given table.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
                region=region
        )
        column_spec_id = column_spec_name.rsplit('/', 1)[-1]

        dataset_name = self.__dataset_name_from_args(dataset=dataset,
                dataset_name=dataset_name,
                dataset_display_name=dataset_display_name,
                project=project,
                region=region)

        request = {
                'name': dataset_name,
                'tables_dataset_metadata': {
                    'weight_column_spec_id': column_spec_id
                }
        }

        return self.client.update_dataset(request)

    def set_test_train_column(self, dataset=None, dataset_display_name=None,
            dataset_name=None, table_spec_name=None, table_spec_index=0,
            column_spec_name=None, column_spec_display_name=None,
            project=None, region=None):
        """Sets the test/train (ml_use) column which designates which data
        belongs to the test and train sets. This column must be categorical.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
                region=region
        )
        column_spec_id = column_spec_name.rsplit('/', 1)[-1]

        dataset_name = self.__dataset_name_from_args(dataset=dataset,
                dataset_name=dataset_name,
                dataset_display_name=dataset_display_name,
                project=project,
                region=region)

        request = {
                'name': dataset_name,
                'tables_dataset_metadata': {
                    'ml_use_column_spec_id': column_spec_id
                }
        }

        return self.client.update_dataset(request)

    def list_models(self, project=None, region=None):
        """List all models in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
        return self.client.list_models(
                self.__location_path(project=project, region=region)
        )

    def create_model(self, model_display_name, dataset=None,
            dataset_display_name=None, dataset_name=None,
            train_budget_milli_node_hours=None, project=None,
            region=None, input_feature_column_specs_included=None, input_feature_column_specs_excluded=None):
    	"""Create a model. This will train your model on the given dataset.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
            input_feature_column_specs_included(Optional[string]):
            	The list of the names of the columns you want to include to train 
            	your model on.
            input_feature_column_specs_excluded(Optional[string]):
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
        if train_budget_milli_node_hours is None:
            raise ValueError('\'train_budget_milli_node_hours\' must be a '
                    'value between 1,000 and 72,000 inclusive')

        if input_feature_column_specs_excluded not in [None, []] and input_feature_column_specs_included not in [None, []]:
            raise ValueError('\'cannot set both input_feature_column_specs_excluded\' and '
                    '\'input_feature_column_specs_included\'')


        dataset_name = self.__dataset_name_from_args(dataset=dataset,
                dataset_name=dataset_name,
                dataset_display_name=dataset_display_name,
                project=project,
                region=region)
        tables_model_metadata = {
                'train_budget_milli_node_hours': train_budget_milli_node_hours
        }
        dataset_id = dataset_name.rsplit('/', 1)[-1]
        columns = [s for s in self.list_column_specs(dataset=dataset, dataset_name = dataset_name, dataset_display_name=dataset_display_name)]

        final_columns = []
        if input_feature_column_specs_included:
        	column_names = [a.display_name for a in columns]
        	if not (all (name in column_names for name in input_feature_column_specs_included)):
        		raise ValueError('invalid name in the list' '\'input_feature_column_specs_included\'')
            for a in columns:
                if a.display_name in input_feature_column_specs_included:
                    final_columns.append(a)

            tables_model_metadata.update(
                {'input_feature_column_specs': final_columns}
            )
        elif input_feature_column_specs_excluded:
            for a in columns:
                if a.display_name not in input_feature_column_specs_excluded:
                    final_columns.append(a)

            tables_model_metadata.update(
                 {'input_feature_column_specs': final_columns}
            )

        request = {
                'display_name': model_display_name,
                'dataset_id': dataset_id,
                'tables_model_metadata': tables_model_metadata
        }


        return self.client.create_model(
                self.__location_path(project=project, region=region),
                request
        )


    def delete_model(self, model=None, model_display_name=None,
            model_name=None, project=None, region=None):
        """Deletes a model. Note this will not delete any datasets associated
        with this model.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
        model_name = self.__model_name_from_args(model=model,
                model_name=model_name,
                model_display_name=model_display_name,
                project=project,
                region=region)

        return self.client.delete_model(model_name)

    def get_model(self, project=None, region=None,
            model_name=None, model_display_name=None):
        """Gets a single model in a particular project and region.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
            raise ValueError('One of \'model_name\' or '
                    '\'model_display_name\' must be set.')

        return next(m for m in self.list_models(project, region)
                if m.name == model_name
                or m.display_name == model_display_name)

    #TODO(jonathanskim): allow deployment from just model ID
    def deploy_model(self, model=None, model_name=None,
            model_display_name=None, project=None, region=None):
        """Deploys a model. This allows you make online predictions using the
        model you've deployed.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
                region=region
        )

        return self.client.deploy_model(model_name)

    def undeploy_model(self, model=None, model_name=None,
            model_display_name=None, project=None, region=None):
        """Undeploys a model.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     client=automl_v1beta1.AutoMlClient(),
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
                region=region
        )

        return self.client.undeploy_model(model_name)

    ## TODO(lwander): support pandas DataFrame as input type
    def predict(self, inputs, model=None, model_name=None,
            model_display_name=None, project=None, region=None):
        """Makes a prediction on a deployed model. This will fail if the model
        was not deployed.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     prediction_client=automl_v1beta1.PredictionServiceClient(),
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
        if model is None:
            model = self.get_model(
                    model_name=model_name,
                    model_display_name=model_display_name,
                    project=project,
                    region=region
            )

        column_specs = model.tables_model_metadata.input_feature_column_specs
        if type(inputs) == dict:
            inputs = [inputs.get(c.display_name, None) for c in column_specs]

        if len(inputs) != len(column_specs):
            raise ValueError(('Dimension mismatch, the number of provided '
                    'inputs ({}) does not match that of the model '
                    '({})').format(
                        len(inputs), len(column_specs)))

        values = []
        for i, c in zip(inputs, column_specs):
            value_type = self.__type_code_to_value_type(c.data_type.type_code)
            values.append({value_type: i})

        request = {
                'row': {
                    'values': values
                }
        }

        return self.prediction_client.predict(model.name, request)

    def batch_predict(self, gcs_input_uris, gcs_output_uri_prefix,
            model=None, model_name=None, model_display_name=None, project=None,
            region=None, inputs=None):
        """Makes a batch prediction on a model. This does _not_ require the
        model to be deployed.

        Example:
            >>> from google.cloud import automl_v1beta1
            >>>
            >>> client = automl_v1beta1.tables.ClientHelper(
            ...     prediction_client=automl_v1beta1.PredictionServiceClient(),
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
            gcs_input_uris (Union[List[string], string])
                Either a list of or a single GCS URI containing the data you
                want to predict off of.
            gcs_output_uri_prefix (string)
                The folder in GCS you want to write output to.
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
        if gcs_input_uris is None or gcs_output_uri_prefix is None:
            raise ValueError('Both \'gcs_input_uris\' and '
                '\'gcs_output_uri_prefix\' must be set.')

        model_name = self.__model_name_from_args(
                model=model,
                model_name=model_name,
                model_display_name=model_display_name,
                project=project,
                region=region
        )

        if type(gcs_input_uris) != list:
            gcs_input_uris = [gcs_input_uris]

        input_request = {
                'gcs_source': {
                    'input_uris': gcs_input_uris
                }
        }

        output_request = {
                'gcs_source': {
                    'output_uri_prefix': gcs_output_uri_prefix
                }
        }

        return self.prediction_client.batch_predict(model_name, input_request,
                output_request)
