# Copyright 2018 Google LLC
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

import functools


def dispatch(func):
    """Return a decorated method that dispatches on the second argument.

    This is the equivalent of :meth:`functools.singledispatch`, but for
    bound methods.
    """
    base_dispatcher = functools.singledispatch(func)

    # Define a wrapper function that works off args[1] instead of args[0].
    # This is needed because we are overloading *methods*, and their first
    # argument is always `self`.
    @functools.wraps(base_dispatcher)
    def wrapper(*args, **kwargs):
        return base_dispatcher.dispatch(args[1].__class__)(*args, **kwargs)

    # The register function is not changed, so let singledispatch do the work.
    wrapper.register = base_dispatcher.register

    # Done; return the decorated method.
    return wrapper
