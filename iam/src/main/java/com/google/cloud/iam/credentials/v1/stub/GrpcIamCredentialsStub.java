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
package com.google.cloud.iam.credentials.v1.stub;

import com.google.api.core.BetaApi;
import com.google.api.gax.core.BackgroundResource;
import com.google.api.gax.core.BackgroundResourceAggregation;
import com.google.api.gax.grpc.GrpcCallSettings;
import com.google.api.gax.grpc.GrpcStubCallableFactory;
import com.google.api.gax.rpc.ClientContext;
import com.google.api.gax.rpc.UnaryCallable;
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
import io.grpc.MethodDescriptor;
import io.grpc.protobuf.ProtoUtils;
import java.io.IOException;
import java.util.concurrent.TimeUnit;
import javax.annotation.Generated;

// AUTO-GENERATED DOCUMENTATION AND CLASS
/**
 * gRPC stub implementation for IAM Service Account Credentials API.
 *
 * <p>This class is for advanced usage and reflects the underlying API directly.
 */
@Generated("by gapic-generator")
@BetaApi("A restructuring of stub classes is planned, so this may break in the future")
public class GrpcIamCredentialsStub extends IamCredentialsStub {

  private static final MethodDescriptor<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
      generateAccessTokenMethodDescriptor =
          MethodDescriptor.<GenerateAccessTokenRequest, GenerateAccessTokenResponse>newBuilder()
              .setType(MethodDescriptor.MethodType.UNARY)
              .setFullMethodName("google.iam.credentials.v1.IAMCredentials/GenerateAccessToken")
              .setRequestMarshaller(
                  ProtoUtils.marshaller(GenerateAccessTokenRequest.getDefaultInstance()))
              .setResponseMarshaller(
                  ProtoUtils.marshaller(GenerateAccessTokenResponse.getDefaultInstance()))
              .build();
  private static final MethodDescriptor<GenerateIdTokenRequest, GenerateIdTokenResponse>
      generateIdTokenMethodDescriptor =
          MethodDescriptor.<GenerateIdTokenRequest, GenerateIdTokenResponse>newBuilder()
              .setType(MethodDescriptor.MethodType.UNARY)
              .setFullMethodName("google.iam.credentials.v1.IAMCredentials/GenerateIdToken")
              .setRequestMarshaller(
                  ProtoUtils.marshaller(GenerateIdTokenRequest.getDefaultInstance()))
              .setResponseMarshaller(
                  ProtoUtils.marshaller(GenerateIdTokenResponse.getDefaultInstance()))
              .build();
  private static final MethodDescriptor<SignBlobRequest, SignBlobResponse>
      signBlobMethodDescriptor =
          MethodDescriptor.<SignBlobRequest, SignBlobResponse>newBuilder()
              .setType(MethodDescriptor.MethodType.UNARY)
              .setFullMethodName("google.iam.credentials.v1.IAMCredentials/SignBlob")
              .setRequestMarshaller(ProtoUtils.marshaller(SignBlobRequest.getDefaultInstance()))
              .setResponseMarshaller(ProtoUtils.marshaller(SignBlobResponse.getDefaultInstance()))
              .build();
  private static final MethodDescriptor<SignJwtRequest, SignJwtResponse> signJwtMethodDescriptor =
      MethodDescriptor.<SignJwtRequest, SignJwtResponse>newBuilder()
          .setType(MethodDescriptor.MethodType.UNARY)
          .setFullMethodName("google.iam.credentials.v1.IAMCredentials/SignJwt")
          .setRequestMarshaller(ProtoUtils.marshaller(SignJwtRequest.getDefaultInstance()))
          .setResponseMarshaller(ProtoUtils.marshaller(SignJwtResponse.getDefaultInstance()))
          .build();
  private static final MethodDescriptor<
          GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
      generateIdentityBindingAccessTokenMethodDescriptor =
          MethodDescriptor
              .<GenerateIdentityBindingAccessTokenRequest,
                  GenerateIdentityBindingAccessTokenResponse>
                  newBuilder()
              .setType(MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(
                  "google.iam.credentials.v1.IAMCredentials/GenerateIdentityBindingAccessToken")
              .setRequestMarshaller(
                  ProtoUtils.marshaller(
                      GenerateIdentityBindingAccessTokenRequest.getDefaultInstance()))
              .setResponseMarshaller(
                  ProtoUtils.marshaller(
                      GenerateIdentityBindingAccessTokenResponse.getDefaultInstance()))
              .build();

  private final BackgroundResource backgroundResources;

  private final UnaryCallable<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
      generateAccessTokenCallable;
  private final UnaryCallable<GenerateIdTokenRequest, GenerateIdTokenResponse>
      generateIdTokenCallable;
  private final UnaryCallable<SignBlobRequest, SignBlobResponse> signBlobCallable;
  private final UnaryCallable<SignJwtRequest, SignJwtResponse> signJwtCallable;
  private final UnaryCallable<
          GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
      generateIdentityBindingAccessTokenCallable;

  private final GrpcStubCallableFactory callableFactory;

  public static final GrpcIamCredentialsStub create(IamCredentialsStubSettings settings)
      throws IOException {
    return new GrpcIamCredentialsStub(settings, ClientContext.create(settings));
  }

  public static final GrpcIamCredentialsStub create(ClientContext clientContext)
      throws IOException {
    return new GrpcIamCredentialsStub(
        IamCredentialsStubSettings.newBuilder().build(), clientContext);
  }

  public static final GrpcIamCredentialsStub create(
      ClientContext clientContext, GrpcStubCallableFactory callableFactory) throws IOException {
    return new GrpcIamCredentialsStub(
        IamCredentialsStubSettings.newBuilder().build(), clientContext, callableFactory);
  }

  /**
   * Constructs an instance of GrpcIamCredentialsStub, using the given settings. This is protected
   * so that it is easy to make a subclass, but otherwise, the static factory methods should be
   * preferred.
   */
  protected GrpcIamCredentialsStub(IamCredentialsStubSettings settings, ClientContext clientContext)
      throws IOException {
    this(settings, clientContext, new GrpcIamCredentialsCallableFactory());
  }

  /**
   * Constructs an instance of GrpcIamCredentialsStub, using the given settings. This is protected
   * so that it is easy to make a subclass, but otherwise, the static factory methods should be
   * preferred.
   */
  protected GrpcIamCredentialsStub(
      IamCredentialsStubSettings settings,
      ClientContext clientContext,
      GrpcStubCallableFactory callableFactory)
      throws IOException {
    this.callableFactory = callableFactory;

    GrpcCallSettings<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
        generateAccessTokenTransportSettings =
            GrpcCallSettings.<GenerateAccessTokenRequest, GenerateAccessTokenResponse>newBuilder()
                .setMethodDescriptor(generateAccessTokenMethodDescriptor)
                .build();
    GrpcCallSettings<GenerateIdTokenRequest, GenerateIdTokenResponse>
        generateIdTokenTransportSettings =
            GrpcCallSettings.<GenerateIdTokenRequest, GenerateIdTokenResponse>newBuilder()
                .setMethodDescriptor(generateIdTokenMethodDescriptor)
                .build();
    GrpcCallSettings<SignBlobRequest, SignBlobResponse> signBlobTransportSettings =
        GrpcCallSettings.<SignBlobRequest, SignBlobResponse>newBuilder()
            .setMethodDescriptor(signBlobMethodDescriptor)
            .build();
    GrpcCallSettings<SignJwtRequest, SignJwtResponse> signJwtTransportSettings =
        GrpcCallSettings.<SignJwtRequest, SignJwtResponse>newBuilder()
            .setMethodDescriptor(signJwtMethodDescriptor)
            .build();
    GrpcCallSettings<
            GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
        generateIdentityBindingAccessTokenTransportSettings =
            GrpcCallSettings
                .<GenerateIdentityBindingAccessTokenRequest,
                    GenerateIdentityBindingAccessTokenResponse>
                    newBuilder()
                .setMethodDescriptor(generateIdentityBindingAccessTokenMethodDescriptor)
                .build();

    this.generateAccessTokenCallable =
        callableFactory.createUnaryCallable(
            generateAccessTokenTransportSettings,
            settings.generateAccessTokenSettings(),
            clientContext);
    this.generateIdTokenCallable =
        callableFactory.createUnaryCallable(
            generateIdTokenTransportSettings, settings.generateIdTokenSettings(), clientContext);
    this.signBlobCallable =
        callableFactory.createUnaryCallable(
            signBlobTransportSettings, settings.signBlobSettings(), clientContext);
    this.signJwtCallable =
        callableFactory.createUnaryCallable(
            signJwtTransportSettings, settings.signJwtSettings(), clientContext);
    this.generateIdentityBindingAccessTokenCallable =
        callableFactory.createUnaryCallable(
            generateIdentityBindingAccessTokenTransportSettings,
            settings.generateIdentityBindingAccessTokenSettings(),
            clientContext);

    backgroundResources = new BackgroundResourceAggregation(clientContext.getBackgroundResources());
  }

  public UnaryCallable<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
      generateAccessTokenCallable() {
    return generateAccessTokenCallable;
  }

  public UnaryCallable<GenerateIdTokenRequest, GenerateIdTokenResponse> generateIdTokenCallable() {
    return generateIdTokenCallable;
  }

  public UnaryCallable<SignBlobRequest, SignBlobResponse> signBlobCallable() {
    return signBlobCallable;
  }

  public UnaryCallable<SignJwtRequest, SignJwtResponse> signJwtCallable() {
    return signJwtCallable;
  }

  public UnaryCallable<
          GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
      generateIdentityBindingAccessTokenCallable() {
    return generateIdentityBindingAccessTokenCallable;
  }

  @Override
  public final void close() {
    shutdown();
  }

  @Override
  public void shutdown() {
    backgroundResources.shutdown();
  }

  @Override
  public boolean isShutdown() {
    return backgroundResources.isShutdown();
  }

  @Override
  public boolean isTerminated() {
    return backgroundResources.isTerminated();
  }

  @Override
  public void shutdownNow() {
    backgroundResources.shutdownNow();
  }

  @Override
  public boolean awaitTermination(long duration, TimeUnit unit) throws InterruptedException {
    return backgroundResources.awaitTermination(duration, unit);
  }
}
