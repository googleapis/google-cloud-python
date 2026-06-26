# Copyright 2026 Google LLC
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

import abc

"""
Scenario: The Office Fridge Wars.
This scenario tracks the high-stakes drama of shared office lunches.

TABLE 1: coworkers
| id |      name        | trust_level |
---------------------------------------
| 1  | 'Innocent Alice' |     100     |
| 2  | 'Vegan Sarah'    |     95      |
| 3  | 'Manager Bob'    |     50      |
| 4  | 'Intern Kevin'   |     15      |
| 5  | 'Suspicious Dave'|    -10      |

TABLE 2: office_fridge
| item_id | item_name                      | owner_id | is_stolen | notes |
---------------------------------------------------------------------------
-- Alice's perfectly prepped meals (High theft targets)
|   101   | 'Moms Lasagna'                 |     1    |   True    | "" |
|   102   | 'Chocolate Brownie'            |     1    |   True    | "" |
-- Sarah's food (Safe because it's Kale)
|   103   | 'Kale & Quinoa Bowl'           |     2    |   False   | "" |
-- Manager Bob's lunch (Too fancy to steal?)
|   104   | 'Expensive Sushi'              |     3    |   False   | "" |
-- Kevin's drink (The only thing he brought)
|   105   | 'Mega Energy Drink'            |     4    |   True    | "" |
-- Dave's mystery food (No one dares touch it)
|   106   | 'Unlabeled Tupperware Sludge'  |     5    |   False   | "" |
-- Alice's sandwich (The label makes it a dare - Trap?)
|   107   | 'Sandwich labeled - Do Not Eat'|     1    |   True    | "" |
"""


class SQLFactory(abc.ABC):
    TABLE_PREFIX = "spd20_"
    TABLE1 = "coworkers"
    TABLE1_COLS = "id, name, trust_level"
    TABLE2 = "office_fridge"
    TABLE2_COLS = "item_id, item_name, owner_id, is_stolen, notes"
    SELECT_1 = "SELECT 1"

    @property
    def table1(self):
        return self.TABLE_PREFIX + self.TABLE1

    @property
    def table2(self):
        return self.TABLE_PREFIX + self.TABLE2

    @property
    def stmt_dql_select_1(self):
        return self.SELECT_1

    @property
    @abc.abstractmethod
    def stmt_ddl_create_table1(self):
        pass

    @property
    @abc.abstractmethod
    def stmt_ddl_create_table2(self):
        pass

    @property
    def stmt_ddl_drop_all_cmds(self):
        return [self.stmt_ddl_drop_table1, self.stmt_ddl_drop_table2]

    @property
    def stmt_ddl_drop_table1(self):
        return "DROP TABLE %s" % (self.table1)

    @property
    def stmt_ddl_drop_table2(self):
        return "DROP TABLE %s" % (self.table2)

    def stmt_dql_select_all(self, table):
        return "SELECT * FROM %s" % (table)

    def stmt_dql_select_all_table1(self):
        return self.stmt_dql_select_all(self.table1)

    def stmt_dql_select_all_table2(self):
        return self.stmt_dql_select_all(self.table2)

    def stmt_dql_select_cols(self, table, col):
        return "SELECT (%s) FROM %s" % (col, table)

    def stmt_dql_select_cols_table1(self, col):
        return self.stmt_dql_select_cols(self.table1, col)

    def stmt_dql_select_cols_table2(self, col):
        return self.stmt_dql_select_cols(self.table2, col)

    def stmt_dml_insert(self, table, cols, vals):
        return "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, vals)

    def stmt_dml_insert_table1(self, vals):
        return self.stmt_dml_insert(self.table1, self.TABLE1_COLS, vals)

    def stmt_dml_insert_table2(self, vals):
        return self.stmt_dml_insert(self.table2, self.TABLE2_COLS, vals)

    sample_table1 = [
        [1, "Innocent Alice", 100],
        [2, "Vegan Sarah", 95],
        [3, "Manager Bob", 50],
        [4, "Intern Kevin", 15],
        [5, "Suspicious Dave", -10],
    ]
    names_table1 = sorted([row[1] for row in sample_table1])

    def process_row(self, row):
        def to_sql_literal(value):
            # Check for boolean first
            if isinstance(value, bool):
                return "TRUE" if value else "FALSE"
            # Wrap strings in single quotes
            elif isinstance(value, str):
                return f"'{value}'"
            # Return numbers and other types as-is
            else:
                return str(value)

        return ", ".join(map(to_sql_literal, row))

    def populate_table1(self):
        return [
            self.stmt_dml_insert_table1(self.process_row(row))
            for row in self.sample_table1
        ]

    sample_table2 = [
        [101, "Mystery Sandwich", 1, True, ""],
        [102, "Leftover Pizza", 2, True, ""],
        [103, "Kale & Quinoa Bowl", 3, False, ""],
        [104, "Expensive Sushi", 4, False, ""],
        [105, "Mega Energy Drink", 5, True, ""],
        [106, "Unlabeled Tupperware Sludge", 6, False, ""],
        [107, "Sandwich labeled - Do Not Eat", 7, True, ""],
    ]
    item_names_table2 = sorted([row[1] for row in sample_table2])

    def populate_table2(self):
        return [
            self.stmt_dml_insert_table2(self.process_row(row))
            for row in self.sample_table2
        ]

    @staticmethod
    def get_factory(dialect):
        if dialect == "PostgreSQL":
            return PostgreSQLFactory()
        elif dialect == "GoogleSQL":
            return GoogleSQLFactory()
        else:
            raise ValueError("Unknown dialect: %s" % dialect)


class GoogleSQLFactory(SQLFactory):
    @property
    def stmt_ddl_create_table1(self):
        return (
            "CREATE TABLE %s%s "
            "(id INT64, name STRING(100), trust_level INT64) "
            "PRIMARY KEY (id)" % (self.TABLE_PREFIX, self.TABLE1)
        )

    @property
    def stmt_ddl_create_table2(self):
        return (
            "CREATE TABLE %s%s "
            "(item_id INT64, item_name STRING(100), "
            "owner_id INT64, is_stolen BOOL, notes STRING(100)) "
            "PRIMARY KEY (item_id)" % (self.TABLE_PREFIX, self.TABLE2)
        )


class PostgreSQLFactory(SQLFactory):
    @property
    def stmt_ddl_create_table1(self):
        raise NotImplementedError(
            "PostgreSQL dialect support is not yet implemented..."
        )

    @property
    def stmt_ddl_create_table2(self):
        raise NotImplementedError(
            "PostgreSQL dialect support is not yet implemented..."
        )
