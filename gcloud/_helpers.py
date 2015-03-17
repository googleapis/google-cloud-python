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
"""Thread-local resource stack.

This module is not part of the public API surface of `gcloud`.
"""

try:
    from threading import local as Local
except ImportError:     # pragma: NO COVER (who doesn't have it?)
    class Local(object):
        """Placeholder for non-threaded applications."""


class _LocalStack(Local):
    """Manage a thread-local LIFO stack of resources.

    Intended for use in :class:`gcloud.datastore.batch.Batch.__enter__`,
    :class:`gcloud.storage.batch.Batch.__enter__`, etc.
    """
    def __init__(self):
        super(_LocalStack, self).__init__()
        self._stack = []

    def __iter__(self):
        """Iterate the stack in LIFO order.
        """
        return iter(reversed(self._stack))

    def push(self, resource):
        """Push a resource onto our stack.
        """
        self._stack.append(resource)

    def pop(self):
        """Pop a resource from our stack.

        :raises: IndexError if the stack is empty.
        :returns: the top-most resource, after removing it.
        """
        return self._stack.pop()

    @property
    def top(self):
        """Get the top-most resource

        :returns: the top-most item, or None if the stack is empty.
        """
        if len(self._stack) > 0:
            return self._stack[-1]


class _LazyProperty(object):
    """Descriptor for lazy loaded property.

    This follows the reify pattern: lazy evaluation and then replacement
    after evaluation.

    :type name: string
    :param name: The name of the attribute / property being evaluated.

    :type deferred_callable: callable that takes no arguments
    :param deferred_callable: The function / method used to evaluate the
                              property.
    """

    def __init__(self, name, deferred_callable):
        self._name = name
        self._deferred_callable = deferred_callable

    def __get__(self, obj, objtype):
        if obj is None:
            return self

        setattr(obj, self._name, self._deferred_callable())
        return getattr(obj, self._name)


def _lazy_property_deco(deferred_callable):
    """Decorator a method to create a :class:`_LazyProperty`.

    :type deferred_callable: callable that takes no arguments
    :param deferred_callable: The function / method used to evaluate the
                              property.

    :rtype: :class:`_LazyProperty`.
    :returns: A lazy property which defers the deferred_callable.
    """
    if isinstance(deferred_callable, staticmethod):
        # H/T: http://stackoverflow.com/a/9527450/1068170
        #      For Python2.7+ deferred_callable.__func__ would suffice.
        deferred_callable = deferred_callable.__get__(True)
    return _LazyProperty(deferred_callable.__name__, deferred_callable)
