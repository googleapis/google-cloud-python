# Copyright 2026 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import importlib
import os
from unittest import mock

from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass


class TestFeatures(SpannerSimpleTestClass):
    def test_features_emulator_and_env(self):
        import django_spanner
        import django_spanner.features

        with mock.patch.dict(os.environ, {"RUNNING_SPANNER_BACKEND_TESTS": "1", "SPANNER_EMULATOR_HOST": "localhost:9010"}):
            with mock.patch.object(django_spanner, "USE_EMULATOR", True):
                importlib.reload(django_spanner.features)
                feat = django_spanner.features.DatabaseFeatures(self.db_wrapper)
                self.assertFalse(feat.supports_foreign_keys)
                self.assertFalse(feat.supports_json_field)
                self.assertTrue(any("test_loaddata" in test for test in feat.skip_tests))

        importlib.reload(django_spanner.features)
