from docfx_yaml import extension

import unittest
from parameterized import parameterized

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

        got1 = extension.find_unique_name(entry1.split("."), entries)
        got2 = extension.find_unique_name(entry2.split("."), entries)

        self.assertEqual(want1, ".".join(got1))
        self.assertEqual(want2, ".".join(got2))


    def test_disambiguate_toc_name(self):

        with open('tests/yaml_post.yaml', 'r') as want_file:
            yaml_want = load(want_file, Loader=Loader)
        disambiguated_names_want = {
            'google.cloud.spanner_admin_database_v1.types': 'spanner_admin_database_v1.types',
            'google.cloud.spanner_admin_instance_v1.types': 'spanner_admin_instance_v1.types',
            'google.cloud.spanner_v1.types': 'spanner_v1.types'
        }

        with open('tests/yaml_pre.yaml', 'r') as test_file:
            yaml_got = load(test_file, Loader=Loader)
        disambiguated_names_got = extension.disambiguate_toc_name(yaml_got)

        self.assertEqual(yaml_want, yaml_got)
        self.assertEqual(disambiguated_names_want, disambiguated_names_got)


    def test_disambiguate_toc_name_duplicate(self):

        with open('tests/yaml_post_duplicate.yaml', 'r') as want_file:
            yaml_want = load(want_file, Loader=Loader)
        disambiguated_names_want = {
            'google.api_core.client_info': 'client_info',
            'google.api_core.gapic_v1.client_info': 'gapic_v1.client_info'
        }

        with open('tests/yaml_pre_duplicate.yaml', 'r') as test_file:
            yaml_got = load(test_file, Loader=Loader)
        disambiguated_names_got = extension.disambiguate_toc_name(yaml_got)


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
        lines_got, xrefs = extension._resolve_reference_in_module_summary(extension.REF_PATTERN, lines_got)
        for xref in xrefs:
            xrefs_got.append(xref)
        lines_got, xrefs = extension._resolve_reference_in_module_summary(extension.REF_PATTERN_LAST, lines_got)
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
        lines_got, xrefs = extension._resolve_reference_in_module_summary(extension.REF_PATTERN, lines_got)
        for xref in xrefs:
            xrefs_got.append(xref)
        lines_got, xrefs = extension._resolve_reference_in_module_summary(extension.REF_PATTERN_LAST, lines_got)
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


    # Test for resolving square bracketed references.
    def test_reference_square_brackets(self):
        xrefs_want = [
            'google.cloud.kms.v1.KeyRing.name',
            'google.cloud.kms.v1.KeyRing',
            'google.cloud.kms.v1.ImportJob',
        ]
        summary_want = """Required.

The <xref uid="google.cloud.kms.v1.KeyRing.name">name</xref> of the <xref uid="google.cloud.kms.v1.KeyRing">KeyRing</xref> associated with the <xref uid="google.cloud.kms.v1.ImportJob">ImportJobs</xref>.
"""
        summary_want = summary_want.split("\n")

        summary = """Required.

The [name][google.cloud.kms.v1.KeyRing.name] of the [KeyRing][google.cloud.kms.v1.KeyRing] associated with the [ImportJobs][google.cloud.kms.v1.ImportJob].
"""
        summary = summary.split("\n")

        summary_got, xrefs_got = extension._resolve_reference_in_module_summary(extension.REF_PATTERN_BRACKETS, summary)

        self.assertEqual(summary_got, summary_want)
        self.assertCountEqual(xrefs_got, xrefs_want)


    # Check that other patterns throws an exception.
    def test_reference_check_error(self):
        with self.assertRaises(ValueError):
            extension._resolve_reference_in_module_summary('.*', 'not a valid ref line'.split('\n'))


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

        top_summary1_got = extension._extract_docstring_info(summary_info1_got, summary1, "")

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

        top_summary2_got = extension._extract_docstring_info(summary_info2_got, summary2, "")
        
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

        top_summary3_got = extension._extract_docstring_info(summary_info3_got, summary3, "")

        self.assertEqual(top_summary3_got, top_summary3_want)
        self.assertEqual(summary_info3_got, summary_info3_want)


    def test_extract_docstring_info_check_error(self):
        ## Test for incorrectly formmatted docstring raising error
        summary4 = """
Description of docstring which should fail. 

:returns:param:
"""
        with self.assertRaises(ValueError):
            extension._extract_docstring_info({}, summary4, "error string")

        summary5 = """
Description of malformed docstring.

Raises:
    Error that should fail: if condition `x`.
"""
        with self.assertRaises(KeyError):
            extension._extract_docstring_info({}, summary5, "malformed docstring")


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

        top_summary_got = extension._extract_docstring_info(summary_info_got, summary, "")
        # Same as the top summary from previous example, compare with that
        self.assertEqual(top_summary_got, self.top_summary1_want)
        self.assertDictEqual(summary_info_got, summary_info_want)


    def test_extract_docstring_info_no_summary(self):
        ## Test parsing docstring with no summary.
        summary =(
"""Args:
    arg1(int): simple description.
    arg2(str): simple description for `arg2`.

Returns:
    str: simple description for return value.

Raises:
    AttributeError: if `condition x`.
"""
        )
        summary_info_got = {
            'variables': {},
            'returns': [],
            'exceptions': []
        }

        top_summary_got = extension._extract_docstring_info(summary_info_got, summary, "")
        self.assertEqual(top_summary_got, "")
        self.assertDictEqual(summary_info_got, self.summary_info1_want)


    def test_find_package_group(self):
        package_group_want = "google.cloud.spanner_v1beta2"
        uid = "google.cloud.spanner_v1beta2.services.admin_database_v1.types"

        package_group_got = extension.find_package_group(uid)
        self.assertEqual(package_group_got, package_group_want)


    def test_pretty_package_name(self):
        package_name_want = "Spanner V1beta2"
        package_group = "google.cloud.spanner_v1beta2"

        package_name_got = extension.pretty_package_name(package_group)
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

        toc_yaml_got = extension.group_by_package(toc_yaml)

        self.assertCountEqual(toc_yaml_got, toc_yaml_want)


    def test_parse_docstring_summary(self):
        # Check that the summary gets parsed correctly.
        attributes_want = []
        summary_want = \
