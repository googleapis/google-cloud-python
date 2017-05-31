# Copyright 2017, Google Inc. All rights reserved.
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

def retry(func, delay=0, count=0, err=None, **kwargs):
    """Attempt to retry a function after the provided delay.

    If there have been too many retries, raise an exception.

    Args:
        func (callable): The function to retry.
        delay (int): The period to delay before retrying; specified in seconds.
        count (int): The number of previous retries that have occurred.
            If this is >= 5, an exception will be raised.
        **kwargs (dict): Other keyword arguments to pass to the function.
    """
    # If there have been too many retries, simply raise the exception.
    if count >= 5:
        raise err

    # Sleep the given delay.
    time.sleep(delay)

    # Try calling the method again.
    return func(delay=delay, count=count, **kwargs)
