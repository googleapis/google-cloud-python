# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Client for interacting with the Stackdriver Logging API"""

import traceback

import gcloud.logging.client
import six


class HTTPContext(object):
    """HTTPContext defines an object that captures the parameter for the
    httpRequest part of Error Reporting API

    :type method: string
    :param method: The type of HTTP request, such as GET, POST, etc.

    :type url: string
    :param url: The URL of the request

    :type user_agent: string
    :param user_agent: The user agent information that is provided with the
                       request.

    :type referrer: string
    :param referrer: The referrer information that is provided with the
                     request.

    :type response_status_code: int
    :param response_status_code: The HTTP response status code for the request.

    :type remote_ip: string
    :param remote_ip: The IP address from which the request originated. This
                      can be IPv4, IPv6, or a token which is derived from
                      the IP address, depending on the data that has been
                      provided in the error report.
    """

    def __init__(self, method=None, url=None,
                 user_agent=None, referrer=None,
                 response_status_code=None, remote_ip=None):
        self.method = method
        self.url = url
        # intentionally camel case for mapping to JSON API expects
        # pylint: disable=invalid-name
        self.userAgent = user_agent
        self.referrer = referrer
        self.responseStatusCode = response_status_code
        self.remoteIp = remote_ip


class Client(object):
    """Error Reporting client. Currently Error Reporting is done by creating
    a Logging client.

    :type project: string
    :param project: the project which the client acts on behalf of. If not
                    passed falls back to the default inferred from the
                    environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.

    :type service: str
    :param service: An identifier of the service, such as the name of the
                    executable, job, or Google App Engine service name. This
                    field is expected to have a low number of values that are
                    relatively stable over time, as opposed to version,
                    which can be changed whenever new code is deployed.


    :type version: str
    :param version: Represents the source code version that the developer
                    provided, which could represent a version label or a Git
                    SHA-1 hash, for example. If the developer did not provide
                    a version, the value is set to default.

    :raises: :class:`ValueError` if the project is neither passed in nor
             set in the environment.
    """

    def __init__(self, project=None,
                 credentials=None,
                 http=None,
                 service=None,
                 version=None):
        self.logging_client = gcloud.logging.client.Client(
            project, credentials, http)
        self.service = service if service else self.DEFAULT_SERVICE
        self.version = version

    DEFAULT_SERVICE = 'python'

    def _send_error_report(self, message,
                           report_location=None, http_context=None, user=None):
        """Makes the call to the Error Reporting API via the log stream.

        This is the lower-level interface to build the payload, generally
        users will use either report() or report_exception() to automatically
        gather the parameters for this method.

        Currently this method sends the Error Report by formatting a structured
        log message according to

        https://cloud.google.com/error-reporting/docs/formatting-error-messages

        :type message: string
        :param message: The stack trace that was reported or logged by the
                   service.

        :type report_location: dict
        :param report_location:  The location in the source code where the
               decision was made to report the error, usually the place
               where it was logged. For a logged exception this would be the
               source line where the exception is logged, usually close to
               the place where it was caught.

               This should be a Python dict that contains the keys 'filePath',
               'lineNumber', and 'functionName'

        :type http_context: :class`gcloud.error_reporting.HTTPContext`
        :param http_context: The HTTP request which was processed when the
                             error was triggered.

        :type user: string
        :param user: The user who caused or was affected by the crash. This can
                     be a user ID, an email address, or an arbitrary token that
                     uniquely identifies the user. When sending an error
                     report, leave this field empty if the user was not
                     logged in. In this  case the Error Reporting system will
                     use other data, such as remote IP address,
                     to distinguish affected users.
        """
        payload = {
            'serviceContext': {
                'service': self.service,
            },
            'message': '{0}'.format(message)
        }

        if self.version:
            payload['serviceContext']['version'] = self.version

        if report_location or http_context or user:
            payload['context'] = {}

        if report_location:
            payload['context']['reportLocation'] = report_location

        if http_context:
            http_context_dict = http_context.__dict__
            # strip out None values
            # once py26 support is dropped this can use dict comprehension
            payload['context']['httpContext'] = dict(
                (k, v) for (k, v) in six.iteritems(http_context_dict)
                if v is not None
            )

        if user:
            payload['context']['user'] = user

        logger = self.logging_client.logger('errors')
        logger.log_struct(payload)

    def report(self, message, http_context=None, user=None):
        """ Reports a message to Stackdriver Error Reporting
        https://cloud.google.com/error-reporting/docs/formatting-error-messages

           :type message: str
           :param message: A user-supplied message to report


          :type http_context: :class`gcloud.error_reporting.HTTPContext`
          :param http_context: The HTTP request which was processed when the
                               error was triggered.

          :type user: string
          :param user: The user who caused or was affected by the crash. This
                       can be a user ID, an email address, or an arbitrary
                       token that uniquely identifies the user. When sending
                       an error report, leave this field empty if the user
                       was not logged in. In this case the Error Reporting
                       system will use other data, such as remote IP address,
                       to distinguish affected users.

           Example::
                >>>  client.report("Something went wrong!")
        """
        stack = traceback.extract_stack()
        last_call = stack[-2]
        file_path = last_call[0]
        line_number = last_call[1]
        function_name = last_call[2]
        report_location = {
            'filePath': file_path,
            'lineNumber': line_number,
            'functionName': function_name
        }

        self._send_error_report(message,
                                http_context=http_context,
                                user=user,
                                report_location=report_location)

    def report_exception(self, http_context=None, user=None):
        """ Reports the details of the latest exceptions to Stackdriver Error
            Reporting.

          :type http_context: :class`gcloud.error_reporting.HTTPContext`
          :param http_context: The HTTP request which was processed when the
                               error was triggered.

          :type user: string
          :param user: The user who caused or was affected by the crash. This
                       can be a user ID, an email address, or an arbitrary
                       token that uniquely identifies the user. When sending an
                       error report, leave this field empty if the user was
                       not logged in. In this case the Error Reporting system
                       will use other data, such as remote IP address,
                       to distinguish affected users.

           Example::

                >>>     try:
                >>>         raise NameError
                >>>     except Exception:
                >>>         client.report_exception()
        """
        self._send_error_report(traceback.format_exc(),
                                http_context=http_context,
                                user=user)