"""```python
from google.api_core.client_options import ClientOptions

from google.cloud.vision_v1 import ImageAnnotatorClient

def get_client_cert():

    # code to load client certificate and private key.

    return client_cert_bytes, client_private_key_bytes

options = ClientOptions(api_endpoint=\"foo.googleapis.com\",

    client_cert_source=get_client_cert)

client = ImageAnnotatorClient(client_options=options)
```

You can also pass a mapping object.

```ruby
from google.cloud.vision_v1 import ImageAnnotatorClient

client = ImageAnnotatorClient(

    client_options={

        \"api_endpoint\": \"foo.googleapis.com\",

        \"client_cert_source\" : get_client_cert

    })

```
"""
        summary = \
"""


.. code-block:: python

\n    from google.api_core.client_options import ClientOptions
\n    from google.cloud.vision_v1 import ImageAnnotatorClient
\n    def get_client_cert():
\n        # code to load client certificate and private key.
\n        return client_cert_bytes, client_private_key_bytes
\n    options = ClientOptions(api_endpoint=\"foo.googleapis.com\",
\n        client_cert_source=get_client_cert)
\n    client = ImageAnnotatorClient(client_options=options)


You can also pass a mapping object.


\n.. code-block:: ruby

\n    from google.cloud.vision_v1 import ImageAnnotatorClient
\n    client = ImageAnnotatorClient(
\n        client_options={
\n            \"api_endpoint\": \"foo.googleapis.com\",
\n            \"client_cert_source\" : get_client_cert
\n        })
"""
        summary_got, attributes_got = extension._parse_docstring_summary(summary)
        self.assertEqual(summary_got, summary_want)
        self.assertEqual(attributes_got, attributes_want)

        # Check that nothing much changes otherwise.
        summary = \
