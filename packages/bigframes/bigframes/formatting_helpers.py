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

import datetime
from typing import Optional

import google.cloud.bigquery as bigquery
import humanize
import IPython
import IPython.display as display
import ipywidgets as widgets

query_job_prop_pairs = {
    "Job Id": "job_id",
    "Destination Table": "destination",
    "Slot Time": "slot_millis",
    "Bytes Processed": "estimated_bytes_processed",
    "Cache hit": "cache_hit",
}


def repr_query_job(query_job: Optional[bigquery.QueryJob]):
    if query_job is None:
        return widgets.HTML("No job information available")
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


def wait_for_job(
    query_job: bigquery.QueryJob,
    max_results: Optional[int] = None,
    progress_bar: Optional[str] = None,
) -> bigquery.table.RowIterator:
    """Return query results. Displays a progress bar while the query is running
    Args:
        query_job:
            The job representing the execution of the query on the server.
        max_results:
            The maximum number of rows the row iterator should return.
    Returns:
        A row iterator over the query results.
    """
    loading_bar = widgets.HTML(get_query_job_loading_html(query_job))
    if progress_bar == "auto":
        progress_bar = "notebook" if in_ipython() else "terminal"

    if progress_bar == "notebook":
        display.display(loading_bar)
        query_result = query_job.result(max_results=max_results)
        query_job.reload()
        loading_bar.close()
    elif progress_bar == "terminal":
        print(get_query_job_loading_string(query_job))
        query_result = query_job.result(max_results=max_results)
        query_job.reload()
    return query_result


def get_job_url(query_job: bigquery.QueryJob):
    if (
        query_job.project is None
        or query_job.location is None
        or query_job.job_id is None
    ):
        return None
    return f"""https://console.cloud.google.com/bigquery?project={query_job.project}&j=bq:{query_job.location}:{query_job.job_id}&page=queryresults"""


def get_query_job_loading_html(query_job: bigquery.QueryJob):
    return f"""Job {query_job.job_id} is {query_job.state}. <a target="_blank" href="{get_job_url(query_job)}">Open Job</a>"""


def get_query_job_loading_string(query_job: bigquery.QueryJob):
    return (
        f"""Job {query_job.job_id} is {query_job.state}. \n{get_job_url(query_job)}"""
    )


def get_formatted_time(val):
    try:
        return humanize.naturaldelta(datetime.timedelta(milliseconds=float(val)))
    except Exception:
        return val


def get_formatted_bytes(val):
    return humanize.naturalsize(val)


def in_ipython():
    """Return True iff we're in a colab-like IPython."""
    return hasattr(IPython.get_ipython(), "kernel")
