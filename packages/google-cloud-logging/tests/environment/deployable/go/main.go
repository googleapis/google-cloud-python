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
	"io/ioutil"
	"log"
	"net/http"
	"os"

	// This is replaced by the local version of cloud logging
	"cloud.google.com/go/compute/metadata"
	"cloud.google.com/go/logging"
)

// PubSubMessage is the logtext of a Pub/Sub event.
type pubSubMessage struct {
	Message struct {
		Data       []byte            `json:"data,omitempty"`
		Attributes map[string]string `json:"attributes,omitempty"`
		ID         string            `json:"id"`
	} `json:"message"`
	Subscription string `json:"subscription"`
}

// CloudRun: Processes a Pub/Sub message through HTTP.
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

	switch msg {
	case "simplelog":
		simplelog(args)
	case "stdLog":
		break
	default:
		break
	}
}

func main() {
	if os.Getenv("ENABLE_SUBSCRIBER") == "" {

		// Set up PubSub for CloudRun
		http.HandleFunc("/", pubsubHTTP)

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

// [Optional] envctl go <env> trigger simpleLog logname=foo,logtext=bar
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
	if val, ok := args["logname"]; ok {
		logname = val
	}

	logtext := "hello world"
	if val, ok := args["logtext"]; ok {
		logtext = val
	}

	logger := client.Logger(logname).StandardLogger(logging.Info)
	logger.Println(logtext)
}
