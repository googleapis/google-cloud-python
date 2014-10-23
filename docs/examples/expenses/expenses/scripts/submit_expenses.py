import csv
import optparse
import os
import textwrap
import sys


from .. import BadReportStatus
from .. import DuplicateReport
from .. import NoSuchReport
from .. import create_report
from .. import delete_report
from .. import update_report


class InvalidCommandLine(ValueError):
    pass


class NotACommand(object):
    def __init__(self, bogus):
        self.bogus = bogus

    def __call__(self):
        raise InvalidCommandLine('Not a command: %s' % self.bogus)


def _get_csv(args):
    try:
        csv_file, = args
    except:
        raise InvalidCommandLine('Specify one CSV file')
    csv_file = os.path.abspath(os.path.normpath(csv_file))
    if not os.path.exists(csv_file):
        raise InvalidCommandLine('Invalid CSV file: %s' % csv_file)
    with open(csv_file) as f:
        return csv_file, list(csv.DictReader(f))


class _Command(object):
    """Base class for create / update commands.
    """
    def __init__(self, submitter, *args):
        self.submitter = submitter
        args = list(args)
        parser = optparse.OptionParser(
            usage="%prog [OPTIONS] CSV_FILE")

        parser.add_option(
            '-e', '--employee-id',
            action='store',
            dest='employee_id',
            default=os.getlogin(),
            help="ID of employee submitting the expense report")

        parser.add_option(
            '-r', '--report-id',
            action='store',
            dest='report_id',
            default=None,
            help="ID of the expense report to update")

        parser.add_option(
            '-d', '--description',
            action='store',
            dest='description',
            default='',
            help="Short description of the expense report")

        options, args = parser.parse_args(args)
        self.employee_id = options.employee_id
        self.report_id = options.report_id
        self.description = options.description
        self.filename, self.rows = _get_csv(args)
        if self.report_id is None:
            fn = os.path.basename(self.filename)
            base, _ = os.path.splitext(fn)
            self.report_id = base


class CreateReport(_Command):
    """Create a new expense report from a CSV file.
    """
    def __call__(self):
        try:
            create_report(self.employee_id, self.report_id, self.rows,
                          self.description)
        except DuplicateReport:
            self.submitter.blather("Report already exists: %s/%s"
                                   % (self.employee_id, self.report_id))
        else:
            self.submitter.blather("Created report: %s/%s"
                                   % (self.employee_id, self.report_id))
            self.submitter.blather("Processed %d rows." % len(self.rows))


class UpdateReport(_Command):
    """Update an existing expense report from a CSV file.
    """
    def __call__(self):
        try:
            update_report(self.employee_id, self.report_id, self.rows,
                          self.description)
        except NoSuchReport:
            self.submitter.blather("No such report: %s/%s"
                                   % (self.employee_id, self.report_id))
        except BadReportStatus as e:
            self.submitter.blather("Invalid report status: %s/%s, %s"
                                   % (self.employee_id, self.report_id,
                                      str(e)))
        else:
            self.submitter.blather("Updated report: %s/%s"
                                   % (self.employee_id, self.report_id))
            self.submitter.blather("Processed %d rows." % len(self.rows))


class DeleteReport(object):
    """Delete an existing expense report.
    """
    def __init__(self, submitter, *args):
        self.submitter = submitter
        args = list(args)
        parser = optparse.OptionParser(
            usage="%prog [OPTIONS] REPORT_ID")

        parser.add_option(
            '-e', '--employee-id',
            action='store',
            dest='employee_id',
            default=os.getlogin(),
            help="ID of employee owning the expense report")

        parser.add_option(
            '-f', '--force',
            action='store_true',
            dest='force',
            default=False,
            help="Delete report even if not in 'pending' status")

        options, args = parser.parse_args(args)
        try:
            self.report_id, = args
        except:
            raise InvalidCommandLine('Specify one report ID')

        self.employee_id = options.employee_id
        self.force = options.force

    def __call__(self):
        try:
            count = delete_report(self.employee_id, self.report_id, self.force)
        except NoSuchReport:
            self.submitter.blather("No such report: %s/%s"
                                   % (self.employee_id, self.report_id))
        except BadReportStatus as e:
            self.submitter.blather("Invalid report status: %s/%s, %s"
                                   % (self.employee_id, self.report_id,
                                      str(e)))
        else:
            self.submitter.blather("Deleted report: %s/%s"
                                   % (self.employee_id, self.report_id))
            self.submitter.blather("Removed %d items." % count)


_COMMANDS = {
    'create': CreateReport,
    'update': UpdateReport,
    'delete': DeleteReport,
}


def get_description(command):
    klass = _COMMANDS[command]
    doc = getattr(klass, '__doc__', '')
    if doc is None:
        return ''
    return ' '.join([x.lstrip() for x in doc.split('\n')])


class SubmitExpenses(object):
    """ Driver for the :command:`submit_expenses` command-line script.
    """
    def __init__(self, argv=None, logger=None):
        self.commands = []
        if logger is None:
            logger = self._print
        self.logger = logger
        self.parse_arguments(argv)

    def parse_arguments(self, argv=None):
        """ Parse subcommands and their options from an argv list.
        """
        # Global options (not bound to sub-command)
        mine = []
        queue = [(None, mine)]

        def _recordCommand(arg):
            if arg is not None:
                queue.append((arg, []))

        for arg in argv:
            if arg in _COMMANDS:
                _recordCommand(arg)
            else:
                queue[-1][1].append(arg)

        _recordCommand(None)

        usage = ("%prog [GLOBAL_OPTIONS] "
                 "[command [COMMAND_OPTIONS]* [COMMAND_ARGS]]")
        parser = optparse.OptionParser(usage=usage)

        parser.add_option(
            '-s', '--help-commands',
            action='store_true',
            dest='help_commands',
            help="Show command help")

        parser.add_option(
            '-q', '--quiet',
            action='store_const', const=0,
            dest='verbose',
            help="Run quietly")

        parser.add_option(
            '-v', '--verbose',
            action='count',
            dest='verbose',
            default=1,
            help="Increase verbosity")

        options, args = parser.parse_args(mine)

        self.options = options

        for arg in args:
            self.commands.append(NotACommand(arg))
            options.help_commands = True

        if options.help_commands:
            keys = sorted(_COMMANDS.keys())
            self.error('Valid commands are:')
            for x in keys:
                self.error(' %s' % x)
                doc = get_description(x)
                if doc:
                    self.error(textwrap.fill(doc,
                                             initial_indent='    ',
                                             subsequent_indent='    '))
            return

        for command_name, args in queue:
            if command_name is not None:
                command = _COMMANDS[command_name](self, *args)
                self.commands.append(command)

    def __call__(self):
        """ Invoke sub-commands parsed by :meth:`parse_arguments`.
        """
        if not self.commands:
            raise InvalidCommandLine('No commands specified')

        for command in self.commands:
            command()

    def _print(self, text):  # pragma NO COVERAGE
        sys.stdout.write('%s\n' % text)

    def error(self, text):
        self.logger(text)

    def blather(self, text, min_level=1):
        if self.options.verbose >= min_level:
            self.logger(text)


def main(argv=sys.argv[1:]):
    try:
        SubmitExpenses(argv)()
    except InvalidCommandLine as e:  # pragma NO COVERAGE
        sys.stdout.write('%s\n' % str(e))
        sys.exit(1)
