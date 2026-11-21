# Copyright 2026 Google LLC All Rights Reserved.
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

from unittest import mock

from google.cloud.spanner_admin_database_v1.types import backup as backup_pb
import pytest

import backup_sample

EXPECTED_BACKUP_LRO_TIMEOUT = 3600


@pytest.mark.parametrize(
    ("sample_fn", "api_method", "args"),
    [
        (backup_sample.create_backup, "create_backup", ("inst", "db", "bk", None)),
        (
            backup_sample.create_backup_with_encryption_key,
            "create_backup",
            ("inst", "db", "bk", "projects/p/locations/l/keyRings/r/cryptoKeys/k"),
        ),
        (
            backup_sample.create_backup_with_multiple_kms_keys,
            "create_backup",
            (
                "inst",
                "db",
                "bk",
                ["projects/p/locations/l/keyRings/r/cryptoKeys/k1"],
            ),
        ),
        (
            backup_sample.copy_backup,
            "copy_backup",
            ("inst", "bk", "projects/p/instances/inst/backups/src"),
        ),
        (
            backup_sample.copy_backup_with_multiple_kms_keys,
            "copy_backup",
            (
                "inst",
                "bk",
                "projects/p/instances/inst/backups/src",
                ["projects/p/locations/l/keyRings/r/cryptoKeys/k1"],
            ),
        ),
    ],
)
def test_backup_lro_polling_timeout(capsys, sample_fn, api_method, args):
    mock_operation = mock.MagicMock()
    mock_operation.result.return_value = backup_pb.Backup(
        name="projects/p/instances/inst/backups/bk",
        state=backup_pb.Backup.State.READY,
    )

    mock_admin_api = mock.MagicMock()
    mock_admin_api.instance_path.return_value = "projects/p/instances/inst"
    mock_admin_api.database_path.return_value = "projects/p/instances/inst/databases/db"
    setattr(getattr(mock_admin_api, api_method), "return_value", mock_operation)

    mock_client = mock.MagicMock()
    mock_client.project = "p"
    mock_client.database_admin_api = mock_admin_api

    with mock.patch("backup_sample.spanner.Client", return_value=mock_client):
        sample_fn(*args)

    mock_operation.result.assert_called_once_with(EXPECTED_BACKUP_LRO_TIMEOUT)
    out, _ = capsys.readouterr()
    assert "projects/p/instances/inst/backups/bk" in out
