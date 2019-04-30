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

"""Support for options."""

import functools
import itertools
import logging

from google.cloud.ndb import exceptions

log = logging.getLogger(__name__)


class Options:
    __slots__ = (
        # Supported
        "retries",
        "timeout",
        # Not yet implemented
        "use_cache",
        "use_memcache",
        "use_datastore",
        "memcache_timeout",
        "max_memcache_items",
        # Might or might not implement
        "force_writes",
        # Deprecated
        "propagation",
    )

    @classmethod
    def options(cls, wrapped):
        @functools.wraps(wrapped)
        def wrapper(arg, **kwargs):
            _options = kwargs.get("_options")
            if not _options:
                _options = cls(**kwargs)
            return wrapped(arg, _options=_options)

        return wrapper

    @classmethod
    def slots(cls):
        return itertools.chain(
            *(
                ancestor.__slots__
                for ancestor in cls.mro()
                if hasattr(ancestor, "__slots__")
            )
        )

    def __init__(self, config=None, **kwargs):
        cls = type(self)
        if config is not None and not isinstance(config, cls):
            raise TypeError(
                "Config must be a {} instance.".format(cls.__name__)
            )

        deadline = kwargs.pop("deadline", None)
        if deadline is not None:
            timeout = kwargs.get("timeout")
            if timeout:
                raise TypeError("Can't specify both 'deadline' and 'timeout'")
            kwargs["timeout"] = deadline

        for key in self.slots():
            default = getattr(config, key, None) if config else None
            setattr(self, key, kwargs.pop(key, default))

        if kwargs.pop("xg", False):
            log.warning(
                "Use of the 'xg' option is deprecated. All transactions are "
                "cross group (up to 25 groups) transactions, by default. This "
                "option is ignored."
            )

        if kwargs:
            raise TypeError(
                "{} got an unexpected keyword argument '{}'".format(
                    type(self).__name__, next(iter(kwargs))
                )
            )

        if self.use_cache is not None:
            raise NotImplementedError

        if self.use_memcache is not None:
            raise NotImplementedError

        if self.use_datastore is not None:
            raise NotImplementedError

        if self.memcache_timeout is not None:
            raise NotImplementedError

        if self.max_memcache_items is not None:
            raise NotImplementedError

        if self.force_writes is not None:
            raise NotImplementedError

        if self.propagation is not None:
            raise exceptions.NoLongerImplementedError()

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        for key in self.slots():
            if getattr(self, key, None) != getattr(other, key, None):
                return False

        return True

    def __repr__(self):
        options = ", ".join(
            [
                "{}={}".format(key, repr(getattr(self, key, None)))
                for key in self.slots()
                if getattr(self, key, None) is not None
            ]
        )
        return "{}({})".format(type(self).__name__, options)

    def copy(self, **kwargs):
        return type(self)(config=self, **kwargs)

    def items(self):
        for name in self.slots():
            yield name, getattr(self, name, None)


class ReadOptions(Options):
    __slots__ = ("read_consistency", "transaction")

    def __init__(self, config=None, **kwargs):
        read_policy = kwargs.pop("read_policy", None)
        if read_policy:
            log.warning(
                "Use of the 'read_policy' options is deprecated. Please use "
                "'read_consistency'"
            )
            if kwargs.get("read_consistency"):
                raise TypeError(
                    "Cannot use both 'read_policy' and 'read_consistency' "
                    "options."
                )
            kwargs["read_consistency"] = read_policy

        super(ReadOptions, self).__init__(config=config, **kwargs)
