# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import sys
from unittest import TestCase

from google.api_core.gapic_v1.client_info import ClientInfo
from spanner.dbapi.version import USER_AGENT, google_client_info


class VersionUtils(TestCase):
    def test_google_client_info(self):
        vers = sys.version_info
        got = google_client_info().to_grpc_metadata()
        want = ClientInfo(
            user_agent=USER_AGENT,
            python_version='%d.%d.%d' % (vers.major, vers.minor, vers.micro or 0),
        ).to_grpc_metadata()
        self.assertEqual(got, want)
