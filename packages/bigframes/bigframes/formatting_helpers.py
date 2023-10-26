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

"""Shared helper functions for formatting jobs related info."""
# TODO(orrbradford): cleanup up typings and documenttion in this file

import datetime
import random
from typing import Any, Optional, Union

import google.api_core.exceptions as api_core_exceptions
import google.cloud.bigquery as bigquery
import humanize
import IPython
import IPython.display as display
import ipywidgets as widgets

import bigframes.constants as constants

GenericJob = Union[
    bigquery.LoadJob, bigquery.ExtractJob, bigquery.QueryJob, bigquery.CopyJob
]

query_job_prop_pairs = {
    "Job Id": "job_id",
    "Destination Table": "destination",
    "Slot Time": "slot_millis",
    "Bytes Processed": "total_bytes_processed",
    "Cache hit": "cache_hit",
}


def add_feedback_link(
    exception: Union[
        api_core_exceptions.RetryError, api_core_exceptions.GoogleAPICallError
    ]
):
    exception.message = exception.message + f" {constants.FEEDBACK_LINK}"


def repr_query_job_html(query_job: Optional[bigquery.QueryJob]):
    """Return query job in html format.
    Args:
        query_job (bigquery.QueryJob, Optional):
            The job representing the execution of the query on the server.
    Returns:
        Pywidget html table.
    """
    if query_job is None:
        return display.HTML("No job information available")
    if query_job.dry_run:
        return display.HTML(
            f"Computation deferred. Computation will process {get_formatted_bytes(query_job.total_bytes_processed)}"
        )
    table_html = "<style> td {text-align: left;}</style>"
    table_html += "<table>"
    for key, value in query_job_prop_pairs.items():
        job_val = getattr(query_job, value)
        if job_val is not None:
            if key == "Job Id":  # add link to job
                table_html += f"""<tr><td>{key}</td><td><a target="_blank" href="{get_job_url(query_job)}">{job_val}</a></td></tr>"""
            elif key == "Slot Time":
                table_html += (
                    f"""<tr><td>{key}</td><td>{get_formatted_time(job_val)}</td></tr>"""
                )
            elif key == "Bytes Processed":
                table_html += f"""<tr><td>{key}</td><td>{get_formatted_bytes(job_val)}</td></tr>"""
            else:
                table_html += f"""<tr><td>{key}</td><td>{job_val}</td></tr>"""
    table_html += "</table>"
    return widgets.HTML(table_html)


def repr_query_job(query_job: Optional[bigquery.QueryJob]):
    """Return query job as a formatted string.
    Args:
        query_job:
            The job representing the execution of the query on the server.
    Returns:
        Pywidget html table.
    """
    if query_job is None:
        return "No job information available"
    if query_job.dry_run:
        return f"Computation deferred. Computation will process {get_formatted_bytes(query_job.total_bytes_processed)}"
    res = "Query Job Info"
    for key, value in query_job_prop_pairs.items():
        job_val = getattr(query_job, value)
        if job_val is not None:
            res += "\n"
            if key == "Job Id":  # add link to job
                res += f"""Job url: {get_job_url(query_job)}"""
            elif key == "Slot Time":
                res += f"""{key}: {get_formatted_time(job_val)}"""
            elif key == "Bytes Processed":
                res += f"""{key}: {get_formatted_bytes(job_val)}"""
            else:
                res += f"""{key}: {job_val}"""
    return res


def wait_for_query_job(
    query_job: bigquery.QueryJob,
    max_results: Optional[int] = None,
    progress_bar: Optional[str] = None,
) -> bigquery.table.RowIterator:
    """Return query results. Displays a progress bar while the query is running
    Args:
        query_job (bigquery.QueryJob, Optional):
            The job representing the execution of the query on the server.
        max_results (int, Optional):
            The maximum number of rows the row iterator should return.
        progress_bar (str, Optional):
            Which progress bar to show.
    Returns:
        A row iterator over the query results.
    """
    if progress_bar == "auto":
        progress_bar = "notebook" if in_ipython() else "terminal"

    try:
        if progress_bar == "notebook":
            display_id = str(random.random())
            loading_bar = display.HTML(get_query_job_loading_html(query_job))
            display.display(loading_bar, display_id=display_id)
            query_result = query_job.result(max_results=max_results)
            query_job.reload()
            display.update_display(
                display.HTML(get_query_job_loading_html(query_job)),
                display_id=display_id,
            )
        elif progress_bar == "terminal":
            initial_loading_bar = get_query_job_loading_string(query_job)
            print(initial_loading_bar)
            query_result = query_job.result(max_results=max_results)
            query_job.reload()
            if initial_loading_bar != get_query_job_loading_string(query_job):
                print(get_query_job_loading_string(query_job))
        else:
            # No progress bar.
            query_result = query_job.result(max_results=max_results)
            query_job.reload()
        return query_result
    except api_core_exceptions.RetryError as exc:
        add_feedback_link(exc)
        raise
    except api_core_exceptions.GoogleAPICallError as exc:
        add_feedback_link(exc)
        raise
    except KeyboardInterrupt:
        query_job.cancel()
        print(
            f"Requested cancellation for {query_job.job_type.capitalize()}"
            f" job {query_job.job_id} in location {query_job.location}..."
        )
        # begin the cancel request before immediately rethrowing
        raise


