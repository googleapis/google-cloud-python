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

/**
 * A client to IAM Service Account Credentials API.
 *
 * <p>The interfaces provided are listed below, along with usage samples.
 *
 * <p>==================== IamCredentialsClient ====================
 *
 * <p>Service Description: A service account is a special type of Google account that belongs to
 * your application or a virtual machine (VM), instead of to an individual end user. Your
 * application assumes the identity of the service account to call Google APIs, so that the users
 * aren't directly involved.
 *
 * <p>Service account credentials are used to temporarily assume the identity of the service
 * account. Supported credential types include OAuth 2.0 access tokens, OpenID Connect ID tokens,
 * self-signed JSON Web Tokens (JWTs), and more.
 *
 * <p>Sample for IamCredentialsClient:
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
 */
package com.google.cloud.iam.credentials.v1;
