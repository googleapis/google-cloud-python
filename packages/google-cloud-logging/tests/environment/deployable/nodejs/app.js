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

var tests = require('./tests.js');

/** ****************** GAE, GKE, GCE ******************
 * Enable app subscriber for all environments, except GCR, GCF.
 */
async function enableSubscriber() {
  if (process.env.ENABLE_SUBSCRIBER) {
    const gcpMetadata = require('gcp-metadata');
    const projectId = await gcpMetadata.project('project-id');
    const topicId = process.env.PUBSUB_TOPIC || 'logging-test';
    const subscriptionId = `${topicId}-subscriber`;
    const topicName = `projects/${projectId}/topics/${topicId}`;
    const subscriptionName = `projects/${projectId}/subscriptions/${subscriptionId}`

    const {PubSub} = require('@google-cloud/pubsub');
    const pubSubClient = new PubSub();
    // Creates a new subscription
    pubSubClient.topic(topicName).createSubscription(subscriptionName);
    listenForMessages(pubSubClient, subscriptionName).catch(console.error);
  }
}
enableSubscriber().catch(console.error);

/**
 * ****************** GCR, GKE, GCE ******************
 * For GCP services that require a running app server, except GAE and GCF.
 * RUNSERVER env var is set in the Dockerfile.
 */
if (process.env.RUNSERVER) {
  const express = require('express');
  const bodyParser = require('body-parser');
  const app = express();

  app.use(bodyParser.json());

  /**
   * Cloud Run to be triggered by Pub/Sub.
   */
  if (process.env.K_CONFIGURATION) {
    app.post('/', (req, res) => {
      if (!req.body) {
        const msg = 'no Pub/Sub message received';
        console.error(`error: ${msg}`);
        res.status(400).send(`Bad Request: ${msg}`);
        return;
      }
      if (!req.body.message) {
        const msg = 'invalid Pub/Sub message format';
        console.error(`error: ${msg}`);
        res.status(400).send(`Bad Request: ${msg}`);
        return;
      }

      const message = req.body.message;
      triggerTest(message);

      res.status(204).send();
    });
  };

  // Start app server
  const PORT = process.env.PORT || 8080;
  app.listen(PORT, () =>
      console.log(`nodejs-pubsub-tutorial listening on port ${PORT}`)
  );
}

/**
 * Background Cloud Function to be triggered by Pub/Sub.
 * This function is exported by index.js, and executed when
 * the trigger topic receives a message.
 *
 * @param {object} message The Pub/Sub message.
 * @param {object} context The event metadata.
 */
exports.pubsubFunction = (message, context) => {
  triggerTest(message);
};

/**
 * ****************** GAE, GKE, GCE ******************
 * Asynchronously listens for pubsub messages until a TIMEOUT is reached.
 * @param pubSubClient
 * @param subscriptionName
 */
async function listenForMessages(pubSubClient, subscriptionName) {
  // References an existing subscription
  const subscription = pubSubClient.subscription(subscriptionName);

  // Handles incoming messages and triggers tests.
  const messageHandler = message => {
    triggerTest(message);
    // "Ack" (acknowledge receipt of) the message
    message.ack();
  };

  // Listen for new messages until timeout is hit or test is done.
  subscription.on('message', messageHandler);

  setTimeout(() => {
    subscription.removeListener('message', messageHandler);
  }, 600000); // max 10 minutes timeout
}

function triggerTest(message) {
  const testName = message.data
      ? Buffer.from(message.data, 'base64').toString()
      : console.error("WARNING: no log function was invoked");

  console.log('Fn invoked with attributes, if any: ');
  console.log(message.attributes);

  if (message.attributes) {
    tests[testName](message.attributes['log_name'], message.attributes['log_text']);
  } else {
    tests[testName]();
  }
}
