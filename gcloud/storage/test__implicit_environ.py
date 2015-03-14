# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest2


class Test__get_production_project(unittest2.TestCase):

    def _callFUT(self):
        from gcloud.storage import _implicit_environ
        return _implicit_environ._get_production_project()

    def test_no_value(self):
        import os
        from gcloud._testing import _Monkey

        environ = {}
        with _Monkey(os, getenv=environ.get):
            project = self._callFUT()
            self.assertEqual(project, None)

    def test_value_set(self):
        import os
        from gcloud._testing import _Monkey
        from gcloud.storage._implicit_environ import _PROJECT_ENV_VAR_NAME

        MOCK_PROJECT = object()
        environ = {_PROJECT_ENV_VAR_NAME: MOCK_PROJECT}
        with _Monkey(os, getenv=environ.get):
            project = self._callFUT()
            self.assertEqual(project, MOCK_PROJECT)


class Test__determine_default_project(unittest2.TestCase):

    def _callFUT(self, project=None):
        from gcloud.storage._implicit_environ import _determine_default_project
        return _determine_default_project(project=project)

    def _determine_default_helper(self, prod=None, project=None):
        from gcloud._testing import _Monkey
        from gcloud.storage import _implicit_environ

        _callers = []

        def prod_mock():
            _callers.append('prod_mock')
            return prod

        patched_methods = {
            '_get_production_project': prod_mock,
        }

        with _Monkey(_implicit_environ, **patched_methods):
            returned_project = self._callFUT(project)

        return returned_project, _callers

    def test_no_value(self):
        project, callers = self._determine_default_helper()
        self.assertEqual(project, None)
        self.assertEqual(callers, ['prod_mock'])

    def test_explicit(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(project=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, [])

    def test_prod(self):
        PROJECT = object()
        project, callers = self._determine_default_helper(prod=PROJECT)
        self.assertEqual(project, PROJECT)
        self.assertEqual(callers, ['prod_mock'])


class Test_set_default_project(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage._testing import _setup_defaults
        _setup_defaults(self)

    def tearDown(self):
        from gcloud.storage._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def _callFUT(self, project=None):
        from gcloud.storage._implicit_environ import set_default_project
        return set_default_project(project=project)

    def test_raises(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import _implicit_environ

        _called_project = []

        def mock_determine(project):
            _called_project.append(project)
            return None

        with _Monkey(_implicit_environ,
                     _determine_default_project=mock_determine):
            self.assertRaises(EnvironmentError, self._callFUT)

        self.assertEqual(_called_project, [None])

    def test_set_correctly(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import _implicit_environ

        self.assertEqual(_implicit_environ._DEFAULTS.project, None)

        PROJECT = object()
        _called_project = []

        def mock_determine(project):
            _called_project.append(project)
            return PROJECT

        with _Monkey(_implicit_environ,
                     _determine_default_project=mock_determine):
            self._callFUT()

        self.assertEqual(_implicit_environ._DEFAULTS.project, PROJECT)
        self.assertEqual(_called_project, [None])


class Test_lazy_loading(unittest2.TestCase):

    def setUp(self):
        from gcloud.storage._testing import _setup_defaults
        _setup_defaults(self, implicit=True)

    def tearDown(self):
        from gcloud.storage._testing import _tear_down_defaults
        _tear_down_defaults(self)

    def test_descriptor_for_project(self):
        from gcloud._testing import _Monkey
        from gcloud.storage import _implicit_environ

        self.assertFalse('project' in _implicit_environ._DEFAULTS.__dict__)

        DEFAULT = object()

        with _Monkey(_implicit_environ,
                     _determine_default_project=lambda: DEFAULT):
            lazy_loaded = _implicit_environ._DEFAULTS.project

        self.assertEqual(lazy_loaded, DEFAULT)
        self.assertTrue('project' in _implicit_environ._DEFAULTS.__dict__)
