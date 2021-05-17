# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

from django_spanner.validation import DatabaseValidation
from django.db import connection
from django.core.checks import Error as DjangoError
from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass
from .models import ModelDecimalField, ModelCharField


class TestValidation(SpannerSimpleTestClass):
    def test_check_field_type_with_decimal_field_not_support_error(self):
        """
        Checks if decimal field fails database validation as it's not
        supported in spanner.
        """
        field = ModelDecimalField._meta.get_field("field")
        validator = DatabaseValidation(connection=connection)
        self.assertEqual(
            validator.check_field(field),
            [
                DjangoError(
                    "DecimalField is not yet supported by Spanner.",
                    obj=field,
                    id="spanner.E001",
                )
            ],
        )

    def test_check_field_type_with_char_field_no_error(self):
        """
        Checks if string field passes database validation.
        """
        field = ModelCharField._meta.get_field("field")
        validator = DatabaseValidation(connection=connection)
        self.assertEqual(
            validator.check_field(field), [],
        )
