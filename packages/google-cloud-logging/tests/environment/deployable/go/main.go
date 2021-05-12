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

package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"

	"cloud.google.com/go/compute/metadata"
	// go/logging is replaced by the local version of cloud logging
	"cloud.google.com/go/logging"
	"cloud.google.com/go/pubsub"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// pubSubMessage is the message format received over HTTP
// ****************** CloudRun ******************
type pubSubMessage struct {
	Message struct {
		Data       []byte            `json:"data,omitempty"`
		Attributes map[string]string `json:"attributes,omitempty"`
		ID         string            `json:"id"`
	} `json:"message"`
	Subscription string `json:"subscription"`
}

// pubsubHTTP processes a Pub/Sub message through HTTP.
// ****************** CloudRun ******************
func pubsubHTTP(w http.ResponseWriter, r *http.Request) {
	var m pubSubMessage
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		log.Printf("ioutil.ReadAll: %v", err)
		http.Error(w, "Bad Request", http.StatusBadRequest)
		return
	}
	if err := json.Unmarshal(body, &m); err != nil {
		log.Printf("json.Unmarshal: %v", err)
		http.Error(w, "Bad Request", http.StatusBadRequest)
		return
	}

	msg := string(m.Message.Data)
	args := m.Message.Attributes
	testLog(msg, args)
}

// PubSubMessage is the message format received by CloudFunctions
// ****************** Functions ******************
type PubSubMessage struct {
	Data       []byte            `json:"data"`
	Attributes map[string]string `json:"attributes"`
}

// PubsubFunction is a background Cloud Function triggered by Pub/Sub
// ****************** Functions ******************
func PubsubFunction(ctx context.Context, m PubSubMessage) error {
	log.Printf("Data is: %v", string(m.Data))
	testLog(string(m.Data), m.Attributes)
	return nil
}

// pullMsgsSync synchronously pulls pubsub messages for a maximum of 2400 seconds
// ****************** App Engine ******************
func pullMsgsSync(sub *pubsub.Subscription) error {
	// Turn on synchronous mode. This makes the subscriber use the Pull RPC rather
	// than the StreamingPull RPC, which is useful for guaranteeing MaxOutstandingMessages.
	sub.ReceiveSettings.Synchronous = true
	sub.ReceiveSettings.MaxOutstandingMessages = 10

	// Receive messages for 1000 seconds.
	ctx, cancel := context.WithTimeout(ctx, 2400*time.Second)
	defer cancel()

	// Create a channel to handle messages to as they come in.
	cm := make(chan *pubsub.Message)
	defer close(cm)
	// Handle individual messages in a goroutine.
	go func() {
		for msg := range cm {
			log.Printf("Got message :%q\n", string(msg.Data))
			testLog(string(msg.Data), msg.Attributes)
			msg.Ack()
		}
	}()
	// Receive blocks until the passed in context is done.
	err := sub.Receive(ctx, func(ctx context.Context, msg *pubsub.Message) {
		cm <- msg
	})
	if err != nil && status.Code(err) != codes.Canceled {
		return fmt.Errorf("receive: %v", err)
	}
	return nil
}

// Initializations for all GCP services
var ctx context.Context

// init executes for all environments, regardless if its a program or package
func init() {
	ctx = context.Background()
}

// main runs for all environments except GCF
func main() {
	// ****************** GAE, GKE, GCE ******************
	// Enable app subscriber for all environments except GCR
	if os.Getenv("ENABLE_SUBSCRIBER") == "true" {
		projectID, err := metadata.ProjectID()
		if err != nil {
			log.Fatalf("metadata.ProjectID: %v", err)
		}
		topicID := os.Getenv("PUBSUB_TOPIC")
		if topicID == "" {
			topicID = "logging-test"
		}
		client, err := pubsub.NewClient(ctx, projectID)
		if err != nil {
			log.Fatalf("pubsub.NewClient: %v", err)
		}
		defer client.Close()
		subscriptionID := topicID + "-subscriber"
		topic := client.Topic(topicID)

		// Create a pull subscription to receive messages
		sub, err := client.CreateSubscription(ctx,
			subscriptionID,
			pubsub.SubscriptionConfig{
				Topic: topic,
			})
		if err != nil {
			log.Fatalf("pubsub.CreateSubscription: %v", err)
		}

		// Blocking call, pulls messages from pubsub until context is cancelled or test ends
		err = pullMsgsSync(sub)
		if err != nil {
			log.Fatalf("pullMsgsSync failed: %v", err)
		}
	}

	// ****************** GCR, GKE, GCE ******************
	// Listen and serve for all environments except GAE
	_, gaeApp := os.LookupEnv("GAE_SERVICE")
	_, gaeRuntime := os.LookupEnv("GAE_VERSION")
	isAppEngine := gaeApp || gaeRuntime
	_, isCloudRun := os.LookupEnv("K_CONFIGURATION")

	if !isAppEngine {
		// Cloud run is triggered through http handler
		if isCloudRun {
			http.HandleFunc("/", pubsubHTTP)
		}

		port := os.Getenv("PORT")
		if port == "" {
			port = "8080"
			log.Printf("Defaulting to port %s", port)
		}
		log.Printf("Listening on port %s", port)
		if err := http.ListenAndServe(":"+port, nil); err != nil {
			log.Fatal(err)
		}
	}
}

// ****************** Test Cases ******************
// [Optional] envctl go <env> trigger simplelog log_name=foo,log_text=bar
func simplelog(args map[string]string) {
	ctx := context.Background()
	projectID, err := metadata.ProjectID()
	if err != nil {
		log.Fatalf("metadata.ProjectID: %v", err)
	}
	client, err := logging.NewClient(ctx, projectID)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}
	defer client.Close()

	logname := "my-log"
	if val, ok := args["log_name"]; ok {
		logname = val
	}

	logtext := "hello world"
	if val, ok := args["log_text"]; ok {
		logtext = val
	}

	logger := client.Logger(logname).StandardLogger(logging.Info)
	logger.Println(logtext)
}

// testLog is a helper function which invokes the correct test functions
func testLog(message string, attrs map[string]string) {
	switch message {
	case "simplelog":
		simplelog(attrs)
	case "stdlog":
		break
	default:
		break
	}
}
