# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess

from django.db.backends.base.client import BaseDatabaseClient
from spanner.dbapi.parse_utils import extract_connection_params


class DatabaseClient(BaseDatabaseClient):
    executable_name = 'spanner'

    @classmethod
    def settings_to_cmd_args(cls, settings_dict):
        args = [cls.executable_name]
        settings = extract_connection_params(cls.settings_dict)
        project_id = settings['project_id']
        if project_id:
            args += ['--project_id=%s' % project_id]
        instance = settings['instance']
        if instance:
            args += ['--instance=%s' % instance]
        db_name = settings['db_name']
        if db_name:
            args += ['--db_name=%s' % db_name]
        auto_commit = settings['auto_commit']
        if auto_commit:
            args += ['--auto_commit=%s' % auto_commit]
        read_only = settings['read_only']
        if read_only:
            args += ['--read_only=%s' % read_only]

        return args

    def runshell(self):
        args = DatabaseClient.settings_to_cmd_args(self.connection.settings_dict)
        subprocess.run(args, check=True)
