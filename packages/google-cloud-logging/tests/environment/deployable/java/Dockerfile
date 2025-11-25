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

# compile local java-logging library
FROM maven:3.8.4 AS lib-env
WORKDIR /app
COPY _library ./
RUN mvn verify --fail-never
RUN mvn -Dmaven.test.skip=true package

# Compile the deployable code.
FROM maven:3.8.4 AS build-env
WORKDIR /app
COPY pom.xml /app/pom.xml
# copy over compiled library
COPY --from=lib-env /app/target/*.jar /app/java-logging.jar
# install java-logging
RUN mvn install:install-file \
    -Dfile=/app/java-logging.jar \
    -DgroupId=com.google.cloud.local \
    -DartifactId=google-cloud-logging \
    -Dversion=0.0.1 \
    -Dpackaging=jar \
    -DgeneratePom=true
# download dependencies as specified in pom.xml
RUN mvn verify --fail-never
COPY src /app/src
RUN mvn -Dmaven.test.skip=true package

# Build runtime image.
FROM openjdk:8-jre-slim
# Copy the compiled files over.
COPY --from=build-env /app/target/ /app/
ENV PORT=8080
# Starts libapp with debugging server at port 5005.
CMD ["java", "-jar", "/app/deployable-1.0.0.jar"]
