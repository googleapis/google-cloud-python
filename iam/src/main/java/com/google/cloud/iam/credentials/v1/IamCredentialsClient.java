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
import com.google.api.gax.core.BackgroundResource;
import com.google.api.gax.rpc.UnaryCallable;
import com.google.api.pathtemplate.PathTemplate;
import com.google.cloud.iam.credentials.v1.stub.IamCredentialsStub;
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
import com.google.protobuf.ByteString;
import com.google.protobuf.Duration;
import java.io.IOException;
import java.util.List;
import java.util.concurrent.TimeUnit;
import javax.annotation.Generated;

// AUTO-GENERATED DOCUMENTATION AND SERVICE
/**
 * Service Description: A service account is a special type of Google account that belongs to your
 * application or a virtual machine (VM), instead of to an individual end user. Your application
 * assumes the identity of the service account to call Google APIs, so that the users aren't
 * directly involved.
 *
 * <p>Service account credentials are used to temporarily assume the identity of the service
 * account. Supported credential types include OAuth 2.0 access tokens, OpenID Connect ID tokens,
 * self-signed JSON Web Tokens (JWTs), and more.
 *
 * <p>This class provides the ability to make remote calls to the backing service through method
 * calls that map to API methods. Sample code to get started:
 *
 * <pre>
 * <code>
 * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
 *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
 *   List&lt;String&gt; delegates = new ArrayList&lt;&gt;();
 *   List&lt;String&gt; scope = new ArrayList&lt;&gt;();
 *   Duration lifetime = Duration.newBuilder().build();
 *   GenerateAccessTokenResponse response = iamCredentialsClient.generateAccessToken(formattedName, delegates, scope, lifetime);
 * }
 * </code>
 * </pre>
 *
 * <p>Note: close() needs to be called on the iamCredentialsClient object to clean up resources such
 * as threads. In the example above, try-with-resources is used, which automatically calls close().
 *
 * <p>The surface of this class includes several types of Java methods for each of the API's
 * methods:
 *
 * <ol>
 *   <li> A "flattened" method. With this type of method, the fields of the request type have been
 *       converted into function parameters. It may be the case that not all fields are available as
 *       parameters, and not every API method will have a flattened method entry point.
 *   <li> A "request object" method. This type of method only takes one parameter, a request object,
 *       which must be constructed before the call. Not every API method will have a request object
 *       method.
 *   <li> A "callable" method. This type of method takes no parameters and returns an immutable API
 *       callable object, which can be used to initiate calls to the service.
 * </ol>
 *
 * <p>See the individual methods for example code.
 *
 * <p>Many parameters require resource names to be formatted in a particular way. To assist with
 * these names, this class includes a format method for each type of name, and additionally a parse
 * method to extract the individual identifiers contained within names that are returned.
 *
 * <p>This class can be customized by passing in a custom instance of IamCredentialsSettings to
 * create(). For example:
 *
 * <p>To customize credentials:
 *
 * <pre>
 * <code>
 * IamCredentialsSettings iamCredentialsSettings =
 *     IamCredentialsSettings.newBuilder()
 *         .setCredentialsProvider(FixedCredentialsProvider.create(myCredentials))
 *         .build();
 * IamCredentialsClient iamCredentialsClient =
 *     IamCredentialsClient.create(iamCredentialsSettings);
 * </code>
 * </pre>
 *
 * To customize the endpoint:
 *
 * <pre>
 * <code>
 * IamCredentialsSettings iamCredentialsSettings =
 *     IamCredentialsSettings.newBuilder().setEndpoint(myEndpoint).build();
 * IamCredentialsClient iamCredentialsClient =
 *     IamCredentialsClient.create(iamCredentialsSettings);
 * </code>
 * </pre>
 */
@Generated("by gapic-generator")
@BetaApi
public class IamCredentialsClient implements BackgroundResource {
  private final IamCredentialsSettings settings;
  private final IamCredentialsStub stub;

  private static final PathTemplate SERVICE_ACCOUNT_PATH_TEMPLATE =
      PathTemplate.createWithoutUrlEncoding("projects/{project}/serviceAccounts/{service_account}");

