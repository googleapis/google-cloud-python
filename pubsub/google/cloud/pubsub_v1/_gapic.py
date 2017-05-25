# Copyright 2017, Google Inc. All rights reserved.
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


def add_methods(SourceClass, blacklist=()):
    """Add wrapped versions of the `api` member's methods to the class.

    Any methods passed in `blacklist` are not added.
    Additionally, any methods explicitly defined on the wrapped class are
    not added.
    """
    def actual_decorator(cls):
        # Reflectively iterate over most of the methods on the source class
        # (the GAPIC) and make wrapped versions available on this client.
        for name in dir(SourceClass):
            # Ignore all private and magic methods.
            if name.startswith('_'):
                continue

            # Ignore anything on our blacklist.
            if name in blacklist:
                continue

            # Retrieve the attribute, and ignore it if it is not callable.
            attr = getattr(self.api, name)
            if not callable(attr):
                continue

            # Add a wrapper method to this object.
            fx = lambda self, *a, **kw: getattr(self.api, name)(*a, **kw)
            fx.__name__ = name
            fx.__doc__ = attr.__doc__
            setattr(self, name, fx)

        # Return the augmented class.
        return cls

    # Simply return the actual decorator; this is returned from this method
    # and actually used to decorate the class.
    return actual_decorator
