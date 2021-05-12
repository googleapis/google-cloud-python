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

# Use the official lightweight Node.js 12 image.
# https://hub.docker.com/_/node
FROM node:12-slim

# Create and change to the app directory.
WORKDIR /usr/src/app

# Copy test script and dependencies to the container image.
COPY package*.json ./
COPY app.js ./
COPY tests.js ./
COPY nodejs-logging ./nodejs-logging

# Install dependencies.
RUN npm install --production

# Environment variable denoting whether to run an app server
ENV RUNSERVER=1

# Run the web service on container startup.
CMD [ "npm", "start" ]
