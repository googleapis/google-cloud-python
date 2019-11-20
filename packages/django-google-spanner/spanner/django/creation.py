from django.db.backends.base.creation import BaseDatabaseCreation


class DatabaseCreation(BaseDatabaseCreation):
    def _destroy_test_db(self, test_database_name, verbosity):
        # Cloud Spanner doesn't support dropping a database.
        pass
