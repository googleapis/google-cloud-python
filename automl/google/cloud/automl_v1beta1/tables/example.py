import argparse
import random
import string

# change to the correct import in the future, after the PR goes through
# to the public client library
import sys

import os

from google.cloud.automl_v1beta1.tables import tables_client

path = (
    "/Users/jonathanskim/Desktop/valiant-healer-197219-5853495a202b.json"
)  # @param {type:'string'}
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

client_autoML = tables_client.TablesClient(
    project="valiant-healer-197219", region="us-central1"
)

# rand_id = ''.join([random.choice(string.ascii_letters + string.digits)
#     for n in range(16)])

# print('Listing datasets...')
# list_datasets = client.list_datasets()
# list_datasets = [d for d in list_datasets]
# print(list_datasets)

# print('Creating a dataset...')
# dataset = client.create_dataset('my_dataset_{}'.format(rand_id))
# print(dataset)

# print('Import data...')
# import_data = dataset.import_data(
#         gcs_input_uris='gs://cloud-ml-tables-data/bank-marketing.csv')

# print('Waiting on import to complete...')
# print(import_data.result())

# print('Getting table specs...')
# table_specs = client.list_table_specs(dataset=dataset)
# table_specs = [s for s in table_specs]
# print(table_specs)

# print('Getting column specs...')
# column_specs = client.list_column_specs(dataset=dataset)
# column_specs = {s.display_name: s for s in column_specs}
# print(column_specs)

# print('Updating column data type...')
# print(client.update_column_spec(dataset=dataset,
#         column_spec_display_name='Job',
#         type_code='CATEGORY'))
# dataset_display_name = 'timeseries'


# print('Setting time column...')
# print(client.set_time_column(dataset_display_name=dataset_display_name,
#          column_spec_display_name='Time'))

# print('Setting target column...')
# client.set_target_column(dataset_display_name=dataset_display_name,
#          column_spec_display_name='HotelsOccupancyrate')

# print('Creating model...')
# create_model = client.create_model('client_example_model', dataset_display_name=dataset_display_name,
#         train_budget_milli_node_hours=1000)
# print('Waiting on training to complete...')
# print(create_model.result())

# print('Listing models...')
# list_models = client.list_models()
# list_models = [m for m in list_models]
# print(list_models)

name = "projects/205653483848/locations/us-central1/models/TBL5737858604153700352"

client_autoML.display_model_evaluation(model_name=name)

# print('Deploying our model...')
# deploy_model = client.deploy_model(model_name = name)
# print('Waiting on deploy to complete...')
# print(deploy_model.result())

# print('Making a predicition...')
# print(client.make_prediction(model=model, inputs={
#     'Age': 31,
#     'Balance': 200,
#     'Campaign': 2,
#     'Contact': 'cellular',
#     'Day': 4,
#     'Default': 'no',
#     'Duration': 12,
#     'Education': 'primary',
#     'Housing': 'yes',
#     'Job': 'blue-collar',
#     'Loan': 'no',
#     'MaritalStatus': 'divorced',
#     'Month': 'jul',
#     'PDays': 4,
#     'POutcome': 'unknown',
#     'Previous': 12
# }))

# print('Undeploying model...')
# print(client.undeploy_model(model=model))

# print('Deleting model...')
# print(client.delete_model(model=model))

# print('Deleting model...')
# print(client.delete_model(model=model))

# print('Deleting dataset...')
# print(client.delete_dataset(dataset=dataset))
