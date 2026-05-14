# Copyright 2026 Google LLC
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

"""Helper to turn string references into REST resources."""

# TODO(b/513204277): Consolidate these transformations with pandas-gbq and bigframes.

import typing

from google.cloud.bigquery import _helpers


ParsedDatasetReference = typing.TypedDict(
    'ParsedDatasetReference',
    {
        "projectId": str,
        "datasetId": str,
    }
)


ParsedTableReference = typing.TypedDict(
    'ParsedTableReference',
    {
        "projectId": str,
        "datasetId": str,
        "tableId": str,
    }
)


def parse_dataset_reference(dataset_id: str, *, default_project: str | None) -> ParsedDatasetReference:
        """Parse a dataset ID string.

        Returns:
            ParsedDatasetReference: A typed dictionary (to avoid circular dependencies).
        
        Raises:
            ValueError: When a fully-qualified dataset ID can't be determined.
        """
        output_dataset_id = dataset_id
        parts = _helpers._split_id(dataset_id)

        if len(parts) == 1:
            if default_project is not None:
                output_project_id = default_project
            else:
                raise ValueError(
                    "When default_project is not set, dataset_id must be a "
                    "fully-qualified dataset ID in standard SQL format, "
                    'e.g., "project.dataset_id" got {}'.format(dataset_id)
                )
        elif len(parts) == 2:
            output_project_id, output_dataset_id = parts
        else:
            raise ValueError(
                "Too many parts in dataset_id. Expected a fully-qualified "
                "dataset ID in standard SQL format, "
                'e.g. "project.dataset_id", got {}'.format(dataset_id)
            )
        
        return {"datasetId": output_dataset_id, "projectId": output_project_id}


def parse_table_reference(table_id: str, *, default_project: str | None) -> ParsedTableReference:
        """Parse a table ID string.

        Returns:
            ParsedTableReference: A typed dictionary (to avoid circular dependencies).
        
        Raises:
            ValueError: When a fully-qualified table ID can't be determined.
        """
        (
            output_project_id,
            output_dataset_id,
            output_table_id,
        ) = _helpers._parse_3_part_id(
            table_id, default_project=default_project, property_name="table_id"
        )

        if output_project_id is None:
            raise ValueError(
                "Could not determine project ID. Supply a fully-qualified table ID, "
                f"such as 'project.dataset.table', got {table_id}."
            )

        return {"projectId": output_project_id, "datasetId": output_dataset_id, "tableId": output_table_id}
