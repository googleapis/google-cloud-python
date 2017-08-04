# Copyright 2017 Google Inc.
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

import pkg_resources
import warnings


def complain(package_name):
    """Issue a warning if `package_name` is installed.

    In a future release, this method will be updated to raise ImportError
    rather than just send a warning.

    Args:
        package_name (str): The name of the obselete package.
    """
    try:
        pkg_resources.get_distribution(package_name)
        warnings.warn(
            'The {pkg} package is now obselete. Please `pip uninstall {pkg}`. '
            'In the future, this warning will become an ImportError.'.format(
                pkg=package_name,
            ),
            DeprecationWarning,
        )
    except pkg_resources.DistributionNotFound:
        pass
