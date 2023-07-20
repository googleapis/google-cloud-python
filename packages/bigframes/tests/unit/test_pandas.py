# Copyright 2023 Google LLC
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

import inspect
import re
import sys

import pytest

import bigframes.pandas
import bigframes.session

leading_whitespace = re.compile(r"^\s+", flags=re.MULTILINE)


def all_session_methods():
    session_attributes = set(
        attribute
        for attribute in dir(bigframes.session.Session)
        if not attribute.startswith("_")
    )
    session_attributes.remove("close")

    for attribute in sorted(session_attributes):
        session_method = getattr(bigframes.session.Session, attribute)
        if not callable(session_method):
            continue  # pragma: no cover
        yield attribute


@pytest.mark.parametrize(
    [
        "method_name",
    ],
    [(method_name,) for method_name in all_session_methods()],
)
def test_method_matches_session(method_name: str):
    if sys.version_info <= (3, 10):
        pytest.skip(
            "Need Python 3.10 to reconcile deferred annotations."
        )  # pragma: no cover

    session_method = getattr(bigframes.session.Session, method_name)
    session_doc = inspect.getdoc(session_method)
    assert session_doc is not None, "docstrings are required"

    pandas_method = getattr(bigframes.pandas, method_name)
    pandas_doc = inspect.getdoc(pandas_method)
    assert pandas_doc is not None, "docstrings are required"
    assert re.sub(leading_whitespace, "", pandas_doc) == re.sub(
        leading_whitespace, "", session_doc
    )

    # Add `eval_str = True` so that deferred annotations are turned into their
    # corresponding type objects. Need Python 3.10 for eval_str parameter.
    session_signature = inspect.signature(session_method, eval_str=True)
    pandas_signature = inspect.signature(pandas_method, eval_str=True)
    assert [
        # Kind includes position, which will be an offset.
        parameter.replace(kind=inspect.Parameter.POSITIONAL_ONLY)
        for parameter in pandas_signature.parameters.values()
    ] == [
        # Kind includes position, which will be an offset.
        parameter.replace(kind=inspect.Parameter.POSITIONAL_ONLY)
        for parameter in session_signature.parameters.values()
        # Don't include the first parameter, which is `self: Session`
    ][
        1:
    ]
    assert pandas_signature.return_annotation == session_signature.return_annotation
