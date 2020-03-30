# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

"""
Grammar for parsing VALUES:
    VALUES      := `VALUES(` + ARGS + `)`
    ARGS        := [EXPR,]*EXPR
    EXPR        := TERMINAL / FUNC
    TERMINAL    := `%s`
    FUNC        := alphanum + `(` + ARGS + `)`
    alphanum    := (a-zA-Z_)[0-9a-ZA-Z_]*

thus given:
    statement: 'VALUES (%s, %s), (%s, LOWER(UPPER(%s)))   , (%s)'
    It'll parse:
        VALUES
            |- ARGS
                |- (TERMINAL, TERMINAL)
                |- (TERMINAL, FUNC
                                |- FUNC
                                    |- (TERMINAL)
                |- (TERMINAL)
"""

from .exceptions import ProgrammingError

ARGS = 'ARGS'
EXPR = 'EXPR'
FUNC = 'FUNC'
TERMINAL = 'TERMINAL'
VALUES = 'VALUES'


class func:
    def __init__(self, func_name, args):
        self.name = func_name
        self.args = args

    def __str__(self):
        return '%s%s' % (self.name, self.args)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.name != other.name:
            return False
        if not isinstance(other.args, type(self.args)):
            return False
        if len(self.args) != len(other.args):
            return False
        return self.args == other.args

    def __len__(self):
        return len(self.args)


class terminal(str):
    """
    terminal represents the unit symbol that can be part of a SQL values clause.
    """
    pass


class a_args:
    def __init__(self, argv):
        self.argv = argv

    def __str__(self):
        return '(' + ', '.join([str(arg) for arg in self.argv]) + ')'

    def __repr__(self):
        return self.__str__()

    def has_expr(self):
        return any([token for token in self.argv if not isinstance(token, terminal)])

    def __len__(self):
        return len(self.argv)

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        s_len, o_len = len(self), len(other)
        if s_len != o_len:
            return False

        for i, s_item in enumerate(self):
            o_item = other[i]
            if s_item != o_item:
                return False

        return True

    def __getitem__(self, index):
        return self.argv[index]

    def homogenous(self):
        """
        Return True if all the arguments are pyformat
        args and have the same number of arguments.
        """
        if not self.all_have_same_argc():
            return False

        for arg in self.argv:
            if isinstance(arg, terminal):
                continue
            elif isinstance(arg, a_args):
                if not arg.homogenous():
                    return False
            else:
                return False
        return True

    def all_have_same_argc(self):
        """
        Return False if all the arguments have the same length.
        """
        if len(self) == 0:
            return True

        arg0_len = len(self.argv[0])
        for arg in self.argv[1:]:
            if len(arg) != arg0_len:
                return False

        return True


class values(a_args):
    def __str__(self):
        return 'VALUES%s' % super().__str__()


def parse_values(stmt):
    return expect(stmt, VALUES)


pyfmt_str = terminal('%s')


def expect(word, token):
    word = word.strip(' ')
    if token == VALUES:
        if not word.startswith('VALUES'):
            raise ProgrammingError('VALUES: `%s` does not start with VALUES' % word)
        word = word[len('VALUES'):].strip(' ')

        all_args = []
        while word:
            word = word.strip(' ')

            word, arg = expect(word, ARGS)
            all_args.append(arg)

            word = word.strip(' ')
            if word == '':
                break
            elif word[0] != ',':
                raise ProgrammingError('VALUES: expected `,` got %s in %s' % (word[0], word))
            else:
                word = word[1:]
        return '', values(all_args)

    elif token == TERMINAL:
        word = word.strip(' ')
        if word != '%s':
            raise ProgrammingError('TERMINAL: `%s` is not %%s' % word)
        return '', pyfmt_str

    elif token == FUNC:
        begins_with_letter = word and (word[0].isalpha() or word[0] == '_')
        if not begins_with_letter:
            raise ProgrammingError('FUNC: `%s` does not begin with `a-zA-z` nor a `_`' % word)

        rest = word[1:]
        end = 0
        for ch in rest:
            if ch.isalnum() or ch == '_':
                end += 1
            else:
                break

        func_name, rest = word[:end+1], word[end+1:].strip(' ')

        word, args = expect(rest, ARGS)
        return word, func(func_name, args)

    elif token == ARGS:
        # The form should be:
        #   (%s)
        #   (%s, %s...)
        #   (FUNC, %s...)
        #   (%s, %s...)
        if not (word and word[0] == '('):
            raise ProgrammingError('ARGS: supposed to begin with `(` in `%s`' % (word))

        word = word[1:]

        terms = []
        while True:
            word = word.strip(' ')
            if not word:
                break
            elif word == '%s':
                terms.append(pyfmt_str)
                word = ''
            elif word.startswith(')'):
                break
            elif not word.startswith('%s'):
                word, parsed = expect(word, FUNC)
                terms.append(parsed)
            else:
                terms.append(pyfmt_str)
                word = word[2:].strip(' ')

            if word and word[0] == ',':
                word = word[1:]

        if (not word) or word[0] != ')':
            raise ProgrammingError('ARGS: supposed to end with `)` in `%s`' % (word))

        word = word[1:]
        return word, a_args(terms)

    elif token == EXPR:
        if word == '%s':
            # Terminal symbol.
            return '', (pyfmt_str)

        # Otherwise we expect a function.
        return expect(word, FUNC)

    else:
        raise ProgrammingError('Unknown token `%s`' % token)


def as_values(values_stmt):
    _, values = parse_values(values_stmt)
    return values
