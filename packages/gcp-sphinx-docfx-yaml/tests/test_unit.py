from docfx_yaml.extension import find_unique_name
from docfx_yaml.extension import disambiguate_toc_name
from docfx_yaml.extension import _extract_docstring_info

import unittest

from yaml import load, Loader

class TestGenerate(unittest.TestCase):
    def test_find_unique_name(self):

        entries = {}
        
        # Disambiguate with unique entries.
        entry1 = "google.cloud.aiplatform.v1.schema.predict.instance_v1.types"
        entry2 = "google.cloud.aiplatform.v1beta2.schema.predict.instance_v1.types"
        want1 = "v1.types"
        want2 = "v1beta2.types"

        for entry in [entry1, entry2]:
            for word in entry.split("."):
                if word not in entries:
                    entries[word] = 1
                else:
                    entries[word] += 1

        got1 = find_unique_name(entry1.split("."), entries)
        got2 = find_unique_name(entry2.split("."), entries)

        self.assertEqual(want1, ".".join(got1))
        self.assertEqual(want2, ".".join(got2))


    def test_disambiguate_toc_name(self):

        want_file = open('tests/yaml_post.yaml', 'r')
        yaml_want = load(want_file, Loader=Loader)

        test_file = open('tests/yaml_pre.yaml', 'r')
        yaml_got = load(test_file, Loader=Loader)
        disambiguate_toc_name(yaml_got)

        want_file.close()
        test_file.close()

        self.assertEqual(yaml_want, yaml_got)

    # Variables used for testing _extract_docstring_info
    top_summary1_want = "\nSimple test for docstring.\n\n"
    summary_info1_want = {
        'variables': {
            'arg1': {
                'var_type': 'int',
                'description': 'simple description.'
            },
            'arg2': {
                'var_type': 'str',
                'description': 'simple description for `arg2`.'
            }
        },
        'returns': [
            {
                'var_type': 'str', 
                'description': 'simple description for return value.'
            }
        ],
        'exceptions': [
            {
                'var_type': 'AttributeError', 
                'description': 'if `condition x`.'
            }
        ]
    }
    

    def test_extract_docstring_info_normal_input(self):

        ## Test for normal input
        summary_info1_got = {
            'variables': {},
            'returns': [],
            'exceptions': []
        }

        summary1 = """
Simple test for docstring.

Args: 
    arg1(int): simple description.
    arg2(str): simple description for `arg2`.

Returns:
    str: simple description for return value.

Raises:
    AttributeError: if `condition x`.
"""

        top_summary1_got = _extract_docstring_info(summary_info1_got, summary1, "")

        self.assertEqual(top_summary1_got, self.top_summary1_want)
        self.assertEqual(summary_info1_got, self.summary_info1_want)


    def test_extract_docstring_info_mixed_format(self):
        ## Test for input coming in mixed format.
        summary2 = """
Simple test for docstring.

:type arg1: int
:param arg1: simple description.
:param arg2: simple description for `arg2`.
:type arg2: str

:rtype: str
:returns: simple description for return value.

:raises AttributeError: if `condition x`. 
"""

        summary_info2_got = {
            'variables': {},
            'returns': [],
            'exceptions': []
        }

        top_summary2_got = _extract_docstring_info(summary_info2_got, summary2, "")
        
        # Output should be same as test 1 with normal input.
        self.assertEqual(top_summary2_got, self.top_summary1_want)
        self.assertEqual(summary_info2_got, self.summary_info1_want)

        
    def test_extract_docstring_info_check_parser(self):
        ## Test for parser to correctly scan docstring tokens and not custom fields
        summary_info3_want = {
            'variables': {},
            'returns': [],
            'exceptions': []
        }

        summary3 = """
Union[int, None]: Expiration time in milliseconds for a partition.

If :attr:`partition_expiration` is set and <xref:type_> is
not set, :attr:`type_` will default to
:attr:`~google.cloud.bigquery.table.TimePartitioningType.DAY`.
It could return :param: with :returns as well.
"""

        summary_info3_got = {
            'variables': {},
            'returns': [],
            'exceptions': []
        }

        # Nothing should change
        top_summary3_want = summary3

        top_summary3_got = _extract_docstring_info(summary_info3_got, summary3, "")

        self.assertEqual(top_summary3_got, top_summary3_want)
        self.assertEqual(summary_info3_got, summary_info3_want)

    def test_extract_docstring_info_check_error(self):
        ## Test for incorrectly formmatted docstring raising error
        summary4 = """
Description of docstring which should fail. 

:returns:param:
"""
        with self.assertRaises(ValueError):
            _extract_docstring_info({}, summary4, "error string")

if __name__ == '__main__':
    unittest.main()
