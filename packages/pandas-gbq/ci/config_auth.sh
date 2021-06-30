#!/bin/bash
# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

set -e
# Don't set -x, because we don't want to leak keys.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# Write key to file if present.
if [ ! -z "$SERVICE_ACCOUNT_KEY" ] ; then
    echo "$SERVICE_ACCOUNT_KEY" | base64 --decode > "$DIR"/service_account.json
fi
