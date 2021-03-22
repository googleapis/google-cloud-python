# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import unittest
from contextlib import contextmanager
from sphinx.application import Sphinx

@contextmanager
def sphinx_build(test_dir):
    os.chdir('tests/{0}'.format(test_dir))

    try:
        app = Sphinx(
            srcdir='doc',
            confdir='doc',
            outdir='_build/yaml',
            doctreedir='_build/.doctrees',
            buildername='html',
        )
        app.build(force_all=True)
        yield
    finally:
        # shutil.rmtree('_build')
        os.chdir('../..')

if __name__ == '__main__':
    with sphinx_build('example'):
        print('Debug finished.')
