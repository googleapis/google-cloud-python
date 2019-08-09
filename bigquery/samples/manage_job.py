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


def manage_job(client):

    # [START bigquery_get_job]
    sql = """
        SELECT corpus
        FROM `bigquery-public-data.samples.shakespeare`
        GROUP BY corpus;
    """
    location = "us"
    job = client.query(sql, location=location)
    job_id = job.job_id

    # [START bigquery_cancel_job]
    # TODO(developer): Uncomment the lines below and replace with your values.
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # job_id = 'bq-job-123x456-123y123z123c'  # replace with your job ID
    # location = 'us'                         # replace with your location

    job = client.cancel_job(job_id, location=location)
    # [END bigquery_cancel_job]

    # TODO(developer): Uncomment the lines below and replace with your values.
    # from google.cloud import bigquery
    # client = bigquery.Client()
    # job_id = 'bq-job-123x456-123y123z123c'  # replace with your job ID
    # location = 'us'                         # replace with your location

    job = client.get_job(job_id, location=location)  # API request

    # Print selected job properties
    print("Details for job {} running in {}:".format(job_id, location))
    print(
        "\tType: {}\n\tState: {}\n\tCreated: {}".format(
            job.job_type, job.state, job.created
        )
    )

    # [END bigquery_get_job]