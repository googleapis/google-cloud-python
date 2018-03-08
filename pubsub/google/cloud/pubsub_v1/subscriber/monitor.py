# Copyright 2018, Google LLC All rights reserved.
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

import sys
import time
import threading


import six


class Monitor(object):
    """A monitor for subscribed objects.

    The monitor allows for output of subscriber `parameters` to be
    printed to stderr after `interval` seconds.

    Args:
        policy (~.pubsub_v1.subscriber.policy.thread.Policy): 
            The `policy` to monitor
        interval (float): The `interval` in seconds to display parameters
        parameters (str or Sequence(str)): The `policy` parameters to output
    """
    NAME = 'name'
    MESSAGES = 'messages'
    P99 = 'p99'
    REQUESTS = 'requests'

    def __init__(self, policy, interval, parameters):
        self.event = threading.Event()
        self.policy = policy
        self.subscription_name = self.policy.subscription.split('/')[-1]
        self.thread = threading.Thread(
            name='{} Monitor'.format(self.subscription_name.capitalize()),
            target=self._timer,
            args=(interval, self.event)
        )
        self.thread.daemon = True
        self._stop_thread = False
        self._build_output(parameters)

    def _start(self, opened):
        """Starts the monitoring thread
        
        Start monitoring if it hasn't started and unblocks if stream is opened

        Args:
            opened (bool): Indicates whether the stream has been opened
        """
        if not self.thread.is_alive():
            self.thread.start()
        if opened:
            self.event.set()

    def _stop(self):
        """Stops the monitoring thread
        
        Blocks the thread from outputing monitoring.
        """
        self.event.clear()

    def _clear(self):
        """Clears the monitoring thread

        Exits the thread
        """
        self.event.set()
        self._stop_thread = True

    def _build_output(self, parameters):
        """Builds the string for monitor output

        Args:
            parameters (str): parameters to output
        """
        self.msg = ''
        if self.NAME in parameters:
            self.msg += '{}\n'.format(self.subscription_name)
        if self.P99 in parameters:
            self.msg += '{}\n'.format(self.policy.histogram.percentile(99))
        if self.MESSAGES in parameters:
            self.msg += '{}\n'.format(len(self.policy.managed_ack_ids))
        if self.REQUESTS in parameters:
            self.msg += '{}\n'.format(self.policy._consumer.pending_requests)

    def _timer(self, interval, event):
        """Main timer loop for thread
       
        Args:
            interval (float): Seconds between monitoring output
            event (~threading.Event): :class:`~threading.Event` for blocking
        """
        while True:
            event.wait()
            if self._stop_thread:
                break
            if six.PY3:
                sys.stderr.write(self.msg)
            else:
                sys.stderr.write(unicode(self.msg))
            time.sleep(interval)
