from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import bytes
from builtins import int
from builtins import object
from builtins import str
from past.builtins import basestring
import bigquery.exceptions as exc
import collections


class ParamEscaper(object):
    """ParamEscaper
    https://github.com/dropbox/PyHive/blob/master/pyhive/common.py
    """

    def escape_args(self, parameters):
        if isinstance(parameters, dict):
            return {k: self.escape_item(v) for k, v in parameters.items()}
        elif isinstance(parameters, (list, tuple)):
            return tuple(self.escape_item(x) for x in parameters)
        else:
            raise exc.ProgrammingError("Unsupported param format: {}".format(parameters))

    def escape_number(self, item):
        return item

    def escape_string(self, item):
        # Need to decode UTF-8 because of old sqlalchemy.
        # Newer SQLAlchemy checks dialect.supports_unicode_binds before encoding Unicode strings
        # as byte strings. The old version always encodes Unicode as byte strings, which breaks
        # string formatting here.
        if isinstance(item, bytes):
            item = item.decode('utf-8')
        # This is good enough when backslashes are literal, newlines are just followed, and the way
        # to escape a single quote is to put two single quotes.
        # (i.e. only special character is single quote)
        return "'{}'".format(item.replace("'", "''"))

    def escape_sequence(self, item):
        l = map(str, map(self.escape_item, item))
        return '(' + ','.join(l) + ')'

    def escape_item(self, item):
        if item is None:
            return 'NULL'
        elif isinstance(item, (int, float)):
            return self.escape_number(item)
        elif isinstance(item, basestring):
            return self.escape_string(item)
        elif isinstance(item, collections.Iterable):
            return self.escape_sequence(item)
        else:
            raise exc.ProgrammingError("Unsupported object {}".format(item))