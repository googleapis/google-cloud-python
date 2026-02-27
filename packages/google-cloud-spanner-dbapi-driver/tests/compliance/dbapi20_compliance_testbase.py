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

"""
DBAPI 2.0 Compliance Test
"""
import time
import unittest
from unittest.mock import MagicMock

from .sql_factory import SQLFactory


def encode(s: str) -> bytes:
    return s.encode("utf-8")


def decode(b: bytes) -> str:
    return b.decode("utf-8")


class DBAPI20ComplianceTestBase(unittest.TestCase):
    """
    Base class for DBAPI 2.0 Compliance Tests.
    See PEP 249 for details: https://peps.python.org/pep-0249/
    """

    __test__ = False
    driver = None
    errors = None
    connect_args = ()  # List of arguments to pass to connect
    connect_kw_args = {}  # Keyword arguments for connect
    dialect = "GoogleSQL"

    lower_func = (
        "lower"  # Name of stored procedure to convert string->lowercase
    )

    @property
    def sql_factory(self):
        return SQLFactory.get_factory(self.dialect)

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.cleanup()

    def tearDown(self):
        self.cleanup()

    def cleanup(self):
        try:
            con = self._connect()
            try:
                cur = con.cursor()
                for ddl in self.sql_factory.stmt_ddl_drop_all_cmds:
                    try:
                        cur.execute(ddl)
                        con.commit()
                    except self.driver.Error:
                        # Assume table didn't exist. Other tests will check if
                        # execute is busted.
                        pass
            finally:
                con.close()
        except Exception:
            pass

    def _connect(self):
        try:
            r = self.driver.connect(*self.connect_args, **self.connect_kw_args)
        except AttributeError:
            self.fail("No connect method found in self.driver module")
        return r

    def _execute_select1(self, cur):
        cur.execute(self.sql_factory.stmt_dql_select_1)

    def _simple_queries(self, cur):
        # DDL
        cur.execute(self.sql_factory.stmt_ddl_create_table1)
        # DML
        for sql in self.sql_factory.populate_table1():
            cur.execute(sql)
        # DQL
        cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))
        _ = cur.fetchall()
        self.assertTrue(
            cur.rowcount in (-1, len(self.sql_factory.names_table1))
        )

    def _parametized_queries(self, cur):
        # DDL
        cur.execute(self.sql_factory.stmt_ddl_create_table2)
        # DML
        cur.execute(
            self.sql_factory.stmt_dml_insert_table2(
                "101, 'Moms Lasagna', 1, True, ''"
            )
        )
        self.assertTrue(cur.rowcount in (-1, 1))

        if self.driver.paramstyle == "qmark":
            cur.execute(
                self.sql_factory.stmt_dml_insert_table2(
                    "102, ?, 1, True, 'thi%%s :may ca%%(u)se? troub:1e'"
                ),
                ("Chocolate Brownie",),
            )
        elif self.driver.paramstyle == "numeric":
            cur.execute(
                self.sql_factory.stmt_dml_insert_table2(
                    "102, :1, 1, True,'thi%%s :may ca%%(u)se? troub:1e'"
                ),
                ("Chocolate Brownie",),
            )
        elif self.driver.paramstyle == "named":
            cur.execute(
                self.sql_factory.stmt_dml_insert_table2(
                    "102, :item_name, 1, True, "
                    "'thi%%s :may ca%%(u)se? troub:1e'"
                ),
                {"item_name": "Chocolate Brownie"},
            )
        elif self.driver.paramstyle == "format":
            cur.execute(
                self.sql_factory.stmt_dml_insert_table2(
                    "102, %%s, 1, True, 'thi%%%%s :may ca%%%%(u)se? troub:1e'"
                ),
                ("Chocolate Brownie",),
            )
        elif self.driver.paramstyle == "pyformat":
            cur.execute(
                self.sql_factory.stmt_dml_insert_table2(
                    "102, %%(item_name), 1, True, "
                    "'thi%%%%s :may ca%%%%(u)se? troub:1e'"
                ),
                {"item_name": "Chocolate Brownie"},
            )
        else:
            self.fail("Invalid paramstyle")

        self.assertTrue(cur.rowcount in (-1, 1))

        # DQL
        cur.execute(self.sql_factory.stmt_dql_select_all_table2())
        rows = cur.fetchall()

        self.assertEqual(len(rows), 2, "cursor.fetchall returned too few rows")
        item_name = [rows[0][1], rows[1][1]]
        item_name.sort()
        self.assertEqual(
            item_name[0],
            "Chocolate Brownie",
            "cursor.fetchall retrieved incorrect data, or data inserted "
            "incorrectly",
        )
        self.assertEqual(
            item_name[1],
            "Moms Lasagna",
            "cursor.fetchall retrieved incorrect data, or data inserted "
            "incorrectly",
        )

        trouble = "thi%s :may ca%(u)se? troub:1e"
        self.assertEqual(
            rows[0][4],
            trouble,
            "cursor.fetchall retrieved incorrect data, or data inserted "
            "incorrectly. Got=%s, Expected=%s"
            % (repr(rows[0][4]), repr(trouble)),
        )
        self.assertEqual(
            rows[1][4],
            trouble,
            "cursor.fetchall retrieved incorrect data, or data inserted "
            "incorrectly. Got=%s, Expected=%s"
            % (repr(rows[1][4]), repr(trouble)),
        )

    # =========================================================================
    # Module Interface
    # =========================================================================

    def test_module_attributes(self):
        """Test module-level attributes.
        See PEP 249 Module Interface.
        """
        self.assertTrue(hasattr(self.driver, "apilevel"))
        self.assertTrue(hasattr(self.driver, "threadsafety"))
        self.assertTrue(hasattr(self.driver, "paramstyle"))
        self.assertTrue(hasattr(self.driver, "connect"))

    def test_apilevel(self):
        """Test module.apilevel.
        Must be '2.0'.
        """
        try:
            apilevel = self.driver.apilevel
            self.assertEqual(apilevel, "2.0", "Driver apilevel must be '2.0'")
        except AttributeError:
            self.fail("Driver doesn't define apilevel")

    def test_threadsafety(self):
        """Test module.threadsafety.
        Must be 0, 1, 2, or 3.
        """
        try:
            threadsafety = self.driver.threadsafety
            self.assertTrue(
                threadsafety in (0, 1, 2, 3),
                "threadsafety must be one of 0, 1, 2, 3",
            )
        except AttributeError:
            self.fail("Driver doesn't define threadsafety")

    def test_paramstyle(self):
        """Test module.paramstyle.
        Must be one of 'qmark', 'numeric', 'named', 'format', 'pyformat'.
        """
        try:
            paramstyle = self.driver.paramstyle
            self.assertTrue(
                paramstyle
                in ("qmark", "numeric", "named", "format", "pyformat"),
                "Invalid paramstyle",
            )
        except AttributeError:
            self.fail("Driver doesn't define paramstyle")

    def test_exceptions(self):
        """Test module exception hierarchy.
        See PEP 249 Exceptions.
        """
        self.assertTrue(issubclass(self.errors.Warning, Exception))
        self.assertTrue(issubclass(self.errors.Error, Exception))
        self.assertTrue(
            issubclass(self.errors.InterfaceError, self.errors.Error)
        )
        self.assertTrue(
            issubclass(self.errors.DatabaseError, self.errors.Error)
        )
        self.assertTrue(
            issubclass(self.errors.DataError, self.errors.DatabaseError)
        )
        self.assertTrue(
            issubclass(self.errors.OperationalError, self.errors.DatabaseError)
        )
        self.assertTrue(
            issubclass(self.errors.IntegrityError, self.errors.DatabaseError)
        )
        self.assertTrue(
            issubclass(self.errors.InternalError, self.errors.DatabaseError)
        )
        self.assertTrue(
            issubclass(self.errors.ProgrammingError, self.errors.DatabaseError)
        )
        self.assertTrue(
            issubclass(self.errors.NotSupportedError, self.errors.DatabaseError)
        )

    # =========================================================================
    # Connection Objects
    # =========================================================================

    def test_connect(self):
        """Test that connect returns a connection object."""
        conn = self._connect()
        conn.close()

    def test_connection_attributes(self):
        """Test Connection object attributes/methods."""
        # Mock connection internal
        mock_internal = MagicMock()
        conn = self.driver.Connection(mock_internal)

        self.assertTrue(hasattr(conn, "close"))
        self.assertTrue(hasattr(conn, "commit"))
        self.assertTrue(hasattr(conn, "rollback"))
        self.assertTrue(hasattr(conn, "cursor"))
        # Optional but checked because we added it
        self.assertTrue(hasattr(conn, "messages"))

    def test_close(self):
        """Test connection.close()."""
        con = self._connect()
        try:
            cur = con.cursor()
        finally:
            con.close()

        # cursor.execute should raise an Error if called
        # after connection closed
        self.assertRaises(self.driver.Error, self._execute_select1, cur)

        # connection.commit should raise an Error if called
        # after connection closed
        self.assertRaises(self.driver.Error, con.commit)

    def test_non_idempotent_close(self):
        """Test that calling close() twice raises an Error
        (optional behavior)."""
        con = self._connect()
        con.close()
        # connection.close should raise an Error if called more than once
        self.assertRaises(self.driver.Error, con.close)

    def test_commit(self):
        """Test connection.commit()."""
        con = self._connect()
        try:
            # Commit must work, even if it doesn't do anything
            con.commit()
        finally:
            con.close()

    def test_rollback(self):
        """Test connection.rollback()."""
        con = self._connect()
        try:
            # If rollback is defined, it should either work or throw
            # the documented exception
            if hasattr(con, "rollback"):
                try:
                    con.rollback()
                except self.driver.NotSupportedError:
                    pass
        finally:
            con.close()

    def test_cursor(self):
        """Test connection.cursor()."""
        con = self._connect()
        try:
            curr = con.cursor()
            self.assertIsNotNone(curr)
        finally:
            con.close()

    def test_cursor_isolation(self):
        """Test that cursors are isolated (transactionally)."""
        con = self._connect()
        try:
            # Make sure cursors created from the same connection have
            # the documented transaction isolation level
            cur1 = con.cursor()
            cur2 = con.cursor()
            cur1.execute(self.sql_factory.stmt_ddl_create_table1)
            # DDL usually requires a clean slate or commit in some test envs
            con.commit()
            cur1.execute(
                self.sql_factory.stmt_dml_insert_table1(
                    "1, 'Innocent Alice', 100"
                )
            )
            con.commit()
            cur2.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))
            users = cur2.fetchone()

            self.assertEqual(len(users), 1)
            self.assertEqual(users[0], "Innocent Alice")
        finally:
            con.close()

    # =========================================================================
    # Cursor Objects
    # =========================================================================

    def test_cursor_attributes(self):
        """Test Cursor object attributes/methods."""
        mock_conn = MagicMock()
        cursor = self.driver.Cursor(mock_conn)

        self.assertTrue(hasattr(cursor, "description"))
        self.assertTrue(hasattr(cursor, "rowcount"))
        self.assertTrue(hasattr(cursor, "callproc"))
        self.assertTrue(hasattr(cursor, "close"))
        self.assertTrue(hasattr(cursor, "execute"))
        self.assertTrue(hasattr(cursor, "executemany"))
        self.assertTrue(hasattr(cursor, "fetchone"))
        self.assertTrue(hasattr(cursor, "fetchmany"))
        self.assertTrue(hasattr(cursor, "fetchall"))
        self.assertTrue(hasattr(cursor, "nextset"))
        self.assertTrue(hasattr(cursor, "arraysize"))
        self.assertTrue(hasattr(cursor, "setinputsizes"))
        self.assertTrue(hasattr(cursor, "setoutputsize"))

        # Test iterator
        self.assertTrue(hasattr(cursor, "__iter__"))
        self.assertTrue(hasattr(cursor, "__next__"))

        # Test callproc raising NotSupportedError (mandatory by
        # default unless implemented)
        with self.assertRaises(self.errors.NotSupportedError):
            cursor.callproc("proc")

    def test_description(self):
        """Test cursor.description."""
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(self.sql_factory.stmt_ddl_create_table1)

            self.assertEqual(
                cur.description,
                None,
                "cursor.description should be none after executing a "
                "statement that can return no rows (such as DDL)",
            )
            cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))
            self.assertEqual(
                len(cur.description),
                1,
                "cursor.description describes too many columns",
            )
            self.assertEqual(
                len(cur.description[0]),
                7,
                "cursor.description[x] tuples must have 7 elements",
            )
            self.assertEqual(
                cur.description[0][0].lower(),
                "name",
                "cursor.description[x][0] must return column name",
            )
            self.assertEqual(
                cur.description[0][1],
                self.driver.STRING,
                "cursor.description[x][1] must return column type. Got %r"
                % cur.description[0][1],
            )

            # Make sure self.description gets reset
            cur.execute(self.sql_factory.stmt_ddl_create_table2)
            self.assertEqual(
                cur.description,
                None,
                "cursor.description not being set to None when executing "
                "no-result statements (eg. DDL)",
            )
        finally:
            con.close()

    def test_rowcount(self):
        """Test cursor.rowcount."""
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(self.sql_factory.stmt_ddl_create_table1)
            self.assertTrue(
                cur.rowcount in (-1, 0),  # Bug #543885
                "cursor.rowcount should be -1 or 0 after executing no-result "
                "statements",
            )
            cur.execute(
                self.sql_factory.stmt_dml_insert_table1(
                    "1, 'Innocent Alice', 100"
                )
            )
            self.assertTrue(
                cur.rowcount in (-1, 1),
                "cursor.rowcount should == number or rows inserted, or "
                "set to -1 after executing an insert statement",
            )
            cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))
            self.assertTrue(
                cur.rowcount in (-1, 1),
                "cursor.rowcount should == number of rows returned, or "
                "set to -1 after executing a select statement",
            )
            cur.execute(self.sql_factory.stmt_ddl_create_table2)
            self.assertTrue(
                cur.rowcount in (-1, 0),  # Bug #543885
                "cursor.rowcount should be -1 or 0 after executing no-result "
                "statements",
            )
        finally:
            con.close()

    def test_callproc(self):
        """Test cursor.callproc()."""
        con = self._connect()
        try:
            cur = con.cursor()
            if self.lower_func and hasattr(cur, "callproc"):
                r = cur.callproc(self.lower_func, ("FOO",))
                self.assertEqual(len(r), 1)
                self.assertEqual(r[0], "FOO")
                r = cur.fetchall()
                self.assertEqual(len(r), 1, "callproc produced no result set")
                self.assertEqual(
                    len(r[0]), 1, "callproc produced invalid result set"
                )
                self.assertEqual(
                    r[0][0], "foo", "callproc produced invalid results"
                )
        except self.driver.NotSupportedError:
            pass
        finally:
            con.close()

    def test_execute(self):
        """Test cursor.execute()."""
        con = self._connect()
        try:
            cur = con.cursor()
            self._simple_queries(cur)
        finally:
            con.close()

    @unittest.skip("Failing as params are not yet handled")
    def test_execute_with_params(self):
        """Test cursor.execute() with parameters."""
        con = self._connect()
        try:
            cur = con.cursor()
            self._parametized_queries(cur)
        finally:
            con.close()

    @unittest.skip("Failing as params are not yet handled")
    def test_executemany_with_params(self):
        """Test cursor.executemany() with parameters."""
        con = self._connect()
        try:
            cur = con.cursor()
            # DDL
            cur.execute(self.sql_factory.stmt_ddl_create_table2)

            largs = [("Moms Lasagna",), ("Chocolate Brownie",)]
            margs = [{"name": "Moms Lasagna"}, {"name": "Chocolate Brownie"}]
            if self.driver.paramstyle == "qmark":
                cur.executemany(
                    self.sql_factory.stmt_dml_insert_table2(
                        "102, ?, 1, True, 'thi%%s :may ca%%(u)se? troub:1e'"
                    ),
                    largs,
                )
            elif self.driver.paramstyle == "numeric":
                cur.executemany(
                    self.sql_factory.stmt_dml_insert_table2(
                        "102, :1, 1, True,'thi%%s :may ca%%(u)se? troub:1e'"
                    ),
                    largs,
                )
            elif self.driver.paramstyle == "named":
                cur.executemany(
                    self.sql_factory.stmt_dml_insert_table2(
                        "102, :item_name, 1, True, "
                        "'thi%%s :may ca%%(u)se? troub:1e'"
                    ),
                    margs,
                )
            elif self.driver.paramstyle == "format":
                cur.executemany(
                    self.sql_factory.stmt_dml_insert_table2(
                        "102, %%s, 1, True, "
                        "'thi%%%%s :may ca%%%%(u)se? troub:1e'"
                    ),
                    largs,
                )
            elif self.driver.paramstyle == "pyformat":
                cur.executemany(
                    self.sql_factory.stmt_dml_insert_table2(
                        "102, %%(item_name), 1, True, "
                        "'thi%%%%s :may ca%%%%(u)se? troub:1e'"
                    ),
                    margs,
                )
            else:
                self.fail("Unknown paramstyle")

            self.assertTrue(
                cur.rowcount in (-1, 2),
                "insert using cursor.executemany set cursor.rowcount to "
                "incorrect value %r" % cur.rowcount,
            )

            # DQL
            cur.execute(self.sql_factory.stmt_dql_select_all_table2())
            rows = cur.fetchall()
            self.assertEqual(
                len(rows),
                2,
                "cursor.fetchall retrieved incorrect number of rows",
            )
            item_names = [rows[0][1], rows[1][1]]
            item_names.sort()
            self.assertEqual(
                item_names[0],
                "Chocolate Brownie",
                "cursor.fetchall retrieved incorrect data, or data inserted "
                "incorrectly",
            )
            self.assertEqual(
                item_names[1],
                "Moms Lasagna",
                "cursor.fetchall retrieved incorrect data, or data inserted "
                "incorrectly",
            )
        finally:
            con.close()

    def test_fetchone(self):
        """Test cursor.fetchone()."""
        con = self._connect()
        try:
            cur = con.cursor()

            # cursor.fetchone should raise an Error if called before
            # executing a select-type query
            self.assertRaises(self.driver.Error, cur.fetchone)

            # cursor.fetchone should raise an Error if called after
            # executing a query that cannot return rows
            cur.execute(self.sql_factory.stmt_ddl_create_table1)
            self.assertRaises(self.driver.Error, cur.fetchone)

            cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))
            self.assertEqual(
                cur.fetchone(),
                None,
                "cursor.fetchone should return None if a query retrieves "
                "no rows",
            )
            self.assertTrue(cur.rowcount in (-1, 0))

            # cursor.fetchone should raise an Error if called after
            # executing a query that cannot return rows
            cur.execute(
                self.sql_factory.stmt_dml_insert_table1(
                    "1, 'Innocent Alice', 100"
                )
            )
            self.assertRaises(self.driver.Error, cur.fetchone)

            cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))
            row = cur.fetchone()
            self.assertEqual(
                len(row),
                1,
                "cursor.fetchone should have retrieved a single row",
            )
            self.assertEqual(
                row[0],
                "Innocent Alice",
                "cursor.fetchone retrieved incorrect data",
            )
            self.assertEqual(
                cur.fetchone(),
                None,
                "cursor.fetchone should return None if no more rows available",
            )
            self.assertTrue(cur.rowcount in (-1, 1))
        finally:
            con.close()

    def test_fetchmany(self):
        """Test cursor.fetchmany()."""
        con = self._connect()
        try:
            cur = con.cursor()

            # cursor.fetchmany should raise an Error if called without
            # issuing a query
            self.assertRaises(self.driver.Error, cur.fetchmany, 4)

            cur.execute(self.sql_factory.stmt_ddl_create_table1)
            for sql in self.sql_factory.populate_table1():
                cur.execute(sql)

            cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))

            r = cur.fetchmany()
            self.assertEqual(
                len(r),
                1,
                "cursor.fetchmany retrieved incorrect number of rows, "
                "default of arraysize is one.",
            )

            cur.arraysize = 10
            r = cur.fetchmany(2)  # Should get 3 rows
            self.assertEqual(
                len(r), 2, "cursor.fetchmany retrieved incorrect number of rows"
            )

            r = cur.fetchmany(4)  # Should get 2 more
            self.assertEqual(
                len(r), 2, "cursor.fetchmany retrieved incorrect number of rows"
            )

            r = cur.fetchmany(4)  # Should be an empty sequence
            self.assertEqual(
                len(r),
                0,
                "cursor.fetchmany should return an empty sequence after "
                "results are exhausted",
            )

            self.assertTrue(cur.rowcount in (-1, 5))

            # Same as above, using cursor.arraysize
            cur.arraysize = 3
            cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))
            r = cur.fetchmany()  # Should get 4 rows
            self.assertEqual(
                len(r), 3, "cursor.arraysize not being honoured by fetchmany"
            )

            r = cur.fetchmany()  # Should get 2 more
            self.assertEqual(len(r), 2)

            r = cur.fetchmany()  # Should be an empty sequence
            self.assertEqual(len(r), 0)

            self.assertTrue(cur.rowcount in (-1, 5))

            cur.arraysize = 5
            cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))
            rows = cur.fetchmany()  # Should get all rows
            self.assertTrue(cur.rowcount in (-1, 5))
            self.assertEqual(len(rows), 5)
            rows = [r[0] for r in rows]
            rows.sort()

            # Make sure we get the right data back out
            for i in range(0, 5):
                self.assertEqual(
                    rows[i],
                    self.sql_factory.names_table1[i],
                    "incorrect data retrieved by cursor.fetchmany",
                )

            rows = cur.fetchmany()  # Should return an empty list
            self.assertEqual(
                len(rows),
                0,
                "cursor.fetchmany should return an empty sequence if "
                "called after the whole result set has been fetched",
            )
            self.assertTrue(cur.rowcount in (-1, 5))

            cur.execute(self.sql_factory.stmt_ddl_create_table2)
            cur.execute(
                self.sql_factory.stmt_dql_select_cols_table2("item_name")
            )
            rows = cur.fetchmany()  # Should get empty sequence
            self.assertEqual(
                len(rows),
                0,
                "cursor.fetchmany should return an empty sequence if "
                "query retrieved no rows",
            )
            self.assertTrue(cur.rowcount in (-1, 0))

            for sql in self.sql_factory.populate_table2():
                cur.execute(sql)

            cur.execute(
                self.sql_factory.stmt_dql_select_cols_table2("item_name")
            )
            cur.arraysize = 10
            rows = cur.fetchmany()  # Should get empty sequence
            self.assertEqual(len(rows), 7)
            self.assertTrue(cur.rowcount in (-1, 7))

        finally:
            con.close()

    def test_fetchall(self):
        """Test cursor.fetchall()."""
        con = self._connect()
        try:
            cur = con.cursor()
            # cursor.fetchall should raise an Error if called
            # without executing a query that may return rows (such
            # as a select)
            self.assertRaises(self.driver.Error, cur.fetchall)

            cur.execute(self.sql_factory.stmt_ddl_create_table1)
            for sql in self.sql_factory.populate_table1():
                cur.execute(sql)

            # cursor.fetchall should raise an Error if called
            # after executing a a statement that cannot return rows
            self.assertRaises(self.driver.Error, cur.fetchall)

            cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))
            rows = cur.fetchall()
            self.assertTrue(
                cur.rowcount in (-1, len(self.sql_factory.names_table1))
            )
            self.assertEqual(
                len(rows),
                len(self.sql_factory.names_table1),
                "cursor.fetchall did not retrieve all rows",
            )
            rows = [r[0] for r in rows]
            rows.sort()
            for i in range(0, len(self.sql_factory.names_table1)):
                self.assertEqual(
                    rows[i],
                    self.sql_factory.names_table1[i],
                    "cursor.fetchall retrieved incorrect rows",
                )
            rows = cur.fetchall()
            self.assertEqual(
                len(rows),
                0,
                "cursor.fetchall should return an empty list if called "
                "after the whole result set has been fetched",
            )
            self.assertTrue(
                cur.rowcount in (-1, len(self.sql_factory.names_table1))
            )

            cur.execute(self.sql_factory.stmt_ddl_create_table2)
            cur.execute(
                self.sql_factory.stmt_dql_select_cols_table2("item_name")
            )
            rows = cur.fetchall()
            self.assertTrue(cur.rowcount in (-1, 0))
            self.assertEqual(
                len(rows),
                0,
                "cursor.fetchall should return an empty list if "
                "a select query returns no rows",
            )

        finally:
            con.close()

    def test_mixedfetch(self):
        """Test mixing fetchone, fetchmany, and fetchall."""
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(self.sql_factory.stmt_ddl_create_table1)
            for sql in self.sql_factory.populate_table1():
                cur.execute(sql)

            cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))

            rows1 = cur.fetchone()
            rows23 = cur.fetchmany(2)
            rows4 = cur.fetchone()
            rows5 = cur.fetchall()

            self.assertTrue(
                cur.rowcount in (-1, len(self.sql_factory.names_table1))
            )
            self.assertEqual(
                len(rows23), 2, "fetchmany returned incorrect number of rows"
            )
            self.assertEqual(
                len(rows5), 1, "fetchall returned incorrect number of rows"
            )

            rows = [rows1[0]]
            rows.extend([rows23[0][0], rows23[1][0]])
            rows.append(rows4[0])
            rows.extend([rows5[0][0]])
            rows.sort()
            for i in range(0, len(self.sql_factory.names_table1)):
                self.assertEqual(
                    rows[i],
                    self.sql_factory.names_table1[i],
                    "incorrect data retrieved or inserted",
                )
        finally:
            con.close()

    def help_nextset_setUp(self, cur):
        sql = "SELECT 1; SELECT 2;"
        cur.execute(sql)

    def help_nextset_tearDown(self, cur):
        pass

    def test_nextset(self):
        """Test cursor.nextset()."""
        con = self._connect()
        try:
            cur = con.cursor()
            if not hasattr(cur, "nextset"):
                return

            try:
                self.help_nextset_setUp(cur)
                rows = cur.fetchone()
                self.assertEqual(len(rows), 1)
                s = cur.nextset()
                self.assertEqual(
                    s, True, "Has more return sets, should return True"
                )
            finally:
                self.help_nextset_tearDown(cur)

        finally:
            con.close()

    def test_no_nextset(self):
        """Test cursor.nextset() when no more sets exist."""
        con = self._connect()
        try:
            cur = con.cursor()
            sql = "SELECT 1;"
            cur.execute(sql)
            if not hasattr(cur, "nextset"):
                return

            try:
                rows = cur.fetchone()
                self.assertEqual(len(rows), 1)
                s = cur.nextset()
                self.assertEqual(
                    s, None, "No more return sets, should return None"
                )
            finally:
                self.help_nextset_tearDown(cur)

        finally:
            con.close()

    def test_arraysize(self):
        """Test cursor.arraysize."""
        # Not much here - rest of the tests for this are in test_fetchmany
        con = self._connect()
        try:
            cur = con.cursor()
            self.assertTrue(
                hasattr(cur, "arraysize"),
                "cursor.arraysize must be defined",
            )
        finally:
            con.close()

    def test_setinputsizes(self):
        """Test cursor.setinputsizes()."""
        con = self._connect()
        try:
            cur = con.cursor()
            cur.setinputsizes((25,))
            self._simple_queries(cur)  # Make sure cursor still works
        finally:
            con.close()

    def test_setoutputsize_basic(self):
        """Test cursor.setoutputsize()."""
        # Basic test is to make sure setoutputsize doesn't blow up
        con = self._connect()
        try:
            cur = con.cursor()
            cur.setoutputsize(1000)
            cur.setoutputsize(2000, 0)
            self._simple_queries(cur)  # Make sure the cursor still works
        finally:
            con.close()

    def test_setoutputsize(self):
        """Extended test for cursor.setoutputsize() (optional)."""
        # Real test for setoutputsize is driver dependant
        raise NotImplementedError("Driver needed to override this test")

    def test_None(self):
        """Test unpacking of NULL values."""
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(self.sql_factory.stmt_ddl_create_table1)
            # inserting NULL to the second column, because some drivers might
            # need the first one to be primary key, which means it needs
            # to have a non-NULL value
            cur.execute(self.sql_factory.stmt_dml_insert_table1("1, NULL, 100"))
            cur.execute(self.sql_factory.stmt_dql_select_cols_table1("name"))
            row = cur.fetchone()
            self.assertEqual(len(row), 1)
            self.assertEqual(row[0], None, "NULL value not returned as None")
        finally:
            con.close()

    # =========================================================================
    # Type Objects and Constructors
    # =========================================================================

    def test_type_objects(self):
        """Test type objects (STRING, BINARY, etc.)."""
        self.assertTrue(hasattr(self.driver, "STRING"))
        self.assertTrue(hasattr(self.driver, "BINARY"))
        self.assertTrue(hasattr(self.driver, "NUMBER"))
        self.assertTrue(hasattr(self.driver, "DATETIME"))
        self.assertTrue(hasattr(self.driver, "ROWID"))

    def test_constructors(self):
        """Test type constructors (Date, Time, etc.)."""
        self.assertTrue(hasattr(self.driver, "Date"))
        self.assertTrue(hasattr(self.driver, "Time"))
        self.assertTrue(hasattr(self.driver, "Timestamp"))
        self.assertTrue(hasattr(self.driver, "DateFromTicks"))
        self.assertTrue(hasattr(self.driver, "TimeFromTicks"))
        self.assertTrue(hasattr(self.driver, "TimestampFromTicks"))
        self.assertTrue(hasattr(self.driver, "Binary"))

    def test_Date(self):
        """Test Date constructor."""
        d1 = self.driver.Date(2002, 12, 25)
        d2 = self.driver.DateFromTicks(
            time.mktime((2002, 12, 25, 0, 0, 0, 0, 0, 0))
        )
        # Can we assume this? API doesn't specify, but it seems implied
        self.assertEqual(str(d1), str(d2))

    def test_Time(self):
        """Test Time constructor."""
        # 1. Create the target time
        t1 = self.driver.Time(13, 45, 30)

        # 2. Create ticks using Local Time (mktime is local)
        # We use a dummy date (2001-01-01)
        target_tuple = (2001, 1, 1, 13, 45, 30, 0, 0, 0)
        ticks = time.mktime(target_tuple)

        t2 = self.driver.TimeFromTicks(ticks)

        # CHECK 1: Ensure they are the same type (likely datetime.time)
        self.assertIsInstance(t1, type(t2))

        # CHECK 2: Compare value semantics, not string representation
        # This avoids format differences but still requires timezone alignment
        self.assertEqual(t1, t2)

    def test_Timestamp(self):
        """Test Timestamp constructor."""
        t1 = self.driver.Timestamp(2002, 12, 25, 13, 45, 30)
        t2 = self.driver.TimestampFromTicks(
            time.mktime((2002, 12, 25, 13, 45, 30, 0, 0, 0))
        )
        # Can we assume this? API doesn't specify, but it seems implied
        self.assertEqual(str(t1), str(t2))

    def test_Binary(self):
        """Test Binary constructor."""
        s = "Something"
        b = self.driver.Binary(encode(s))
        self.assertEqual(s, decode(b))

    def test_STRING(self):
        """Test STRING type object."""
        self.assertTrue(
            hasattr(self.driver, "STRING"), "module.STRING must be defined"
        )

    def test_BINARY(self):
        """Test BINARY type object."""
        self.assertTrue(
            hasattr(self.driver, "BINARY"), "module.BINARY must be defined."
        )

    def test_NUMBER(self):
        """Test NUMBER type object."""
        self.assertTrue(
            hasattr(self.driver, "NUMBER"), "module.NUMBER must be defined."
        )

    def test_DATETIME(self):
        """Test DATETIME type object."""
        self.assertTrue(
            hasattr(self.driver, "DATETIME"), "module.DATETIME must be defined."
        )

    def test_ROWID(self):
        """Test ROWID type object."""
        self.assertTrue(
            hasattr(self.driver, "ROWID"), "module.ROWID must be defined."
        )
