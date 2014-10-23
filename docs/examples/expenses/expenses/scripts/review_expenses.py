import csv
import optparse
import os
import textwrap
import sys

from .. import NoSuchReport
from .. import approve_report
from .. import get_report_info
from .. import list_reports
from .. import reject_report


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


class ListReports(object):
    """List expense reports according to specified criteria.
    """
    def __init__(self, submitter, *args):
        self.submitter = submitter
        args = list(args)
        parser = optparse.OptionParser(
            usage="%prog [OPTIONS]")

        parser.add_option(
            '-e', '--employee-id',
            action='store',
            dest='employee_id',
            default=None,
            help="ID of the employee whose expense reports to list")

        parser.add_option(
            '-s', '--status',
            action='store',
            dest='status',
            default=None,
            help="Status of expense reports to list")

        options, args = parser.parse_args(args)
        self.employee_id = options.employee_id
        self.status = options.status

    def __call__(self):
        _cols = [
            ('employee_id', 'Employee ID'),
            ('report_id', 'Report ID'),
            ('created', 'Created'),
            ('updated', 'Updated'),
            ('description', 'Description'),
            ('status', 'Status'),
            ('memo', 'Memo'),
            ]
        writer = csv.writer(sys.stdout)
        writer.writerow([x[1] for x in _cols])
        for report in list_reports(self.employee_id, self.status):
            writer.writerow([report[x[0]] for x in _cols])


class ShowReport(object):
    """Dump the contents of a given expense report.
    """
    def __init__(self, submitter, *args):
        self.submitter = submitter
        args = list(args)
        parser = optparse.OptionParser(
            usage="%prog [OPTIONS] EMPLOYEE_ID REPORT_ID")

        _, args = parser.parse_args(args)
        try:
            self.employee_id, self.report_id, = args
        except:
            raise InvalidCommandLine('Specify employee ID, report ID')

    def __call__(self):
        _cols = ['Date', 'Vendor', 'Type', 'Quantity', 'Price', 'Memo']
        try:
            info = get_report_info(self.employee_id, self.report_id)
        except NoSuchReport:
            self.submitter.blather("No such report: %s/%s"
                                   % (self.employee_id, self.report_id))
        else:
            self.submitter.blather("Employee-ID: %s" % info['employee_id'])
            self.submitter.blather("Report-ID: %s" % info['report_id'])
            self.submitter.blather("Report-Status: %s" % info['status'])
            self.submitter.blather("Created: %s" % info['created'])
            self.submitter.blather("Updated: %s" % info['updated'])
            self.submitter.blather("Description: %s" % info['description'])
            self.submitter.blather("")
            writer = csv.writer(sys.stdout)
            writer.writerow([x for x in _cols])
            for item in info['items']:
                writer.writerow([item[x] for x in _cols])


class ApproveReport(object):
    """Approve a given expense report.
    """
    def __init__(self, submitter, *args):
        self.submitter = submitter
        args = list(args)
        parser = optparse.OptionParser(
            usage="%prog [OPTIONS] EMPLOYEE_ID REPORT_ID")

        parser.add_option(
            '-c', '--check-number',
            action='store',
            dest='check_number',
            default='',
            help="Check number issued to pay the expense report")

        options, args = parser.parse_args(args)
        try:
            self.employee_id, self.report_id, = args
        except:
            raise InvalidCommandLine('Specify employee ID, report ID')
        self.check_number = options.check_number

    def __call__(self):
        approve_report(self.employee_id, self.report_id, self.check_number)
        memo = ('' if self.check_number is None else
                ', check #%s' % self.check_number)
        self.submitter.blather("Approved report: %s/%s%s" %
                               (self.employee_id, self.report_id, memo))


class RejectReport(object):
    """Reject a given expense report.
    """
    def __init__(self, submitter, *args):
        self.submitter = submitter
        args = list(args)
        parser = optparse.OptionParser(
            usage="%prog [OPTIONS] EMPLOYEE_ID REPORT_ID")

        parser.add_option(
            '-r', '--reason',
            action='store',
            dest='reason',
            default=None,
            help="Reason for rejecting the expense report")

        options, args = parser.parse_args(args)
        try:
            self.employee_id, self.report_id, = args
        except:
            raise InvalidCommandLine('Specify employee ID, report ID')
        self.reason = options.reason

    def __call__(self):
        reject_report(self.employee_id, self.report_id, self.reason)
        memo = ('' if self.reason is None else ', reason: %s' % self.reason)
        self.submitter.blather("Rejected report: %s/%s%s" %
                               (self.employee_id, self.report_id, memo))


_COMMANDS = {
    'list': ListReports,
    'show': ShowReport,
    'approve': ApproveReport,
    'reject': RejectReport,
}


def get_description(command):
    klass = _COMMANDS[command]
    doc = getattr(klass, '__doc__', '')
    if doc is None:
        return ''
    return ' '.join([x.lstrip() for x in doc.split('\n')])


class ReviewExpenses(object):
    """ Driver for the :command:`review_expenses` command-line script.
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
        sys.stdout.write('%s/n' % text)

    def error(self, text):
        self.logger(text)

    def blather(self, text, min_level=1):
        if self.options.verbose >= min_level:
            self.logger(text)


def main(argv=sys.argv[1:]):
    try:
        ReviewExpenses(argv)()
    except InvalidCommandLine as e:  # pragma NO COVERAGE
        sys.stdout.write('%s\n' % (str(e)))
        sys.exit(1)
