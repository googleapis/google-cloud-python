# Copyright 2021 Google LLC
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

"""Helpers for interacting with the job REST APIs from the client."""

import copy
import uuid
from typing import Any, Dict, TYPE_CHECKING, Optional

import google.api_core.exceptions as core_exceptions
from google.api_core import retry as retries

from google.cloud.bigquery import job

# Avoid circular imports
if TYPE_CHECKING:  # pragma: NO COVER
    from google.cloud.bigquery.client import Client


# The purpose of _TIMEOUT_BUFFER_MILLIS is to allow the server-side timeout to
# happen before the client-side timeout. This is not strictly neccessary, as the
# client retries client-side timeouts, but the hope by making the server-side
# timeout slightly shorter is that it can save the server from some unncessary
# processing time.
#
# 250 milliseconds is chosen arbitrarily, though should be about the right
# order of magnitude for network latency and switching delays. It is about the
# amount of time for light to circumnavigate the world twice.
_TIMEOUT_BUFFER_MILLIS = 250


def make_job_id(job_id: Optional[str] = None, prefix: Optional[str] = None) -> str:
    """Construct an ID for a new job.

    Args:
        job_id: the user-provided job ID.
        prefix: the user-provided prefix for a job ID.

    Returns:
        str: A job ID
    """
    if job_id is not None:
        return job_id
    elif prefix is not None:
        return str(prefix) + str(uuid.uuid4())
    else:
        return str(uuid.uuid4())


def query_jobs_insert(
    client: "Client",
    query: str,
    job_config: Optional[job.QueryJobConfig],
    job_id: Optional[str],
    job_id_prefix: Optional[str],
    location: Optional[str],
    project: str,
    retry: retries.Retry,
    timeout: Optional[float],
    job_retry: retries.Retry,
) -> job.QueryJob:
    """Initiate a query using jobs.insert.

    See: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/insert
    """
    job_id_given = job_id is not None
    job_id_save = job_id
    job_config_save = job_config

    def do_query():
        # Make a copy now, so that original doesn't get changed by the process
        # below and to facilitate retry
        job_config = copy.deepcopy(job_config_save)

        job_id = make_job_id(job_id_save, job_id_prefix)
        job_ref = job._JobReference(job_id, project=project, location=location)
        query_job = job.QueryJob(job_ref, query, client=client, job_config=job_config)

        try:
            query_job._begin(retry=retry, timeout=timeout)
        except core_exceptions.Conflict as create_exc:
            # The thought is if someone is providing their own job IDs and they get
            # their job ID generation wrong, this could end up returning results for
            # the wrong query. We thus only try to recover if job ID was not given.
            if job_id_given:
                raise create_exc

            try:
                query_job = client.get_job(
                    job_id,
                    project=project,
                    location=location,
                    retry=retry,
                    timeout=timeout,
                )
            except core_exceptions.GoogleAPIError:  # (includes RetryError)
                raise
            else:
                return query_job
        else:
            return query_job

    future = do_query()
    # The future might be in a failed state now, but if it's
    # unrecoverable, we'll find out when we ask for it's result, at which
    # point, we may retry.
    if not job_id_given:
        future._retry_do_query = do_query  # in case we have to retry later
        future._job_retry = job_retry

    return future


def _to_query_request(job_config: Optional[job.QueryJobConfig]) -> Dict[str, Any]:
    """Transform from Job resource to QueryRequest resource.

    Most of the keys in job.configuration.query are in common with
    QueryRequest. If any configuration property is set that is not available in
    jobs.query, it will result in a server-side error.
    """
    request_body = {}
    job_config_resource = job_config.to_api_repr() if job_config else {}
    query_config_resource = job_config_resource.get("query", {})

    request_body.update(query_config_resource)

    # These keys are top level in job resource and query resource.
    if "labels" in job_config_resource:
        request_body["labels"] = job_config_resource["labels"]
    if "dryRun" in job_config_resource:
        request_body["dryRun"] = job_config_resource["dryRun"]

    # Default to standard SQL.
    request_body.setdefault("useLegacySql", False)

    # Since jobs.query can return results, ensure we use the lossless timestamp
    # format. See: https://github.com/googleapis/python-bigquery/issues/395
    request_body.setdefault("formatOptions", {})
    request_body["formatOptions"]["useInt64Timestamp"] = True  # type: ignore

    return request_body


