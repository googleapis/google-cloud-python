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
import com.google.iam.credentials.v1.GenerateAccessTokenRequest;
import com.google.iam.credentials.v1.GenerateAccessTokenResponse;
import com.google.iam.credentials.v1.GenerateIdTokenRequest;
import com.google.iam.credentials.v1.GenerateIdTokenResponse;
import com.google.iam.credentials.v1.GenerateIdentityBindingAccessTokenRequest;
import com.google.iam.credentials.v1.GenerateIdentityBindingAccessTokenResponse;
import com.google.iam.credentials.v1.SignBlobRequest;
import com.google.iam.credentials.v1.SignBlobResponse;
import com.google.iam.credentials.v1.SignJwtRequest;
import com.google.iam.credentials.v1.SignJwtResponse;
import com.google.protobuf.GeneratedMessageV3;
import com.google.protos.google.iam.credentials.v1.IAMCredentialsGrpc.IAMCredentialsImplBase;
import io.grpc.stub.StreamObserver;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

@javax.annotation.Generated("by GAPIC")
@BetaApi
public class MockIAMCredentialsImpl extends IAMCredentialsImplBase {
  private ArrayList<GeneratedMessageV3> requests;
  private Queue<Object> responses;

  public MockIAMCredentialsImpl() {
    requests = new ArrayList<>();
    responses = new LinkedList<>();
  }

  public List<GeneratedMessageV3> getRequests() {
    return requests;
  }

  public void addResponse(GeneratedMessageV3 response) {
    responses.add(response);
  }

  public void setResponses(List<GeneratedMessageV3> responses) {
    this.responses = new LinkedList<Object>(responses);
  }

  public void addException(Exception exception) {
    responses.add(exception);
  }

  public void reset() {
    requests = new ArrayList<>();
    responses = new LinkedList<>();
  }

  @Override
  public void generateAccessToken(
      GenerateAccessTokenRequest request,
      StreamObserver<GenerateAccessTokenResponse> responseObserver) {
    Object response = responses.remove();
    if (response instanceof GenerateAccessTokenResponse) {
      requests.add(request);
      responseObserver.onNext((GenerateAccessTokenResponse) response);
      responseObserver.onCompleted();
    } else if (response instanceof Exception) {
      responseObserver.onError((Exception) response);
    } else {
      responseObserver.onError(new IllegalArgumentException("Unrecognized response type"));
    }
  }

  @Override
  public void generateIdToken(
      GenerateIdTokenRequest request, StreamObserver<GenerateIdTokenResponse> responseObserver) {
    Object response = responses.remove();
    if (response instanceof GenerateIdTokenResponse) {
      requests.add(request);
      responseObserver.onNext((GenerateIdTokenResponse) response);
      responseObserver.onCompleted();
    } else if (response instanceof Exception) {
      responseObserver.onError((Exception) response);
    } else {
      responseObserver.onError(new IllegalArgumentException("Unrecognized response type"));
    }
  }

  @Override
  public void signBlob(SignBlobRequest request, StreamObserver<SignBlobResponse> responseObserver) {
    Object response = responses.remove();
    if (response instanceof SignBlobResponse) {
      requests.add(request);
      responseObserver.onNext((SignBlobResponse) response);
      responseObserver.onCompleted();
    } else if (response instanceof Exception) {
      responseObserver.onError((Exception) response);
    } else {
      responseObserver.onError(new IllegalArgumentException("Unrecognized response type"));
    }
  }

  @Override
  public void signJwt(SignJwtRequest request, StreamObserver<SignJwtResponse> responseObserver) {
    Object response = responses.remove();
    if (response instanceof SignJwtResponse) {
      requests.add(request);
      responseObserver.onNext((SignJwtResponse) response);
      responseObserver.onCompleted();
    } else if (response instanceof Exception) {
      responseObserver.onError((Exception) response);
    } else {
      responseObserver.onError(new IllegalArgumentException("Unrecognized response type"));
    }
  }

  @Override
  public void generateIdentityBindingAccessToken(
      GenerateIdentityBindingAccessTokenRequest request,
      StreamObserver<GenerateIdentityBindingAccessTokenResponse> responseObserver) {
    Object response = responses.remove();
    if (response instanceof GenerateIdentityBindingAccessTokenResponse) {
      requests.add(request);
      responseObserver.onNext((GenerateIdentityBindingAccessTokenResponse) response);
      responseObserver.onCompleted();
    } else if (response instanceof Exception) {
      responseObserver.onError((Exception) response);
    } else {
      responseObserver.onError(new IllegalArgumentException("Unrecognized response type"));
    }
  }
}