"""
.. literalinclude::
    note that these are not supported yet, so they will be ignored for now.

And any other documentation that the source code would have could go here.
"""
        summary_want = summary + "\n"

        summary_got, attributes_got = extension._parse_docstring_summary(summary)
        self.assertEqual(summary_got, summary_want)
        self.assertEqual(attributes_got, attributes_want)

        # Check that exception is raised if code block is not indented.
        summary = \
"""


.. code:: python

\nprint("This should throw an exception.")
\nfor i in range(10):
\n    print(i)
"""
        with self.assertRaises(ValueError):
            extension._parse_docstring_summary(summary)

        # Check that notices are processed properly.
        summary_want = \
"""<aside class="note">
<b>Note:</b>
this is a note.
</aside>
<aside class="caution">
<b>Caution:</b>
another type of notice.
</aside>
<aside class="key-term">
<b>Key Term:</b>
hyphenated term notice.
</aside>"""

        summary = \
"""
.. note::
\n    this is a note.


.. caution::
\n    another type of notice.


.. key-term::
\n    hyphenated term notice.
"""

        summary_got, attributes_got = extension._parse_docstring_summary(summary)
        self.assertEqual(summary_got, summary_want)
        self.assertEqual(attributes_got, attributes_want)

        # Check that exception is raised if block is not formatted properly.

        summary = \
"""
.. warning::
this is not a properly formatted warning.
"""
        with self.assertRaises(ValueError):
            extension._parse_docstring_summary(summary)

    def test_parse_docstring_summary_attributes(self):
        # Test parsing docstring with attributes.
        attributes_want = [
            {
                "id": "simple name",
                "description": "simple description",
                "var_type": 'str'
            }
        ]
        summary = \
"""


.. attribute:: simple name

\nsimple description

\n:type: str
"""

        summary_got, attributes_got = extension._parse_docstring_summary(summary)
        self.assertCountEqual(attributes_got, attributes_want)

        # Check multiple attributes are parsed.
        attributes_want = [
            {
                "id": "simple name",
                "description": "simple description",
                "var_type": "str"
            },
            {
                "id": "table_insert_request",
                "description": "Table insert request.",
                "var_type": "google.cloud.bigquery_logging_v1.types.TableInsertRequest"
            }
        ]

        summary = \
"""


.. attribute:: simple name

\nsimple description

\n:type: str


.. attribute:: table_insert_request

\nTable insert request.

\n:type: google.cloud.bigquery_logging_v1.types.TableInsertRequest
"""
        summary_got, attributes_got = extension._parse_docstring_summary(summary)

        self.assertCountEqual(attributes_got, attributes_want)
        for attribute_got, attribute_want in zip(attributes_got, attributes_want):
            self.assertDictEqual(attribute_got, attribute_want)

        # Check only attributes in valid format gets parsed.
        attributes_want = [
            {
                "id": "proper name",
                "description": "proper description.",
                "var_type": "str"
            }
        ]
        summary = \
