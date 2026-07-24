# Copyright 2017 Google LLC
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

"""Expand and validate URL path templates.

This module provides the :func:`expand` and :func:`validate` functions for
interacting with Google-style URL `path templates`_ which are commonly used
in Google APIs for `resource names`_.

.. _path templates: https://github.com/googleapis/googleapis/blob
    /57e2d376ac7ef48681554204a3ba78a414f2c533/google/api/http.proto#L212
.. _resource names: https://cloud.google.com/apis/design/resource_names
"""

from __future__ import unicode_literals

import copy
import functools
import re
import urllib.parse
from collections import deque

# Regular expression for extracting variable parts from a path template.
# The variables can be expressed as:
#
# - "*": a single-segment positional variable, for example: "books/*"
# - "**": a multi-segment positional variable, for example: "shelf/**/book/*"
# - "{name}": a single-segment wildcard named variable, for example
#   "books/{name}"
# - "{name=*}: same as above.
# - "{name=**}": a multi-segment wildcard named variable, for example
#   "shelf/{name=**}"
# - "{name=/path/*/**}": a multi-segment named variable with a sub-template.
_VARIABLE_RE = re.compile(
    r"""
    (  # Capture the entire variable expression
        (?P<positional>\*\*?)  # Match & capture * and ** positional variables.
        |
        # Match & capture named variables {name}
        {
            (?P<name>[^/]+?)
            # Optionally match and capture the named variable's template.
            (?:=(?P<template>.+?))?
        }
    )
    """,
    re.VERBOSE,
)

# Segment expressions used for validating paths against a template.
_SINGLE_SEGMENT_PATTERN = r"([^/]+)"
_MULTI_SEGMENT_PATTERN = r"(.+)"


class _PathValidationFailed(Exception):
    """Internal exception used when an invalid path is encountered."""


def _validate_multi_segment_value(val: str) -> bool:
    """Validate a multi-segment wildcard value.

    This function implements the dot and double-dot traversal validation rule
    for values matching '**'. It splits the value by '/' into segments and
    simulates path traversal:
    - '.' segments do not modify the segment count.
    - '..' segments decrease the leftover segment count by 1.
    - Any other segments increase the leftover segment count by 1.

    Validation fails if:
    - Path traversal overflows to the left (leftover segment count drops below 0),
      meaning it would traverse out of the multi-segment value boundaries.
    - No segments remain after executing all path traversal commands (leftover
      segment count is 0), meaning the entire value is consumed.

    Examples:
        >>> _validate_multi_segment_value("instance/my-instance")
        True
        >>> _validate_multi_segment_value("instance/my-instance/..")
        True
        >>> _validate_multi_segment_value("instance/../..")
        False

    Args:
        val (str): The value matched to the '**' wildcard to validate.

    Returns:
        bool: True if the value is valid and does not violate traversal boundaries,
            False otherwise.
    """
    if val in ("", ".", ".."):
        return False

    segments = val.split("/")
    leftover_segments = 0
    unseen_segments = len(segments)

    for segment in segments:
        unseen_segments -= 1
        if segment == "..":
            leftover_segments -= 1
        elif segment not in (".", ""):
            leftover_segments += 1

        if leftover_segments < 0:
            return False
        if leftover_segments > unseen_segments:
            return True

    return leftover_segments > 0


