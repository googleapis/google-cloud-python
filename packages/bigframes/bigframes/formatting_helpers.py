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

from __future__ import annotations

import datetime
import html
import random
from typing import Any, Optional, Type, TYPE_CHECKING, Union

import bigframes_vendored.constants as constants
import google.api_core.exceptions as api_core_exceptions
import google.cloud.bigquery as bigquery
import humanize
import IPython
import IPython.display as display

if TYPE_CHECKING:
    import bigframes.core.events

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


def create_exception_with_feedback_link(
    exception: Type[Exception],
    arg: str = "",
):
    if arg:
        return exception(arg + f" {constants.FEEDBACK_LINK}")

    return exception(constants.FEEDBACK_LINK)


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
                res += f"""Job url: {get_job_url(
                    project_id=query_job.project,
                    location=query_job.location,
                    job_id=query_job.job_id,
                )}"""
            elif key == "Slot Time":
                res += f"""{key}: {get_formatted_time(job_val)}"""
            elif key == "Bytes Processed":
                res += f"""{key}: {get_formatted_bytes(job_val)}"""
            else:
                res += f"""{key}: {job_val}"""
    return res


current_display: Optional[display.HTML] = None
current_display_id: Optional[str] = None
previous_display_html: str = ""


def progress_callback(
    event: bigframes.core.events.Event,
):
    """Displays a progress bar while the query is running"""
    global current_display, current_display_id, previous_display_html

    try:
        import bigframes._config
        import bigframes.core.events
    except ImportError:
        # Since this gets called from __del__, skip if the import fails to avoid
        # ImportError: sys.meta_path is None, Python is likely shutting down.
        # This will allow cleanup to continue.
        return

    progress_bar = bigframes._config.options.display.progress_bar

    if progress_bar == "auto":
        progress_bar = "notebook" if in_ipython() else "terminal"

    if progress_bar == "notebook":
        if (
            isinstance(event, bigframes.core.events.ExecutionStarted)
            or current_display is None
            or current_display_id is None
        ):
            previous_display_html = ""
            current_display_id = str(random.random())
            current_display = display.HTML("Starting.")
            display.display(
                current_display,
                display_id=current_display_id,
            )

        if isinstance(event, bigframes.core.events.BigQuerySentEvent):
            previous_display_html = render_bqquery_sent_event_html(event)
            display.update_display(
                display.HTML(previous_display_html),
                display_id=current_display_id,
            )
        elif isinstance(event, bigframes.core.events.BigQueryRetryEvent):
            previous_display_html = render_bqquery_retry_event_html(event)
            display.update_display(
                display.HTML(previous_display_html),
                display_id=current_display_id,
            )
        elif isinstance(event, bigframes.core.events.BigQueryReceivedEvent):
            previous_display_html = render_bqquery_received_event_html(event)
            display.update_display(
                display.HTML(previous_display_html),
                display_id=current_display_id,
            )
        elif isinstance(event, bigframes.core.events.BigQueryFinishedEvent):
            previous_display_html = render_bqquery_finished_event_html(event)
            display.update_display(
                display.HTML(previous_display_html),
                display_id=current_display_id,
            )
        elif isinstance(event, bigframes.core.events.ExecutionFinished):
            display.update_display(
                display.HTML(f"✅ Completed. {previous_display_html}"),
                display_id=current_display_id,
            )
        elif isinstance(event, bigframes.core.events.SessionClosed):
            display.update_display(
                display.HTML(f"Session {event.session_id} closed."),
                display_id=current_display_id,
            )
    elif progress_bar == "terminal":
        if isinstance(event, bigframes.core.events.ExecutionStarted):
            print("Starting execution.")
        elif isinstance(event, bigframes.core.events.BigQuerySentEvent):
            message = render_bqquery_sent_event_plaintext(event)
            print(message)
        elif isinstance(event, bigframes.core.events.BigQueryRetryEvent):
            message = render_bqquery_retry_event_plaintext(event)
            print(message)
        elif isinstance(event, bigframes.core.events.BigQueryReceivedEvent):
            message = render_bqquery_received_event_plaintext(event)
            print(message)
        elif isinstance(event, bigframes.core.events.BigQueryFinishedEvent):
            message = render_bqquery_finished_event_plaintext(event)
            print(message)
        elif isinstance(event, bigframes.core.events.ExecutionFinished):
            print("Execution done.")


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


def render_query_references(
    *,
    project_id: Optional[str],
    location: Optional[str],
    job_id: Optional[str],
    request_id: Optional[str],
) -> str:
    query_id = ""
    if request_id and not job_id:
        query_id = f" with request ID {project_id}:{location}.{request_id}"
    return query_id


def render_job_link_html(
    *,
    project_id: Optional[str],
    location: Optional[str],
    job_id: Optional[str],
) -> str:
    job_url = get_job_url(
        project_id=project_id,
        location=location,
        job_id=job_id,
    )
    if job_url:
        job_link = f' [<a target="_blank" href="{job_url}">Job {project_id}:{location}.{job_id} details</a>]'
    else:
        job_link = ""
    return job_link


def render_job_link_plaintext(
    *,
    project_id: Optional[str],
    location: Optional[str],
    job_id: Optional[str],
) -> str:
    job_url = get_job_url(
        project_id=project_id,
        location=location,
        job_id=job_id,
    )
    if job_url:
        job_link = f" Job {project_id}:{location}.{job_id} details: {job_url}"
    else:
        job_link = ""
    return job_link


