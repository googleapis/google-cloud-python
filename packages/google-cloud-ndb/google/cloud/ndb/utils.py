# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Low-level utilities used internally by ``ndb``"""


import functools
import inspect
import threading


__all__ = []


def code_info(*args, **kwargs):
    raise NotImplementedError


DEBUG = True


def decorator(*args, **kwargs):
    raise NotImplementedError


def frame_info(*args, **kwargs):
    raise NotImplementedError


def func_info(*args, **kwargs):
    raise NotImplementedError


def gen_info(*args, **kwargs):
    raise NotImplementedError


def get_stack(*args, **kwargs):
    raise NotImplementedError


def logging_debug(*args, **kwargs):
    raise NotImplementedError


class keyword_only(object):
    """A decorator to get some of the functionality of keyword-only arguments
    from Python 3. It takes allowed keyword args and default values as
    parameters. Raises TypeError if a keyword argument not included in those
    parameters is passed in.
    """

    def __init__(self, **kwargs):
        self.defaults = kwargs

    def __call__(self, wrapped):
        @functools.wraps(wrapped)
        def wrapper(*args, **kwargs):
            new_kwargs = self.defaults.copy()
            for kwarg in kwargs:
                if kwarg not in new_kwargs:
                    raise TypeError(
                        "%s() got an unexpected keyword argument '%s'"
                        % (wrapped.__name__, kwarg)
                    )
            new_kwargs.update(kwargs)
            return wrapped(*args, **new_kwargs)

        return wrapper


def positional(max_pos_args):
    """A decorator to declare that only the first N arguments may be
    positional. Note that for methods, n includes 'self'. This decorator
    retains TypeError functionality from previous version, but adds two
    attributes that can be used in combination with other decorators that
    depend on inspect.signature, only available in Python 3. Note that this
    decorator has to be closer to the function definition than other decorators
    that need to access `_positional_names` or `_positional_args`.
    """

    def positional_decorator(wrapped):
        root = getattr(wrapped, "_wrapped", wrapped)
        wrapped._positional_args = max_pos_args
        argspec = inspect.getargspec(root)
        wrapped._argspec = argspec
        wrapped._positional_names = argspec.args[:max_pos_args]

        @functools.wraps(wrapped)
        def positional_wrapper(*args, **kwds):
            if len(args) > max_pos_args:
                plural_s = ""
                if max_pos_args != 1:
                    plural_s = "s"
                raise TypeError(
                    "%s() takes at most %d positional argument%s (%d given)"
                    % (wrapped.__name__, max_pos_args, plural_s, len(args))
                )
            return wrapped(*args, **kwds)

        return positional_wrapper

    return positional_decorator


threading_local = threading.local


def tweak_logging(*args, **kwargs):
    raise NotImplementedError


def wrapping(*args, **kwargs):
    raise NotImplementedError
