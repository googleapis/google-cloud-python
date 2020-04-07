import os

from django.core import checks
from django.db.backends.base.validation import BaseDatabaseValidation
from django.db.models import DecimalField


class DatabaseValidation(BaseDatabaseValidation):

    def check_field_type(self, field, field_type):
        errors = []
        # Disable the error when running the Django test suite.
        if os.environ.get('RUNNING_SPANNER_BACKEND_TESTS') != '1' and isinstance(field, DecimalField):
            errors.append(
                checks.Error(
                    'DecimalField is not yet supported by Spanner.',
                    obj=field,
                    id='spanner.E001',
                )
            )
        return errors
