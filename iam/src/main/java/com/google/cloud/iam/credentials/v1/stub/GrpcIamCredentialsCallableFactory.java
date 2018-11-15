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
import com.google.api.gax.grpc.GrpcCallSettings;
import com.google.api.gax.grpc.GrpcCallableFactory;
import com.google.api.gax.grpc.GrpcStubCallableFactory;
import com.google.api.gax.rpc.BatchingCallSettings;
import com.google.api.gax.rpc.BidiStreamingCallable;
import com.google.api.gax.rpc.ClientContext;
import com.google.api.gax.rpc.ClientStreamingCallable;
import com.google.api.gax.rpc.OperationCallSettings;
import com.google.api.gax.rpc.OperationCallable;
import com.google.api.gax.rpc.PagedCallSettings;
import com.google.api.gax.rpc.ServerStreamingCallSettings;
import com.google.api.gax.rpc.ServerStreamingCallable;
import com.google.api.gax.rpc.StreamingCallSettings;
import com.google.api.gax.rpc.UnaryCallSettings;
import com.google.api.gax.rpc.UnaryCallable;
import com.google.longrunning.Operation;
import com.google.longrunning.stub.OperationsStub;
import javax.annotation.Generated;

// AUTO-GENERATED DOCUMENTATION AND CLASS
/**
 * gRPC callable factory implementation for IAM Service Account Credentials API.
 *
 * <p>This class is for advanced usage.
 */
@Generated("by gapic-generator")
@BetaApi("The surface for use by generated code is not stable yet and may change in the future.")
public class GrpcIamCredentialsCallableFactory implements GrpcStubCallableFactory {
  @Override
  public <RequestT, ResponseT> UnaryCallable<RequestT, ResponseT> createUnaryCallable(
      GrpcCallSettings<RequestT, ResponseT> grpcCallSettings,
      UnaryCallSettings<RequestT, ResponseT> callSettings,
      ClientContext clientContext) {
    return GrpcCallableFactory.createUnaryCallable(grpcCallSettings, callSettings, clientContext);
  }

  @Override
  public <RequestT, ResponseT, PagedListResponseT>
      UnaryCallable<RequestT, PagedListResponseT> createPagedCallable(
          GrpcCallSettings<RequestT, ResponseT> grpcCallSettings,
          PagedCallSettings<RequestT, ResponseT, PagedListResponseT> pagedCallSettings,
          ClientContext clientContext) {
    return GrpcCallableFactory.createPagedCallable(
        grpcCallSettings, pagedCallSettings, clientContext);
  }

  @Override
  public <RequestT, ResponseT> UnaryCallable<RequestT, ResponseT> createBatchingCallable(
      GrpcCallSettings<RequestT, ResponseT> grpcCallSettings,
      BatchingCallSettings<RequestT, ResponseT> batchingCallSettings,
      ClientContext clientContext) {
    return GrpcCallableFactory.createBatchingCallable(
        grpcCallSettings, batchingCallSettings, clientContext);
  }

  @BetaApi(
      "The surface for long-running operations is not stable yet and may change in the future.")
  @Override
  public <RequestT, ResponseT, MetadataT>
      OperationCallable<RequestT, ResponseT, MetadataT> createOperationCallable(
          GrpcCallSettings<RequestT, com.google.longrunning.Operation> grpcCallSettings,
          OperationCallSettings<RequestT, ResponseT, MetadataT> operationCallSettings,
          ClientContext clientContext,
          OperationsStub operationsStub) {
    return GrpcCallableFactory.createOperationCallable(
        grpcCallSettings, operationCallSettings, clientContext, operationsStub);
  }

  @Override
  public <RequestT, ResponseT>
      BidiStreamingCallable<RequestT, ResponseT> createBidiStreamingCallable(
          GrpcCallSettings<RequestT, ResponseT> grpcCallSettings,
          StreamingCallSettings<RequestT, ResponseT> streamingCallSettings,
          ClientContext clientContext) {
    return GrpcCallableFactory.createBidiStreamingCallable(
        grpcCallSettings, streamingCallSettings, clientContext);
  }

  @Override
  public <RequestT, ResponseT>
      ServerStreamingCallable<RequestT, ResponseT> createServerStreamingCallable(
          GrpcCallSettings<RequestT, ResponseT> grpcCallSettings,
          ServerStreamingCallSettings<RequestT, ResponseT> streamingCallSettings,
          ClientContext clientContext) {
    return GrpcCallableFactory.createServerStreamingCallable(
        grpcCallSettings, streamingCallSettings, clientContext);
  }

  @Override
  public <RequestT, ResponseT>
      ClientStreamingCallable<RequestT, ResponseT> createClientStreamingCallable(
          GrpcCallSettings<RequestT, ResponseT> grpcCallSettings,
          StreamingCallSettings<RequestT, ResponseT> streamingCallSettings,
          ClientContext clientContext) {
    return GrpcCallableFactory.createClientStreamingCallable(
        grpcCallSettings, streamingCallSettings, clientContext);
  }
}
