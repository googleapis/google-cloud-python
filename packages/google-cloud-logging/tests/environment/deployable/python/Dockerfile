# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.7-slim

# This Dockerfile must be built at the repo root

# show python logs as they occur
ENV PYTHONUNBUFFERED=0

# Install test code dependencies.
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# Add test scripts.
COPY router.py /app/
COPY snippets.py /app/

# install logging from local directory.
WORKDIR /app
ENV PATH="/app:${PATH}"
COPY python-logging /app/python-logging
RUN pip install -e /app/python-logging

# Start script
CMD python router.py