  /**
   * Formats a string containing the fully-qualified path to represent a service_account resource.
   */
  public static final String formatServiceAccountName(String project, String serviceAccount) {
    return SERVICE_ACCOUNT_PATH_TEMPLATE.instantiate(
        "project", project,
        "service_account", serviceAccount);
  }

  /**
   * Parses the project from the given fully-qualified path which represents a service_account
   * resource.
   */
  public static final String parseProjectFromServiceAccountName(String serviceAccountName) {
    return SERVICE_ACCOUNT_PATH_TEMPLATE.parse(serviceAccountName).get("project");
  }

  /**
   * Parses the service_account from the given fully-qualified path which represents a
   * service_account resource.
   */
  public static final String parseServiceAccountFromServiceAccountName(String serviceAccountName) {
    return SERVICE_ACCOUNT_PATH_TEMPLATE.parse(serviceAccountName).get("service_account");
  }

  /** Constructs an instance of IamCredentialsClient with default settings. */
  public static final IamCredentialsClient create() throws IOException {
    return create(IamCredentialsSettings.newBuilder().build());
  }

  /**
   * Constructs an instance of IamCredentialsClient, using the given settings. The channels are
   * created based on the settings passed in, or defaults for any settings that are not set.
   */
  public static final IamCredentialsClient create(IamCredentialsSettings settings)
      throws IOException {
    return new IamCredentialsClient(settings);
  }

  /**
   * Constructs an instance of IamCredentialsClient, using the given stub for making calls. This is
   * for advanced usage - prefer to use IamCredentialsSettings}.
   */
  @BetaApi("A restructuring of stub classes is planned, so this may break in the future")
  public static final IamCredentialsClient create(IamCredentialsStub stub) {
    return new IamCredentialsClient(stub);
  }

  /**
   * Constructs an instance of IamCredentialsClient, using the given settings. This is protected so
   * that it is easy to make a subclass, but otherwise, the static factory methods should be
   * preferred.
   */
  protected IamCredentialsClient(IamCredentialsSettings settings) throws IOException {
    this.settings = settings;
    this.stub = ((IamCredentialsStubSettings) settings.getStubSettings()).createStub();
  }

  @BetaApi("A restructuring of stub classes is planned, so this may break in the future")
  protected IamCredentialsClient(IamCredentialsStub stub) {
    this.settings = null;
    this.stub = stub;
  }

  public final IamCredentialsSettings getSettings() {
    return settings;
  }

