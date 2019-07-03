#!/bin/bash
# Copyright 2019 Google LLC
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

PLUGIN_OPTIONS=""

# Parse out options.
while [ -n "$1" ]; do
  case "$1" in
    -- )
      shift
      break
      ;;
    * )
      # If this switch begins with "--python-gapic-" or "--gapic-", then it is
      # meant for us.
      if [[ $1 == --python-gapic-* ]]; then
        PLUGIN_OPTIONS="$PLUGIN_OPTIONS,$1=$2"
        shift 2
      elif [[ $1 == --gapic-* ]]; then
        PLUGIN_OPTIONS="$PLUGIN_OPTIONS,$1=$2"
        shift 2
      else
        # Ignore anything we do not recognize.
        shift
      fi
      ;;
  esac
done

protoc --proto_path=/protos/ --proto_path=/in/ \
       --python_gapic_out=/out/ \
       --python_gapic_opt=${PLUGIN_OPTIONS:1} \
       `find /in/ -name *.proto`
