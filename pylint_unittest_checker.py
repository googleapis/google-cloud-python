"""Plugin for pylint to suppress warnings on tests.

Turns off the following pylint errors/warnings:
- Docstring checks in test modules.
- Too few public methods on test classes.
- Too many public methods on subclasses of unittest.TestCase.
- Invalid names on all functions/methods.
- Private attribute mangling outside __init__ method.
- Invalid variable name assignment.
"""

import importlib
import unittest
import unittest2

import astroid
import pylint.checkers
import pylint.interfaces


MAX_PUBLIC_METHODS = 20


def is_test_module(checker, module_node):
    """Boolean to determine if a module is a test module."""
    return checker.get_test_module(module_node) is not None


def get_unittest_class(checker, class_node):
    """Get a corresponding Python class object for a TestCase subclass."""
    module_obj = checker.get_test_module(class_node.root())
    if module_obj is None:
        return

    class_obj = getattr(module_obj, class_node.name, None)
    try:
        if issubclass(class_obj,
                      (unittest.TestCase, unittest2.TestCase)):
            return class_obj
    except TypeError:
        pass


def suppress_too_many_methods(checker, class_node):
    """Suppress too-many-public-methods warnings on a TestCase.

    Checks that the current class (`class_node`) is a subclass
    of unittest.TestCase or unittest2.TestCase before suppressing.

    To make reasonable, still checks the number of public methods defined
    explicitly on the subclass.
    """
    class_obj = get_unittest_class(checker, class_node)
    if class_obj is None:
        return

    checker.linter.disable('too-many-public-methods',
                           scope='module', line=class_node.fromlineno)

    # Count the number of public methods defined locally.
    nb_public_methods = 0
    for method in class_node.methods():
        if (method.name in class_obj.__dict__ and
                not method.name.startswith('_')):
            nb_public_methods += 1

    # Add a message if we exceed MAX_PUBLIC_METHODS.
    if nb_public_methods > MAX_PUBLIC_METHODS:
        checker.add_message('too-many-public-methods', node=class_node,
                            args=(nb_public_methods,
                                  MAX_PUBLIC_METHODS))


def suppress_too_few_methods(checker, class_node):
    """Suppress too-few-public-methods warnings on test classes."""
    if not is_test_module(checker, class_node.root()):
        return

    checker.linter.disable('too-few-public-methods',
                           scope='module', line=class_node.fromlineno)


def suppress_invalid_fn_name(checker, function_node):
    """Suppress invalid-name warnings on method names in a test."""
    if not is_test_module(checker, function_node.root()):
        return

    checker.linter.disable('invalid-name', scope='module',
                           line=function_node.fromlineno)


def transform_ignored_docstrings(checker, astroid_obj):
    """Module/Class/Function transformer to ignore docstrings.

    The astroid object is edited so as to appear that a docstring
    is set.
    """
    if isinstance(astroid_obj, astroid.scoped_nodes.Module):
        module = astroid_obj
    else:
        module = astroid_obj.root()

    if not is_test_module(checker, module):
        return

    # Fool `pylint` by setting a dummy docstring.
    if astroid_obj.doc in ('', None):
        astroid_obj.doc = 'NOT EMPTY STRING.'


class UnittestChecker(pylint.checkers.BaseChecker):
    """Checker for unit test modules."""

    __implements__ = pylint.interfaces.IAstroidChecker

    name = 'unittest_checker'
    # `msgs` must be non-empty to register successfully. We spoof an error
    # message string of length 5.
    msgs = {'E_FLS': ('%r', 'UNUSED')}

    # So that this checker is executed before others, even the name checker.
    priority = 0

    def __init__(self, linter=None):
        super(UnittestChecker, self).__init__(linter=linter)
        self._checked_modules = {}

    def get_test_module(self, module_node):
        """Gets a corresponding Python module object for a test node.

        The `module_node` is an astroid object from the parsed tree.

        Caches results on instance to memoize work.
        """
        if module_node not in self._checked_modules:
            module_file = module_node.name.rsplit('.', 1)[-1]
            if module_file.startswith('test'):
                module_obj = importlib.import_module(module_node.name)
                self._checked_modules[module_node] = module_obj
            else:
                self._checked_modules[module_node] = None
        return self._checked_modules[module_node]

    def visit_module(self, module_node):
        """Checker specific method when module is linted."""
        transform_ignored_docstrings(self, module_node)

    def visit_class(self, class_node):
        """Checker specific method when class is linted."""
        transform_ignored_docstrings(self, class_node)
        suppress_too_many_methods(self, class_node)
        suppress_too_few_methods(self, class_node)

    def visit_function(self, function_node):
        """Checker specific method when function is linted."""
        suppress_invalid_fn_name(self, function_node)
        transform_ignored_docstrings(self, function_node)

    def visit_assattr(self, assign_attr_node):
        """Checker specific method when attribute assignment is linted."""
        if not is_test_module(self, assign_attr_node.root()):
            return

        if assign_attr_node.attrname.startswith('_'):
            self.linter.disable('attribute-defined-outside-init',
                                scope='module', line=assign_attr_node.lineno)

    def visit_assname(self, assign_name_node):
        """Checker specific method when variable assignment is linted."""
        if not is_test_module(self, assign_name_node.root()):
            return

        self.linter.disable('invalid-name', scope='module',
                            line=assign_name_node.lineno)


def register(linter):
    """required method to auto register this checker"""
    linter.register_checker(UnittestChecker(linter))
