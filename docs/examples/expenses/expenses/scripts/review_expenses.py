import csv
import optparse
import os
import textwrap
import sys


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

    def list_reports(self):
        return [
            {"Report ID": "sally/2013-11-19",
             "Description": "Onsite Training, Mountain View",
             "Status": "Paid",
             "Memo": "Check #3715",
            },
            {"Report ID": "sally/2014-04-19",
             "Description": "PyCon 2014, Montreal",
             "Status": "Paid",
             "Memo": "Check #3992",
            },
            {"Report ID": "sally/2014-09-01",
             "Description": "Frotz project kickoff, San Jose",
             "Status": "Pending",
             "Memo": "",
            },
        ]

    def __call__(self):
        fieldnames = ["Report ID", "Description", "Status", "Memo"]
        writer = csv.DictWriter(sys.stdout, fieldnames)
        writer.writerow(dict(zip(fieldnames, fieldnames)))
        for report in self.list_reports():
            writer.writerow(report)


class ShowReport(object):
    """Dump the contents of a given expense report.
    """
    def __init__(self, submitter, *args):
        self.submitter = submitter
        args = list(args)
        parser = optparse.OptionParser(
            usage="%prog [OPTIONS] REPORT_ID")

        options, args = parser.parse_args(args)
        try:
            self.report_id, = args
        except:
            raise InvalidCommandLine('Specify one report ID')

    def get_report_info(self):
        return {}

    def __call__(self):
        """
        Report-ID: sally/expenses-2014-09-01
        Report-Status: Pending
        Employee-ID: sally
        Description: Frotz project kickoff, San Jose
        """
        info = self.get_report_info()
        self.submitter.blather("Report-ID: %s" % self.report_id)
        self.submitter.blather("Report-Status: %s" %
                                info.get('status', 'Unknown'))
        self.submitter.blather("Employee-ID: %s" %
                                info.get('employee_id', 'Unknown'))
        self.submitter.blather("Description: %s" %
                                info.get('description', 'Unknown'))


class ApproveReport(object):
    """Approve a given expense report.
    """
    def __init__(self, submitter, *args):
        self.submitter = submitter
        args = list(args)
        parser = optparse.OptionParser(
            usage="%prog [OPTIONS] REPORT_ID")

        parser.add_option(
            '-c', '--check-number',
            action='store',
            dest='check_number',
            default=None,
            help="Check number issued to pay the expense report")

        options, args = parser.parse_args(args)
        try:
            self.report_id, = args
        except:
            raise InvalidCommandLine('Specify one report ID')
        self.check_number = options.check_number

    def __call__(self):
        memo = ('' if self.check_number is None
                    else ', check #%s' % self.check_number)
        self.submitter.blather("Approved, report ID: %s%s" %
                                (self.report_id, memo))


class RejectReport(object):
    """Reject a given expense report.
    """
    def __init__(self, submitter, *args):
        self.submitter = submitter
        args = list(args)
        parser = optparse.OptionParser(
            usage="%prog [OPTIONS] REPORT_ID")

        parser.add_option(
            '-r', '--reason',
            action='store',
            dest='reason',
            default=None,
            help="Reason for rejecting the expense report")

        options, args = parser.parse_args(args)
        try:
            self.report_id, = args
        except:
            raise InvalidCommandLine('Specify one report ID')
        self.reason = options.reason

    def __call__(self):
        memo = ('' if self.reason is None
                    else ', reason: %s' % self.reason)
        self.submitter.blather("Rejected, report ID: %s%s" %
                                (self.report_id, memo))


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
            current, current_args = queue[-1]
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
        print(text)

    def error(self, text):
        self.logger(text)

    def blather(self, text, min_level=1):
        if self.options.verbose >= min_level:
            self.logger(text)


def main(argv=sys.argv[1:]):
    try:
        ReviewExpenses(argv)()
    except InvalidCommandLine as e:  # pragma NO COVERAGE
        print(str(e))
        sys.exit(1)