@functools.lru_cache(maxsize=1024)
def _build_capture_pattern(template_str: str) -> tuple[re.Pattern, tuple[str, ...]]:
    """Build a regex pattern to capture wildcard matches from a template.

    This function parses a template string containing positional/named
    wildcards ('*' or '**'), compiles it into a regular expression, and
    records the order and types of all wildcards to allow extracting
    sub-segments for individual validation.

    Args:
        template_str (str): The template string (e.g. "projects/*/locations/*").

    Returns:
        tuple[re.Pattern, tuple[str, ...]]: A tuple containing:
            - The compiled regex pattern string with capture groups.
            - A list of wildcard type strings ('*' or '**') in matching order.
    """
    wildcard_types = []
    parts = []
    last_idx = 0
    for match in _VARIABLE_RE.finditer(template_str):
        literal = template_str[last_idx : match.start()]
        parts.append(re.escape(literal))

        positional = match.group("positional")
        template = match.group("template")

        if positional == "*":
            wildcard_types.append("*")
            replaced = _SINGLE_SEGMENT_PATTERN
        elif positional == "**":
            wildcard_types.append("**")
            replaced = _MULTI_SEGMENT_PATTERN
        elif not template or template == "*":
            wildcard_types.append("*")
            replaced = _SINGLE_SEGMENT_PATTERN
        elif template == "**":
            wildcard_types.append("**")
            replaced = _MULTI_SEGMENT_PATTERN
        else:
            sub_pattern, sub_types = _build_capture_pattern(template)
            wildcard_types.extend(sub_types)
            replaced = sub_pattern.pattern

        parts.append(replaced)
        last_idx = match.end()
    literal = template_str[last_idx:]
    parts.append(re.escape(literal))

    pattern = "".join(parts)
    return re.compile(pattern), tuple(wildcard_types)


def _extract_and_validate_wildcards(
    val: str, template_str: str | None, property_name: str | None = None
) -> None:
    """Extract and validate wildcard variables against path traversal rules.

    This function attempts to structurally match the variable's value against
    its template. If the value structurally matches, it extracts the substrings
    corresponding to the individual wildcards and enforces safety constraints:
    - Single-segment matches ('*') must not be exactly '.' or '..' because
      this breaks the URI routing contract and leads to path traversal.
    - Multi-segment matches ('**') are checked using _validate_multi_segment_value
      to ensure path traversal commands do not consume the entire value or
      escape the starting boundaries of the matched parameter.

    If the value does not structurally match the template, this function allows
    it to pass through without error. This delegates the rejection of the malformed
    string to the standard routing mechanisms (like `validate()`) to ensure that
    `additional_bindings` are evaluated correctly.

    Examples:
        >>> _extract_and_validate_wildcards("us-central1", None, "region")
        None
        >>> _extract_and_validate_wildcards("..", None, "region")
        ValueError("Invalid value .. for region.")
        >>> _extract_and_validate_wildcards(
        ...     "projects/my-proj/locations/.", "projects/*/locations/*", "parent"
        ... )
        ValueError("Invalid value projects/my-proj/locations/. for parent.")

    Args:
        val (str): The raw string value to validate.
        template_str (str): The template string of the variable (e.g. 'projects/*/locations/*').
        property_name (str | None): The name of the property being validated, used
            to construct descriptive error messages.

    Raises:
        ValueError: If a wildcard within a structurally valid value violates path traversal rules.
    """
    try:
        if template_str is None or template_str == "*":
            # Single-segment templates (None or "*") cannot match exactly "." or ".."
            # and cannot have multi-segment paths resolving to 0 segments.
            #
            # Empty strings pose no traversal security risk here.
            if val and not _validate_multi_segment_value(val):
                raise _PathValidationFailed()
        elif template_str == "**":
            # Multi-segment templates ("**") must represent at least one valid,
            # non-escaped segment.
            if not _validate_multi_segment_value(val):
                raise _PathValidationFailed()
        else:
            # Compile the sub-template into a regex capture pattern
            # to isolate and validate individual wildcard values.
            pattern, wildcard_types = _build_capture_pattern(template_str)

            m = pattern.fullmatch(val)
            if m is not None:
                # Validate each wildcard value within its matched boundaries,
                # preventing traversals from escaping their structural positions.
                for captured_val in m.groups():
                    if not _validate_multi_segment_value(captured_val):
                        raise _PathValidationFailed()
            else:
                # For values that don't match the pattern, ensure the value doesn't
                # resolve to 0 segments (e.g. "projects/..").
                if val and not _validate_multi_segment_value(val):
                    raise _PathValidationFailed()
    except _PathValidationFailed:
        raise ValueError(
            f"Invalid value {val} for {property_name or 'positional variable'}."
        )


