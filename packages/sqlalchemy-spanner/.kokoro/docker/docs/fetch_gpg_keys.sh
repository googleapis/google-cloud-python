#!/bin/bash
# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bsd

# A script to fetch gpg keys with retry.
# Avoid jinja parsing the file.
#

function retry {
    if [[ "${#}" -le 1 ]]; then
	echo "Usage: ${0} retry_count commands.."
	exit 1
    fi
    local retries=${1}
    local command="${@:2}"
    until [[ "${retries}" -le 0 ]]; do
	$command && return 0
	if [[ $? -ne 0 ]]; then
	    echo "command failed, retrying"
	    ((retries--))
	fi
    done
    return 1
}

# 3.6.9, 3.7.5 (Ned Deily)
retry 3 gpg --keyserver ha.pool.sks-keyservers.net --recv-keys \
      0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D

# 3.8.0 (Łukasz Langa)
retry 3 gpg --keyserver ha.pool.sks-keyservers.net --recv-keys \
      E3FF2839C048B25C084DEBE9B26995E310250568

#
