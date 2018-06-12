# Copyright 2017 Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python client for Google Cloud Firestore Watch."""

WATCH_TARGET_ID = 0x5079  # "Py"

class Watch(object):
    pass

'''
You can listen to a document with the onSnapshot() method. An initial call 
using the callback you provide creates a document snapshot immediately with the
\current contents of the single document. Then, each time the contents change,
another call updates the document snapshot.

db.collection("cities")
    .onSnapshot


Internal: Count: 1, Average: 4.0
Get Realtime Updates with Cloud Firestore
You can listen to a document with the onSnapshot() method. An initial call using
the callback you provide creates a document snapshot immediately with the
current contents of the single document. Then, each time the contents change,
another call updates the document snapshot.

Note: Realtime listeners are not yet supported in the Python, Go, or PHP client
libraries.

db.collection("cities").doc("SF")
    .onSnapshot(function(doc) {
        console.log("Current data: ", doc.data());
    });
test.firestore.js

Events for local changes
Local writes in your app will invoke snapshot listeners immediately. This is
because of an important feature called "latency compensation." When you perform
a write, your listeners will be notified with the new data before the data is
sent to the backend.

Retrieved documents have a metadata.hasPendingWrites property that indicates
whether the document has local changes that haven't been written to the backend
yet. You can use this property to determine the source of events received by
your snapshot listener:
'''