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

from test_utils.retry import RetryErrors

from .script_utils import ScriptRunner
from .script_utils import Command

class LogsNotFound(RuntimeError):
    """raised when filter returns no logs."""
    pass

class Common:
    _client = Client()
    # environment name must be set by subclass
    environment = None

    def _add_time_condition_to_filter(self, filter_str, timestamp=None):
        time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        if not timestamp:
            timestamp = datetime.now(timezone.utc) - timedelta(minutes=10)
        return f'"{filter_str}" AND timestamp > "{timestamp.strftime(time_format)}"'


    def _get_logs(self, filter_str=None):
        if not filter_str:
            _, filter_str = self._script.run_command(Command.GetFilter)
        iterator = self._client.list_entries(filter_=filter_str)
        entries = list(iterator)
        if not entries:
            raise LogsNotFound
        return entries

    def _trigger(self, function, **kwargs):
        timestamp = datetime.now(timezone.utc)
        args_str = ",".join([f'{k}="{v}"' for k, v in kwargs.items()])
        self._script.run_command(Command.Trigger, [function, args_str])

    @classmethod
    def setUpClass(cls):
        if not cls.environment:
            raise NotImplementedError("environment not set by subclass")
        if not cls.language:
            raise NotImplementedError("language not set by subclass")
        cls._script = ScriptRunner(cls.environment, cls.language)
        # check if already setup
        status, _ = cls._script.run_command(Command.Verify)
        if status == 0:
            if os.getenv("NO_CLEAN"):
                # ready to go
                return
            else:
                # reset environment
                status, _ = cls._script.run_command(Command.Destroy)
                assert status == 0
        # deploy test code to GCE
        status, _ = cls._script.run_command(Command.Deploy)
        # verify code is running
        status, _ = cls._script.run_command(Command.Verify)
        assert status == 0

    @classmethod
    def tearDown_class(cls):
        # by default, destroy environment on each run
        # allow skipping deletion for development
        if not os.getenv("NO_CLEAN"):
            cls._script.run_command(Command.Destroy)

    @RetryErrors(exception=LogsNotFound)
    def test_receive_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name}: {uuid.uuid1()}"
        self._trigger("pylogging", log_text=log_text)
        # give the command time to be received
        sleep(30)
        filter_str = self._add_time_condition_to_filter(log_text)
        # retrieve resulting logs
        log_list = self._get_logs(filter_str)

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
