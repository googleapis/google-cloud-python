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
import re
import yaml
import shutil
import unittest

from contextlib import contextmanager

from sphinx.application import Sphinx


@contextmanager
def sphinx_build(test_dir):
    """ Use contextmanager to ensure build cleaning after testing.
    """

    os.chdir('tests/{0}'.format(test_dir))

    try:
        app = Sphinx(
            srcdir='./doc',
            confdir='./doc',
            outdir='_build/text',
            doctreedir='_build/.doctrees',
            buildername='html'
        )
        app.build(force_all=True)
        yield
    finally:
        shutil.rmtree('_build')
        os.chdir('../..')


class YamlTests(unittest.TestCase):
    build_path = '_build/text/docfx_yaml' #: Path of all the yaml files.

    yaml_files = { #: yaml files needed to be tested.
        "class_files": {
            "google": [
                "format.google.foo.Foo.yml",
                "format.google.foo.FooException.InternalFoo.yml",
                "format.google.foo.FooException.yml"
            ],
            "numpy": [
                "format.numpy.foo.Foo.yml",
                "format.numpy.foo.FooException.InternalFoo.yml",
                "format.numpy.foo.FooException.yml"
            ],
            "rst": [
                "format.rst.directives.DirectivesFoo.yml",
                "format.rst.enum.EnumFoo.yml",
                "format.rst.foo.Foo.yml",
                "format.rst.foo.FooException.InternalFoo.yml",
                "format.rst.foo.FooException.yml",
                "format.rst.foo.InheritFoo.yml"
            ],
            "namespacepackage": [
                "nspkg.native.native_foo.Foo.yml",
                "nspkg.pkgutil.pkgutil_foo.Foo.yml",
                "nspkg.pkg_resources.pkg_resources_foo.Foo.yml"
            ]
        },
        "module_files": {
            "google": [
                "format.google.foo.yml"
            ],
            "numpy": [
                "format.numpy.foo.yml"
            ],
            "rst": [
                "format.rst.directives.yml",
                "format.rst.enum.yml",
                "format.rst.foo.yml"
            ]
        },
        "package_files": {
            "namesapcepackage": [
                "nspkg.yml",
                "nspkg.native.native_foo.yml",
                "nspkg.pkgutil.yml",
                "nspkg.pkgutil.pkgutil_foo.yml",
                "nspkg.pkg_resources.yml",
                "nspkg.pkg_resources.pkg_resources_foo.yml"
            ],
            "format": [
                "format.yml",
                "format.rst.yml",
                "format.google.yml",
                "format.numpy.yml"
            ]
        }
    }

    def test_uid(self):
        """
        Test whether uids are generated correctly.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['rst'][0]), 'r') as f:
                # Test uids in format.rst.directives.DirectivesFoo.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['uid'],
                    'format.rst.directives.DirectivesFoo'
                )

            with open(os.path.join(self.build_path, self.yaml_files['module_files']['rst'][1]), 'r') as f:
                # Test uids in format.rst.enum.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['uid'],
                    'format.rst.enum'
                )

            with open(os.path.join(self.build_path, self.yaml_files['package_files']['format'][2]), 'r') as f:
                # Test uids in format.google.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['uid'],
                    'format.google'
                )

    def test_name(self):
        """
        Test whether names are generated correctly.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['rst'][0]), 'r') as f:
                # Test names in format.rst.directives.DirectivesFoo.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['name'],
                    'DirectivesFoo'
                )

                self.assertEqual(
                    data['items'][1]['name'],
                    'method_remarks()'
                )  # Test name of method format.rst.directives.DirectivesFoo.method_remarks

            with open(os.path.join(self.build_path, self.yaml_files['module_files']['rst'][1]), 'r') as f:
                # Test names in format.rst.enum.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['name'],
                    'enum'
                )

            with open(os.path.join(self.build_path, self.yaml_files['package_files']['format'][2]), 'r') as f:
                # Test names in format.google.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['name'],
                    'google'
                )

    def test_alert_box(self):
        """
        Test whether alert boxes are generated correctly.
        Avaliable alert boxes are Note, Warning, Tip and Important
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['rst'][0]), 'r') as f:
                # Test alert boxes in format.rst.directives.DirectivesFoo.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['summary'],
                    'Docstring of class <xref:format.rst.directives.DirectivesFoo>.\n\n\n> [!NOTE]\n> Note content from class docstring.\n>\n> Second line of note content.\n>\n> many lines of content.\n>\n\n\n> [!WARNING]\n> Warning message from class docstring.\n>\n> Second line.\n>\n\n\n> [!TIP]\n> Tip content. <xref:format.rst.foo.Foo>\n>\n\n\n> [!IMPORTANT]\n> Important content.\n>\n\n\n> [!CAUTION]\n> Caution content.\n>'
                )  # Test alert box in summary section

                self.assertEqual(
                    data['items'][0]['remarks'],
                    'Remarks from class.\nMulti-line content should be supported.\n\n\n> [!NOTE]\n> Note conetnt under class remarks.\n>\n> Second line of note content.\n>\n> [!WARNING]\n> Warning content under class remarks.\n>\n> Second line.\n>\n> <xref:format.rst.foo.Foo>\n>\n> [!TIP]\n> Tip content.\n>\n> [!IMPORTANT]\n> Important content.\n>\n> [!CAUTION]\n> Caution content.\n>\n'
                )  # Test alert box in remarks section

    def test_summary(self):
        """
        Test module/package/class summary being extracted.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['rst'][3])) as f:
                # Test summary in format.rst.foo.FooException.InternalFoo.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['summary'].replace('\n', ' ').strip(),
                    'Docstring of internal class <xref:format.rst.foo.FooException.InternalFoo>. '
                    'This class is an internal class of <xref:format.rst.foo.FooException>.'
                )

            with open(os.path.join(self.build_path, self.yaml_files['module_files']['numpy'][0])) as f:
                # Test summary in module format.numpy.foo.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['summary'].strip(),
                    'Docstring of <xref:format.numpy.foo> module.'
                )

            with open(os.path.join(self.build_path, self.yaml_files['package_files']['format'][1])) as f:
                # Test summary in  format.rst.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['summary'].strip(),
                    'Docstring of package <xref:format.rst>.'
                )

    def test_references(self):
        """
        Test references are properly inserted.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['rst'][2])) as f:
                # Test format.rst.foo.Foo.yml
                data = yaml.safe_load(f)

                self.assertIn(
                    'references',
                    data
                )  # Test references is added.

                self.assertEqual(
                    data['references'][0]['parent'],
                    'format.rst.foo.Foo'
                )  # Test reference value

                self.assertEqual(
                    data['references'][-1]['spec.python'][2]['uid'],
                    'int'
                )  # Test reference spec

    def test_inheritance(self):
        """
        Test multiple inheritance is properly resolved.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['rst'][5])) as f:
                # Test format.rst.foo.InheritFoo.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data['items'][0]['inheritance'][0]['type'],
                    'format.rst.foo.Foo'
                )

                self.assertEqual(
                    data['items'][0]['inheritance'][1]['type'],
                    'builtins.dict'
                )

    def test_source(self):
        """
        Test source info is parsed properly.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['namespacepackage'][1])) as f:
                # Test source info of class Foo in nspkg.pkgutil.pkgutil_foo.Foo.yml
                data = yaml.safe_load(f)

                self.assertIn(
                    'source',
                    data['items'][0]
                )

                self.assertEqual(
                    data['items'][0]['source']['id'],
                    'Foo'
                )

                self.assertIn(
                    'format{sep}rst{sep}foo.py'.format(sep = os.sep),
                    data['items'][0]['source']['path']
                )

                self.assertEqual(
                    23,
                    data['items'][0]['source']['startLine']
                )

            with open(os.path.join(self.build_path, self.yaml_files['module_files']['rst'][1])) as f:
                # Test source info of module format.rst.enum in format.rst.enum.yml
                data = yaml.safe_load(f)

                self.assertIn(
                    'source',
                    data['items'][0]
                )

                self.assertEqual(
                    data['items'][0]['source']['id'],
                    'enum'
                )

                self.assertIn(
                    'format{sep}rst{sep}enum.py'.format(sep = os.sep),
                    data['items'][0]['source']['path']
                )

                self.assertEqual(
                    0,
                    data['items'][0]['source']['startLine']
                )

            with open(os.path.join(self.build_path, self.yaml_files['package_files']['format'][2])) as f:
                # Test source info of package google in format.google.yml
                data = yaml.safe_load(f)

                self.assertIn(
                    'source',
                    data['items'][0]
                )

                self.assertEqual(
                    data['items'][0]['source']['id'],
                    'google'
                )

                self.assertIn(
                    'format{sep}google{sep}__init__.py'.format(sep = os.sep),
                    data['items'][0]['source']['path']
                )

                self.assertEqual(
                    0,
                    data['items'][0]['source']['startLine']
                )

    def test_external_link(self):
        """
        Test external link should be written in markdown format.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['rst'][2])) as f:
                # Test format.rst.foo.Foo.yml
                data = yaml.safe_load(f)

                for item in data['items']:
                    if item['uid'] == 'format.rst.foo.Foo.method_external_link':
                        summary = re.sub(r'\n+', '\n', item['summary']).strip()
                        summary_lines = summary.split('\n')

                        self.assertIn(
                            '[Link Text](http://inline.external.link)',
                            summary_lines[1]
                        )

                        self.assertNotIn(  # Seperated link not supported.
                            '[Seperated Link](http://seperated.external.link)',
                            summary_lines[2]
                        )
                        return

                self.fail()

    def test_google_format(self):
        """
        Test google-style docstring.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['google'][0])) as f:
                # Test format.google.foo.Foo.yml
                data = yaml.safe_load(f)

                for item in data['items']:
                    if item['uid'] == 'format.google.foo.Foo.method_seealso':
                        self.assertEqual(
                            item['seealsoContent'].strip(),
                            'Seealso contents.\n  Multi-line should be supported.'
                        )

    def test_numpy_format(self):
        """
        Test numpy-style docstring.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['numpy'][0])) as f:
                # Test format.numpy.foo.Foo.yml
                data = yaml.safe_load(f)

                for item in data['items']:
                    if item['uid'] == 'format.numpy.foo.Foo.method_seealso':
                        self.assertEqual(
                            re.sub(r'\s+', ' ', item['seealsoContent']).strip(),
                            '<xref:format.numpy.foo.Foo.mathod_note> See also target.'
                        )  # Test see also centent from numpy format.

    def test_toc(self):
        """
        Test toc structure.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, 'toc.yml')) as f:
                # Test toc.yml
                data = yaml.safe_load(f)

                self.assertEqual(
                    data[0]['uid'],
                    'project-example'
                )  # Test project name node

                self.assertEqual(
                    len(data[0]['items']),
                    3
                )  # Test there are three package nodes.
                   # Actually should be two, cuz namespace package should be placed in father nodes.
                   # TODO: To be fixed in future.

                self.assertEqual(
                    data[0]['items'][0]['uid'],
                    'format'
                )  # Test format package in toc.

                self.assertEqual(
                    data[0]['items'][1]['uid'],
                    'nspkg'
                )  # Test nspkg package in toc.

    def test_index(self):
        """
        Test index information of project.
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, 'index.yml')) as yml_file:
                # Test index.yml
                data = yaml.safe_load(yml_file)

                self.assertEqual(
                    'project-example',
                    data['items'][0]['uid']
                )  # Test there is only one item for project-example

                self.assertIn(
                    'format',
                    data['items'][0]['children']
                )  # Test format package is in index.yml

                self.assertIn(
                    'nspkg',
                    data['items'][0]['children']
                )  # Test nspkg package is in index.yml

                self.assertIn(
                    'nspkg.native.native_foo',
                    data['items'][0]['children']
                )  # Test nspkg.native.native_foo package is in index.yml
                   # Actually this should not be in index.
                   # TODO: To be fixed in future.

    def test_examples(self):
        """
        Test example contents
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['rst'][2])) as f:
                # Test format.rst.foo.Foo.yml
                data = yaml.safe_load(f)

                for item in data['items']:
                    if item['uid'] == 'format.rst.foo.Foo.method_example':
                        self.assertIn(
                            'example',
                            item
                        )  # Test example field existance

                        self.assertIn(
                            'VALUE0 = 0 #: Inline docstring of VALUE0',
                            item['example'][0]
                        )  # Test example content

    def test_seealso(self):
        """
        Test seealso contents
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['rst'][2])) as f:
                # Test format.rst.foo.Foo.yml
                data = yaml.safe_load(f)

                for item in data['items']:
                    if item['uid'] == 'format.rst.foo.Foo.method_seealso':
                        self.assertIn(
                            'seealsoContent',
                            item
                        )  # Test seealso field existance

                        self.assertIn(
                            'Seealso contents.\n  Multi-line should be supported.',
                            item['seealsoContent']
                        )  # Test seealso content

    def test_enum(self):
        """
        Test enum type support
        """
        with sphinx_build('example'):
            with open(os.path.join(self.build_path, self.yaml_files['class_files']['rst'][1])) as f:
                data = yaml.safe_load(f)
                for item in data['items']:
                    if item['uid'] == 'format.rst.enum.EnumFoo':
                        self.assertEqual(
                            item['children'],
                            ['format.rst.enum.EnumFoo.VALUE0', 'format.rst.enum.EnumFoo.VALUE1']
                        )  # Test containing all enum values
                    if item['uid'] == 'format.rst.enum.EnumFoo.VALUE0':
                        self.assertEqual(
                            item['syntax'],
                            {'content': 'VALUE0 = 0', 'return': {'type': ['format.rst.enum.EnumFoo']}}
                        )  # Test enum value syntax
                        self.assertEqual(
                            item['type'],
                            'attribute'
                        )  # Test enum value type
