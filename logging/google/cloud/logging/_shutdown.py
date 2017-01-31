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
import httplib2
import os
import signal
import sys
import traceback

from google.cloud.logging.environment_vars import _APPENGINE_FLEXIBLE_ENV_VM
from google.cloud.logging.environment_vars import _APPENGINE_FLEXIBLE_ENV_FLEX

_METADATA_SERVICE_ADDR = '169.254.169.254'
_APPENGINE_SERVICE = 'appengine.googleapis.com'


def _fetch_metadata(metdata_path):
    url = 'http://{}/computeMetadata/v1/{}'.format(_METADATA_SERVICE_ADDR,
                                                   metdata_path)
    h = httplib2.Http()
    headers = {'Metadata-Flavor': 'Google'}
    resp, content = h.request(url, 'GET')

    return content


def _get_gae_instance():
    return _fetch_metadata('instance/attributes/gae_backend_instance')


def _get_gae_backend():
    return _fetch_metadata('instance/attributes/gae_backend_name')


def _get_gae_version():
    return _fetch_metadata('instance/attributes/gae_backend_version')


def _write_stacktrace_log(client, traces):
    gae_version = _get_gae_version()
    gae_backend = _get_gae_backend()
    gae_instance = _get_gae_instance()

    text_payload = '{}\nThread traces\n{}'.format(gae_instance, traces)
    logger_name = 'projects/{}/logs/'
    'appengine.googleapis.com%2Fapp.shutdown'.format(client.project)

    resource = {'type': 'gae_app', 'labels': {'project_id': client.project,
                                              'version_id': gae_version,
                                              'module_id': gae_backend}}

    labels = {'appengine.googleapis.com/version_id': gae_version,
              'compute.googleapis.com/resource_type': 'instance',
              'appengine.googleapis.com/instance_name': gae_instance,
              'appengine.googleapis.com / module_id': gae_backend, }
    entry = {'text_payload': text_payload}

    entries = [entry]

    client.logging_api.write_entries(
        entries, logger_name=logger_name, resource=resource, labels=labels)


def _is_on_appengine():
    return (os.getenv(_APPENGINE_FLEXIBLE_ENV_VM) or os.getenv(
        _APPENGINE_FLEXIBLE_ENV_FLEX))


def _report_stacktraces(client, signal, frame):
    """
    Reports the stacktraces of all active threads to Stackdriver Logging.

    :type client: `google.cloud.logging.Client`
    :param client: Stackdriver loggingclient.

    :type signal: int
    :param signal: Signal number.

    :type frame: frame object
    :param frame: The current stack frame.
    """
    traces = ''
    for threadId, stack in sys._current_frames().items():
        traces += '\n# ThreadID: {}'.format(threadId)
        for filename, lineno, name, line in traceback.extract_stack(stack):
            traces += 'File: {}, line {}, in {}'.format(
                filename, lineno, name)
    _write_stacktrace_log(client, traces)


def setup_shutdown_stacktrace_reporting(client):
    """Installs a SIGTERM handler to log stack traces to  Stackdriver.

    :type client: `google.cloud.logging.Client`
    :param client: Stackdriver logging client.
    """
    if not _is_on_appengine():
        raise Exception('Shutdown reporting is only supported on App Engine '
                        'flexible environment.')
    signal.signal(signal.SIGTERM, functools.partial(_report_stacktraces, client))
