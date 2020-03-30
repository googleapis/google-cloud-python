# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import sys
from unittest import TestCase

from google.api_core.gapic_v1.client_info import ClientInfo
from spanner_dbapi.version import DEFAULT_USER_AGENT, google_client_info

vers = sys.version_info


class VersionUtils(TestCase):
    def test_google_client_info_default_useragent(self):
        got = google_client_info().to_grpc_metadata()
        want = ClientInfo(
            user_agent=DEFAULT_USER_AGENT,
            python_version='%d.%d.%d' % (vers.major, vers.minor, vers.micro or 0),
        ).to_grpc_metadata()
        self.assertEqual(got, want)

    def test_google_client_info_custom_useragent(self):
        got = google_client_info('custom-user-agent').to_grpc_metadata()
        want = ClientInfo(
            user_agent='custom-user-agent',
            python_version='%d.%d.%d' % (vers.major, vers.minor, vers.micro or 0),
        ).to_grpc_metadata()
        self.assertEqual(got, want)
