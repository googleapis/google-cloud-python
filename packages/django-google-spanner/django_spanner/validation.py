import os

from django.core import checks
from django.db.backends.base.validation import BaseDatabaseValidation
from django.db.models import DecimalField


class DatabaseValidation(BaseDatabaseValidation):
    def check_field_type(self, field, field_type):
        """Check field type and collect errors.

        :type field: :class:`~django.db.migrations.operations.models.fields.FieldOperation`
        :param field: The field of the table.

        :type field_type: str
        :param field_type: The type of the field.

        :rtype: list
        :return: A list of errors.
        """
        errors = []
        # Disable the error when running the Django test suite.
        if os.environ.get(
            "RUNNING_SPANNER_BACKEND_TESTS"
        ) != "1" and isinstance(field, DecimalField):
            errors.append(
                checks.Error(
                    "DecimalField is not yet supported by Spanner.",
                    obj=field,
                    id="spanner.E001",
                )
            )
        return errors
