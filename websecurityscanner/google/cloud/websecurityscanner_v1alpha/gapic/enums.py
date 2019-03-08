# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wrappers for protocol buffer enum types."""

import enum


class Finding(object):
    class FindingType(enum.IntEnum):
        """
        Types of Findings.

        Attributes:
          FINDING_TYPE_UNSPECIFIED (int): The invalid finding type.
          MIXED_CONTENT (int): A page that was served over HTTPS also resources over HTTP. A
          man-in-the-middle attacker could tamper with the HTTP resource and gain
          full access to the website that loads the resource or to monitor the
          actions taken by the user.
          OUTDATED_LIBRARY (int): The version of an included library is known to contain a security issue.
          The scanner checks the version of library in use against a known list of
          vulnerable libraries. False positives are possible if the version
          detection fails or if the library has been manually patched.
          ROSETTA_FLASH (int): This type of vulnerability occurs when the value of a request parameter
          is reflected at the beginning of the response, for example, in requests
          using JSONP. Under certain circumstances, an attacker may be able to
          supply an alphanumeric-only Flash file in the vulnerable parameter
          causing the browser to execute the Flash file as if it originated on the
          vulnerable server.
          XSS_CALLBACK (int): A cross-site scripting (XSS) bug is found via JavaScript callback. For
          detailed explanations on XSS, see
          https://www.google.com/about/appsecurity/learning/xss/.
          XSS_ERROR (int): A potential cross-site scripting (XSS) bug due to JavaScript breakage.
          In some circumstances, the application under test might modify the test
          string before it is parsed by the browser. When the browser attempts to
          runs this modified test string, it will likely break and throw a
          JavaScript execution error, thus an injection issue is occurring.
          However, it may not be exploitable. Manual verification is needed to see
          if the test string modifications can be evaded and confirm that the issue
          is in fact an XSS vulnerability. For detailed explanations on XSS, see
          https://www.google.com/about/appsecurity/learning/xss/.
          CLEAR_TEXT_PASSWORD (int): An application appears to be transmitting a password field in clear text.
          An attacker can eavesdrop network traffic and sniff the password field.
        """

        FINDING_TYPE_UNSPECIFIED = 0
        MIXED_CONTENT = 1
        OUTDATED_LIBRARY = 2
        ROSETTA_FLASH = 5
        XSS_CALLBACK = 3
        XSS_ERROR = 4
        CLEAR_TEXT_PASSWORD = 6


class ScanConfig(object):
    class TargetPlatform(enum.IntEnum):
        """
        Cloud platforms supported by Cloud Web Security Scanner.

        Attributes:
          TARGET_PLATFORM_UNSPECIFIED (int): The target platform is unknown. Requests with this enum value will be
          rejected with INVALID\_ARGUMENT error.
          APP_ENGINE (int): Google App Engine service.
          COMPUTE (int): Google Compute Engine service.
        """

        TARGET_PLATFORM_UNSPECIFIED = 0
        APP_ENGINE = 1
        COMPUTE = 2

    class UserAgent(enum.IntEnum):
        """
        Type of user agents used for scanning.

        Attributes:
          USER_AGENT_UNSPECIFIED (int): The user agent is unknown. Service will default to CHROME\_LINUX.
          CHROME_LINUX (int): Chrome on Linux. This is the service default if unspecified.
          CHROME_ANDROID (int): Chrome on Android.
          SAFARI_IPHONE (int): Safari on IPhone.
        """

        USER_AGENT_UNSPECIFIED = 0
        CHROME_LINUX = 1
        CHROME_ANDROID = 2
        SAFARI_IPHONE = 3


class ScanRun(object):
    class ExecutionState(enum.IntEnum):
        """
        Types of ScanRun execution state.

        Attributes:
          EXECUTION_STATE_UNSPECIFIED (int): Represents an invalid state caused by internal server error. This value
          should never be returned.
          QUEUED (int): The scan is waiting in the queue.
          SCANNING (int): The scan is in progress.
          FINISHED (int): The scan is either finished or stopped by user.
        """

        EXECUTION_STATE_UNSPECIFIED = 0
        QUEUED = 1
        SCANNING = 2
        FINISHED = 3

    class ResultState(enum.IntEnum):
        """
        Types of ScanRun result state.

        Attributes:
          RESULT_STATE_UNSPECIFIED (int): Default value. This value is returned when the ScanRun is not yet
          finished.
          SUCCESS (int): The scan finished without errors.
          ERROR (int): The scan finished with errors.
          KILLED (int): The scan was terminated by user.
        """

        RESULT_STATE_UNSPECIFIED = 0
        SUCCESS = 1
        ERROR = 2
        KILLED = 3
