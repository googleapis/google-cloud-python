# Welcome to the gCloud DNS Demo! (hit enter)

# We're going to walk through some of the basics...,
# Don't worry though. You don't need to do anything, just keep hitting enter...

# Let's start by importing the demo module and getting a connection:
from gcloud.dns import demo
connection = demo.get_connection()

# Lets create a zone.
zone = connection.create_zone('zone', 'zone.com.', 'My zone.')

# Lets see what records the zone has...
print connection.get_records('zone')

# Lets add a A record to the zone.
zone.add_a('zone.com.', ['1.1.1.1'], 9000)

# Lets commit the changes of the zone with...
zone.save()

# Lets see what records the zone has...
print connection.get_records('zone')

# Finally lets clean up and delete our test zone.
zone.delete(force=True)
