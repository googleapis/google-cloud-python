# pragma NO COVER
# Welcome to the gCloud Storage Demo! (hit enter)

# We're going to walk through some of the basics...,
# Don't worry though. You don't need to do anything, just keep hitting enter...

# Let's start by importing the demo module and getting a connection:
from gcloud.storage import demo
connection = demo.get_connection()

# OK, now let's look at all of the buckets...
print(connection.get_all_buckets())  # This might take a second...

# Now let's create a new bucket...
import time
bucket_name = ("bucket-%s" % time.time()).replace(".", "")  # Get rid of dots.
print(bucket_name)
bucket = connection.create_bucket(bucket_name)
print(bucket)

# Let's look at all of the buckets again...
print(connection.get_all_buckets())

# How about we create a new key inside this bucket.
key = bucket.new_key("my-new-file.txt")

# Now let's put some data in there.
key.set_contents_from_string("this is some data!")

# ... and we can read that data back again.
print(key.get_contents_as_string())

# Now let's delete that key.
print(key.delete())

# And now that we're done, let's delete that bucket...
print(bucket.delete())

# Alright! That's all!
# Here's an interactive prompt for you now...
