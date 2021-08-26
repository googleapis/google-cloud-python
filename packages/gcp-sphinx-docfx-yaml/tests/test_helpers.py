from docfx_yaml.extension import extract_keyword
from docfx_yaml.extension import indent_code_left


import unittest

from yaml import load, Loader

class TestGenerate(unittest.TestCase):
    def test_indent_code_left(self):
        # Check that the code indents to left based on first line.
        code_want = \
"""def foo():
    print('test function for indent')
    return ('left-indented-code')
"""

        code = \
"""    def foo():
        print('test function for indent')
        return ('left-indented-code')
"""
        code = indent_code_left(code)
        self.assertEqual(code, code_want)

        # Check that if there's no whitespace, it does not indent
        code_want = \
"""
print('test function for no impact indent')
for i in range(10):
    print(i)
    if i%5 == 0:
        i += 1
    else:
        continue
"""

        code_got = indent_code_left(code_want)
        # Confirm that nothing changes.
        self.assertEqual(code_got, code_want)


    def test_extract_keyword(self):
        # Check that keyword properly gets processed.
        keyword_want = "attribute"

        keyword_line = ".. attribute:: "
        keyword_got = extract_keyword(keyword_line)

        self.assertEqual(keyword_got, keyword_want)

        # Check that keyword is not retrieved for bad formats.
        keyword_line = ".. attribute:"

        # Should raise an exception..
        with self.assertRaises(ValueError):
            keyword_got = extract_keyword(keyword_line)


if __name__ == '__main__':
    unittest.main()