  @BetaApi("A restructuring of stub classes is planned, so this may break in the future")
  public IamCredentialsStub getStub() {
    return stub;
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Generates an OAuth 2.0 access token for a service account.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   List&lt;String&gt; delegates = new ArrayList&lt;&gt;();
   *   List&lt;String&gt; scope = new ArrayList&lt;&gt;();
   *   Duration lifetime = Duration.newBuilder().build();
   *   GenerateAccessTokenResponse response = iamCredentialsClient.generateAccessToken(formattedName, delegates, scope, lifetime);
   * }
   * </code></pre>
   *
   * @param name The resource name of the service account for which the credentials are requested,
   *     in the following format: `projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}`.
   * @param delegates The sequence of service accounts in a delegation chain. Each service account
   *     must be granted the `roles/iam.serviceAccountTokenCreator` role on its next service account
   *     in the chain. The last service account in the chain must be granted the
   *     `roles/iam.serviceAccountTokenCreator` role on the service account that is specified in the
   *     `name` field of the request.
   *     <p>The delegates must have the following format:
   *     `projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}`
   * @param scope Code to identify the scopes to be included in the OAuth 2.0 access token. See
   *     https://developers.google.com/identity/protocols/googlescopes for more information. At
   *     least one value required.
   * @param lifetime The desired lifetime duration of the access token in seconds. Must be set to a
   *     value less than or equal to 3600 (1 hour). If a value is not specified, the token's
   *     lifetime will be set to a default value of one hour.
   * @throws com.google.api.gax.rpc.ApiException if the remote call fails
   */
  public final GenerateAccessTokenResponse generateAccessToken(
      String name, List<String> delegates, List<String> scope, Duration lifetime) {
    SERVICE_ACCOUNT_PATH_TEMPLATE.validate(name, "generateAccessToken");
    GenerateAccessTokenRequest request =
        GenerateAccessTokenRequest.newBuilder()
            .setName(name)
            .addAllDelegates(delegates)
            .addAllScope(scope)
            .setLifetime(lifetime)
            .build();
    return generateAccessToken(request);
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Generates an OAuth 2.0 access token for a service account.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   List&lt;String&gt; scope = new ArrayList&lt;&gt;();
   *   GenerateAccessTokenRequest request = GenerateAccessTokenRequest.newBuilder()
   *     .setName(formattedName)
   *     .addAllScope(scope)
   *     .build();
   *   GenerateAccessTokenResponse response = iamCredentialsClient.generateAccessToken(request);
   * }
   * </code></pre>
   *
   * @param request The request object containing all of the parameters for the API call.
   * @throws com.google.api.gax.rpc.ApiException if the remote call fails
   */
  public final GenerateAccessTokenResponse generateAccessToken(GenerateAccessTokenRequest request) {
    return generateAccessTokenCallable().call(request);
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Generates an OAuth 2.0 access token for a service account.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   List&lt;String&gt; scope = new ArrayList&lt;&gt;();
   *   GenerateAccessTokenRequest request = GenerateAccessTokenRequest.newBuilder()
   *     .setName(formattedName)
   *     .addAllScope(scope)
   *     .build();
   *   ApiFuture&lt;GenerateAccessTokenResponse&gt; future = iamCredentialsClient.generateAccessTokenCallable().futureCall(request);
   *   // Do something
   *   GenerateAccessTokenResponse response = future.get();
   * }
   * </code></pre>
   */
  public final UnaryCallable<GenerateAccessTokenRequest, GenerateAccessTokenResponse>
      generateAccessTokenCallable() {
    return stub.generateAccessTokenCallable();
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Generates an OpenID Connect ID token for a service account.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   List&lt;String&gt; delegates = new ArrayList&lt;&gt;();
   *   String audience = "";
   *   boolean includeEmail = false;
   *   GenerateIdTokenResponse response = iamCredentialsClient.generateIdToken(formattedName, delegates, audience, includeEmail);
   * }
   * </code></pre>
   *
   * @param name The resource name of the service account for which the credentials are requested,
   *     in the following format: `projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}`.
   * @param delegates The sequence of service accounts in a delegation chain. Each service account
   *     must be granted the `roles/iam.serviceAccountTokenCreator` role on its next service account
   *     in the chain. The last service account in the chain must be granted the
   *     `roles/iam.serviceAccountTokenCreator` role on the service account that is specified in the
   *     `name` field of the request.
   *     <p>The delegates must have the following format:
   *     `projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}`
   * @param audience The audience for the token, such as the API or account that this token grants
   *     access to.
   * @param includeEmail Include the service account email in the token. If set to `true`, the token
   *     will contain `email` and `email_verified` claims.
   * @throws com.google.api.gax.rpc.ApiException if the remote call fails
   */
  public final GenerateIdTokenResponse generateIdToken(
      String name, List<String> delegates, String audience, boolean includeEmail) {
    SERVICE_ACCOUNT_PATH_TEMPLATE.validate(name, "generateIdToken");
    GenerateIdTokenRequest request =
        GenerateIdTokenRequest.newBuilder()
            .setName(name)
            .addAllDelegates(delegates)
            .setAudience(audience)
            .setIncludeEmail(includeEmail)
            .build();
    return generateIdToken(request);
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Generates an OpenID Connect ID token for a service account.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   String audience = "";
   *   GenerateIdTokenRequest request = GenerateIdTokenRequest.newBuilder()
   *     .setName(formattedName)
   *     .setAudience(audience)
   *     .build();
   *   GenerateIdTokenResponse response = iamCredentialsClient.generateIdToken(request);
   * }
   * </code></pre>
   *
   * @param request The request object containing all of the parameters for the API call.
   * @throws com.google.api.gax.rpc.ApiException if the remote call fails
   */
  public final GenerateIdTokenResponse generateIdToken(GenerateIdTokenRequest request) {
    return generateIdTokenCallable().call(request);
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Generates an OpenID Connect ID token for a service account.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   String audience = "";
   *   GenerateIdTokenRequest request = GenerateIdTokenRequest.newBuilder()
   *     .setName(formattedName)
   *     .setAudience(audience)
   *     .build();
   *   ApiFuture&lt;GenerateIdTokenResponse&gt; future = iamCredentialsClient.generateIdTokenCallable().futureCall(request);
   *   // Do something
   *   GenerateIdTokenResponse response = future.get();
   * }
   * </code></pre>
   */
  public final UnaryCallable<GenerateIdTokenRequest, GenerateIdTokenResponse>
      generateIdTokenCallable() {
    return stub.generateIdTokenCallable();
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Signs a blob using a service account's system-managed private key.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   List&lt;String&gt; delegates = new ArrayList&lt;&gt;();
   *   ByteString payload = ByteString.copyFromUtf8("");
   *   SignBlobResponse response = iamCredentialsClient.signBlob(formattedName, delegates, payload);
   * }
   * </code></pre>
   *
   * @param name The resource name of the service account for which the credentials are requested,
   *     in the following format: `projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}`.
   * @param delegates The sequence of service accounts in a delegation chain. Each service account
   *     must be granted the `roles/iam.serviceAccountTokenCreator` role on its next service account
   *     in the chain. The last service account in the chain must be granted the
   *     `roles/iam.serviceAccountTokenCreator` role on the service account that is specified in the
   *     `name` field of the request.
   *     <p>The delegates must have the following format:
   *     `projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}`
   * @param payload The bytes to sign.
   * @throws com.google.api.gax.rpc.ApiException if the remote call fails
   */
  public final SignBlobResponse signBlob(String name, List<String> delegates, ByteString payload) {
    SERVICE_ACCOUNT_PATH_TEMPLATE.validate(name, "signBlob");
    SignBlobRequest request =
        SignBlobRequest.newBuilder()
            .setName(name)
            .addAllDelegates(delegates)
            .setPayload(payload)
            .build();
    return signBlob(request);
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Signs a blob using a service account's system-managed private key.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   ByteString payload = ByteString.copyFromUtf8("");
   *   SignBlobRequest request = SignBlobRequest.newBuilder()
   *     .setName(formattedName)
   *     .setPayload(payload)
   *     .build();
   *   SignBlobResponse response = iamCredentialsClient.signBlob(request);
   * }
   * </code></pre>
   *
   * @param request The request object containing all of the parameters for the API call.
   * @throws com.google.api.gax.rpc.ApiException if the remote call fails
   */
  public final SignBlobResponse signBlob(SignBlobRequest request) {
    return signBlobCallable().call(request);
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Signs a blob using a service account's system-managed private key.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   ByteString payload = ByteString.copyFromUtf8("");
   *   SignBlobRequest request = SignBlobRequest.newBuilder()
   *     .setName(formattedName)
   *     .setPayload(payload)
   *     .build();
   *   ApiFuture&lt;SignBlobResponse&gt; future = iamCredentialsClient.signBlobCallable().futureCall(request);
   *   // Do something
   *   SignBlobResponse response = future.get();
   * }
   * </code></pre>
   */
  public final UnaryCallable<SignBlobRequest, SignBlobResponse> signBlobCallable() {
    return stub.signBlobCallable();
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Signs a JWT using a service account's system-managed private key.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   List&lt;String&gt; delegates = new ArrayList&lt;&gt;();
   *   String payload = "";
   *   SignJwtResponse response = iamCredentialsClient.signJwt(formattedName, delegates, payload);
   * }
   * </code></pre>
   *
   * @param name The resource name of the service account for which the credentials are requested,
   *     in the following format: `projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}`.
   * @param delegates The sequence of service accounts in a delegation chain. Each service account
   *     must be granted the `roles/iam.serviceAccountTokenCreator` role on its next service account
   *     in the chain. The last service account in the chain must be granted the
   *     `roles/iam.serviceAccountTokenCreator` role on the service account that is specified in the
   *     `name` field of the request.
   *     <p>The delegates must have the following format:
   *     `projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}`
   * @param payload The JWT payload to sign: a JSON object that contains a JWT Claims Set.
   * @throws com.google.api.gax.rpc.ApiException if the remote call fails
   */
  public final SignJwtResponse signJwt(String name, List<String> delegates, String payload) {
    SERVICE_ACCOUNT_PATH_TEMPLATE.validate(name, "signJwt");
    SignJwtRequest request =
        SignJwtRequest.newBuilder()
            .setName(name)
            .addAllDelegates(delegates)
            .setPayload(payload)
            .build();
    return signJwt(request);
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Signs a JWT using a service account's system-managed private key.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   String payload = "";
   *   SignJwtRequest request = SignJwtRequest.newBuilder()
   *     .setName(formattedName)
   *     .setPayload(payload)
   *     .build();
   *   SignJwtResponse response = iamCredentialsClient.signJwt(request);
   * }
   * </code></pre>
   *
   * @param request The request object containing all of the parameters for the API call.
   * @throws com.google.api.gax.rpc.ApiException if the remote call fails
   */
  public final SignJwtResponse signJwt(SignJwtRequest request) {
    return signJwtCallable().call(request);
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Signs a JWT using a service account's system-managed private key.
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   String payload = "";
   *   SignJwtRequest request = SignJwtRequest.newBuilder()
   *     .setName(formattedName)
   *     .setPayload(payload)
   *     .build();
   *   ApiFuture&lt;SignJwtResponse&gt; future = iamCredentialsClient.signJwtCallable().futureCall(request);
   *   // Do something
   *   SignJwtResponse response = future.get();
   * }
   * </code></pre>
   */
  public final UnaryCallable<SignJwtRequest, SignJwtResponse> signJwtCallable() {
    return stub.signJwtCallable();
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Exchange a JWT signed by third party identity provider to an OAuth 2.0 access token
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   List&lt;String&gt; scope = new ArrayList&lt;&gt;();
   *   String jwt = "";
   *   GenerateIdentityBindingAccessTokenResponse response = iamCredentialsClient.generateIdentityBindingAccessToken(formattedName, scope, jwt);
   * }
   * </code></pre>
   *
   * @param name The resource name of the service account for which the credentials are requested,
   *     in the following format: `projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}`.
   * @param scope Code to identify the scopes to be included in the OAuth 2.0 access token. See
   *     https://developers.google.com/identity/protocols/googlescopes for more information. At
   *     least one value required.
   * @param jwt Required. Input token. Must be in JWT format according to RFC7523
   *     (https://tools.ietf.org/html/rfc7523) and must have 'kid' field in the header. Supported
   *     signing algorithms: RS256 (RS512, ES256, ES512 coming soon). Mandatory payload fields
   *     (along the lines of RFC 7523, section 3): - iss: issuer of the token. Must provide a
   *     discovery document at $iss/.well-known/openid-configuration . The document needs to be
   *     formatted according to section 4.2 of the OpenID Connect Discovery 1.0 specification. -
   *     iat: Issue time in seconds since epoch. Must be in the past. - exp: Expiration time in
   *     seconds since epoch. Must be less than 48 hours after iat. We recommend to create tokens
   *     that last shorter than 6 hours to improve security unless business reasons mandate longer
   *     expiration times. Shorter token lifetimes are generally more secure since tokens that have
   *     been exfiltrated by attackers can be used for a shorter time. you can configure the maximum
   *     lifetime of the incoming token in the configuration of the mapper. The resulting Google
   *     token will expire within an hour or at "exp", whichever is earlier. - sub: JWT subject,
   *     identity asserted in the JWT. - aud: Configured in the mapper policy. By default the
   *     service account email.
   *     <p>Claims from the incoming token can be transferred into the output token accoding to the
   *     mapper configuration. The outgoing claim size is limited. Outgoing claims size must be less
   *     than 4kB serialized as JSON without whitespace.
   *     <p>Example header: { "alg": "RS256", "kid": "92a4265e14ab04d4d228a48d10d4ca31610936f8" }
   *     Example payload: { "iss": "https://accounts.google.com", "iat": 1517963104, "exp":
   *     1517966704, "aud": "https://iamcredentials.googleapis.com/", "sub":
   *     "113475438248934895348", "my_claims": { "additional_claim": "value" } }
   * @throws com.google.api.gax.rpc.ApiException if the remote call fails
   */
  public final GenerateIdentityBindingAccessTokenResponse generateIdentityBindingAccessToken(
      String name, List<String> scope, String jwt) {
    SERVICE_ACCOUNT_PATH_TEMPLATE.validate(name, "generateIdentityBindingAccessToken");
    GenerateIdentityBindingAccessTokenRequest request =
        GenerateIdentityBindingAccessTokenRequest.newBuilder()
            .setName(name)
            .addAllScope(scope)
            .setJwt(jwt)
            .build();
    return generateIdentityBindingAccessToken(request);
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Exchange a JWT signed by third party identity provider to an OAuth 2.0 access token
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   List&lt;String&gt; scope = new ArrayList&lt;&gt;();
   *   String jwt = "";
   *   GenerateIdentityBindingAccessTokenRequest request = GenerateIdentityBindingAccessTokenRequest.newBuilder()
   *     .setName(formattedName)
   *     .addAllScope(scope)
   *     .setJwt(jwt)
   *     .build();
   *   GenerateIdentityBindingAccessTokenResponse response = iamCredentialsClient.generateIdentityBindingAccessToken(request);
   * }
   * </code></pre>
   *
   * @param request The request object containing all of the parameters for the API call.
   * @throws com.google.api.gax.rpc.ApiException if the remote call fails
   */
  public final GenerateIdentityBindingAccessTokenResponse generateIdentityBindingAccessToken(
      GenerateIdentityBindingAccessTokenRequest request) {
    return generateIdentityBindingAccessTokenCallable().call(request);
  }

  // AUTO-GENERATED DOCUMENTATION AND METHOD
  /**
   * Exchange a JWT signed by third party identity provider to an OAuth 2.0 access token
   *
   * <p>Sample code:
   *
   * <pre><code>
   * try (IamCredentialsClient iamCredentialsClient = IamCredentialsClient.create()) {
   *   String formattedName = IamCredentialsClient.formatServiceAccountName("[PROJECT]", "[SERVICE_ACCOUNT]");
   *   List&lt;String&gt; scope = new ArrayList&lt;&gt;();
   *   String jwt = "";
   *   GenerateIdentityBindingAccessTokenRequest request = GenerateIdentityBindingAccessTokenRequest.newBuilder()
   *     .setName(formattedName)
   *     .addAllScope(scope)
   *     .setJwt(jwt)
   *     .build();
   *   ApiFuture&lt;GenerateIdentityBindingAccessTokenResponse&gt; future = iamCredentialsClient.generateIdentityBindingAccessTokenCallable().futureCall(request);
   *   // Do something
   *   GenerateIdentityBindingAccessTokenResponse response = future.get();
   * }
   * </code></pre>
   */
  public final UnaryCallable<
          GenerateIdentityBindingAccessTokenRequest, GenerateIdentityBindingAccessTokenResponse>
      generateIdentityBindingAccessTokenCallable() {
    return stub.generateIdentityBindingAccessTokenCallable();
  }

  @Override
  public final void close() {
    stub.close();
  }

  @Override
  public void shutdown() {
    stub.shutdown();
  }

  @Override
  public boolean isShutdown() {
    return stub.isShutdown();
  }

  @Override
  public boolean isTerminated() {
    return stub.isTerminated();
  }

  @Override
  public void shutdownNow() {
    stub.shutdownNow();
  }

  @Override
  public boolean awaitTermination(long duration, TimeUnit unit) throws InterruptedException {
    return stub.awaitTermination(duration, unit);
  }
}
