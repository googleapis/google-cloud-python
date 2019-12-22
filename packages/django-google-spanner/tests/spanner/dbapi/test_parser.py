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

from unittest import TestCase

from spanner.dbapi.exceptions import ProgrammingError
from spanner.dbapi.parser import (
    ARGS, FUNC, TERMINAL, VALUES, a_args, expect, func, pyfmt_str, values,
)


class ParserTests(TestCase):
    def test_terminal(self):
        cases = [
            ('%s', '', pyfmt_str),
            ('  %s', '', pyfmt_str),
            ('  %s   ', '', pyfmt_str),
        ]

        for text, want_unconsumed, want_parsed in cases:
            with self.subTest(text=text):
                got_unconsumed, got_parsed = expect(text, TERMINAL)
                self.assertEqual(got_parsed, want_parsed)
                self.assertEqual(got_unconsumed, want_unconsumed)

    def test_terminal_fail(self):
        cases = [
            ('', 'TERMINAL: `` is not %s'),
            ('fdp', 'TERMINAL: `fdp` is not %s'),
            ('%%s', 'TERMINAL: `%%s` is not %s'),
            ('%sa', 'TERMINAL: `%sa` is not %s'),
        ]

        for text, wantException in cases:
            with self.subTest(text=text):
                self.assertRaisesRegex(ProgrammingError, wantException, lambda: expect(text, TERMINAL))

    def test_func(self):
        cases = [
            ('_91())', ')', func('_91', a_args([]))),
            ('_a()', '', func('_a', a_args([]))),
            ('___()', '', func('___', a_args([]))),
            ('abc()', '', func('abc', a_args([]))),
            (
                'AF112(%s, LOWER(%s, %s), rand(%s, %s, TAN(%s, %s)))',
                '',
                func('AF112', a_args([
                    pyfmt_str,
                    func('LOWER', a_args([pyfmt_str, pyfmt_str])),
                    func('rand', a_args([
                        pyfmt_str, pyfmt_str, func('TAN', a_args([pyfmt_str, pyfmt_str])),
                    ])),
                ])),
            ),
        ]

        for text, want_unconsumed, want_parsed in cases:
            with self.subTest(text=text):
                got_unconsumed, got_parsed = expect(text, FUNC)
                self.assertEqual(got_parsed, want_parsed)
                self.assertEqual(got_unconsumed, want_unconsumed)

    def test_func_fail(self):
        cases = [
            ('', 'FUNC: `` does not begin with `a-zA-z` nor a `_`'),
            ('91', 'FUNC: `91` does not begin with `a-zA-z` nor a `_`'),
            ('_91', 'supposed to begin with `\\(`'),
            ('_91(', 'supposed to end with `\\)`'),
            ('_.()', 'supposed to begin with `\\(`'),
            ('_a.b()', 'supposed to begin with `\\(`'),
        ]

        for text, wantException in cases:
            with self.subTest(text=text):
                self.assertRaisesRegex(ProgrammingError, wantException, lambda: expect(text, FUNC))

    def test_a_args(self):
        cases = [
            ('()', '', a_args([])),
            ('(%s)', '', a_args([pyfmt_str])),
            ('(%s,)', '', a_args([pyfmt_str])),
            ('(%s),', ',', a_args([pyfmt_str])),
            (
                '(%s,%s, f1(%s, %s))', '', a_args([
                    pyfmt_str, pyfmt_str, func('f1', a_args([pyfmt_str, pyfmt_str])),
                ]),
            ),
        ]

        for text, want_unconsumed, want_parsed in cases:
            with self.subTest(text=text):
                got_unconsumed, got_parsed = expect(text, ARGS)
                self.assertEqual(got_parsed, want_parsed)
                self.assertEqual(got_unconsumed, want_unconsumed)

    def test_a_args_fail(self):
        cases = [
            ('', 'ARGS: supposed to begin with `\\(`'),
            ('(',  'ARGS: supposed to end with `\\)`'),
            (')',  'ARGS: supposed to begin with `\\(`'),
            ('(%s,%s, f1(%s, %s), %s', 'ARGS: supposed to end with `\\)`'),
        ]

        for text, wantException in cases:
            with self.subTest(text=text):
                self.assertRaisesRegex(ProgrammingError, wantException, lambda: expect(text, ARGS))

    def test_expect_values(self):
        cases = [
            ('VALUES ()', '', values([a_args([])])),
            ('VALUES', '', values([])),
            ('VALUES(%s)', '', values([a_args([pyfmt_str])])),
            ('    VALUES    (%s)    ', '', values([a_args([pyfmt_str])])),
            ('VALUES(%s, %s)', '', values([a_args([pyfmt_str, pyfmt_str])])),
            (
                'VALUES(%s, %s, LOWER(%s, %s))', '',
                values([
                    a_args([
                        pyfmt_str,
                        pyfmt_str,
                        func('LOWER', a_args([pyfmt_str, pyfmt_str])),
                    ]),
                ]),
            ),
            (
                'VALUES (UPPER(%s)), (%s)',
                '',
                values([
                    a_args([
                        func('UPPER', a_args([pyfmt_str])),
                    ]),
                    a_args([
                        pyfmt_str,
                    ]),
                ]),
            ),
        ]

        for text, want_unconsumed, want_parsed in cases:
            with self.subTest(text=text):
                got_unconsumed, got_parsed = expect(text, VALUES)
                self.assertEqual(got_parsed, want_parsed)
                self.assertEqual(got_unconsumed, want_unconsumed)

    def test_expect_values_fail(self):
        cases = [
            ('', 'VALUES: `` does not start with VALUES'),
            (
                'VALUES(%s, %s, (%s, %s))',
                'FUNC: `\\(%s, %s\\)\\)` does not begin with `a-zA-z` nor a `_`',
            ),
            ('VALUES(%s),,', 'ARGS: supposed to begin with `\\(` in `,`'),
        ]

        for text, wantException in cases:
            with self.subTest(text=text):
                self.assertRaisesRegex(ProgrammingError, wantException, lambda: expect(text, VALUES))
