// Copyright 2021 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package envtest.deployable;

import org.slf4j.LoggerFactory;
import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.google.cloud.pubsub.v1.AckReplyConsumer;
import com.google.cloud.pubsub.v1.MessageReceiver;
import com.google.cloud.pubsub.v1.Subscriber;
import com.google.cloud.pubsub.v1.SubscriptionAdminClient;
import com.google.pubsub.v1.PushConfig;
import com.google.pubsub.v1.ProjectTopicName;
import com.google.pubsub.v1.ProjectSubscriptionName;
import com.google.common.util.concurrent.MoreExecutors;
import com.google.pubsub.v1.PubsubMessage;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.io.IOException;
import java.lang.Thread;
import java.lang.InterruptedException;
import java.lang.NoSuchMethodException;
import java.lang.IllegalAccessException;
import java.lang.reflect.InvocationTargetException;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.auth.oauth2.ServiceAccountCredentials;
import com.google.cloud.logging.Severity;
import com.google.cloud.pubsub.v1.AckReplyConsumer;
import com.google.cloud.pubsub.v1.MessageReceiver;
import com.google.cloud.pubsub.v1.Subscriber;
import com.google.cloud.pubsub.v1.SubscriptionAdminClient;
import com.google.pubsub.v1.ProjectSubscriptionName;
import com.google.pubsub.v1.PubsubMessage;
import com.google.pubsub.v1.PushConfig;
import com.google.pubsub.v1.TopicName;
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.Map;
import java.lang.reflect.Method;

import java.io.BufferedReader;
import java.net.URL;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.HttpURLConnection;

/**
 * This class serves as an entry point for the Spring Boot app
 * Here, we check to ensure all required environment variables are set
 */
@SpringBootApplication
public class DeployableApplication {

    private static final org.slf4j.Logger logger = LoggerFactory.getLogger(DeployableApplication.class);

    private static String getProjectId() throws RuntimeException {
        try {
            // try reading from service account
            GoogleCredentials credentials = GoogleCredentials.getApplicationDefault();
            if (credentials instanceof ServiceAccountCredentials) {
              String id = ((ServiceAccountCredentials) credentials).getProjectId();
              if (id != null){
                  return id;
              }
            }
            // try grabbing from metadata server
            URL url = new URL("http://metadata.google.internal/computeMetadata/v1/project/project-id");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestProperty("Metadata-Flavor", "Google");
            BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
            String line = reader.readLine();
            return line;
        } catch (IOException e){
            System.out.println(e);
        }
        throw new RuntimeException("could not find project ID");
    }

    private static void startPubsubSubscription() throws IOException, RuntimeException {
        // create variables
        String projectId = getProjectId();
        String topicId = System.getenv().getOrDefault("PUBSUB_TOPIC", "logging-test");
        String subscriptionId = topicId + "-subscriber";
        TopicName topicName = TopicName.of(projectId, topicId);
        ProjectSubscriptionName subscriptionName = ProjectSubscriptionName.of(projectId, subscriptionId);
        // create subscription
        SubscriptionAdminClient subscriptionClient = SubscriptionAdminClient.create();
        subscriptionClient.createSubscription(
               subscriptionName,
               topicName,
               PushConfig.newBuilder().build(),
               20);
        // define callback
        MessageReceiver receiver = (PubsubMessage message, AckReplyConsumer consumer) -> {
          consumer.ack();
          String fnName = message.getData().toStringUtf8();
          Map<String, String> args = message.getAttributes();
          triggerSnippet(fnName, args);
        };
        // start subscriber
        Subscriber subscriber = null;
        try {
          subscriber = Subscriber.newBuilder(subscriptionName, receiver).build();
          subscriber.startAsync().awaitRunning();
          System.out.printf("Listening for messages on %s:\n", subscriptionName.toString());
          subscriber.awaitTerminated();
        } finally {
          subscriber.stopAsync().awaitTerminated();
        }
    }

    public static void triggerSnippet(String fnName, Map<String,String> args) {
      try {
          Snippets obj = new Snippets();
          Class c = obj.getClass();
          Method found = c.getDeclaredMethod(fnName, new Class[] {Map.class});
          found.invoke(obj, args);
      } catch (NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
          System.out.println(e.toString());
      }
    }

    public static void main(String[] args) throws IOException, RuntimeException {
        String projectId = "";
        String topicId;
        String subscriptionId;


        Logger root = (Logger)LoggerFactory.getLogger(org.slf4j.Logger.ROOT_LOGGER_NAME);
        root.setLevel(Level.INFO);

        // ****************** GAE, GKE, GCE ******************
        // Enable app subscriber for all environments except GCR
        Boolean enableSubscriber = Boolean.parseBoolean(System.getenv().getOrDefault("ENABLE_SUBSCRIBER", "false"));
        System.out.format("ENV: ENABLE_SUBSCRIBER=true\n");
        if (enableSubscriber) {
          // start a pub/sub server and listen for messages
          startPubsubSubscription();
          return;
        }

        // GCR, GAE Standard
        Boolean runServer = Boolean.parseBoolean(System.getenv().getOrDefault("RUNSERVER", "0"));
        System.out.format("ENV: RUNSERVER=%b\n", runServer);
        if (runServer) {
          // hand off execution to DeployableHttpController
          SpringApplication.run(DeployableApplication.class, args);
          return;
        }
    }
}
