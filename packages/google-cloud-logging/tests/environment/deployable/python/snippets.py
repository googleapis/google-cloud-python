# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os


try:
    import google.cloud.logging
    from google.cloud.logging_v2._helpers import retrieve_metadata_server
except ImportError:
    # import at runtime for GAE environments
    import pip
    import importlib
    import site

    pip.main(["install", "-e", "./python-logging"])
    importlib.reload(site)
    import google.cloud.logging
    from google.cloud.logging_v2._helpers import retrieve_metadata_server


def simplelog(log_name=None, log_text="simple_log", severity="DEFAULT", **kwargs):
    # allowed severity: default, debug, info, notice, warning, error, critical, alert, emergency
    severity = severity.upper()
    client = google.cloud.logging.Client()
    logger = client.logger(log_name)
    logger.log_text(log_text, severity=severity)


def pylogging(log_text="pylogging", severity="WARNING", **kwargs):
    # allowed severity: debug, info, warning, error, critical
    severity = severity.upper()
    if severity == "DEBUG":
        logging.debug(log_text)
    elif severity == "INFO":
        logging.info(log_text)
    elif severity == "WARNING":
        logging.warning(log_text)
    elif severity == "ERROR":
        logging.error(log_text)
    else:
        logging.critical(log_text)

def pylogging_flask(log_text="pylogging_flask", path="/", base_url="http://google", agent="Chrome", trace="123", **kwargs):
    import flask
    app = flask.Flask(__name__)
    with app.test_request_context(
            path, base_url, headers={'User-Agent': agent, "X_CLOUD_TRACE_CONTEXT": trace}):
        logging.info(log_text)

def print_handlers(**kwargs):
    root_logger = logging.getLogger()
    handlers_str = ", ".join([type(h).__name__ for h in root_logger.handlers])
    logging.info(handlers_str)


def remove_stream_handlers(**kwargs):
    logger = logging.getLogger()
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            logging.error(handler)
            logger.removeHandler(handler)


def print_env_vars(env_var=None, **kwargs):
    if env_var:
        value = os.environ.get(env_var, None)
        if value:
            logging.error(value)
        else:
            logging.error(f"{env_var}: not found")
    else:
        logging.error(os.environ)


def get_metadata_server(metadata_key=None, **kwargs):
    if metadata_key is None:
        metadata_key = ""
    data = retrieve_metadata_server(metadata_key)
    logging.error(f"key: {metadata_key}, data:{data}")
