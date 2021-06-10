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


def pylogging_json(log_text=None, severity="WARNING", **kwargs):
    # allowed severity: debug, info, warning, error, critical

    # build json message
    message = {}
    for k in kwargs.keys():
        message[k] = kwargs[k]

    severity = severity.upper()
    if severity == "DEBUG":
        logging.debug(message)
    elif severity == "INFO":
        logging.info(message)
    elif severity == "WARNING":
        logging.warning(message)
    elif severity == "ERROR":
        logging.error(message)
    else:
        logging.critical(message)

def pylogging(log_text="pylogging", severity="WARNING", **kwargs):
    # allowed severity: debug, info, warning, error, critical

    # build http request if fields given as argument
    http_keys = ["protocol", "requestUrl", "userAgent", "requestMethod"]
    if any([k in kwargs for k in http_keys]):
        http_request = {}
        for key in http_keys:
            if key in kwargs:
                http_request[key] = kwargs[key]
        kwargs["http_request"] = http_request
    # build source location if given as argument
    source_keys = ["line", "file", "function"]
    if any([k in kwargs for k in http_keys]):
        source_location = {}
        for key in source_keys:
            if key in kwargs:
                source_location[key] = kwargs[key]
        kwargs["source_location"] = source_location
    # build custom labels
    label_prefix = "label_"
    label_keys = [k for k in kwargs.keys() if k.startswith(label_prefix)]
    if label_keys:
        labels = {}
        for k in label_keys:
            adjusted_key = k[len(label_prefix) :]
            labels[adjusted_key] = kwargs[k]
        kwargs["labels"] = labels

    severity = severity.upper()
    if severity == "DEBUG":
        logging.debug(log_text, extra=kwargs)
    elif severity == "INFO":
        logging.info(log_text, extra=kwargs)
    elif severity == "WARNING":
        logging.warning(log_text, extra=kwargs)
    elif severity == "ERROR":
        logging.error(log_text, extra=kwargs)
    else:
        logging.critical(log_text, extra=kwargs)

def pylogging_multiline(log_text="pylogging", second_line="line 2", **kwargs):
    logging.error(f"{log_text}\n{second_line}")

def pylogging_complex_chars(**kwargs):
    logging.error('}"{!@[')

def pylogging_with_formatter(log_text="pylogging", format_str="%(name)s :: %(levelname)s :: %(message)s", **kwargs):
    root_logger = logging.getLogger()
    handler = root_logger.handlers[0]
    handler.setFormatter(logging.Formatter(fmt=format_str))
    logging.error(log_text)
    handler.setFormatter(None)

def pylogging_with_arg(log_text="my_arg", **kwargs):
    logging.error("Arg: %s", log_text)

def pylogging_flask(
    log_text="pylogging_flask",
    path="/",
    base_url="http://google",
    agent="Chrome",
    trace="123",
    **kwargs,
):
    import flask

    app = flask.Flask(__name__)
    with app.test_request_context(
        path, base_url, headers={"User-Agent": agent, "X_CLOUD_TRACE_CONTEXT": trace}
    ):
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
