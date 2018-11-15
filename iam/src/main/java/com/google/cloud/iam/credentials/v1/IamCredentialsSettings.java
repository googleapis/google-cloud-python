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

import com.google.api.core.ApiFunction;
import com.google.api.core.BetaApi;
import com.google.api.gax.core.GoogleCredentialsProvider;
import com.google.api.gax.core.InstantiatingExecutorProvider;
import com.google.api.gax.grpc.InstantiatingGrpcChannelProvider;
import com.google.api.gax.rpc.ApiClientHeaderProvider;
import com.google.api.gax.rpc.ClientContext;
import com.google.api.gax.rpc.ClientSettings;
import com.google.api.gax.rpc.TransportChannelProvider;
import com.google.api.gax.rpc.UnaryCallSettings;
import com.google.cloud.iam.credentials.v1.stub.IamCredentialsStubSettings;
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
import java.io.IOException;
import java.util.List;
import javax.annotation.Generated;

// AUTO-GENERATED DOCUMENTATION AND CLASS
/**
 * Settings class to configure an instance of {@link IamCredentialsClient}.
 *
 * <p>The default instance has everything set to sensible defaults:
 *
 * <ul>
 *   <li>The default service address (iamcredentials.googleapis.com) and default port (443) are
 *       used.
 *   <li>Credentials are acquired automatically through Application Default Credentials.
 *   <li>Retries are configured for idempotent methods but not for non-idempotent methods.
 * </ul>
 *
 * <p>The builder of this class is recursive, so contained classes are themselves builders. When
 * build() is called, the tree of builders is called to create the complete settings object. For
 * example, to set the total timeout of generateAccessToken to 30 seconds:
 *
 * <pre>
 * <code>
 * IamCredentialsSettings.Builder iamCredentialsSettingsBuilder =
 *     IamCredentialsSettings.newBuilder();
 * iamCredentialsSettingsBuilder.generateAccessTokenSettings().getRetrySettings().toBuilder()
 *     .setTotalTimeout(Duration.ofSeconds(30));
 * IamCredentialsSettings iamCredentialsSettings = iamCredentialsSettingsBuilder.build();
 * </code>
 * </pre>
 */
@Generated("by gapic-generator")
@BetaApi
public class IamCredentialsSettings extends ClientSettings<IamCredentialsSettings> {
  /** Returns the object with the settings used for calls to generateAccessToken. */
  public UnaryCallSettings<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
      generateAccessTokenSettings() {
    return ((IamCredentialsStubSettings) getStubSettings()).generateAccessTokenSettings();
  }

  /** Returns the object with the settings used for calls to generateIdToken. */
  public UnaryCallSettings<GenerateIdTokenRequest, GenerateIdTokenResponse>
      generateIdTokenSettings() {
    return ((IamCredentialsStubSettings) getStubSettings()).generateIdTokenSettings();
  }

  /** Returns the object with the settings used for calls to signBlob. */
  public UnaryCallSettings<SignBlobRequest, SignBlobResponse> signBlobSettings() {
    return ((IamCredentialsStubSettings) getStubSettings()).signBlobSettings();
  }

  /** Returns the object with the settings used for calls to signJwt. */
  public UnaryCallSettings<SignJwtRequest, SignJwtResponse> signJwtSettings() {
    return ((IamCredentialsStubSettings) getStubSettings()).signJwtSettings();
  }

  /** Returns the object with the settings used for calls to generateIdentityBindingAccessToken. */
  public UnaryCallSettings<
          GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
      generateIdentityBindingAccessTokenSettings() {
    return ((IamCredentialsStubSettings) getStubSettings())
        .generateIdentityBindingAccessTokenSettings();
  }

  public static final IamCredentialsSettings create(IamCredentialsStubSettings stub)
      throws IOException {
    return new IamCredentialsSettings.Builder(stub.toBuilder()).build();
  }

  /** Returns a builder for the default ExecutorProvider for this service. */
  public static InstantiatingExecutorProvider.Builder defaultExecutorProviderBuilder() {
    return IamCredentialsStubSettings.defaultExecutorProviderBuilder();
  }

  /** Returns the default service endpoint. */
  public static String getDefaultEndpoint() {
    return IamCredentialsStubSettings.getDefaultEndpoint();
  }

