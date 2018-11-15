/*
 * Copyright 2018 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.google.cloud.iam.credentials.v1;

import com.google.api.core.BetaApi;
import com.google.api.gax.grpc.testing.MockGrpcService;
import com.google.protobuf.GeneratedMessageV3;
import io.grpc.ServerServiceDefinition;
import java.util.List;

@javax.annotation.Generated("by GAPIC")
@BetaApi
public class MockIAMCredentials implements MockGrpcService {
  private final MockIAMCredentialsImpl serviceImpl;

  public MockIAMCredentials() {
    serviceImpl = new MockIAMCredentialsImpl();
  }

  @Override
  public List<GeneratedMessageV3> getRequests() {
    return serviceImpl.getRequests();
  }

  @Override
  public void addResponse(GeneratedMessageV3 response) {
    serviceImpl.addResponse(response);
  }

  @Override
  public void addException(Exception exception) {
    serviceImpl.addException(exception);
  }

  @Override
  public ServerServiceDefinition getServiceDefinition() {
    return serviceImpl.bindService();
  }

  @Override
  public void reset() {
    serviceImpl.reset();
  }
}
