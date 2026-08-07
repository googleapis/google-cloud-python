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

import os
import uuid

import pytest
from google.cloud import bigquery, dataform_v1beta1

import bigframes.core.global_session as global_session
import bigframes.pandas as bpd


def test_productionize_e2e(session, project_id, dataset_id, tmp_path):
    # 1. Define unique table names
    unique_suffix = uuid.uuid4().hex[:8]
    source_table = f"{dataset_id}.test_prod_src_{unique_suffix}"
    dest_table = f"{dataset_id}.test_prod_dest_{unique_suffix}"
    udf_name = f"my_e2e_udf_{unique_suffix}"

    # Seed the source table with some data
    df_source = bpd.DataFrame({"col": [1, 2, 3, 4, 5]}, session=session)
    df_source.to_gbq(source_table, if_exists="replace")

    try:
        # 2. Run the pipeline in productionize mode
        with global_session._GlobalSessionContext(session):
            with bpd.productionize() as pipeline:
                # Define a parameter
                limit_val = bpd.parameter("limit_val", dtype=int)

                # Define a managed UDF
                @bpd.udf(input_types=[int], output_type=int, name=udf_name)
                def add_one(x):
                    return x + 1

                # Read, filter, map, and write
                df = bpd.read_gbq(source_table)
                df_filtered = df[df["col"] > limit_val]
                df_mapped = df_filtered.copy()
                df_mapped["col"] = add_one(df_filtered["col"])

                df_mapped.to_gbq(dest_table, if_exists="replace")

        # 3. Verify SQL compilation by running it on BigQuery
        sql = pipeline.to_sql()
        assert "@limit_val" in sql
        assert udf_name in sql

        # Run the SQL script on BigQuery with a parameter value
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("limit_val", "INT64", 2)]
        )
        query_job = session.bqclient.query(sql, job_config=job_config)
        query_job.result()  # Wait for the script to complete

        # Verify the destination table was created and contains the expected data
        # Source: [1, 2, 3, 4, 5] -> Filter > 2: [3, 4, 5] -> Add 1: [4, 5, 6]
        df_result = session.read_gbq(dest_table)
        pd_df = df_result.to_pandas()
        assert list(pd_df["col"].sort_values()) == [4, 5, 6]

        # 4. Verify Dataform export by uploading and compiling in the real repo
        target_dir = str(tmp_path)
        pipeline.export_dataform(target_dir)

        # Connect to Dataform
        dataform_client = dataform_v1beta1.DataformClient()
        repo_name = "projects/bigframes-testing/locations/us-central1/repositories/bigframes-testing-dataform"
        workspace_id = f"test-ws-{unique_suffix}"
        workspace_name = f"{repo_name}/workspaces/{workspace_id}"

        # Create a temporary workspace
        print(f"Creating Dataform workspace: {workspace_id}")
        dataform_client.create_workspace(
            request=dataform_v1beta1.CreateWorkspaceRequest(
                parent=repo_name,
                workspace_id=workspace_id,
            )
        )

        try:
            # Initialize the workspace with package.json and workflow_settings.yaml
            # (since the repository might be empty)
            package_json_content = """{
  "dependencies": {
    "@dataform/core": "3.0.2"
  }
}"""
            dataform_client.write_file(
                request=dataform_v1beta1.WriteFileRequest(
                    workspace=workspace_name,
                    path="package.json",
                    contents=package_json_content.encode("utf-8"),
                )
            )

            # Extract the dataset name from the fully qualified dataset_id
            dataset_name = dataset_id.split(".")[-1]
            workflow_settings_content = f"""defaultProject: {project_id}
defaultDataset: {dataset_name}
defaultLocation: us-central1
"""
            dataform_client.write_file(
                request=dataform_v1beta1.WriteFileRequest(
                    workspace=workspace_name,
                    path="workflow_settings.yaml",
                    contents=workflow_settings_content.encode("utf-8"),
                )
            )

            # Recursively upload all exported files to the workspace
            for root, _, files in os.walk(target_dir):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, target_dir)

                    with open(local_path, "r", encoding="utf-8") as f:
                        contents = f.read()

                    # Write the file to the workspace
                    dataform_client.write_file(
                        request=dataform_v1beta1.WriteFileRequest(
                            workspace=workspace_name,
                            path=relative_path,
                            contents=contents.encode("utf-8"),
                        )
                    )

            # Trigger compilation of the workspace
            print("Compiling Dataform workspace...")
            compilation_result = dataform_client.create_compilation_result(
                request=dataform_v1beta1.CreateCompilationResultRequest(
                    parent=repo_name,
                    compilation_result=dataform_v1beta1.CompilationResult(
                        workspace=workspace_name
                    ),
                )
            )

            # Verify there are no compilation errors
            errors = compilation_result.compilation_errors
            if errors:
                error_messages = "\n".join(f"{e.path}: {e.message}" for e in errors)
                pytest.fail(
                    f"Dataform compilation failed with errors:\n{error_messages}"
                )

            print("Dataform compilation succeeded!")

        finally:
            # Clean up the workspace
            print(f"Deleting Dataform workspace: {workspace_id}")
            try:
                dataform_client.delete_workspace(name=workspace_name)
            except Exception as e:
                print(f"Failed to delete workspace {workspace_id}: {e}")

    finally:
        # Clean up BigQuery tables and UDFs
        print("Cleaning up BigQuery resources...")
        try:
            session.bqclient.delete_table(source_table, not_found_ok=True)
        except Exception:
            pass
        try:
            session.bqclient.delete_table(dest_table, not_found_ok=True)
        except Exception:
            pass
        try:
            # Delete the UDF
            session.bqclient.delete_routine(
                f"{dataset_id}.{udf_name}", not_found_ok=True
            )
        except Exception:
            pass
