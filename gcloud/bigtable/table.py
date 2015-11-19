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

"""User friendly container for Google Cloud Bigtable Table."""


from gcloud.bigtable.column_family import ColumnFamily
from gcloud.bigtable.row import Row


class Table(object):
    """Representation of a Google Cloud Bigtable Table.

    :type table_id: str
    :param table_id: The ID of the table.

    :type cluster: :class:`.cluster.Cluster`
    :param cluster: The cluster that owns the table.
    """

    def __init__(self, table_id, cluster):
        self.table_id = table_id
        self._cluster = cluster

    def column_family(self, column_family_id):
        """Factory to create a column family associated with this table.

        :type column_family_id: str
        :param column_family_id: The ID of the column family. Must be of the
                                 form ``[_a-zA-Z0-9][-_.a-zA-Z0-9]*``.

        :rtype: :class:`.column_family.ColumnFamily`
        :returns: A column family owned by this table.
        """
        return ColumnFamily(column_family_id, self)

    def row(self, row_key):
        """Factory to create a row associated with this table.

        :type row_key: bytes
        :param row_key: The key for the row being created.

        :rtype: :class:`.Row`
        :returns: A row owned by this table.
        """
        return Row(row_key, self)