def _expand_variable_match(positional_vars, named_vars, match):
    """Expand a matched variable with its value.

    Args:
        positional_vars (list): A list of positional variables. This list will
            be modified.
        named_vars (dict): A dictionary of named variables.
        match (re.Match): A regular expression match.

    Returns:
        str: The expanded variable to replace the match.

    Raises:
        ValueError: If a positional or named variable is required by the
            template but not specified or if an unexpected template expression
            is encountered.
    """
    positional = match.group("positional")
    name = match.group("name")
    template = match.group("template")

    if name is not None:
        try:
            val = str(named_vars[name])
            _extract_and_validate_wildcards(val, template, name)
            return urllib.parse.quote(val, safe="/")
        except KeyError:
            raise ValueError(
                "Named variable '{}' not specified and needed by template "
                "`{}` at position {}".format(name, match.string, match.start())
            )
    elif positional is not None:
        try:
            val = str(positional_vars.pop(0))
            _extract_and_validate_wildcards(val, positional, None)
            return urllib.parse.quote(val, safe="/")
        except IndexError:
            raise ValueError(
                "Positional variable not specified and needed by template "
                "`{}` at position {}".format(match.string, match.start())
            )
    else:
        raise ValueError("Unknown template expression {}".format(match.group(0)))


def expand(tmpl, *args, **kwargs):
    """Expand a path template with the given variables.

    .. code-block:: python

        >>> expand('users/*/messages/*', 'me', '123')
        users/me/messages/123
        >>> expand('/v1/{name=shelves/*/books/*}', name='shelves/1/books/3')
        /v1/shelves/1/books/3

    Args:
        tmpl (str): The path template.
        args: The positional variables for the path.
        kwargs: The named variables for the path.

    Returns:
        str: The expanded path

    Raises:
        ValueError: If a positional or named variable is required by the
            template but not specified or if an unexpected template expression
            is encountered.
    """
    replacer = functools.partial(_expand_variable_match, list(args), kwargs)
    return _VARIABLE_RE.sub(replacer, tmpl)


def _replace_variable_with_pattern(match):
    """Replace a variable match with a pattern that can be used to validate it.

    Args:
        match (re.Match): A regular expression match

    Returns:
        str: A regular expression pattern that can be used to validate the
            variable in an expanded path.

    Raises:
        ValueError: If an unexpected template expression is encountered.
    """
    positional = match.group("positional")
    name = match.group("name")
    template = match.group("template")
    if name is not None:
        if not template:
            return _SINGLE_SEGMENT_PATTERN.format(name)
        elif template == "**":
            return _MULTI_SEGMENT_PATTERN.format(name)
        else:
            return _generate_pattern_for_template(template)
    elif positional == "*":
        return _SINGLE_SEGMENT_PATTERN
    elif positional == "**":
        return _MULTI_SEGMENT_PATTERN
    else:
        raise ValueError("Unknown template expression {}".format(match.group(0)))


def _generate_pattern_for_template(tmpl):
    """Generate a pattern that can validate a path template.

    Args:
        tmpl (str): The path template

    Returns:
        str: A regular expression pattern that can be used to validate an
            expanded path template.
    """
    return _VARIABLE_RE.sub(_replace_variable_with_pattern, tmpl)


def get_field(request, field):
    """Get the value of a field from a given dictionary.

    Args:
        request (dict | Message): A dictionary or a Message object.
        field (str): The key to the request in dot notation.

    Returns:
        The value of the field.
    """
    parts = field.split(".")
    value = request

    for part in parts:
        if not isinstance(value, dict):
            value = getattr(value, part, None)
        else:
            value = value.get(part)
    if isinstance(value, dict):
        return
    return value