def get_job_url(
    *,
    project_id: Optional[str],
    location: Optional[str],
    job_id: Optional[str],
):
    """Return url to the query job in cloud console.

    Returns:
        String url.
    """
    if project_id is None or location is None or job_id is None:
        return None
    return f"""https://console.cloud.google.com/bigquery?project={project_id}&j=bq:{location}:{job_id}&page=queryresults"""


def render_bqquery_sent_event_html(
    event: bigframes.core.events.BigQuerySentEvent,
) -> str:
    """Return progress bar html string
    Args:
        query_job (bigquery.QueryJob):
            The job representing the execution of the query on the server.
    Returns:
        Html string.
    """

    job_link = render_job_link_html(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
    )
    query_id = render_query_references(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
        request_id=event.request_id,
    )
    query_text_details = f"<details><summary>SQL</summary><pre>{html.escape(event.query)}</pre></details>"

    return f"""
    Query started{query_id}.{job_link}{query_text_details}
    """


def render_bqquery_sent_event_plaintext(
    event: bigframes.core.events.BigQuerySentEvent,
) -> str:
    """Return progress bar html string
    Args:
        query_job (bigquery.QueryJob):
            The job representing the execution of the query on the server.
    Returns:
        Html string.
    """

    job_link = render_job_link_plaintext(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
    )
    query_id = render_query_references(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
        request_id=event.request_id,
    )

    return f"Query started{query_id}.{job_link}"


def render_bqquery_retry_event_html(
    event: bigframes.core.events.BigQueryRetryEvent,
) -> str:
    """Return progress bar html string for retry event."""

    job_link = render_job_link_html(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
    )
    query_id = render_query_references(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
        request_id=event.request_id,
    )
    query_text_details = f"<details><summary>SQL</summary><pre>{html.escape(event.query)}</pre></details>"

    return f"""
    Retrying query{query_id}.{job_link}{query_text_details}
    """


def render_bqquery_retry_event_plaintext(
    event: bigframes.core.events.BigQueryRetryEvent,
) -> str:
    """Return progress bar plaintext string for retry event."""

    job_link = render_job_link_plaintext(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
    )
    query_id = render_query_references(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
        request_id=event.request_id,
    )
    return f"Retrying query{query_id}.{job_link}"


def render_bqquery_received_event_html(
    event: bigframes.core.events.BigQueryReceivedEvent,
) -> str:
    """Return progress bar html string for received event."""

    job_link = render_job_link_html(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
    )
    query_id = render_query_references(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
        request_id=None,
    )

    query_plan_details = ""
    if event.query_plan:
        plan_str = "\n".join([str(entry) for entry in event.query_plan])
        query_plan_details = f"<details><summary>Query Plan</summary><pre>{html.escape(plan_str)}</pre></details>"

    return f"""
    Query{query_id} is {event.state}.{job_link}{query_plan_details}
    """


def render_bqquery_received_event_plaintext(
    event: bigframes.core.events.BigQueryReceivedEvent,
) -> str:
    """Return progress bar plaintext string for received event."""

    job_link = render_job_link_plaintext(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
    )
    query_id = render_query_references(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
        request_id=None,
    )
    return f"Query{query_id} is {event.state}.{job_link}"


def render_bqquery_finished_event_html(
    event: bigframes.core.events.BigQueryFinishedEvent,
) -> str:
    """Return progress bar html string for finished event."""

    bytes_str = ""
    if event.total_bytes_processed is not None:
        bytes_str = f" {humanize.naturalsize(event.total_bytes_processed)}"

    slot_time_str = ""
    if event.slot_millis is not None:
        slot_time = datetime.timedelta(milliseconds=event.slot_millis)
        slot_time_str = f" in {humanize.naturaldelta(slot_time)} of slot time"

    job_link = render_job_link_html(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
    )
    query_id = render_query_references(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
        request_id=None,
    )
    return f"""
    Query processed{bytes_str}{slot_time_str}{query_id}.{job_link}
    """


def render_bqquery_finished_event_plaintext(
    event: bigframes.core.events.BigQueryFinishedEvent,
) -> str:
    """Return progress bar plaintext string for finished event."""

    bytes_str = ""
    if event.total_bytes_processed is not None:
        bytes_str = f" {humanize.naturalsize(event.total_bytes_processed)} processed."

    slot_time_str = ""
    if event.slot_millis is not None:
        slot_time = datetime.timedelta(milliseconds=event.slot_millis)
        slot_time_str = f" Slot time: {humanize.naturaldelta(slot_time)}."

    job_link = render_job_link_plaintext(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
    )
    query_id = render_query_references(
        project_id=event.billing_project,
        location=event.location,
        job_id=event.job_id,
        request_id=None,
    )
    return f"Query{query_id} finished.{bytes_str}{slot_time_str}{job_link}"


def get_base_job_loading_html(job: GenericJob):
    """Return progress bar html string
    Args:
        job (GenericJob):
            The job representing the execution of the query on the server.
    Returns:
        Html string.
    """
    return f"""{job.job_type.capitalize()} job {job.job_id} is {job.state}. <a target="_blank" href="{get_job_url(
        project_id=job.job_id,
        location=job.location,
        job_id=job.job_id,
    )}">Open Job</a>"""


def get_base_job_loading_string(job: GenericJob):
    """Return progress bar string
    Args:
        job (GenericJob):
            The job representing the execution of the query on the server.
    Returns:
        String
    """
    return f"""{job.job_type.capitalize()} job {job.job_id} is {job.state}. \n{get_job_url(
        project_id=job.job_id,
        location=job.location,
        job_id=job.job_id,
    )}"""


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