  /** Returns the default service scopes. */
  public static List<String> getDefaultServiceScopes() {
    return IamCredentialsStubSettings.getDefaultServiceScopes();
  }

  /** Returns a builder for the default credentials for this service. */
  public static GoogleCredentialsProvider.Builder defaultCredentialsProviderBuilder() {
    return IamCredentialsStubSettings.defaultCredentialsProviderBuilder();
  }

  /** Returns a builder for the default ChannelProvider for this service. */
  public static InstantiatingGrpcChannelProvider.Builder defaultGrpcTransportProviderBuilder() {
    return IamCredentialsStubSettings.defaultGrpcTransportProviderBuilder();
  }

  public static TransportChannelProvider defaultTransportChannelProvider() {
    return IamCredentialsStubSettings.defaultTransportChannelProvider();
  }

  @BetaApi("The surface for customizing headers is not stable yet and may change in the future.")
  public static ApiClientHeaderProvider.Builder defaultApiClientHeaderProviderBuilder() {
    return IamCredentialsStubSettings.defaultApiClientHeaderProviderBuilder();
  }

  /** Returns a new builder for this class. */
  public static Builder newBuilder() {
    return Builder.createDefault();
  }

  /** Returns a new builder for this class. */
  public static Builder newBuilder(ClientContext clientContext) {
    return new Builder(clientContext);
  }

  /** Returns a builder containing all the values of this settings class. */
  public Builder toBuilder() {
    return new Builder(this);
  }

  protected IamCredentialsSettings(Builder settingsBuilder) throws IOException {
    super(settingsBuilder);
  }

  /** Builder for IamCredentialsSettings. */
  public static class Builder extends ClientSettings.Builder<IamCredentialsSettings, Builder> {
    protected Builder() throws IOException {
      this((ClientContext) null);
    }

    protected Builder(ClientContext clientContext) {
      super(IamCredentialsStubSettings.newBuilder(clientContext));
    }

    private static Builder createDefault() {
      return new Builder(IamCredentialsStubSettings.newBuilder());
    }

    protected Builder(IamCredentialsSettings settings) {
      super(settings.getStubSettings().toBuilder());
    }

    protected Builder(IamCredentialsStubSettings.Builder stubSettings) {
      super(stubSettings);
    }

    public IamCredentialsStubSettings.Builder getStubSettingsBuilder() {
      return ((IamCredentialsStubSettings.Builder) getStubSettings());
    }

    // NEXT_MAJOR_VER: remove 'throws Exception'
    /**
     * Applies the given settings updater function to all of the unary API methods in this service.
     *
     * <p>Note: This method does not support applying settings to streaming methods.
     */
    public Builder applyToAllUnaryMethods(
        ApiFunction<UnaryCallSettings.Builder<?, ?>, Void> settingsUpdater) throws Exception {
      super.applyToAllUnaryMethods(
          getStubSettingsBuilder().unaryMethodSettingsBuilders(), settingsUpdater);
      return this;
    }

    /** Returns the builder for the settings used for calls to generateAccessToken. */
    public UnaryCallSettings.Builder<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
        generateAccessTokenSettings() {
      return getStubSettingsBuilder().generateAccessTokenSettings();
    }

    /** Returns the builder for the settings used for calls to generateIdToken. */
    public UnaryCallSettings.Builder<GenerateIdTokenRequest, GenerateIdTokenResponse>
        generateIdTokenSettings() {
      return getStubSettingsBuilder().generateIdTokenSettings();
    }

    /** Returns the builder for the settings used for calls to signBlob. */
    public UnaryCallSettings.Builder<SignBlobRequest, SignBlobResponse> signBlobSettings() {
      return getStubSettingsBuilder().signBlobSettings();
    }

    /** Returns the builder for the settings used for calls to signJwt. */
    public UnaryCallSettings.Builder<SignJwtRequest, SignJwtResponse> signJwtSettings() {
      return getStubSettingsBuilder().signJwtSettings();
    }

    /**
     * Returns the builder for the settings used for calls to generateIdentityBindingAccessToken.
     */
    public UnaryCallSettings.Builder<
            GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
        generateIdentityBindingAccessTokenSettings() {
      return getStubSettingsBuilder().generateIdentityBindingAccessTokenSettings();
    }

    @Override
    public IamCredentialsSettings build() throws IOException {
      return new IamCredentialsSettings(this);
    }
  }
}