def _to_query_job(
    client: "Client",
    query: str,
    request_config: Optional[job.QueryJobConfig],
    query_response: Dict[str, Any],
) -> job.QueryJob:
    job_ref_resource = query_response["jobReference"]
    job_ref = job._JobReference._from_api_repr(job_ref_resource)
    query_job = job.QueryJob(job_ref, query, client=client)
    query_job._properties.setdefault("configuration", {})

    # Not all relevant properties are in the jobs.query response. Populate some
    # expected properties based on the job configuration.
    if request_config is not None:
        query_job._properties["configuration"].update(request_config.to_api_repr())

    query_job._properties["configuration"].setdefault("query", {})
    query_job._properties["configuration"]["query"]["query"] = query
    query_job._properties["configuration"]["query"].setdefault("useLegacySql", False)

    query_job._properties.setdefault("statistics", {})
    query_job._properties["statistics"].setdefault("query", {})
    query_job._properties["statistics"]["query"]["cacheHit"] = query_response.get(
        "cacheHit"
    )
    query_job._properties["statistics"]["query"]["schema"] = query_response.get(
        "schema"
    )
    query_job._properties["statistics"]["query"][
        "totalBytesProcessed"
    ] = query_response.get("totalBytesProcessed")

    # Set errors if any were encountered.
    query_job._properties.setdefault("status", {})
    if "errors" in query_response:
        # Set errors but not errorResult. If there was an error that failed
        # the job, jobs.query behaves like jobs.getQueryResults and returns a
        # non-success HTTP status code.
        errors = query_response["errors"]
        query_job._properties["status"]["errors"] = errors

    # Transform job state so that QueryJob doesn't try to restart the query.
    job_complete = query_response.get("jobComplete")
    if job_complete:
        query_job._properties["status"]["state"] = "DONE"
        # TODO: https://github.com/googleapis/python-bigquery/issues/589
        # Set the first page of results if job is "complete" and there is
        # only 1 page of results. Otherwise, use the existing logic that
        # refreshes the job stats.
        #
        # This also requires updates to `to_dataframe` and the DB API connector
        # so that they don't try to read from a destination table if all the
        # results are present.
    else:
        query_job._properties["status"]["state"] = "PENDING"

    return query_job


def query_jobs_query(
    client: "Client",
    query: str,
    job_config: Optional[job.QueryJobConfig],
    location: Optional[str],
    project: str,
    retry: retries.Retry,
    timeout: Optional[float],
    job_retry: retries.Retry,
) -> job.QueryJob:
    """Initiate a query using jobs.query.

    See: https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
    """
    path = f"/projects/{project}/queries"
    request_body = _to_query_request(job_config)

    if timeout is not None:
        # Subtract a buffer for context switching, network latency, etc.
        request_body["timeoutMs"] = max(0, int(1000 * timeout) - _TIMEOUT_BUFFER_MILLIS)
    request_body["location"] = location
    request_body["query"] = query

    def do_query():
        request_body["requestId"] = make_job_id()
        span_attributes = {"path": path}
        api_response = client._call_api(
            retry,
            span_name="BigQuery.query",
            span_attributes=span_attributes,
            method="POST",
            path=path,
            data=request_body,
            timeout=timeout,
        )
        return _to_query_job(client, query, job_config, api_response)

    future = do_query()

    # The future might be in a failed state now, but if it's
    # unrecoverable, we'll find out when we ask for it's result, at which
    # point, we may retry.
    future._retry_do_query = do_query  # in case we have to retry later
    future._job_retry = job_retry

    return future