"""


.. attribute:: table_insert_request

\nTable insert request.

\ntype: google.cloud.bigquery_logging_v1.types.TableInsertRequest


.. attribute:: proper name

\nproper description.

\n:type: str
"""
        summary_got, attributes_got = extension._parse_docstring_summary(summary)

        # Check that we are returned only one item.
        self.assertCountEqual(attributes_got, attributes_want)
        for attribute_got, attribute_want in zip(attributes_got, attributes_want):
            self.assertDictEqual(attribute_got, attribute_want)


    def test_merge_markdown_and_package_toc(self):
        known_uids = {'acl','batch','blob','client','constants','fileio','hmac_key','notification','retry'}
        markdown_pages = {
            'storage': [
                {'name': 'FileIO', 'href': 'fileio.md'},
                {'name': 'Retry', 'href': 'retry.md'},
                {'name': 'Notification', 'href': 'notification.md'},
                {'name': 'HMAC Key Metadata', 'href': 'hmac_key.md'},
                {'name': 'Batches', 'href': 'batch.md'},
                {'name': 'Constants', 'href': 'constants.md'},
                {'name': 'Storage Client', 'href': 'client.md'},
                {'name': 'Blobs / Objects', 'href': 'blobs.md'}
            ],
            'acl': [
                {'name': 'ACL', 'href': 'acl.md'},
                {'name': 'ACL guide', 'href': 'acl_guide.md'}
            ],
            '/': [
                {'name': 'Overview', 'href': 'index.md'},
                {'name': 'Changelog', 'href': 'changelog.md'}
            ],
        }
        pkg_toc_yaml = [
            {'name': 'Storage',
                'items': [
                    {'name': 'acl', 'uid': 'google.cloud.storage.acl', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.acl'}]},
                    {'name': 'batch', 'uid': 'google.cloud.storage.batch', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.batch'}]},
                    {'name': 'blob', 'uid': 'google.cloud.storage.blob', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.blob'}]},
                    {'name': 'bucket', 'uid': 'google.cloud.storage.bucket', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.bucket'}]},
                    {'name': 'client', 'uid': 'google.cloud.storage.client', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.client'}]},
                    {'name': 'constants', 'uid': 'google.cloud.storage.constants'},
                    {'name': 'fileio', 'uid': 'google.cloud.storage.fileio', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.fileio'}]},
                    {'name': 'hmac_key', 'uid': 'google.cloud.storage.hmac_key', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.hmac_key'}]},
                    {'name': 'notification', 'uid': 'google.cloud.storage.notification', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.notification'}]},
                    {'name': 'retry', 'uid': 'google.cloud.storage.retry', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.retry'}]},
                ]
             },
        ]

        added_pages, merged_pkg_toc_yaml = extension.merge_markdown_and_package_toc(
            pkg_toc_yaml, markdown_pages, known_uids)

        expected_added_pages = {'index.md', 'changelog.md', 'blobs.md', 'acl_guide.md'}
        expected_merged_pkg_toc_yaml = [
            {'name': 'Overview', 'href': 'index.md'},
            {'name': 'Changelog', 'href': 'changelog.md'},
            {'name': 'Storage',
                'items': [
                    {'name': 'Blobs / Objects', 'href': 'blobs.md'},
                    {'name': 'acl', 'uid': 'google.cloud.storage.acl', 'items': [
                        {'name': 'ACL guide', 'href': 'acl_guide.md'},
                        {'name': 'Overview', 'uid': 'google.cloud.storage.acl'},
                    ]},
                    {'name': 'batch', 'uid': 'google.cloud.storage.batch', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.batch'}]},
                    {'name': 'blob', 'uid': 'google.cloud.storage.blob', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.blob'}]},
                    {'name': 'bucket', 'uid': 'google.cloud.storage.bucket', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.bucket'}]},
                    {'name': 'client', 'uid': 'google.cloud.storage.client', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.client'}]},
                    {'name': 'constants', 'uid': 'google.cloud.storage.constants'},
                    {'name': 'fileio', 'uid': 'google.cloud.storage.fileio', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.fileio'}]},
                    {'name': 'hmac_key', 'uid': 'google.cloud.storage.hmac_key', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.hmac_key'}]},
                    {'name': 'notification', 'uid': 'google.cloud.storage.notification', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.notification'}]},
                    {'name': 'retry', 'uid': 'google.cloud.storage.retry', 'items': [{'name': 'Overview', 'uid': 'google.cloud.storage.retry'}]},
                ]
             },
        ]
        self.assertSetEqual(added_pages, expected_added_pages)
        self.assertListEqual(merged_pkg_toc_yaml, expected_merged_pkg_toc_yaml)


if __name__ == '__main__':
    unittest.main()
