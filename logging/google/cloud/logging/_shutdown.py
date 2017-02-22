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

from google.cloud.logging.environment_vars import _APPENGINE_FLEXIBLE_ENV_VM
from google.cloud.logging.environment_vars import _APPENGINE_FLEXIBLE_ENV_FLEX


# Maximum size in bytes to send to Stackdriver Logging in one entry
MAX_PAYLOAD_SIZE = 1024 * 100


def _get_gae_instance():
    """Returns the App Engine Flexible instance."""
    return os.getenv('GAE_INSTANCE')


def _get_gae_service():
    """Returns the App Engine Flexible service."""
    return os.getenv('GAE_SERVICE')


def _get_gae_version():
    """Returns the App Engine Flexible version."""
    return os.getenv('GAE_VERSION')


def _split_entry(payload):
    """Splits payload into lists of maximum 100Kb.

    Stackdriver Logging payloads are a maximum of 100Kb.
    """
    return [payload[i:i + MAX_PAYLOAD_SIZE]
            for i in range(0, len(payload), MAX_PAYLOAD_SIZE)]


def _write_stacktrace_log(client, traces):
    """Writes the trace logs to the appropriate GAE resource in Stackdriver.

    :type client: `google.cloud.logging.Client`
    :param client: Stackdriver logging client.

    :type traces: str
    :param traces: String containing the stacktrace info to write to
                   Stackdriver logging.
    """
    gae_version = _get_gae_version()
    gae_service = _get_gae_service()
    gae_instance = _get_gae_instance()

    text_payload = '{}\nThread traces\n{}'.format(gae_instance, traces)
    logger_name = 'projects/{}/logs/appengine.googleapis.com%2Fapp.shutdown'.format(client.project)

    resource = {'type': 'gae_app', 'labels': {'project_id': client.project,
                                              'version_id': gae_version,
                                              'module_id': gae_service}}

    labels = {'appengine.googleapis.com/version_id': gae_version,
              'compute.googleapis.com/resource_type': 'instance',
              'appengine.googleapis.com/instance_name': gae_instance,
              'appengine.googleapis.com / module_id': gae_service, }

    split_payloads = _split_entry(bytes(text_payload))
    entries = [{'text_payload': payload} for payload in split_payloads]

    print "SENDINT ENTRY %s logger  %s resource %s " % (entries, logger_name,
                                                        resource )
    client.logging_api.write_entries(
        entries, logger_name=logger_name, resource=resource, labels=labels)


def _is_on_appengine():
    """Returns True if the environment is detected as App Engine flexible."""
    return (os.getenv(_APPENGINE_FLEXIBLE_ENV_VM) or os.getenv(
        _APPENGINE_FLEXIBLE_ENV_FLEX))


def _report_stacktraces(client, signal, frame):
    """Reports the stacktraces of all active threads to Stackdriver Logging.

    :type client: `google.cloud.logging.Client`
    :param client: Stackdriver logging client.

    :type signal: int
    :param signal: Signal number.

    :type frame: frame object
    :param frame: The current stack frame.
    """
    traces = ''
    print "RUNNING SIGNAL HANDLER!"
    for threadId, stack in sys._current_frames().items():
        traces += '\n# ThreadID: {}'.format(threadId)
        for filename, lineno, name, line in traceback.extract_stack(stack):
            traces += 'File: {}, line {}, in {}'.format(
                filename, lineno, name)

    _write_stacktrace_log(client, traces)

def fml(signal, frame):
    print "MY LIFE IS F'ed"



def setup_shutdown_stacktrace_reporting(client):
    """Installs a SIGTERM handler to log stack traces to  Stackdriver.

    :type client: `google.cloud.logging.Client`
    :param client: Stackdriver logging client.
    """
    if not _is_on_appengine():
        raise RuntimeError('Shutdown reporting is only supported on App '
                           'Engine flexible environment.')
    print "INSTALLIGN SIGNAL HANDLER"
    signal.signal(signal.SIGTERM, functools.partial(_report_stacktraces, client))
