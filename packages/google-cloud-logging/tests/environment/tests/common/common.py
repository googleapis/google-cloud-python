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
import os
import sys
import uuid
import inspect

from .script_utils import ScriptRunner
from .script_utils import Command


class Common:
    _client = Client()
    # environment name must be set by subclass
    environment = None

    def _get_logs(self, timestamp=None):
        time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        if not timestamp:
            timestamp = datetime.now(timezone.utc) - timedelta(minutes=10)
        _, filter_str = self._script.run_command(Command.GetFilter)
        filter_str += ' AND timestamp > "%s"' % timestamp.strftime(time_format)
        iterator = self._client.list_entries(filter_=filter_str)
        entries = list(iterator)
        return entries

    def _trigger(self, function, return_logs=True, **kwargs):
        timestamp = datetime.now(timezone.utc)
        args_str = ",".join([f'{k}="{v}"' for k, v in kwargs.items()])
        self._script.run_command(Command.Trigger, [function, args_str])
        # give the command time to be received
        sleep(30)
        if return_logs:
            log_list = self._get_logs(timestamp)
            return log_list

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

    def test_receive_log(self):
        log_text = f"{inspect.currentframe().f_code.co_name}: {uuid.uuid1()}"
        log_list = self._trigger("pylogging", log_text=log_text)
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
