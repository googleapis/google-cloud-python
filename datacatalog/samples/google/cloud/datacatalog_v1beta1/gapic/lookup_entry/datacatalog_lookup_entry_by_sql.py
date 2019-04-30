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

# DO NOT EDIT! This is a generated sample ("Request",  "datacatalog_lookup_entry_by_sql")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-datacatalog

import sys

# [START datacatalog_lookup_entry_by_sql]

from google.cloud import datacatalog_v1beta1
from google.cloud.datacatalog_v1beta1 import enums


def sample_lookup_entry():
    """Get a Data Catalog entry for a resource by SQL identifier."""
    # [START datacatalog_lookup_entry_by_sql_core]

    client = datacatalog_v1beta1.DataCatalogClient()

    sql_resource = 'bigquery.`bigquery-public-data`.stackoverflow.posts_questions'

    response = client.lookup_entry(sql_resource=sql_resource)
    print('linked_resource: {}'.format(response.linked_resource))
    print('type: {}'.format(enums.EntryType(response.type).name))
    print('Schema:')
    for column in response.schema.columns:
        print('\t{}\t({} {})'.format(column.column, column.mode, column.type))

    # [END datacatalog_lookup_entry_by_sql_core]


# [END datacatalog_lookup_entry_by_sql]


def main():
    sample_lookup_entry()


if __name__ == '__main__':
    main()
