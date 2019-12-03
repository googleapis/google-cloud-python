from django.db.backends.base.features import BaseDatabaseFeatures


class DatabaseFeatures(BaseDatabaseFeatures):
    supports_foreign_keys = False
    supports_transactions = False

    # Django tests that aren't supported by Spanner.
    skip_tests = (
        # No Django transaction management in Spanner.
        'basic.tests.SelectOnSaveTests.test_select_on_save_lying_update',
        # spanner.django monkey patches AutoField to have a default value.
        'basic.tests.ModelTest.test_hash',
    )
