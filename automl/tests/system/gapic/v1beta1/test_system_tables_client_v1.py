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

import os
import pandas
import pytest
import random
import string
import time
import unittest

from google.cloud import automl_v1beta1
from google.api_core import exceptions
from google.cloud.automl_v1beta1.gapic import enums

PROJECT = os.environ["PROJECT_ID"]
REGION = "us-central1"
MAX_WAIT_TIME_SECONDS = 30
MAX_SLEEP_TIME_SECONDS = 5
STATIC_DATASET = "test_dataset_do_not_delete"
STATIC_MODEL = "test_model_do_not_delete"
RUNNING_IN_VPCSC = os.getenv("GOOGLE_CLOUD_TESTS_IN_VPCSC", "").lower() == "true"

ID = "{rand}_{time}".format(
    rand="".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(4)]
    ),
    time=int(time.time()),
)


def _id(name):
    return "{}_{}".format(name, ID)


class TestSystemTablesClient(object):
    def cancel_and_wait(self, op):
        op.cancel()
        start = time.time()
        sleep_time = 1
        while time.time() - start < MAX_WAIT_TIME_SECONDS:
            if op.cancelled():
                return
            time.sleep(sleep_time)
            sleep_time = min(sleep_time * 2, MAX_SLEEP_TIME_SECONDS)
        assert op.cancelled()

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_list_datasets(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        dataset = self.ensure_dataset_ready(client)
        # will raise if not found
        next(
            iter(
                [d for d in client.list_datasets(timeout=10) if d.name == dataset.name]
            )
        )

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_list_models(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        model = self.ensure_model_ready(client)
        # will raise if not found
        next(iter([m for m in client.list_models(timeout=10) if m.name == model.name]))

    def test_create_delete_dataset(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        display_name = _id("t_cr_dl")
        dataset = client.create_dataset(display_name)
        assert dataset is not None
        assert (
            dataset.name == client.get_dataset(dataset_display_name=display_name).name
        )
        client.delete_dataset(dataset=dataset)

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_import_data(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        display_name = _id("t_import")
        dataset = client.create_dataset(display_name)
        op = client.import_data(
            dataset=dataset,
            gcs_input_uris="gs://cloud-ml-tables-data/bank-marketing.csv",
        )
        self.cancel_and_wait(op)
        client.delete_dataset(dataset=dataset)

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_import_pandas_dataframe(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        display_name = _id("t_import_pandas")
        dataset = client.create_dataset(display_name)
        dataframe = pandas.DataFrame({"test-col1": [1, 2], "test-col2": [3, 4]})
        op = client.import_data(
            project=PROJECT, dataset=dataset, pandas_dataframe=dataframe
        )
        self.cancel_and_wait(op)
        client.delete_dataset(dataset=dataset)

    def ensure_dataset_ready(self, client):
        dataset = None
        try:
            dataset = client.get_dataset(dataset_display_name=STATIC_DATASET)
        except exceptions.NotFound:
            dataset = client.create_dataset(STATIC_DATASET)

        if dataset.example_count is None or dataset.example_count == 0:
            op = client.import_data(
                dataset=dataset,
                gcs_input_uris="gs://cloud-ml-tables-data/bank-marketing.csv",
            )
            op.result()
            dataset = client.get_dataset(dataset_name=dataset.name)

        return dataset

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_list_column_specs(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        dataset = self.ensure_dataset_ready(client)
        # will raise if not found
        next(
            iter(
                [
                    d
                    for d in client.list_column_specs(dataset=dataset)
                    if d.display_name == "Deposit"
                ]
            )
        )

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_get_column_spec(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        dataset = self.ensure_dataset_ready(client)
        name = [d for d in client.list_column_specs(dataset=dataset)][0].name
        assert client.get_column_spec(name).name == name

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_list_table_specs(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        dataset = self.ensure_dataset_ready(client)
        name = [d for d in client.list_table_specs(dataset=dataset)][0].name
        assert client.get_table_spec(name).name == name

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_set_column_nullable(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        dataset = self.ensure_dataset_ready(client)
        client.update_column_spec(
            dataset=dataset, column_spec_display_name="POutcome", nullable=True
        )
        columns = {c.display_name: c for c in client.list_column_specs(dataset=dataset)}
        assert columns["POutcome"].data_type.nullable == True

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_set_target_column(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        dataset = self.ensure_dataset_ready(client)
        client.set_target_column(dataset=dataset, column_spec_display_name="Age")
        columns = {c.display_name: c for c in client.list_column_specs(dataset=dataset)}
        dataset = client.get_dataset(dataset_name=dataset.name)
        metadata = dataset.tables_dataset_metadata
        assert columns["Age"].name.endswith(
            "/{}".format(metadata.target_column_spec_id)
        )

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_set_weight_column(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        dataset = self.ensure_dataset_ready(client)
        client.set_weight_column(dataset=dataset, column_spec_display_name="Duration")
        columns = {c.display_name: c for c in client.list_column_specs(dataset=dataset)}
        dataset = client.get_dataset(dataset_name=dataset.name)
        metadata = dataset.tables_dataset_metadata
        assert columns["Duration"].name.endswith(
            "/{}".format(metadata.weight_column_spec_id)
        )

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_set_weight_and_target_column(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        dataset = self.ensure_dataset_ready(client)
        client.set_weight_column(dataset=dataset, column_spec_display_name="Day")
        client.set_target_column(dataset=dataset, column_spec_display_name="Campaign")
        columns = {c.display_name: c for c in client.list_column_specs(dataset=dataset)}
        dataset = client.get_dataset(dataset_name=dataset.name)
        metadata = dataset.tables_dataset_metadata
        assert columns["Day"].name.endswith(
            "/{}".format(metadata.weight_column_spec_id)
        )
        assert columns["Campaign"].name.endswith(
            "/{}".format(metadata.target_column_spec_id)
        )

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_create_delete_model(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        dataset = self.ensure_dataset_ready(client)
        client.set_target_column(dataset=dataset, column_spec_display_name="Deposit")
        display_name = _id("t_cr_dl")
        op = client.create_model(
            display_name, dataset=dataset, train_budget_milli_node_hours=1000
        )
        self.cancel_and_wait(op)
        client.delete_model(model_display_name=display_name)

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_list_model_evaluations(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        model = self.ensure_model_online(client)
        # will raise if not found
        next(
            iter(
                [
                    m
                    for m in client.list_model_evaluations(model=model)
                    if m.display_name is not None
                ]
            )
        )

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_get_model_evaluation(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        model = self.ensure_model_online(client)
        name = [m for m in client.list_model_evaluations(model=model)][0].name
        assert client.get_model_evaluation(model_evaluation_name=name).name == name

    @unittest.skipIf(RUNNING_IN_VPCSC, "Test is not VPCSC compatible.")
    def test_online_predict(self):
        client = automl_v1beta1.TablesClient(project=PROJECT, region=REGION)
        model = self.ensure_model_online(client)
        result = client.predict(
            inputs={
                "Age": 31,
                "Balance": 200,
                "Campaign": 2,
                "Contact": "cellular",
                "Day": 4,
                "Default": "no",
                "Duration": 12,
                "Education": "primary",
                "Housing": "yes",
                "Job": "blue-collar",
                "Loan": "no",
                "MaritalStatus": "divorced",
                "Month": "jul",
                "PDays": 4,
                "POutcome": None,
                "Previous": 12,
            },
            model=model,
        )
        assert result is not None

    def ensure_model_online(self, client):
        model = self.ensure_model_ready(client)
        if model.deployment_state != enums.Model.DeploymentState.DEPLOYED:
            client.deploy_model(model=model).result()

        return client.get_model(model_name=model.name)

    def ensure_model_ready(self, client):
        try:
            return client.get_model(model_display_name=STATIC_MODEL)
        except exceptions.NotFound:
            pass

        dataset = self.ensure_dataset_ready(client)
        client.set_target_column(dataset=dataset, column_spec_display_name="Deposit")
        client.clear_weight_column(dataset=dataset)
        client.clear_test_train_column(dataset=dataset)
        client.update_column_spec(
            dataset=dataset, column_spec_display_name="POutcome", nullable=True
        )
        op = client.create_model(
            STATIC_MODEL, dataset=dataset, train_budget_milli_node_hours=1000
        )
        op.result()
        return client.get_model(model_display_name=STATIC_MODEL)
