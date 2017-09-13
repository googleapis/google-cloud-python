from google.cloud.spanner import Client
from .streaming_utils import INSTANCE_NAME as STREAMING_INSTANCE

STANDARD_INSTANCE = 'google-cloud-python-systest'


def scrub_instances(client):

    for instance in client.list_instances():
        if instance.name == STREAMING_INSTANCE:
            print('Not deleting streaming instance: {}'.format(
                STREAMING_INSTANCE))
            continue
        elif instance.name == STANDARD_INSTANCE:
            print('Not deleting standard instance: {}'.format(
                STANDARD_INSTANCE))
        else:
            print("deleting instance: {}".format(instance.name))
            instance.delete()


if __name__ == '__main__':
    client = Client()
    scrub_instances(client)
