from docfx_yaml.extension import find_unique_name
from docfx_yaml.extension import disambiguate_toc_name
from docfx_yaml.extension import _resolve_reference_in_module_summary
from docfx_yaml.extension import REF_PATTERN
from docfx_yaml.extension import REF_PATTERN_LAST
from docfx_yaml.extension import _extract_docstring_info
from docfx_yaml.extension import find_package_group
from docfx_yaml.extension import pretty_package_name
from docfx_yaml.extension import group_by_package
from docfx_yaml.extension import extract_header_from_markdown

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
        disambiguated_names_want = {
            'google.cloud.spanner_admin_database_v1.types': 'spanner_admin_database_v1.types',
            'google.cloud.spanner_admin_instance_v1.types': 'spanner_admin_instance_v1.types', 
            'google.cloud.spanner_v1.types': 'spanner_v1.types'
        }

        test_file = open('tests/yaml_pre.yaml', 'r')
        yaml_got = load(test_file, Loader=Loader)
        disambiguated_names_got = disambiguate_toc_name(yaml_got)

        want_file.close()
        test_file.close()

        self.assertEqual(yaml_want, yaml_got)
        self.assertEqual(disambiguated_names_want, disambiguated_names_got)


    def test_disambiguate_toc_name_duplicate(self):

        want_file = open('tests/yaml_post_duplicate.yaml', 'r')
        yaml_want = load(want_file, Loader=Loader)
        disambiguated_names_want = {
            'google.api_core.client_info': 'client_info', 
            'google.api_core.gapic_v1.client_info': 'gapic_v1.client_info'
        }
        
        test_file = open('tests/yaml_pre_duplicate.yaml', 'r')
        yaml_got = load(test_file, Loader=Loader)
        disambiguated_names_got = disambiguate_toc_name(yaml_got)

        want_file.close()
        test_file.close()

        self.assertEqual(yaml_want, yaml_got)
        self.assertEqual(disambiguated_names_want, disambiguated_names_got)


    def test_reference_in_summary(self):
        lines_got = """
If a ``stream`` is attached to this download, then the downloaded
resource will be written to the stream.

Args:
    transport (~google.cloud.requests.Session): A ``requests`` object which can
        make authenticated requests.

    timeout (Optional[Union[float, Tuple[float, float]]]):
        The number of seconds to wait for the server response.
        Depending on the retry strategy, a request may be repeated
        several times using the same timeout each time.

        Can also be passed as a tuple (connect_timeout, read_timeout).
        See :meth:`google.cloud.requests.Session.request` documentation for details.

Returns:
    ~google.cloud.requests.Response: The HTTP response returned by ``transport``.

Raises:
    ~google.cloud.resumable_media.common.DataCorruption: If the download's
        checksum doesn't agree with server-computed checksum.
    ValueError: If the current :class:`Download` has already
        finished.
"""
        lines_got = lines_got.split("\n")
        xrefs_got = []
        # Resolve over different regular expressions for different types of reference patterns.
        lines_got, xrefs = _resolve_reference_in_module_summary(REF_PATTERN, lines_got)
        for xref in xrefs:
            xrefs_got.append(xref)
        lines_got, xrefs = _resolve_reference_in_module_summary(REF_PATTERN_LAST, lines_got)
        for xref in xrefs:
            xrefs_got.append(xref)

        lines_want = """
If a ``stream`` is attached to this download, then the downloaded
resource will be written to the stream.

Args:
    transport (<xref uid="google.cloud.requests.Session">Session</xref>): A ``requests`` object which can
        make authenticated requests.

    timeout (Optional[Union[float, Tuple[float, float]]]):
        The number of seconds to wait for the server response.
        Depending on the retry strategy, a request may be repeated
        several times using the same timeout each time.

        Can also be passed as a tuple (connect_timeout, read_timeout).
        See <xref uid="google.cloud.requests.Session.request">request</xref> documentation for details.

Returns:
    <xref uid="google.cloud.requests.Response">Response</xref>: The HTTP response returned by ``transport``.

Raises:
    <xref uid="google.cloud.resumable_media.common.DataCorruption">DataCorruption</xref>: If the download's
        checksum doesn't agree with server-computed checksum.
    ValueError: If the current `Download` has already
        finished.
"""
        lines_want = lines_want.split("\n")
        xrefs_want = [
          "google.cloud.requests.Session",
          "google.cloud.requests.Session.request",
          "google.cloud.requests.Response",
          "google.cloud.resumable_media.common.DataCorruption"
        ]

        self.assertEqual(lines_got, lines_want)
        self.assertCountEqual(xrefs_got, xrefs_want)
        # assertCountEqual is a misleading name but checks that two lists contain
        # same items regardless of order, as long as items in list are sortable.


    # Test for added xref coverage and third party xrefs staying as-is
    def test_reference_in_summary_more_xrefs(self):
        lines_got = """
If a ~dateutil.time.stream() is attached to this download, then the downloaded
resource will be written to the stream.

Args:
    transport (~google.cloud.requests.Session()): A ``requests`` object which can
        make authenticated requests.

    timeout (Optional[Union[float, Tuple[float, float]]]):
        The number of seconds to wait for the server response.
        Depending on the retry strategy, a request may be repeated
        several times using the same timeout each time.

        Can also be passed as a :func:`~google.cloud.requests.tuple()` (connect_timeout, read_timeout).
        See :meth:`google.cloud.requests.Session.request()` documentation for details.
"""
        lines_got = lines_got.split("\n")
        xrefs_got = []
        # Resolve over different regular expressions for different types of reference patterns.
        lines_got, xrefs = _resolve_reference_in_module_summary(REF_PATTERN, lines_got)
        for xref in xrefs:
            xrefs_got.append(xref)
        lines_got, xrefs = _resolve_reference_in_module_summary(REF_PATTERN_LAST, lines_got)
        for xref in xrefs:
            xrefs_got.append(xref)

        lines_want = """
If a `dateutil.time.stream()` is attached to this download, then the downloaded
resource will be written to the stream.

Args:
    transport (<xref uid="google.cloud.requests.Session">Session()</xref>): A ``requests`` object which can
        make authenticated requests.

    timeout (Optional[Union[float, Tuple[float, float]]]):
        The number of seconds to wait for the server response.
        Depending on the retry strategy, a request may be repeated
        several times using the same timeout each time.

        Can also be passed as a <xref uid="google.cloud.requests.tuple">tuple()</xref> (connect_timeout, read_timeout).
        See <xref uid="google.cloud.requests.Session.request">request()</xref> documentation for details.
"""
        lines_want = lines_want.split("\n")
        xrefs_want = [
          "google.cloud.requests.Session",
          "google.cloud.requests.tuple",
          "google.cloud.requests.Session.request"
        ]

        self.assertEqual(lines_got, lines_want)
        self.assertCountEqual(xrefs_got, xrefs_want)
        # assertCountEqual is a misleading name but checks that two lists contain
        # same items regardless of order, as long as items in list are sortable.


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

        summary5 = """
Description of malformed docstring.

Raises:
    Error that should fail: if condition `x`.
"""
        with self.assertRaises(KeyError):
            _extract_docstring_info({}, summary5, "malformed docstring")


    def test_extract_docstring_info_with_xref(self):
        ## Test with xref included in the summary, ensure they're processed as-is
        summary_info_want = {
            'variables': {
                'arg1': {
                    'var_type': '<xref uid="google.spanner_v1.type.Type">Type</xref>',
                    'description': 'simple description.'
                },
                'arg2': {
                    'var_type': '~google.spanner_v1.type.dict',
                    'description': 'simple description for `arg2`.'
                }
            },
            'returns': [
                {
                    'var_type': '<xref uid="Pair">Pair</xref>', 
                    'description': 'simple description for return value.'
                }
            ],
            'exceptions': [
                {
                    'var_type': '<xref uid="SpannerException">SpannerException</xref>', 
                    'description': 'if `condition x`.'
                }
            ]
        }

        summary = """
Simple test for docstring.

:type arg1: <xref uid="google.spanner_v1.type.Type">Type</xref>
:param arg1: simple description.
:param arg2: simple description for `arg2`.
:type arg2: ~google.spanner_v1.type.dict

:rtype: <xref uid="Pair">Pair</xref>
:returns: simple description for return value.

:raises <xref uid="SpannerException">SpannerException</xref>: if `condition x`. 
"""

        summary_info_got = {
            'variables': {},
            'returns': [],
            'exceptions': []
        }

        top_summary_got = _extract_docstring_info(summary_info_got, summary, "")
        # Same as the top summary from previous example, compare with that
        self.assertEqual(top_summary_got, self.top_summary1_want)
        self.assertDictEqual(summary_info_got, summary_info_want)


    def test_find_package_group(self):
        package_group_want = "google.cloud.spanner_v1beta2"
        uid = "google.cloud.spanner_v1beta2.services.admin_database_v1.types"

        package_group_got = find_package_group(uid)
        self.assertEqual(package_group_got, package_group_want)


    def test_pretty_package_name(self):
        package_name_want = "Spanner V1beta2"
        package_group = "google.cloud.spanner_v1beta2"

        package_name_got = pretty_package_name(package_group)
        self.assertEqual(package_name_got, package_name_want)


    def test_group_by_package(self):
        toc_yaml_want = [
            {
                "name": "Spanner Admin Database V1",
                "uidname":"google.cloud.spanner_admin_database_v1",
                "items": [
                    {
                      "name":"database_admin",
                      "uidname":"google.cloud.spanner_admin_database_v1.services.database_admin",
                      "items":[
                          {
                            "name":"Overview",
                            "uidname":"google.cloud.spanner_admin_database_v1.services.database_admin",
                            "uid":"google.cloud.spanner_admin_database_v1.services.database_admin"
                          },
                          {
                            "name":"ListBackupOperationsAsyncPager",
                            "uidname":"google.cloud.spanner_admin_database_v1.services.database_admin.pagers.ListBackupOperationsAsyncPager",
                            "uid":"google.cloud.spanner_admin_database_v1.services.database_admin.pagers.ListBackupOperationsAsyncPager"
                          }
                      ]
                    },
                    {
                      "name":"spanner_admin_database_v1.types",
                      "uidname":"google.cloud.spanner_admin_database_v1.types",
                      "items":[
                          {
                            "name":"Overview",
                            "uidname":"google.cloud.spanner_admin_database_v1.types",
                            "uid":"google.cloud.spanner_admin_database_v1.types"
                          },
                          {
                            "name":"BackupInfo",
                            "uidname":"google.cloud.spanner_admin_database_v1.types.BackupInfo",
                            "uid":"google.cloud.spanner_admin_database_v1.types.BackupInfo"
                          }
                      ]
                    },
                ]
            },
            {
                "name": "Spanner V1",
                "uidname":"google.cloud.spanner_v1",
                "items": [
                    {
                      "name":"pool",
                      "uidname":"google.cloud.spanner_v1.pool",
                      "items":[
                          {
                            "name":"Overview",
                            "uidname":"google.cloud.spanner_v1.pool",
                            "uid":"google.cloud.spanner_v1.pool"
                          },
                          {
                            "name":"AbstractSessionPool",
                            "uidname":"google.cloud.spanner_v1.pool.AbstractSessionPool",
                            "uid":"google.cloud.spanner_v1.pool.AbstractSessionPool"
                          }
                      ]
                    }
                ]
            }
        ]

        toc_yaml = [
            {
              "name":"database_admin",
              "uidname":"google.cloud.spanner_admin_database_v1.services.database_admin",
              "items":[
                  {
                    "name":"Overview",
                    "uidname":"google.cloud.spanner_admin_database_v1.services.database_admin",
                    "uid":"google.cloud.spanner_admin_database_v1.services.database_admin"
                  },
                  {
                    "name":"ListBackupOperationsAsyncPager",
                    "uidname":"google.cloud.spanner_admin_database_v1.services.database_admin.pagers.ListBackupOperationsAsyncPager",
                    "uid":"google.cloud.spanner_admin_database_v1.services.database_admin.pagers.ListBackupOperationsAsyncPager"
                  }
              ]
            },
            {
              "name":"spanner_admin_database_v1.types",
              "uidname":"google.cloud.spanner_admin_database_v1.types",
              "items":[
                  {
                    "name":"Overview",
                    "uidname":"google.cloud.spanner_admin_database_v1.types",
                    "uid":"google.cloud.spanner_admin_database_v1.types"
                  },
                  {
                    "name":"BackupInfo",
                    "uidname":"google.cloud.spanner_admin_database_v1.types.BackupInfo",
                    "uid":"google.cloud.spanner_admin_database_v1.types.BackupInfo"
                  }
              ]
            },
            {
              "name":"pool",
              "uidname":"google.cloud.spanner_v1.pool",
              "items":[
                  {
                    "name":"Overview",
                    "uidname":"google.cloud.spanner_v1.pool",
                    "uid":"google.cloud.spanner_v1.pool"
                  },
                  {
                    "name":"AbstractSessionPool",
                    "uidname":"google.cloud.spanner_v1.pool.AbstractSessionPool",
                    "uid":"google.cloud.spanner_v1.pool.AbstractSessionPool"
                  }
              ]
            }
        ]

        toc_yaml_got = group_by_package(toc_yaml)

        self.assertCountEqual(toc_yaml_got, toc_yaml_want)


    def test_extract_header_from_markdown(self):
        # Check the header for a normal markdown file.
        header_line_want = "Test header for a simple markdown file."

        mdfile = open('tests/markdown_example.md', 'r')
        header_line_got = extract_header_from_markdown(mdfile)

        self.assertEqual(header_line_got, header_line_want)
        mdfile.close()

        # The header should be the same even with the license header.
        header_line_with_license_want = header_line_want

        mdfile = open('tests/markdown_example_header.md', 'r')
        header_line_with_license_got = extract_header_from_markdown(mdfile)

        self.assertEqual(header_line_with_license_got, header_line_with_license_want)
        mdfile.close()


    def test_extract_header_from_markdown_check_error(self):
        # Check an exception is thrown for markdown files that's not well
        # formatted.
        mdfile = open('tests/markdown_example_bad.md', 'r')
        with self.assertRaises(ValueError):
            header_line = extract_header_from_markdown(mdfile)

        mdfile.close()

        mdfile = open('tests/markdown_example_noheader.md', 'r')
        with self.assertRaises(ValueError):
            header_line = extract_header_from_markdown(mdfile)

        mdfile.close()



if __name__ == '__main__':
    unittest.main()
