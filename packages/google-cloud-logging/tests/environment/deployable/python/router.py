# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from google.cloud import pubsub_v1
import uuid
import snippets
from inspect import getmembers, isfunction
import google.auth
import logging
from flask import Flask, request
import base64

try:
    import google.cloud.logging
except ImportError:
    # import at runtime for GAE environments
    import pip
    import importlib
    import site

    pip.main(["install", "-e", "./python-logging"])
    importlib.reload(site)
    import google.cloud.logging

app = Flask(__name__)

_test_functions = {
    name: func for (name, func) in getmembers(snippets) if isfunction(func)
}


# used in Cloud Functions
def pubsub_gcf(event, context):
    initialize_client()

    if "data" not in event:
        logging.error("invalid pubsub message")
    msg_str = base64.b64decode(event["data"]).decode("utf-8")
    kwargs = event.get("attributes", {})
    found_func = _test_functions.get(msg_str, None)
    if found_func:
        found_func(**kwargs)
    else:
        logging.error(f"function {msg_str} not found")


# grabs pubsub message out of request
# used in Cloud Run
@app.route("/", methods=["POST"])
def pubsub_http():
    envelope = request.get_json()
    if not envelope or not isinstance(envelope, dict) or "message" not in envelope:
        return "Bad Request: invalid pub/sub message", 400
    pubsub_message = envelope["message"]
    kwargs = (
        pubsub_message["attributes"] if "attributes" in pubsub_message.keys() else {}
    )
    msg_str = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
    found_func = _test_functions.get(msg_str, None)
    if found_func:
        found_func(**kwargs)
        return ("", 200)
    else:
        return f"Bad Request: function {msg_str} not found", 400


# recieves pubsub messages when the script is run directly (GKE)
def pubsub_callback(message):
    msg_str = message.data.decode("utf-8")
    kwargs = message.attributes
    message.ack()
    found_func = _test_functions.get(msg_str, None)
    if found_func:
        found_func(**kwargs)
    else:
        logging.error(f"function {msg_str} not found")

def initialize_client():
    # set up logging
    client = google.cloud.logging.Client()
    client.setup_logging(log_level=logging.DEBUG)

if __name__ == "__main__":
    initialize_client()

    if os.getenv("ENABLE_SUBSCRIBER", None):
        # set up pubsub listener
        topic_id = os.getenv("PUBSUB_TOPIC", "logging-test")
        _, project_id = google.auth.default()
        subscription_id = f"{topic_id}-subscriber"
        subscriber = pubsub_v1.SubscriberClient()
        topic_name = f"projects/{project_id}/topics/{topic_id}"
        subscription_name = f"projects/{project_id}/subscriptions/{subscription_id}"
        subscriber.create_subscription(name=subscription_name, topic=topic_name)
        future = subscriber.subscribe(subscription_name, pubsub_callback)
        try:
            print(f"listening for pubsub messages at {topic_id}")
            future.result()
        except KeyboardInterrupt:
            future.cancel()

    # set up flask server
    if os.getenv("ENABLE_FLASK", None):
        port = os.getenv("PORT", 8080)
        app.run(debug=True, host="0.0.0.0", port=port)