def wait_for_job(job: GenericJob, progress_bar: Optional[str] = None):
    """Waits for job results. Displays a progress bar while the job is running
    Args:
        job (GenericJob):
            The bigquery job to be executed.
        progress_bar (str, Optional):
            Which progress bar to show.
    """
    if progress_bar == "auto":
        progress_bar = "notebook" if in_ipython() else "terminal"

    try:
        if progress_bar == "notebook":
            display_id = str(random.random())
            loading_bar = display.HTML(get_base_job_loading_html(job))
            display.display(loading_bar, display_id=display_id)
            job.result()
            job.reload()
            display.update_display(
                display.HTML(get_base_job_loading_html(job)), display_id=display_id
            )
        elif progress_bar == "terminal":
            inital_loading_bar = get_base_job_loading_string(job)
            print(inital_loading_bar)
            job.result()
            job.reload()
            if get_base_job_loading_string != inital_loading_bar:
                print(get_base_job_loading_string(job))
        else:
            # No progress bar.
            job.result()
            job.reload()
    except api_core_exceptions.RetryError as exc:
        add_feedback_link(exc)
        raise
    except api_core_exceptions.GoogleAPICallError as exc:
        add_feedback_link(exc)
        raise
    except KeyboardInterrupt:
        job.cancel()
        print(
            f"Requested cancellation for {job.job_type.capitalize()}"
            f" job {job.job_id} in location {job.location}..."
        )
        # begin the cancel request before immediately rethrowing
        raise


def get_job_url(query_job: GenericJob):
    """Return url to the query job in cloud console.
    Args:
        query_job (GenericJob):
            The job representing the execution of the query on the server.
    Returns:
        String url.
    """
    if (
        query_job.project is None
        or query_job.location is None
        or query_job.job_id is None
    ):
        return None
    return f"""https://console.cloud.google.com/bigquery?project={query_job.project}&j=bq:{query_job.location}:{query_job.job_id}&page=queryresults"""


def get_query_job_loading_html(query_job: bigquery.QueryJob):
    """Return progress bar html string
    Args:
        query_job (bigquery.QueryJob):
            The job representing the execution of the query on the server.
    Returns:
        Html string.
    """
    return f"""Query job {query_job.job_id} is {query_job.state}. {get_bytes_processed_string(query_job.total_bytes_processed)}<a target="_blank" href="{get_job_url(query_job)}">Open Job</a>"""


def get_query_job_loading_string(query_job: bigquery.QueryJob):
    """Return progress bar string
    Args:
        query_job (bigquery.QueryJob):
            The job representing the execution of the query on the server.
    Returns:
        String
    """
    return f"""Query job {query_job.job_id} is {query_job.state}.{get_bytes_processed_string(query_job.total_bytes_processed)} \n{get_job_url(query_job)}"""


def get_base_job_loading_html(job: GenericJob):
    """Return progress bar html string
    Args:
        job (GenericJob):
            The job representing the execution of the query on the server.
    Returns:
        Html string.
    """
    return f"""{job.job_type.capitalize()} job {job.job_id} is {job.state}. <a target="_blank" href="{get_job_url(job)}">Open Job</a>"""


def get_base_job_loading_string(job: GenericJob):
    """Return progress bar string
    Args:
        job (GenericJob):
            The job representing the execution of the query on the server.
    Returns:
        String
    """
    return f"""{job.job_type.capitalize()} job {job.job_id} is {job.state}. \n{get_job_url(job)}"""


def get_formatted_time(val):
    """Try to format time
    Args:
        val (Any):
            Time in ms.
    Returns:
        Duration string
    """
    try:
        return humanize.naturaldelta(datetime.timedelta(milliseconds=float(val)))
    except Exception:
        return val


def get_formatted_bytes(val):
    """Try to format bytes
    Args:
        val (Any):
            Bytes to format
    Returns:
        Duration string
    """
    if isinstance(val, int):
        return humanize.naturalsize(val)
    return "N/A"


def get_bytes_processed_string(val: Any):
    """Try to get bytes processed string. Return empty if passed non int value"""
    bytes_processed_string = ""
    if isinstance(val, int):
        bytes_processed_string = f"""{get_formatted_bytes(val)} processed. """
    return bytes_processed_string


def in_ipython():
    """Return True iff we're in a colab-like IPython."""
    return hasattr(IPython.get_ipython(), "kernel")
