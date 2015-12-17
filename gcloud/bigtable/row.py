# Copyright 2015 Google Inc. All rights reserved.
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

"""User friendly container for Google Cloud Bigtable Row."""


from gcloud._helpers import _to_bytes
from gcloud.bigtable._generated import bigtable_data_pb2 as data_pb2


class Row(object):
    """Representation of a Google Cloud Bigtable Row.

    :type row_key: bytes
    :param row_key: The key for the current row.

    :type table: :class:`Table <gcloud.bigtable.table.Table>`
    :param table: The table that owns the row.
    """

    def __init__(self, row_key, table):
        self._row_key = _to_bytes(row_key)
        self._table = table


class RowFilter(object):
    """Basic filter to apply to cells in a row.

    These values can be combined via :class:`RowFilterChain`,
    :class:`RowFilterUnion` and :class:`ConditionalRowFilter`.

    .. note::

        This class is a do-nothing base class for all row filters.
    """

    def __ne__(self, other):
        return not self.__eq__(other)


class _RegexFilter(RowFilter):
    """Row filter that uses a regular expression.

    The ``regex`` must be valid RE2 patterns. See Google's
    `RE2 reference`_ for the accepted syntax.

    .. _RE2 reference: https://github.com/google/re2/wiki/Syntax

    :type regex: bytes or str
    :param regex: A regular expression (RE2) for some row filter.
    """

    def __init__(self, regex):
        self.regex = regex

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.regex == self.regex


class RowKeyRegexFilter(_RegexFilter):
    """Row filter for a row key regular expression.

    The ``regex`` must be valid RE2 patterns. See Google's
    `RE2 reference`_ for the accepted syntax.

    .. _RE2 reference: https://github.com/google/re2/wiki/Syntax

    .. note::

        Special care need be used with the expression used. Since
        each of these properties can contain arbitrary bytes, the ``\\C``
        escape sequence must be used if a true wildcard is desired. The ``.``
        character will not match the new line character ``\\n``, which may be
        present in a binary value.

    :type regex: bytes
    :param regex: A regular expression (RE2) to match cells from rows with row
                  keys that satisfy this regex. For a
                  ``CheckAndMutateRowRequest``, this filter is unnecessary
                  since the row key is already specified.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(row_key_regex_filter=self.regex)


class FamilyNameRegexFilter(_RegexFilter):
    """Row filter for a family name regular expression.

    The ``regex`` must be valid RE2 patterns. See Google's
    `RE2 reference`_ for the accepted syntax.

    .. _RE2 reference: https://github.com/google/re2/wiki/Syntax

    :type regex: str
    :param regex: A regular expression (RE2) to match cells from columns in a
                  given column family. For technical reasons, the regex must
                  not contain the ``':'`` character, even if it is not being
                  used as a literal.
    """

    def to_pb(self):
        """Converts the row filter to a protobuf.

        :rtype: :class:`.data_pb2.RowFilter`
        :returns: The converted current object.
        """
        return data_pb2.RowFilter(family_name_regex_filter=self.regex)
