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

import com.google.api.core.ApiFunction;
import com.google.api.core.BetaApi;
import com.google.api.gax.core.GaxProperties;
import com.google.api.gax.core.GoogleCredentialsProvider;
import com.google.api.gax.core.InstantiatingExecutorProvider;
import com.google.api.gax.grpc.GaxGrpcProperties;
import com.google.api.gax.grpc.GrpcTransportChannel;
import com.google.api.gax.grpc.InstantiatingGrpcChannelProvider;
import com.google.api.gax.retrying.RetrySettings;
import com.google.api.gax.rpc.ApiClientHeaderProvider;
import com.google.api.gax.rpc.ClientContext;
import com.google.api.gax.rpc.StatusCode;
import com.google.api.gax.rpc.StubSettings;
import com.google.api.gax.rpc.TransportChannelProvider;
import com.google.api.gax.rpc.UnaryCallSettings;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableMap;
import com.google.common.collect.ImmutableSet;
import com.google.common.collect.Lists;
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
import org.threeten.bp.Duration;

// AUTO-GENERATED DOCUMENTATION AND CLASS
/**
 * Settings class to configure an instance of {@link IamCredentialsStub}.
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
 * IamCredentialsStubSettings.Builder iamCredentialsSettingsBuilder =
 *     IamCredentialsStubSettings.newBuilder();
 * iamCredentialsSettingsBuilder.generateAccessTokenSettings().getRetrySettings().toBuilder()
 *     .setTotalTimeout(Duration.ofSeconds(30));
 * IamCredentialsStubSettings iamCredentialsSettings = iamCredentialsSettingsBuilder.build();
 * </code>
 * </pre>
 */
@Generated("by gapic-generator")
@BetaApi
public class IamCredentialsStubSettings extends StubSettings<IamCredentialsStubSettings> {
  /** The default scopes of the service. */
  private static final ImmutableList<String> DEFAULT_SERVICE_SCOPES =
      ImmutableList.<String>builder().add("https://www.googleapis.com/auth/cloud-platform").build();

  private final UnaryCallSettings<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
      generateAccessTokenSettings;
  private final UnaryCallSettings<GenerateIdTokenRequest, GenerateIdTokenResponse>
      generateIdTokenSettings;
  private final UnaryCallSettings<SignBlobRequest, SignBlobResponse> signBlobSettings;
  private final UnaryCallSettings<SignJwtRequest, SignJwtResponse> signJwtSettings;
  private final UnaryCallSettings<
          GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
      generateIdentityBindingAccessTokenSettings;

  /** Returns the object with the settings used for calls to generateAccessToken. */
  public UnaryCallSettings<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
      generateAccessTokenSettings() {
    return generateAccessTokenSettings;
  }

  /** Returns the object with the settings used for calls to generateIdToken. */
  public UnaryCallSettings<GenerateIdTokenRequest, GenerateIdTokenResponse>
      generateIdTokenSettings() {
    return generateIdTokenSettings;
  }

  /** Returns the object with the settings used for calls to signBlob. */
  public UnaryCallSettings<SignBlobRequest, SignBlobResponse> signBlobSettings() {
    return signBlobSettings;
  }

  /** Returns the object with the settings used for calls to signJwt. */
  public UnaryCallSettings<SignJwtRequest, SignJwtResponse> signJwtSettings() {
    return signJwtSettings;
  }

  /** Returns the object with the settings used for calls to generateIdentityBindingAccessToken. */
  public UnaryCallSettings<
          GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
      generateIdentityBindingAccessTokenSettings() {
    return generateIdentityBindingAccessTokenSettings;
  }

  @BetaApi("A restructuring of stub classes is planned, so this may break in the future")
  public IamCredentialsStub createStub() throws IOException {
    if (getTransportChannelProvider()
        .getTransportName()
        .equals(GrpcTransportChannel.getGrpcTransportName())) {
      return GrpcIamCredentialsStub.create(this);
    } else {
      throw new UnsupportedOperationException(
          "Transport not supported: " + getTransportChannelProvider().getTransportName());
    }
  }

  /** Returns a builder for the default ExecutorProvider for this service. */
  public static InstantiatingExecutorProvider.Builder defaultExecutorProviderBuilder() {
    return InstantiatingExecutorProvider.newBuilder();
  }

  /** Returns the default service endpoint. */
  public static String getDefaultEndpoint() {
    return "iamcredentials.googleapis.com:443";
  }

  /** Returns the default service scopes. */
  public static List<String> getDefaultServiceScopes() {
    return DEFAULT_SERVICE_SCOPES;
  }

  /** Returns a builder for the default credentials for this service. */
  public static GoogleCredentialsProvider.Builder defaultCredentialsProviderBuilder() {
    return GoogleCredentialsProvider.newBuilder().setScopesToApply(DEFAULT_SERVICE_SCOPES);
  }

