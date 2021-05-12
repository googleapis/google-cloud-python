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

from time import sleep
from datetime import datetime
from datetime import timezone
import os
import sys
from shlex import split
import subprocess
import signal
from enum import Enum
from pathlib import Path


class Command(Enum):
    Deploy = "deploy"
    Destroy = "destroy"
    Verify = "verify"
    GetFilter = "filter-string"
    Trigger = "trigger"


class ScriptRunner:
    def __init__(self, environment, language):
        run_dir = os.path.dirname(os.path.realpath(__file__))
        repo_root = Path(run_dir).parent.parent
        self.script_path = os.path.join(repo_root, "envctl/envctl")
        self.environment = environment
        self.language = language
        env_path = os.path.join(
            repo_root, f"envctl/env_scripts/{language}/{environment}.sh"
        )
        if not os.path.exists(env_path):
            raise RuntimeError(f"{env_path} does not exist")

    def run_command(self, command, args=[]):
        if not command or not isinstance(command, Command):
            raise RuntimeError(f"unknown command: {command}")
        os.setpgrp()
        complete = False
        try:
            full_command = [self.script_path, self.language, self.environment] + split(
                command.value
            )
            for arg in args:
                full_command.append(arg)
            print(full_command)
            result = subprocess.run(full_command, capture_output=True)
            complete = True
            return result.returncode, result.stdout.decode("utf-8"), result.stderr.decode("utf-8")
        except Exception as e:
            print(e)
        finally:
            if not complete:
                # kill background process if script is terminated
                # os.killpg(0, signal.SIGTERM)
                return 1, None
