# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import unittest

from unittest import mock


class TestParser(unittest.TestCase):
    def test_func(self):
        from google.cloud.spanner_dbapi.parser import FUNC
        from google.cloud.spanner_dbapi.parser import a_args
        from google.cloud.spanner_dbapi.parser import expect
        from google.cloud.spanner_dbapi.parser import func
        from google.cloud.spanner_dbapi.parser import pyfmt_str

        cases = [
            ("_91())", ")", func("_91", a_args([]))),
            ("_a()", "", func("_a", a_args([]))),
            ("___()", "", func("___", a_args([]))),
            ("abc()", "", func("abc", a_args([]))),
            (
                "AF112(%s, LOWER(%s, %s), rand(%s, %s, TAN(%s, %s)))",
                "",
                func(
                    "AF112",
                    a_args(
                        [
                            pyfmt_str,
                            func("LOWER", a_args([pyfmt_str, pyfmt_str])),
                            func(
                                "rand",
                                a_args(
                                    [
                                        pyfmt_str,
                                        pyfmt_str,
                                        func(
                                            "TAN",
                                            a_args([pyfmt_str, pyfmt_str]),
                                        ),
                                    ]
                                ),
                            ),
                        ]
                    ),
                ),
            ),
        ]

        for text, want_unconsumed, want_parsed in cases:
            with self.subTest(text=text):
                got_unconsumed, got_parsed = expect(text, FUNC)
                self.assertEqual(got_parsed, want_parsed)
                self.assertEqual(got_unconsumed, want_unconsumed)

    def test_func_fail(self):
        from google.cloud.spanner_dbapi.exceptions import ProgrammingError
        from google.cloud.spanner_dbapi.parser import FUNC
        from google.cloud.spanner_dbapi.parser import expect

        cases = [
            ("", "FUNC: `` does not begin with `a-zA-z` nor a `_`"),
            ("91", "FUNC: `91` does not begin with `a-zA-z` nor a `_`"),
            ("_91", "supposed to begin with `\\(`"),
            ("_91(", "supposed to end with `\\)`"),
            ("_.()", "supposed to begin with `\\(`"),
            ("_a.b()", "supposed to begin with `\\(`"),
        ]

        for text, wantException in cases:
            with self.subTest(text=text):
                self.assertRaisesRegex(
                    ProgrammingError, wantException, lambda: expect(text, FUNC)
                )

    def test_func_eq(self):
        from google.cloud.spanner_dbapi.parser import func

        func1 = func("func1", None)
        func2 = func("func2", None)
        self.assertFalse(func1 == object)
        self.assertFalse(func1 == func2)
        func2.name = func1.name
        func1.args = 0
        func2.args = "0"
        self.assertFalse(func1 == func2)
        func1.args = [0]
        func2.args = [0, 0]
        self.assertFalse(func1 == func2)
        func2.args = func1.args
        self.assertTrue(func1 == func2)

    def test_a_args(self):
        from google.cloud.spanner_dbapi.parser import ARGS
        from google.cloud.spanner_dbapi.parser import a_args
        from google.cloud.spanner_dbapi.parser import expect
        from google.cloud.spanner_dbapi.parser import func
        from google.cloud.spanner_dbapi.parser import pyfmt_str

        cases = [
            ("()", "", a_args([])),
            ("(%s)", "", a_args([pyfmt_str])),
            ("(%s,)", "", a_args([pyfmt_str])),
            ("(%s),", ",", a_args([pyfmt_str])),
            (
                "(%s,%s, f1(%s, %s))",
                "",
                a_args(
                    [
                        pyfmt_str,
                        pyfmt_str,
                        func("f1", a_args([pyfmt_str, pyfmt_str])),
                    ]
                ),
            ),
        ]

        for text, want_unconsumed, want_parsed in cases:
            with self.subTest(text=text):
                got_unconsumed, got_parsed = expect(text, ARGS)
                self.assertEqual(got_parsed, want_parsed)
                self.assertEqual(got_unconsumed, want_unconsumed)

    def test_a_args_fail(self):
        from google.cloud.spanner_dbapi.exceptions import ProgrammingError
        from google.cloud.spanner_dbapi.parser import ARGS
        from google.cloud.spanner_dbapi.parser import expect

        cases = [
            ("", "ARGS: supposed to begin with `\\(`"),
            ("(", "ARGS: supposed to end with `\\)`"),
            (")", "ARGS: supposed to begin with `\\(`"),
            ("(%s,%s, f1(%s, %s), %s", "ARGS: supposed to end with `\\)`"),
        ]

        for text, wantException in cases:
            with self.subTest(text=text):
                self.assertRaisesRegex(
                    ProgrammingError, wantException, lambda: expect(text, ARGS)
                )

    def test_a_args_has_expr(self):
        from google.cloud.spanner_dbapi.parser import a_args

        self.assertFalse(a_args([]).has_expr())
        self.assertTrue(a_args([[0]]).has_expr())

    def test_a_args_eq(self):
        from google.cloud.spanner_dbapi.parser import a_args

        a1 = a_args([0])
        self.assertFalse(a1 == object())
        a2 = a_args([0, 0])
        self.assertFalse(a1 == a2)
        a1.argv = [0, 1]
        self.assertFalse(a1 == a2)
        a2.argv = [0, 1]
        self.assertTrue(a1 == a2)

    def test_a_args_homogeneous(self):
        from google.cloud.spanner_dbapi.parser import a_args
        from google.cloud.spanner_dbapi.parser import terminal

        a_obj = a_args([a_args([terminal(10 ** i)]) for i in range(10)])
        self.assertTrue(a_obj.homogenous())

        a_obj = a_args([a_args([[object()]]) for _ in range(10)])
        self.assertFalse(a_obj.homogenous())

    def test_a_args__is_equal_length(self):
        from google.cloud.spanner_dbapi.parser import a_args

        a_obj = a_args([])
        self.assertTrue(a_obj._is_equal_length())

    def test_values(self):
        from google.cloud.spanner_dbapi.parser import a_args
        from google.cloud.spanner_dbapi.parser import terminal
        from google.cloud.spanner_dbapi.parser import values

        a_obj = a_args([a_args([terminal(10 ** i)]) for i in range(10)])
        self.assertEqual(str(values(a_obj)), "VALUES%s" % str(a_obj))

    def test_expect(self):
        from google.cloud.spanner_dbapi.parser import ARGS
        from google.cloud.spanner_dbapi.parser import EXPR
        from google.cloud.spanner_dbapi.parser import FUNC
        from google.cloud.spanner_dbapi.parser import expect
        from google.cloud.spanner_dbapi.parser import pyfmt_str
        from google.cloud.spanner_dbapi import exceptions

        with self.assertRaises(exceptions.ProgrammingError):
            expect(word="", token=ARGS)
        with self.assertRaises(exceptions.ProgrammingError):
            expect(word="ABC", token=ARGS)
        with self.assertRaises(exceptions.ProgrammingError):
            expect(word="(", token=ARGS)

        expected = "", pyfmt_str
        self.assertEqual(expect("%s", EXPR), expected)

        expected = expect("function()", FUNC)
        self.assertEqual(expect("function()", EXPR), expected)

        with self.assertRaises(exceptions.ProgrammingError):
            expect(word="", token="ABC")

    def test_expect_values(self):
        from google.cloud.spanner_dbapi.parser import VALUES
        from google.cloud.spanner_dbapi.parser import a_args
        from google.cloud.spanner_dbapi.parser import expect
        from google.cloud.spanner_dbapi.parser import func
        from google.cloud.spanner_dbapi.parser import pyfmt_str
        from google.cloud.spanner_dbapi.parser import values

        cases = [
            ("VALUES ()", "", values([a_args([])])),
            ("VALUES", "", values([])),
            ("VALUES(%s)", "", values([a_args([pyfmt_str])])),
            ("    VALUES    (%s)    ", "", values([a_args([pyfmt_str])])),
            ("VALUES(%s, %s)", "", values([a_args([pyfmt_str, pyfmt_str])])),
            (
                "VALUES(%s, %s, LOWER(%s, %s))",
                "",
                values(
                    [
                        a_args(
                            [
                                pyfmt_str,
                                pyfmt_str,
                                func("LOWER", a_args([pyfmt_str, pyfmt_str])),
                            ]
                        )
                    ]
                ),
            ),
            (
                "VALUES (UPPER(%s)), (%s)",
                "",
                values(
                    [
                        a_args([func("UPPER", a_args([pyfmt_str]))]),
                        a_args([pyfmt_str]),
                    ]
                ),
            ),
        ]

        for text, want_unconsumed, want_parsed in cases:
            with self.subTest(text=text):
                got_unconsumed, got_parsed = expect(text, VALUES)
                self.assertEqual(got_parsed, want_parsed)
                self.assertEqual(got_unconsumed, want_unconsumed)

    def test_expect_values_fail(self):
        from google.cloud.spanner_dbapi.exceptions import ProgrammingError
        from google.cloud.spanner_dbapi.parser import VALUES
        from google.cloud.spanner_dbapi.parser import expect

        cases = [
            ("", "VALUES: `` does not start with VALUES"),
            (
                "VALUES(%s, %s, (%s, %s))",
                "FUNC: `\\(%s, %s\\)\\)` does not begin with `a-zA-z` nor a `_`",
            ),
            ("VALUES(%s),,", "ARGS: supposed to begin with `\\(` in `,`"),
        ]

        for text, wantException in cases:
            with self.subTest(text=text):
                self.assertRaisesRegex(
                    ProgrammingError,
                    wantException,
                    lambda: expect(text, VALUES),
                )

    def test_as_values(self):
        from google.cloud.spanner_dbapi.parser import as_values

        values = (1, 2)
        with mock.patch(
            "google.cloud.spanner_dbapi.parser.parse_values",
            return_value=values,
        ):
            self.assertEqual(as_values(None), values[1])
