# Welcome to the gCloud Storage Demo! (hit enter)
# We're going to walk through some of the basics...
# Don't worry though. You don't need to do anything, just keep hitting enter...

# Copyright 2014 Google Inc. All rights reserved.
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

# Let's start by importing the demo module and getting a client:
import time

from gcloud import storage
from gcloud.storage import demo

client = storage.Client(project=demo.PROJECT_ID)

# OK, now let's look at all of the buckets...
print(list(client.list_buckets()))  # This might take a second...

# Now let's create a new bucket...
bucket_name = ("bucket-%s" % time.time()).replace(".", "")  # Get rid of dots.
print(bucket_name)
bucket = client.create_bucket(bucket_name)
print(bucket)

# Let's look at all of the buckets again...
print(list(client.list_buckets()))

# How about we create a new blob inside this bucket.
blob = bucket.blob("my-new-file.txt")

# Now let's put some data in there.
blob.upload_from_string("this is some data!")

# ... and we can read that data back again.
print(blob.download_as_string())

# Now let's delete that blob.
print(blob.delete())

# And now that we're done, let's delete that bucket...
print(bucket.delete())

# Alright! That's all!
# Here's an interactive prompt for you now...
