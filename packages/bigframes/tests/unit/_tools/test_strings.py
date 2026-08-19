# Copyright 2025 Google LLC
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

"""Tests for helper methods for processing strings with minimal dependencies.

Please keep the dependencies used in this subpackage to a minimum to avoid the
risk of circular dependencies.
"""

import base64
import random
import sys
import uuid

import pytest

from bigframes._tools import strings

# To stress test some unicode comparisons.
# https://stackoverflow.com/a/39682429/101923
ALL_UNICODE_CHARS = "".join(chr(i) for i in range(32, 0x110000) if chr(i).isprintable())
RANDOM_STRINGS = (
    pytest.param(str(uuid.uuid4()), id="uuid4"),
    pytest.param(hex(random.randint(0, sys.maxsize)), id="hex"),
    pytest.param(
        base64.b64encode(
            "".join(random.choice(ALL_UNICODE_CHARS) for _ in range(100)).encode(
                "utf-8"
            )
        ).decode("utf-8"),
        id="base64",
    ),
    pytest.param(
        "".join(random.choice(ALL_UNICODE_CHARS) for _ in range(8)), id="unicode8"
    ),
    pytest.param(
        "".join(random.choice(ALL_UNICODE_CHARS) for _ in range(64)), id="unicode64"
    ),
)


def random_char_not_equal(avoid: str):
    random_char = avoid
    while random_char == avoid:
        random_char = random.choice(ALL_UNICODE_CHARS)
    return random_char


def random_deletion(original: str):
    """original string with one character removed"""
    char_index = random.randrange(len(original))
    return original[:char_index] + original[char_index + 1 :]


def random_insertion(original: str):
    char_index = random.randrange(len(original))
    random_char = random.choice(ALL_UNICODE_CHARS)
    return original[: char_index + 1] + random_char + original[char_index + 1 :]


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    (
        ("", "", 0),
        ("abc", "abc", 0),
        # Deletions
        ("abcxyz", "abc", 3),
        ("xyzabc", "abc", 3),
        ("AXYZBC", "ABC", 3),
        ("AXYZBC", "XYZ", 3),
        # Insertions
        ("abc", "abcxyz", 3),
        ("abc", "xyzabc", 3),
        # Substitutions
        ("abc", "aBc", 1),
        ("abcxyz", "aBcXyZ", 3),
        # Combinations
        ("abcdefxyz", "abcExyzα", 4),
    ),
)
def test_levenshtein_distance(left: str, right: str, expected: int):
    assert strings.levenshtein_distance(left, right) == expected


@pytest.mark.parametrize(("random_string",), RANDOM_STRINGS)
def test_levenshtein_distance_equal_strings(random_string: str):
    """Mini fuzz test with different strings."""
    assert strings.levenshtein_distance(random_string, random_string) == 0


@pytest.mark.parametrize(("random_string",), RANDOM_STRINGS)
def test_levenshtein_distance_random_deletion(random_string: str):
    """Mini fuzz test with different strings."""

    num_deleted = random.randrange(1, min(10, len(random_string)))
    assert 1 <= num_deleted < len(random_string)

    deleted = random_string
    for _ in range(num_deleted):
        deleted = random_deletion(deleted)

    assert deleted != random_string
    assert len(deleted) == len(random_string) - num_deleted
    assert strings.levenshtein_distance(random_string, deleted) == num_deleted


@pytest.mark.parametrize(("random_string",), RANDOM_STRINGS)
def test_levenshtein_distance_random_insertion(random_string: str):
    """Mini fuzz test with different strings."""

    num_inserted = random.randrange(1, min(10, len(random_string)))
    assert 1 <= num_inserted < len(random_string)

    inserted = random_string
    for _ in range(num_inserted):
        inserted = random_insertion(inserted)

    assert inserted != random_string
    assert len(inserted) == len(random_string) + num_inserted
    assert strings.levenshtein_distance(random_string, inserted) == num_inserted


@pytest.mark.parametrize(("random_string",), RANDOM_STRINGS)
def test_levenshtein_distance_random_substitution(random_string: str):
    """Mini fuzz test with different strings.

    Note: we don't do multiple substitutions here to avoid accidentally
    substituting the same character twice.
    """
    char_index = random.randrange(len(random_string))
    replaced_char = random_string[char_index]
    random_char = random_char_not_equal(replaced_char)
    substituted = (
        random_string[:char_index] + random_char + random_string[char_index + 1 :]
    )
    assert substituted != random_string
    assert len(substituted) == len(random_string)
    assert strings.levenshtein_distance(random_string, substituted) == 1
