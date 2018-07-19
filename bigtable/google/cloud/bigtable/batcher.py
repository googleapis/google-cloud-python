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

"""User friendly container for Google Cloud Bigtable MutationBatcher."""


import sys

FLUSH_COUNT = 1000
MAX_MUTATIONS = 100000
MAX_ROW_BYTES = 5242880  # 5MB


class MutationsBatcher(object):
    """ Batch mutations using limits MAX_ROW_BYTES, MAX_MUTATIONS and
    FLUSH_COUNT. A batch is sent to finish_batch() if any of these limits is
    exceeded.

    :type table: class
    :param table: class:`~google.cloud.bigtable.table.Table`.

    :type flush_count: int
    :param flush_count: (Optional) Max number of rows to flush. If it
    reaches the max number of rows it calls finish_batch() to mutate the
    current row batch. Default is FLUSH_COUNT (1000 rows).

    :type max_mutations: int
    :param max_mutations: (Optional)  Max number of row mutations to flush.
    If it reaches the max number of row mutations it calls finish_batch() to
    mutate the current row batch. Default is MAX_MUTATIONS (100000 mutations).

    :type max_row_bytes: int
    :param max_row_bytes: (Optional) Max number of row mutations size to
    flush. If it reaches the max number of row mutations size it calls
    finish_batch() to mutate the current row batch. Default is MAX_ROW_BYTES
    (5 MB).
    """

    def __init__(self, table, flush_count=FLUSH_COUNT,
                 max_mutations=MAX_MUTATIONS, max_row_bytes=MAX_ROW_BYTES):
        self.rows = []
        self.total_mutation_count = 0
        self.total_size = 0
        self.table = table
        self.flush_count = flush_count
        self.max_mutations = max_mutations
        self.max_row_bytes = max_row_bytes

    def add_row(self, row):
        """ Add a row using batching logic and finish current batch if
        necessary.

        :type row: class
        :param row: class:`~google.cloud.bigtable.row.DirectRow`.
        """
        mutation_size = sys.getsizeof(row._get_mutations())
        if (self.total_size + mutation_size) >= self.max_row_bytes:
            self.finish_batch()

        mutation_count = len(row._get_mutations())
        if (self.total_mutation_count + mutation_count) >= self.max_mutations:
            self.finish_batch()

        self.rows.append(row)
        self.total_mutation_count += mutation_count
        self.total_size += mutation_size

        if len(self.rows) >= self.flush_count:
            self.finish_batch()

    def finish_batch(self):
        """ Mutate multiple rows in bulk and start a new batch.
        """
        self.table.mutate_rows(self.rows)
        self.total_mutation_count = 0
        self.total_size = 0
        self.rows = []
