# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from django_spanner.utils import check_django_compatability
from django.core.exceptions import ImproperlyConfigured
from django_spanner.utils import add_dummy_where
import django
import django_spanner
from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass


class TestUtils(SpannerSimpleTestClass):
    SQL_WITH_WHERE = "Select 1 from Table WHERE 1=1"
    SQL_WITHOUT_WHERE = "Select 1 from Table"
    # Only active LTS django versions (2.2.*, 3.2.*) are supported by this library right now.
    SUPPORTED_DJANGO_VERSIONS = [(2, 2), (3, 2)]

    def test_check_django_compatability_match(self):
        """
        Checks django compatibility match.
        """
        django_spanner.__version__ = "2.2"
        django.VERSION = (2, 2, 19, "alpha", 0)
        check_django_compatability(self.SUPPORTED_DJANGO_VERSIONS)

    def test_check_django_compatability_mismatch(self):
        """
        Checks django compatibility mismatch.
        """
        django_spanner.__version__ = "2.2"
        django.VERSION = (3, 1, 19, "alpha", 0)
        with self.assertRaises(ImproperlyConfigured):
            check_django_compatability(self.SUPPORTED_DJANGO_VERSIONS)

    def test_add_dummy_where_with_where_present_and_not_added(self):
        """
        Checks if dummy where clause is not added when present in select
        statement.
        """
        updated_sql = add_dummy_where(self.SQL_WITH_WHERE)
        self.assertEqual(updated_sql, self.SQL_WITH_WHERE)

    def test_add_dummy_where_with_where_not_present_and_added(self):
        """
        Checks if dummy where clause is added when not present in select
        statement.
        """
        updated_sql = add_dummy_where(self.SQL_WITHOUT_WHERE)
        self.assertEqual(updated_sql, self.SQL_WITH_WHERE)
