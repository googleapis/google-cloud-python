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

""" Docstring of :mod:`conflict.foo` module.
"""

foo_var = []
""" Docstring of module variable :any:`conflict.foo.foo_var`."""


def function(arg1, arg2, arg3, arg4):
    """ Docstring of :func:`conflict.foo.function` function.

    :param int arg1: Parameter arg1 of :func:`~conflict.foo.function`.
    :param float arg2: Parameter arg2 of :func:`~conflict.foo.function`.
    :param boolean arg3: Parameter arg3 of :func:`~conflict.foo.function`.
    :param str arg4: Parameter arg4 of :func:`~conflict.foo.function`.
    """
    pass


class Foo(object):
    """ Docstring of :class:`conflict.foo.Foo` class in rst format.

    :var attr: Docstring of :class:`conflict.foo.Foo.attr` from class docstring.
    :vartype attr: ~conflict.enum.EnumFoo

    :param init_arg1: Parameter init_arg1 from class docstring.
    :type init_arg1: float
    :param list[int] init_arg2: Parameter init_arg2 from class docstring.
    """

    attr = 1
    """ Docstring of :class:`conflict.foo.Foo.attr` from attrbute docstring."""

    def __init__(self, init_arg1, init_arg2):
        """ Docstring of constructor of Foo. Will not be shown.

        :param init_arg1: Parameter init_arg1 from constructor's docstring.
        :type init_arg1: float
        :param list[int] init_arg2: Parameter init_arg2 from constructor's docstring.
        """

    @property
    def attr_getter(self):
        """ Docstring of :meth:`conflict.foo.Foo.attr_getter` @property.
        """
        return self.attr

    @classmethod
    def class_method(cls, arg1):
        """ Docstring of :class:`conflict.foo.Foo.class_method` @classmethod.

        :param cls: Class object of :class:`conflict.foo.Foo`.
        :type cls: class
        :param str arg1: Parameter arg1 of :meth:`conflict.foo.Foo.class_method`.
        """
        pass

    @staticmethod
    def static_method():
        """ Docstring of :meth:`conflict.foo.Foo.static_method` @staticmethod.
        """
        pass

    def method(self):
        """ Docstring of normal class method :meth:`conflict.foo.Foo.method`.
        """
        pass

    def method_return(self):
        """ Docstring of :meth:`conflict.foo.Foo.method_return`.

        :return: This method returns a value.
        :rtype: boolean
        """
        return False

    def method_multiline(self):
        """ Docstring of :meth:`conflict.foo.Foo.method_multiline`.
        This docstring has multiple lines of contents.
        And this should work perfectly.
        """
        pass

    def method_exception(self):
        """ Docstring of :meth:`conflict.foo.Foo.method_exception`.

        :raises: :class:`Exception` This function raises
            exception.
        """
        raise Exception()

    def method_external_link(self):
        """ Docstring of :meth:`conflict.foo.Foo.method_external_link`.
        Inline link should be transformed to markdown: `Link Text <http://inline.external.link>`_.
        And seperated link will fail: `Seperated Link`_

        .. _Seperated Link: http://seperated.external.link
        """
        pass

    def method_seealso(self):
        """ Docstring of :meth:`conflict.foo.Foo.method_seealso`.

        .. seealso::
            Seealso contents.
            Multi-line should be supported.
            And reference to :class:`conflict.foo.Foo` should be okay.
        """
        pass

    def method_note(self):
        """ Docstring of :meth:`conflict.foo.Foo.method_note`.

        .. note::
            This is content of note.
            Another line of note contents.
        """
        pass

    def method_warning(self):
        """ Docstring of :meth:`conflict.foo.Foo.method_warning`.

        .. warning::
            This is content of warning.
        """
        pass

    def method_code(self):
        """ Docstring of :meth:`conflict.foo.Foo.method_code`.

        .. code-block:: python

            >>> import numpy as np
            >>> a = np.ndarray([1,2,3,4,5])

        Another way of code block::

            import numpy as np
            b = np.random.random(10)
        """
        pass

    def method_example(self):
        """ Docstring of :meth:`conflict.foo.Foo.method_example`.

        .. admonition::
            This is Example content.
            Should support multi-line.
            Can also include file:

            .. literalinclude:: ../format/rst/enum.py
        """
        pass

    def method_default_value(self, arg1='default string', arg2=None):
        """ Docstring of :meth:`conflict.foo.Foo.method_default_value`.

        :param str arg1: Parameter arg1 of :meth:`conflict.foo.Foo.method_default_value`, default value is 'default string'.
        :param object arg2: Paremeter arg2 of :meth:`conflict.foo.Foo.method_default_value` default value is None.
        """
        pass

    def method_default_value_comma(self, arg1=(1,2,3)):
        """ Docstring of :meth:`conflict.foo.Foo.method_default_value_comma`.
        The default value of method parameter contains comma thus will fail to parse.

        :param tuple arg1: Parameter arg1 of :meth:`conflict.foo.Foo.method_default_value_comma`, default value is (1,2,3).
        """
        pass
