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
import javax.annotation.Generated;

// AUTO-GENERATED DOCUMENTATION AND CLASS
/**
 * Base stub class for IAM Service Account Credentials API.
 *
 * <p>This class is for advanced usage and reflects the underlying API directly.
 */
@Generated("by gapic-generator")
@BetaApi("A restructuring of stub classes is planned, so this may break in the future")
public abstract class IamCredentialsStub implements BackgroundResource {

  public UnaryCallable<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
      generateAccessTokenCallable() {
    throw new UnsupportedOperationException("Not implemented: generateAccessTokenCallable()");
  }

  public UnaryCallable<GenerateIdTokenRequest, GenerateIdTokenResponse> generateIdTokenCallable() {
    throw new UnsupportedOperationException("Not implemented: generateIdTokenCallable()");
  }

  public UnaryCallable<SignBlobRequest, SignBlobResponse> signBlobCallable() {
    throw new UnsupportedOperationException("Not implemented: signBlobCallable()");
  }

  public UnaryCallable<SignJwtRequest, SignJwtResponse> signJwtCallable() {
    throw new UnsupportedOperationException("Not implemented: signJwtCallable()");
  }

  public UnaryCallable<
          GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
      generateIdentityBindingAccessTokenCallable() {
    throw new UnsupportedOperationException(
        "Not implemented: generateIdentityBindingAccessTokenCallable()");
  }

  @Override
  public abstract void close();
}
