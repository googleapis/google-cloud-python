# Copyright 2017 Google Inc.
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

"""Module for code related to shutdown logging."""

import functools
import os
import signal
import sys
import traceback

from google.cloud.logging._environment_vars import APPENGINE_FLEXIBLE_ENV_VM
from google.cloud.logging._environment_vars import APPENGINE_FLEXIBLE_ENV_FLEX
from google.cloud.logging._environment_vars import GAE_SERVICE
from google.cloud.logging._environment_vars import GAE_VERSION
from google.cloud import _helpers

import six

# Maximum size in bytes to send to Stackdriver Logging in one entry
_MAX_PAYLOAD_SIZE = 100 * 1024

_LOGGER_NAME_TMPL = 'projects/{}/logs/appengine.googleapis.com%2Fapp.shutdown'


def _get_gae_instance():
    """Returns the App Engine Flexible instance."""
    return os.getenv(APPENGINE_FLEXIBLE_ENV_FLEX)


def _get_gae_service():
    """Returns the App Engine Flexible service."""
    return os.getenv(GAE_SERVICE)


def _get_gae_version():
    """Returns the App Engine Flexible version."""
    return os.getenv(GAE_VERSION)


def _split_entry(payload):
    """Splits payload into lists of maximum 100Kb.

    Stackdriver Logging payloads are a maximum of 100Kb.
    """
    return [payload[i:i + _MAX_PAYLOAD_SIZE]
            for i in six.moves.xrange(0, len(payload), _MAX_PAYLOAD_SIZE)]


def _write_stacktrace_log(client, traces):
    """Writes the trace logs to the appropriate GAE resource in Stackdriver.

    :type client: :class:`google.cloud.logging.Client`
    :param client: Stackdriver logging client.

    :type traces: str
    :param traces: String containing the stacktrace info to write to
                   Stackdriver logging.
    """
    gae_version = _get_gae_version()
    gae_service = _get_gae_service()
    gae_instance = _get_gae_instance()

    text_payload = '{}\nThread traces\n{}'.format(gae_instance, traces)

    logger_name = _LOGGER_NAME_TMPL.format(client.project)

    resource = {
        'type': 'gae_app',
        'labels': {
            'project_id': client.project,
            'version_id': gae_version,
            'module_id': gae_service,
        },
    }

    labels = {
        'appengine.googleapis.com/version_id': gae_version,
        'compute.googleapis.com/resource_type': 'instance',
        'appengine.googleapis.com/instance_name': gae_instance,
        'appengine.googleapis.com/module_id': gae_service,
    }

    split_payloads = _split_entry(_helpers._to_bytes(text_payload))
    entries = [{'text_payload': payload} for payload in split_payloads]

    client.logging_api.write_entries(
        entries, logger_name=logger_name, resource=resource, labels=labels)


def _is_on_appengine():
    """Returns True if the environment is detected as App Engine flexible."""
    return (os.getenv(APPENGINE_FLEXIBLE_ENV_VM) or os.getenv(
        APPENGINE_FLEXIBLE_ENV_FLEX))


def _report_stacktraces(
        client, signal_, frame):  # pylint: disable=unused-argument
    """Reports the stacktraces of all active threads to Stackdriver Logging.

    :type client: `google.cloud.logging.Client`
    :param client: Stackdriver logging client.

    :type signal_: int
    :param signal_: Signal number. Unused parameter since this function always
                    expects SIGTERM, but the parameter is required to match
                    the function signature for a signal handler.

    :type frame: frame object
    :param frame: The current stack frame. Unused parameter, this parameter
                  is required to match the function signature for a signal
                  handler.
    """
    traces = []
    for thread_id, stack in sys._current_frames().items():
        traces.append('\n# ThreadID: {}\n'.format(thread_id))
        for filename, lineno, name, _ in traceback.extract_stack(stack):
            traces.append('File: {}, line {}, in {}'.format(
                filename, lineno, name))

    _write_stacktrace_log(client, ''.join(traces))


def setup_stacktrace_crash_report(client):
    """Installs a SIGTERM handler to log stack traces to Stackdriver.

    :type client: `google.cloud.logging.Client`
    :param client: Stackdriver logging client.
    """
    if not _is_on_appengine():
        raise RuntimeError('Shutdown reporting is only supported on App '
                           'Engine flexible environment.')
    signal.signal(
        signal.SIGTERM, functools.partial(_report_stacktraces, client))
