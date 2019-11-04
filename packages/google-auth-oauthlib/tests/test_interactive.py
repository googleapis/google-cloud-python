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

import mock


def test_get_user_credentials():
    from google_auth_oauthlib import flow
    from google_auth_oauthlib import interactive as module_under_test

    mock_flow_instance = mock.create_autospec(flow.InstalledAppFlow, instance=True)

    with mock.patch(
        "google_auth_oauthlib.flow.InstalledAppFlow", autospec=True
    ) as mock_flow:
        mock_flow.from_client_config.return_value = mock_flow_instance
        module_under_test.get_user_credentials(
            ["scopes"], "some-client-id", "shh-secret"
        )

    mock_flow.from_client_config.assert_called_once_with(mock.ANY, scopes=["scopes"])
    actual_client_config = mock_flow.from_client_config.call_args[0][0]
    assert actual_client_config["installed"]["client_id"] == "some-client-id"
    assert actual_client_config["installed"]["client_secret"] == "shh-secret"
    mock_flow_instance.run_console.assert_called_once()
