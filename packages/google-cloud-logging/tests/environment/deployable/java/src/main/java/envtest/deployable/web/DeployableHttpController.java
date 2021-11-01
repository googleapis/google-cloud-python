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


package envtest.deployable.web;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import com.google.cloud.MonitoredResource;
import com.google.cloud.logging.LogEntry;
import com.google.cloud.logging.Logging;
import com.google.cloud.logging.LoggingOptions;
import com.google.cloud.logging.Payload.StringPayload;
import com.google.cloud.logging.Severity;
import java.util.Collections;

import org.springframework.beans.factory.annotation.Autowired;

import io.grpc.StatusRuntimeException;

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

import java.util.Base64;
import org.apache.commons.lang3.StringUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;
import org.eclipse.jetty.util.B64Code;
import envtest.deployable.DeployableApplication;
/**
 * Defines a controller to handle HTTP requests.
 */
@RestController
public final class DeployableHttpController {


    @GetMapping("/")
    public String helloWorld() {
        String message = "It's running!";

        return message;
    }

    /**
     * This function will be triggered by incomming pub/sub messages from envctl.
     * It will then find and execute the requested test snippet, based on the
     * contents of the pub/sub payload
     */
    @RequestMapping(value = "/", method = RequestMethod.POST)
    public ResponseEntity pubsub_receive(@RequestBody Map<String, Object> payload) {
        Map<String, Object> pubsubMessage = (Map<String, Object>) payload.get("message");
        Map<String, String> args = Collections.emptyMap();
        if (pubsubMessage.containsKey("attributes")) {
           args = (Map<String, String>) pubsubMessage.get("attributes");
        }
        String encodedName = (String) pubsubMessage.get("data");
        String fnName = B64Code.decode(encodedName, "UTF-8");
        DeployableApplication.triggerSnippet(fnName, args);
        return new ResponseEntity<>(fnName, HttpStatus.OK);
    }
}