  /** Returns a builder for the default ChannelProvider for this service. */
  public static InstantiatingGrpcChannelProvider.Builder defaultGrpcTransportProviderBuilder() {
    return InstantiatingGrpcChannelProvider.newBuilder();
  }

  public static TransportChannelProvider defaultTransportChannelProvider() {
    return defaultGrpcTransportProviderBuilder().build();
  }

  @BetaApi("The surface for customizing headers is not stable yet and may change in the future.")
  public static ApiClientHeaderProvider.Builder defaultApiClientHeaderProviderBuilder() {
    return ApiClientHeaderProvider.newBuilder()
        .setGeneratedLibToken(
            "gapic", GaxProperties.getLibraryVersion(IamCredentialsStubSettings.class))
        .setTransportToken(
            GaxGrpcProperties.getGrpcTokenName(), GaxGrpcProperties.getGrpcVersion());
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

  protected IamCredentialsStubSettings(Builder settingsBuilder) throws IOException {
    super(settingsBuilder);

    generateAccessTokenSettings = settingsBuilder.generateAccessTokenSettings().build();
    generateIdTokenSettings = settingsBuilder.generateIdTokenSettings().build();
    signBlobSettings = settingsBuilder.signBlobSettings().build();
    signJwtSettings = settingsBuilder.signJwtSettings().build();
    generateIdentityBindingAccessTokenSettings =
        settingsBuilder.generateIdentityBindingAccessTokenSettings().build();
  }

  /** Builder for IamCredentialsStubSettings. */
  public static class Builder extends StubSettings.Builder<IamCredentialsStubSettings, Builder> {
    private final ImmutableList<UnaryCallSettings.Builder<?, ?>> unaryMethodSettingsBuilders;

    private final UnaryCallSettings.Builder<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
        generateAccessTokenSettings;
    private final UnaryCallSettings.Builder<GenerateIdTokenRequest, GenerateIdTokenResponse>
        generateIdTokenSettings;
    private final UnaryCallSettings.Builder<SignBlobRequest, SignBlobResponse> signBlobSettings;
    private final UnaryCallSettings.Builder<SignJwtRequest, SignJwtResponse> signJwtSettings;
    private final UnaryCallSettings.Builder<
            GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
        generateIdentityBindingAccessTokenSettings;

    private static final ImmutableMap<String, ImmutableSet<StatusCode.Code>>
        RETRYABLE_CODE_DEFINITIONS;

    static {
      ImmutableMap.Builder<String, ImmutableSet<StatusCode.Code>> definitions =
          ImmutableMap.builder();
      definitions.put(
          "idempotent",
          ImmutableSet.copyOf(
              Lists.<StatusCode.Code>newArrayList(
                  StatusCode.Code.DEADLINE_EXCEEDED, StatusCode.Code.UNAVAILABLE)));
      definitions.put("non_idempotent", ImmutableSet.copyOf(Lists.<StatusCode.Code>newArrayList()));
      RETRYABLE_CODE_DEFINITIONS = definitions.build();
    }

    private static final ImmutableMap<String, RetrySettings> RETRY_PARAM_DEFINITIONS;

    static {
      ImmutableMap.Builder<String, RetrySettings> definitions = ImmutableMap.builder();
      RetrySettings settings = null;
      settings =
          RetrySettings.newBuilder()
              .setInitialRetryDelay(Duration.ofMillis(100L))
              .setRetryDelayMultiplier(1.3)
              .setMaxRetryDelay(Duration.ofMillis(60000L))
              .setInitialRpcTimeout(Duration.ofMillis(20000L))
              .setRpcTimeoutMultiplier(1.0)
              .setMaxRpcTimeout(Duration.ofMillis(20000L))
              .setTotalTimeout(Duration.ofMillis(600000L))
              .build();
      definitions.put("default", settings);
      RETRY_PARAM_DEFINITIONS = definitions.build();
    }

    protected Builder() {
      this((ClientContext) null);
    }

    protected Builder(ClientContext clientContext) {
      super(clientContext);

      generateAccessTokenSettings = UnaryCallSettings.newUnaryCallSettingsBuilder();

      generateIdTokenSettings = UnaryCallSettings.newUnaryCallSettingsBuilder();

      signBlobSettings = UnaryCallSettings.newUnaryCallSettingsBuilder();

      signJwtSettings = UnaryCallSettings.newUnaryCallSettingsBuilder();

      generateIdentityBindingAccessTokenSettings = UnaryCallSettings.newUnaryCallSettingsBuilder();

      unaryMethodSettingsBuilders =
          ImmutableList.<UnaryCallSettings.Builder<?, ?>>of(
              generateAccessTokenSettings,
              generateIdTokenSettings,
              signBlobSettings,
              signJwtSettings,
              generateIdentityBindingAccessTokenSettings);

      initDefaults(this);
    }

    private static Builder createDefault() {
      Builder builder = new Builder((ClientContext) null);
      builder.setTransportChannelProvider(defaultTransportChannelProvider());
      builder.setCredentialsProvider(defaultCredentialsProviderBuilder().build());
      builder.setInternalHeaderProvider(defaultApiClientHeaderProviderBuilder().build());
      builder.setEndpoint(getDefaultEndpoint());
      return initDefaults(builder);
    }

    private static Builder initDefaults(Builder builder) {

      builder
          .generateAccessTokenSettings()
          .setRetryableCodes(RETRYABLE_CODE_DEFINITIONS.get("idempotent"))
          .setRetrySettings(RETRY_PARAM_DEFINITIONS.get("default"));

      builder
          .generateIdTokenSettings()
          .setRetryableCodes(RETRYABLE_CODE_DEFINITIONS.get("idempotent"))
          .setRetrySettings(RETRY_PARAM_DEFINITIONS.get("default"));

      builder
          .signBlobSettings()
          .setRetryableCodes(RETRYABLE_CODE_DEFINITIONS.get("idempotent"))
          .setRetrySettings(RETRY_PARAM_DEFINITIONS.get("default"));

      builder
          .signJwtSettings()
          .setRetryableCodes(RETRYABLE_CODE_DEFINITIONS.get("idempotent"))
          .setRetrySettings(RETRY_PARAM_DEFINITIONS.get("default"));

      builder
          .generateIdentityBindingAccessTokenSettings()
          .setRetryableCodes(RETRYABLE_CODE_DEFINITIONS.get("idempotent"))
          .setRetrySettings(RETRY_PARAM_DEFINITIONS.get("default"));

      return builder;
    }

    protected Builder(IamCredentialsStubSettings settings) {
      super(settings);

      generateAccessTokenSettings = settings.generateAccessTokenSettings.toBuilder();
      generateIdTokenSettings = settings.generateIdTokenSettings.toBuilder();
      signBlobSettings = settings.signBlobSettings.toBuilder();
      signJwtSettings = settings.signJwtSettings.toBuilder();
      generateIdentityBindingAccessTokenSettings =
          settings.generateIdentityBindingAccessTokenSettings.toBuilder();

      unaryMethodSettingsBuilders =
          ImmutableList.<UnaryCallSettings.Builder<?, ?>>of(
              generateAccessTokenSettings,
              generateIdTokenSettings,
              signBlobSettings,
              signJwtSettings,
              generateIdentityBindingAccessTokenSettings);
    }

    // NEXT_MAJOR_VER: remove 'throws Exception'
    /**
     * Applies the given settings updater function to all of the unary API methods in this service.
     *
     * <p>Note: This method does not support applying settings to streaming methods.
     */
    public Builder applyToAllUnaryMethods(
        ApiFunction<UnaryCallSettings.Builder<?, ?>, Void> settingsUpdater) throws Exception {
      super.applyToAllUnaryMethods(unaryMethodSettingsBuilders, settingsUpdater);
      return this;
    }

    public ImmutableList<UnaryCallSettings.Builder<?, ?>> unaryMethodSettingsBuilders() {
      return unaryMethodSettingsBuilders;
    }

    /** Returns the builder for the settings used for calls to generateAccessToken. */
    public UnaryCallSettings.Builder<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
        generateAccessTokenSettings() {
      return generateAccessTokenSettings;
    }

    /** Returns the builder for the settings used for calls to generateIdToken. */
    public UnaryCallSettings.Builder<GenerateIdTokenRequest, GenerateIdTokenResponse>
        generateIdTokenSettings() {
      return generateIdTokenSettings;
    }

    /** Returns the builder for the settings used for calls to signBlob. */
    public UnaryCallSettings.Builder<SignBlobRequest, SignBlobResponse> signBlobSettings() {
      return signBlobSettings;
    }

    /** Returns the builder for the settings used for calls to signJwt. */
    public UnaryCallSettings.Builder<SignJwtRequest, SignJwtResponse> signJwtSettings() {
      return signJwtSettings;
    }

    /**
     * Returns the builder for the settings used for calls to generateIdentityBindingAccessToken.
     */
    public UnaryCallSettings.Builder<
            GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
        generateIdentityBindingAccessTokenSettings() {
      return generateIdentityBindingAccessTokenSettings;
    }

    @Override
    public IamCredentialsStubSettings build() throws IOException {
      return new IamCredentialsStubSettings(this);
    }
  }
}
