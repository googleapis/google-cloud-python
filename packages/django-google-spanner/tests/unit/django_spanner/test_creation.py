# Copyright 2026 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import os
from unittest import mock
from django_spanner.creation import DatabaseCreation
from tests.unit.django_spanner.simple_test import SpannerSimpleTestClass


class TestCreation(SpannerSimpleTestClass):
    def setUp(self):
        super().setUp()
        self.db_wrapper.settings_dict = dict(self.settings_dict)
        self.db_wrapper.settings_dict["TEST"] = {"NAME": "test_db"}
        self.creation = DatabaseCreation(self.db_wrapper)

    def test_mark_skips(self):
        with mock.patch("django.conf.settings.INSTALLED_APPS", ["django.contrib.contenttypes"]):
            self.db_wrapper.features.skip_tests = (
                "django.contrib.contenttypes.models.ContentType",
            )
            self.creation.mark_skips()

    def test_create_test_db_user_cancel(self):
        with mock.patch.object(self.creation, "_execute_create_test_db", side_effect=Exception("err")):
            with mock.patch("builtins.input", return_value="no"):
                with self.assertRaises(SystemExit) as cm:
                    self.creation._create_test_db(verbosity=1, autoclobber=False, keepdb=False)
                self.assertEqual(cm.exception.code, 1)

    def test_create_test_db_recreate_error_exit(self):
        with mock.patch.object(self.creation, "_execute_create_test_db", side_effect=Exception("err")):
            with mock.patch.object(self.creation, "_destroy_test_db", side_effect=Exception("destroy_err")):
                with self.assertRaises(SystemExit) as cm:
                    self.creation._create_test_db(verbosity=1, autoclobber=True, keepdb=False)
                self.assertEqual(cm.exception.code, 2)

    def test_create_test_db(self):
        with mock.patch.dict(os.environ, {"RUNNING_SPANNER_BACKEND_TESTS": "1"}):
            with mock.patch.object(self.creation, "mark_skips") as mock_mark:
                with mock.patch("django.db.backends.base.creation.BaseDatabaseCreation.create_test_db"):
                    self.creation.create_test_db()
                    mock_mark.assert_called_once()

        # Without env var
        env = dict(os.environ)
        env.pop("RUNNING_SPANNER_BACKEND_TESTS", None)
        with mock.patch.dict(os.environ, env, clear=True):
            with mock.patch("django.db.backends.base.creation.BaseDatabaseCreation.create_test_db"):
                self.creation.create_test_db()

    def test_mark_skips_success_and_attribute_error(self):
        class DummyTestCase:
            def test_foo(self): pass
        with mock.patch("django.conf.settings.INSTALLED_APPS", ["tests"]):
            with mock.patch("django_spanner.creation.import_string", return_value=DummyTestCase):
                with mock.patch.object(self.creation.connection.features, "skip_tests", {"tests.DummyTestCase.test_foo", "tests.DummyTestCase.test_non_existent"}):
                    self.creation.mark_skips()
                    self.assertTrue(hasattr(DummyTestCase.test_foo, "__unittest_skip__"))

    def test_create_test_db_internal(self):
        with mock.patch.object(self.creation, "_execute_create_test_db", side_effect=[Exception("db exists"), None]):
            with mock.patch.object(self.creation, "_destroy_test_db") as mock_destroy:
                with mock.patch.object(self.creation, "log") as mock_log:
                    self.creation._create_test_db(verbosity=1, autoclobber=True, keepdb=False)
                    mock_destroy.assert_called_once()
                    mock_log.assert_called()

        with mock.patch.object(self.creation, "_execute_create_test_db", side_effect=[Exception("db exists"), None]):
            with mock.patch.object(self.creation, "_destroy_test_db"):
                self.creation._create_test_db(verbosity=0, autoclobber=True, keepdb=False)

    def test_create_test_db_internal_error_keepdb(self):
        with mock.patch.object(self.creation, "_execute_create_test_db", side_effect=Exception("create error")):
            dbname = self.creation._create_test_db(verbosity=1, autoclobber=True, keepdb=True)
            self.assertEqual(dbname, "test_db")

    def test_create_test_db_internal_error_recreate(self):
        with mock.patch.object(self.creation, "_execute_create_test_db", side_effect=[Exception("err1"), None]):
            with mock.patch.object(self.creation, "_destroy_test_db") as mock_destroy:
                dbname = self.creation._create_test_db(verbosity=1, autoclobber=True, keepdb=False)
                mock_destroy.assert_called_once()
                self.assertEqual(dbname, "test_db")

    def test_execute_create_and_destroy_test_db(self):
        mock_instance = mock.MagicMock()
        with mock.patch.object(type(self.db_wrapper), "instance", new_callable=mock.PropertyMock(return_value=mock_instance)):
            self.creation._execute_create_test_db(None, {"dbname": "test_db"}, keepdb=False)
            mock_instance.database.assert_called_with("test_db")
            mock_instance.database.return_value.create.assert_called_once()

            self.creation._destroy_test_db("test_db", verbosity=1)
            mock_instance.database.assert_called_with("test_db")
            mock_instance.database.return_value.drop.assert_called_once()
