#!/bin/bash
# Copyright 2022 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License"); ...
set -eo pipefail

pwd

NOX_SESSION_ARG=""
NOX_FILE_ARG=""

[[ -z "${NOX_SESSION}" ]] || NOX_SESSION_ARG="-s ${NOX_SESSION}"
[[ -z "${NOX_FILE}" ]] || NOX_FILE_ARG="-f ${NOX_FILE}"

# 3-Attempt retry loop to absorb GCP quota limits and network blips
for attempt in 1 2 3; do
  echo "============================================"
  echo "Execution attempt $attempt of 3..."
  echo "============================================"
  
  if uvx --with 'nox[uv]' nox ${NOX_SESSION_ARG} ${NOX_FILE_ARG}; then
    echo "Tests passed successfully!"
    exit 0
  fi
  
  if [[ $attempt -lt 3 ]]; then
    echo "Tests failed. Backing off for 15 seconds to absorb quota limits..."
    sleep 15
  fi
done

echo "Tests failed after 3 attempts. Hard failure."
exit 1