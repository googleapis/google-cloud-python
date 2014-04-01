# Welcome to the gCloud DNS Demo! (hit enter)

# We're going to walk through some of the basics...,
# Don't worry though. You don't need to do anything, just keep hitting enter...

# Let's start by importing the demo module and getting a connection:
from gcloud.dns import demo
connection = demo.get_connection()
print connection.get_project('gceremote')
