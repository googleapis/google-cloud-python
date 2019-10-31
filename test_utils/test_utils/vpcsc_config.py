# -*- coding: utf-8 -*-
#
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

import os

import pytest


INSIDE_VPCSC_ENVVAR = "GOOGLE_CLOUD_TESTS_IN_VPCSC"
PROJECT_INSIDE_ENVVAR = "PROJECT_ID"
PROJECT_OUTSIDE_ENVVAR = "GOOGLE_CLOUD_TESTS_VPCSC_OUTSIDE_PERIMETER_PROJECT"


class VPCSCTestConfig(object):
    """System test utility for VPCSC detection.
    
    See: https://cloud.google.com/vpc-service-controls/docs/
    """

    @property
    def inside_vpcsc(self):
        """Is the test environment inside VPCSC.

        Returns:
            bool: true if the environment is inside VPCSC, else false.
        """
        value = os.environ.get(INSIDE_VPCSC_ENVVAR, "true").lower()
        return value == "true"

    @property
    def project_inside(self):
        """Project ID for testing outside access.

        Returns:
            str: project ID used for testing outside access; None if undefined.
        """
        return os.environ.get(PROJECT_INSIDE_ENVVAR, None)

    @property
    def project_outside(self):
        """Project ID for testing inside access.

        Returns:
            str: project ID used for testing inside access; None if undefined.
        """
        return os.environ.get(PROJECT_OUTSIDE_ENVVAR, None)

    def skip_if_running_inside_vpcsc(self, testcase):
        """Test decorator: skip if running inside VPCSC."""
        reason = "Running inside VPCSC"
        skip = pytest.mark.skipif(self.inside_vpcsc, reason=reason)
        return skip(testcase)

    def skip_if_running_outside_vpcsc(self, testcase):
        """Test decorator: skip if running outside VPCSC."""
        reason = "Running outside VPCSC"
        skip = pytest.mark.skipif(not self.inside_vpcsc, reason=reason)
        return skip(testcase)

    def skip_if_inside_vpcsc(self, testcase):
        """Test decorator: skip if inside project env var not set."""
        reason = "Running inside VPCSC"
        skip = pytest.mark.skipif(self.inside_vpcsc, reason=reason)
        return skip(testcase)

    def skip_if_no_inside_project(self, testcase):
        """Test decorator: skip if inside project env var not set."""
        reason = "Missing envvar: {}".format(PROJECT_INSIDE_ENVVAR)
        skip = pytest.mark.skipif(self.project_inside is None, reason=reason)
        return skip(testcase)

    def skip_if_no_outside_project(self, testcase):
        """Test decorator: skip if outside project env var not set."""
        reason = "Missing envvar: {}".format(PROJECT_OUTSIDE_ENVVAR)
        skip = pytest.mark.skipif(self.project_outside is None, reason=reason)
        return skip(testcase)


vpcsc_config = VPCSCTestConfig()
