# Copyright 2019 Google LLC
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


from google.cloud.pubsub_v1 import _gapic


class SourceClass(object):
    def __init__(self):
        self.x = "x"

    def method(self):
        return "source class instance method"

    @staticmethod
    def static_method():
        return "source class static method"

    @classmethod
    def class_method(cls):
        return "source class class method"

    @classmethod
    def blacklisted_method(cls):  # pragma: NO COVER
        return "source class blacklisted method"


def test_add_method():
    @_gapic.add_methods(SourceClass, ("blacklisted_method",))
    class Foo(object):
        def __init__(self):
            self.api = SourceClass()

        def method(self):  # pragma: NO COVER
            return "foo class instance method"

    foo = Foo()

    # Any method that's callable and not blacklisted is "inherited".
    assert set(["method", "static_method", "class_method"]) <= set(dir(foo))
    assert "blacklisted_method" not in dir(foo)

    # Source Class's static and class methods become static methods.
    assert type(Foo.__dict__["static_method"]) == staticmethod
    assert foo.static_method() == "source class static method"
    assert type(Foo.__dict__["class_method"]) == staticmethod
    assert foo.class_method() == "source class class method"

    # The decorator changes the behavior of instance methods of the wrapped class.
    # method() is called on an instance of the Source Class (stored as an
    # attribute on the wrapped class).
    assert foo.method() == "source class instance method"
