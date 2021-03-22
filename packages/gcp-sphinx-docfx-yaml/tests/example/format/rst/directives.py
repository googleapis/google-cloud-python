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

# coding: utf-8

""" Docstring of module :mod:`format.rst.directives`.
This module is used for testing self-defined directives.

.. remarks:: Remarks from module directives.
"""

module_var = ''
""".. remarks:: Remarks from module variable."""


def func():
    """
    .. remarks:: Remarks from module function.
    """
    pass


class DirectivesFoo(object):
    """ Docstring of class :class:`format.rst.directives.DirectivesFoo`.

    .. note::
        Note content from class docstring.
        Second line of note content.
        many lines of content.

    .. warning::
        Warning message from class docstring.
        Second line.

    .. tip::
        Tip content. :class:`format.rst.foo.Foo`

    .. important::
        Important content.

    .. caution::
        Caution content.

    .. remarks:: Remarks from class.
        Multi-line content should be supported.

        .. note::
            Note conetnt under class remarks.
            Second line of note content.

        .. warning::
            Warning content under class remarks.
            Second line.
            :class:`format.rst.foo.Foo`

        .. tip::
            Tip content.

        .. important::
            Important content.

        .. caution::
            Caution content.
    """

    var_remarks = ''
    """ .. remarks:: Remarks from class attribute :class:`format.rst.directives.DirectivesFoo.var_remarks`."""

    def method_remarks(self):
        """
        .. remarks:: Remarks from class method :meth:`format.rst.directives.DirectivesFoo.method_remarks`
            Another reference: :class:`format.rst.directives.DirectivesFoo`
        """
        pass
