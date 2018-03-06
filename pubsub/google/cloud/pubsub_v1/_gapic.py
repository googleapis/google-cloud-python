# Copyright 2017, Google LLC All rights reserved.
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

from __future__ import absolute_import

import functools


def add_methods(source_class, blacklist=()):
    """Add wrapped versions of the `api` member's methods to the class.

    Any methods passed in `blacklist` are not added.
    Additionally, any methods explicitly defined on the wrapped class are
    not added.
    """
    def wrap(wrapped_fx):
        """Wrap a GAPIC method; preserve its name and docstring."""
        # If this is a static or class method, then we need to *not*
        # send self as the first argument.
        #
        # Similarly, for instance methods, we need to send self.api rather
        # than self, since that is where the actual methods were declared.
        instance_method = True
        self = getattr(wrapped_fx, '__self__', None)
        if issubclass(type(self), type):
            instance_method = False

        # Okay, we have figured out what kind of method this is; send
        # down the correct wrapper function.
        if instance_method:
            fx = lambda self, *a, **kw: wrapped_fx(self.api, *a, **kw)  # noqa
            return functools.wraps(wrapped_fx)(fx)
        fx = lambda self, *a, **kw: wrapped_fx(*a, **kw)  # noqa
        return functools.wraps(wrapped_fx)(fx)

    def actual_decorator(cls):
        # Reflectively iterate over most of the methods on the source class
        # (the GAPIC) and make wrapped versions available on this client.
        for name in dir(source_class):
            # Ignore all private and magic methods.
            if name.startswith('_'):
                continue

            # Ignore anything on our blacklist.
            if name in blacklist:
                continue

            # Retrieve the attribute, and ignore it if it is not callable.
            attr = getattr(source_class, name)
            if not callable(attr):
                continue

            # Add a wrapper method to this object.
            fx = wrap(getattr(source_class, name))
            setattr(cls, name, fx)

        # Return the augmented class.
        return cls

    # Simply return the actual decorator; this is returned from this method
    # and actually used to decorate the class.
    return actual_decorator
