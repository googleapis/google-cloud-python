# Welcome to the gCloud Compute Demo! (hit enter)

# We're going to walk through some of the basics...,
# Don't worry though. You don't need to do anything, just keep hitting enter...

# Let's start by importing the demo module and getting a connection:
from gcloud.compute import demo
connection = demo.get_connection()

# OK, now let's retrieve an instance
instance = connection.get_instance('gcloud-computeengine-instance',
                                   'us-central1-b')

# Let us give that instance a reset - Got the reset!
instance.reset()

# Thats it for now more is coming soon