def delete_field(request, field):
    """Delete the value of a field from a given dictionary.

    Args:
        request (dict | Message): A dictionary object or a Message.
        field (str): The key to the request in dot notation.
    """
    parts = deque(field.split("."))
    while len(parts) > 1:
        part = parts.popleft()
        if not isinstance(request, dict):
            if hasattr(request, part):
                request = getattr(request, part, None)
            else:
                return
        else:
            request = request.get(part)
    part = parts.popleft()
    if not isinstance(request, dict):
        if hasattr(request, part):
            request.ClearField(part)
        else:
            return
    else:
        request.pop(part, None)


def validate(tmpl, path):
    """Validate a path against the path template.

    .. code-block:: python

        >>> validate('users/*/messages/*', 'users/me/messages/123')
        True
        >>> validate('users/*/messages/*', 'users/me/drafts/123')
        False
        >>> validate('/v1/{name=shelves/*/books/*}', /v1/shelves/1/books/3)
        True
        >>> validate('/v1/{name=shelves/*/books/*}', /v1/shelves/1/tapes/3)
        False

    Args:
        tmpl (str): The path template.
        path (str): The expanded path.

    Returns:
        bool: True if the path matches.
    """
    pattern = _generate_pattern_for_template(tmpl) + "$"
    return True if re.match(pattern, path) is not None else False


def transcode(http_options, message=None, **request_kwargs):
    """Transcodes a grpc request pattern into a proper HTTP request following the rules outlined here,
    https://github.com/googleapis/googleapis/blob/master/google/api/http.proto#L44-L312

     Args:
         http_options (list(dict)): A list of dicts which consist of these keys,
             'method'    (str): The http method
             'uri'       (str): The path template
             'body'      (str): The body field name (optional)
             (This is a simplified representation of the proto option `google.api.http`)

         message (Message) : A request object (optional)
         request_kwargs (dict) : A dict representing the request object

     Returns:
         dict: The transcoded request with these keys,
             'method'        (str)   : The http method
             'uri'           (str)   : The expanded uri
             'body'          (dict | Message)  : A dict or a Message representing the body (optional)
             'query_params'  (dict | Message)  : A dict or Message mapping query parameter variables and values

     Raises:
         ValueError: If the request does not match the given template.
    """
    transcoded_value = message or request_kwargs
    bindings = []
    for http_option in http_options:
        request = {}

        # Assign path
        uri_template = http_option["uri"]
        fields = [
            (m.group("name"), m.group("template"))
            for m in _VARIABLE_RE.finditer(uri_template)
        ]
        bindings.append((uri_template, fields))

        path_args = {field: get_field(transcoded_value, field) for field, _ in fields}
        request["uri"] = expand(uri_template, **path_args)

        if not validate(uri_template, request["uri"]) or not all(path_args.values()):
            continue

        # Remove fields used in uri path from request
        leftovers = copy.deepcopy(transcoded_value)
        for path_field, _ in fields:
            delete_field(leftovers, path_field)

        # Assign body and query params
        body = http_option.get("body")

        if body:
            if body == "*":
                request["body"] = leftovers
                if message:
                    request["query_params"] = message.__class__()
                else:
                    request["query_params"] = {}
            else:
                try:
                    if message:
                        request["body"] = getattr(leftovers, body)
                        delete_field(leftovers, body)
                    else:
                        request["body"] = leftovers.pop(body)
                except (KeyError, AttributeError):
                    continue
                request["query_params"] = leftovers
        else:
            request["query_params"] = leftovers
        request["method"] = http_option["method"]
        return request

    bindings_description = [
        '\n\tURI: "{}"\n\tRequired request fields:\n\t\t{}'.format(
            uri,
            "\n\t\t".join(
                [
                    'field: "{}", pattern: "{}"'.format(n, p if p else "*")
                    for n, p in fields
                ]
            ),
        )
        for uri, fields in bindings
    ]

    raise ValueError(
        "Invalid request."
        "\nSome of the fields of the request message are either not initialized or "
        "initialized with an invalid value."
        "\nPlease make sure your request matches at least one accepted HTTP binding."
        "\nTo match a binding the request message must have all the required fields "
        "initialized with values matching their patterns as listed below:{}".format(
            "\n".join(bindings_description)
        )
    )
