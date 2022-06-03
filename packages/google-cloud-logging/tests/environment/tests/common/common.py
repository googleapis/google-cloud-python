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

import google.cloud.logging
from google.cloud._helpers import UTC
from google.cloud.logging_v2 import ProtobufEntry
from google.cloud.logging_v2.handlers.handlers import CloudLoggingHandler
from google.cloud.logging_v2.handlers.transports import SyncTransport
from google.cloud.logging_v2 import Client
from google.cloud.logging_v2.resource import Resource
from google.cloud.logging_v2 import entries
from google.cloud.logging_v2._helpers import LogSeverity

from time import sleep
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import os
import sys
import uuid
import inspect
import random

from test_utils.retry import RetryErrors
from grpc import RpcError

from .script_utils import ScriptRunner
from .script_utils import Command


class LogsNotFound(RuntimeError):
    """raised when filter returns no logs."""

    pass


class Common:
    _client = Client()
    # environment name and monitored resource values must be set by subclass
    environment = None
    monitored_resource_name = None
    monitored_resource_labels = None

    def _add_time_condition_to_filter(self, filter_str, timestamp=None):
        """
        Appends a 10 minute limit to an arbitrary filter string
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        if not timestamp:
            timestamp = datetime.now(timezone.utc) - timedelta(minutes=10)
        return f'"{filter_str}" AND timestamp > "{timestamp.strftime(time_format)}"'

    def _get_logs(self, filter_str=None, ignore_protos=True):
        """
        Helper function to retrieve the text and json logs using an input
        filter string.

        Parameters:
            filter_str (str): the filter string determining which logs to include
            ignore_protos (bool): when disabled, matching protobuf entries will be included.
                This may result false positives from AuditLogs on certain projects

        Returns:
            list[LogEntry]
        """
        if not filter_str:
            _, filter_str, _ = self._script.run_command(Command.GetFilter)
        iterator = self._client.list_entries(filter_=filter_str)
        entries = list(iterator)
        if ignore_protos:
            # in most cases, we want to ignore AuditLogs in our tests
            entries = [e for e in entries if not isinstance(e, ProtobufEntry)]
        if not entries:
            raise LogsNotFound
        return entries

    def _trigger(self, snippet, **kwargs):
        """
        Helper function for triggering a snippet deployed in a cloud environment
        """
        timestamp = datetime.now(timezone.utc)
        args_str = ",".join([f'{k}="{v}"' for k, v in kwargs.items()])
        self._script.run_command(Command.Trigger, [snippet, args_str])

    @RetryErrors(exception=(LogsNotFound, RpcError), delay=2, max_tries=2)
    def trigger_and_retrieve(
        self,
        log_text,
        snippet,
        append_uuid=True,
        ignore_protos=True,
        max_tries=5,
        **kwargs,
    ):
        """
        Trigger a snippet deployed in the cloud by envctl, and return resulting
        logs.

        Parameters:
            log_text (str): passed as an argument to the snippet function.
                Typically used for the body of the resulting log,
            snippet (str): the name of the snippet to trigger.
            append_uuid (bool): when true, appends a unique suffix to log_text,
                to ensure old logs aren't picket up in later runs
            ignore_protos: when disabled, matching protobuf entries will be included.
                This may result false positives from AuditLogs on certain projects
            max_tries (int): number of times to retry if logs haven't been found
            **kwargs: additional arguments are passed as arguments to the snippet function

        Returns:
            list[LogEntry]
        """

        if append_uuid:
            log_text = f"{log_text} {uuid.uuid1()}"
        self._trigger(snippet, log_text=log_text, **kwargs)
        sleep(10)
        filter_str = self._add_time_condition_to_filter(log_text)
        print(filter_str)
        # give the command time to be received
        tries = 0
        while tries < max_tries:
            # retrieve resulting logs
            try:
                log_list = self._get_logs(filter_str, ignore_protos)
                return log_list
            except RpcError as e:
                print(f"RPC error: {e}")
                # most RpcErrors come from exceeding the reads per minute quota
                # wait between 5-15 minutes
                # use a randomized backoff so parallel runs don't start up at
                # the same time again
                sleep(random.randint(300, 900))
                tries += 1
            except LogsNotFound as e:
                print("logs not found...")
                # logs may not have been fully ingested into Cloud Logging
                # Wait before trying again
                sleep(10 * (tries + 1))
                tries += 1
        # log not found
        raise LogsNotFound

    @classmethod
    def setUpClass(cls):
        if not cls.environment:
            raise NotImplementedError("environment not set by subclass")
        if not cls.language:
            raise NotImplementedError("language not set by subclass")
        cls._script = ScriptRunner(cls.environment, cls.language)
        # check if already setup
        status, _, _ = cls._script.run_command(Command.Verify)
        if status == 0:
            if os.getenv("NO_CLEAN"):
                # ready to go
                return
            else:
                # reset environment
                status, _, _ = cls._script.run_command(Command.Destroy)
                assert status == 0
        # deploy test code to GCE
        status, _, err = cls._script.run_command(Command.Deploy)
        if status != 0:
            print(err)
        # verify code is running
        status, _, err = cls._script.run_command(Command.Verify)
        if status != 0:
            print(err)
        assert status == 0

    @classmethod
    def tearDown_class(cls):
        # by default, destroy environment on each run
        # allow skipping deletion for development
        if not os.getenv("NO_CLEAN"):
            cls._script.run_command(Command.Destroy)

    def test_receive_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text, "simplelog")

        found_log = None
        for log in log_list:
            message = (
                log.payload.get("message", None)
                if isinstance(log.payload, dict)
                else str(log.payload)
            )
            if message and log_text in message:
                found_log = log
        self.assertIsNotNone(found_log, "expected log text not found")

    def test_receive_unicode_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name} 嗨 世界 😀"
        log_list = self.trigger_and_retrieve(log_text, "simplelog")

        found_log = None
        for log in log_list:
            message = (
                log.payload.get("message", None)
                if isinstance(log.payload, dict)
                else str(log.payload)
            )
            if message and log_text in message:
                found_log = log
        self.assertIsNotNone(found_log, "expected unicode log not found")

    def test_json_log(self):
        if self.language not in ["python"]:
            # TODO: other languages to also support this test
            return True
        log_text = f"{inspect.currentframe().f_code.co_name} {uuid.uuid1()}"
        log_dict = {"unicode_field": "嗨 世界 😀", "num_field": 2}
        log_list = self.trigger_and_retrieve(
            log_text, "jsonlog", append_uuid=False, **log_dict
        )

        found_log = log_list[-1]

        self.assertIsNotNone(found_log, "expected log text not found")
        self.assertTrue(isinstance(found_log.payload, dict), "expected jsonPayload")
        expected_dict = {"message": log_text, **log_dict}
        self.assertEqual(found_log.payload, expected_dict)

    def test_monitored_resource(self):
        if self.language == "java":
            # TODO: implement in java
            return True

        log_text = f"{inspect.currentframe().f_code.co_name}"
        log_list = self.trigger_and_retrieve(log_text, "simplelog")
        found_resource = log_list[-1].resource

        self.assertIsNotNone(self.monitored_resource_name)
        self.assertIsNotNone(self.monitored_resource_labels)

        self.assertEqual(found_resource.type, self.monitored_resource_name)
        for label in self.monitored_resource_labels:
            self.assertTrue(
                found_resource.labels[label], f"resource.labels[{label}] is not set"
            )

    def test_severity(self):
        log_text = f"{inspect.currentframe().f_code.co_name}"
        severities = [
            "EMERGENCY",
            "ALERT",
            "CRITICAL",
            "ERROR",
            "WARNING",
            "NOTICE",
            "INFO",
            "DEBUG",
        ]
        for severity in severities:
            log_list = self.trigger_and_retrieve(
                log_text, "simplelog", severity=severity
            )
            found_severity = log_list[-1].severity
            self.assertEqual(found_severity.lower(), severity.lower())
        # DEFAULT severity should result in empty field
        log_list = self.trigger_and_retrieve(log_text, "simplelog", severity="DEFAULT")
        self.assertIsNone(log_list[-1].severity)
