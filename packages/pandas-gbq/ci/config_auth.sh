#!/bin/bash
set -e
# Don't set -x, because we don't want to leak keys.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# Write key to file if present.
if [ ! -z "$SERVICE_ACCOUNT_KEY" ] ; then
    echo "$SERVICE_ACCOUNT_KEY" | base64 --decode > "$DIR"/service_account.json
fi
