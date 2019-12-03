import os
from unittest import skip

from django.conf import settings
from django.db.backends.base.creation import BaseDatabaseCreation
from django.utils.module_loading import import_string


class DatabaseCreation(BaseDatabaseCreation):
    def mark_skips(self):
        """Skip tests that don't work on Spanner."""
        for test_name in self.connection.features.skip_tests:
            test_case_name, _, method_name = test_name.rpartition('.')
            test_app = test_name.split('.')[0]
            # Importing a test app that isn't installed raises RuntimeError.
            if test_app in settings.INSTALLED_APPS:
                test_case = import_string(test_case_name)
                method = getattr(test_case, method_name)
                setattr(test_case, method_name, skip('unsupported by Spanner')(method))

    def create_test_db(self, *args, **kwargs):
        # This environment variable is set by the Travis build script or
        # by a developer running the tests locally.
        if os.environ.get('RUNNING_SPANNER_BACKEND_TESTS'):
            self.mark_skips()
        super().create_test_db(*args, **kwargs)

    def _destroy_test_db(self, test_database_name, verbosity):
        # Cloud Spanner doesn't support dropping a database.
        pass
