# Copyright 2020 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

import os

from google.cloud import spanner_v1 as spanner


def main():
    client = spanner.Client()
    ins = client.instance(os.environ.get('SPANNER_INSTANCE', 'django-tests'))
    if not ins.exists():
        ins.create()
        print('Created instance: %s' % ins.name)
    else:
        print('%s already exists' % ins.name)


if __name__ == '__main__':
    main()
