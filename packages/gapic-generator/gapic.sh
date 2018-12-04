#!/bin/bash
# Copyright 2018 Google LLC
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

CMD="$0"

# Set variables used by this script.
# All of these are set in options below, and all but $PATH are required.
IMAGE=
IN=
OUT=
PROTO_PATH=`pwd`

# Print help and exit.
function show_help {
  echo "Usage: $CMD --image IMAGE --in IN_DIR --out OUT_DIR [--path PATH_DIR]"
  echo ""
  echo "Required arguments:"
  echo "      --image  The Docker image to use. The script will attempt to pull"
  echo "               it if it is not present."
  echo "  -i, --in     A directory containing the protos describing the API"
  echo "               to be generated."
  echo "  -o, --out    Destination directory for the completed client library."
  echo ""
  echo "Optional arguments:"
  echo "  -p, --path   The base import path for the protos. Assumed to be the"
  echo "               current working directory if unspecified."
  echo "  -h, --help   This help information."
  exit 0
}

# Parse out options.
while true; do
  case "$1" in
    -h | --help ) show_help ;;
    --image ) IMAGE="$2"; shift 2 ;;
    -i | --in ) IN="$2"; shift 2 ;;
    -o | --out ) OUT="$2"; shift 2 ;;
    -p | --path ) PROTO_PATH=$2; shift 2 ;;
    -- ) shift; break; ;;
    * ) break ;;
  esac
done

# Ensure that all required options are set.
if [ -z "$IMAGE" ] || [ -z "$IN" ] || [ -z "$OUT" ]; then
  >&2 echo "Required argument missing."
  >&2 echo "The --image, --in, and --out arguments are all required."
  >&2 echo "Run $CMD --help for more information."
  exit 64
fi

# Ensure that the input directory exists (and is a directory).
if ! [ -d $IN ]; then
  >&2 echo "Directory does not exist: $IN"
  exit 2
fi

# Ensure Docker is running and seems healthy.
# This is mostly a check to bubble useful errors quickly.
if ! docker ps > /dev/null; then
  exit $?
fi

# If the output directory does not exist, create it.
if ! mkdir -p $OUT ; then
  exit $?
fi

# If the output directory is not empty, warn (but continue).
if [ "$(ls -A $OUT )"]; then
  >&2 echo "Warning: Output directory is not empty."
fi

# If the image is not yet on the machine, pull it.
if ! docker images $IMAGE > /dev/null; then
  echo "Image $IMAGE not found; pulling."
  if ! docker pull $IMAGE; then
    exit $?
  fi
fi

# Generate the client library.
docker run \
  --mount type=bind,source=${PROTO_PATH}/${IN},destination=/in/${IN},readonly \
  --mount type=bind,source=$OUT,destination=/out \
  --rm \
  --user $UID \
  $IMAGE
exit $?
