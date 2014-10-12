from gcloud import connection


class Connection(connection.JsonConnection):
    """"""

    API_VERSION = 'v1beta1'
    """"""

    API_URL_TEMPLATE = '{api_base}/pubsub/{api_version}'
    """"""

    @classmethod
    def build_api_url(cls, resource_type, resource_id=None, method=None, base_url=None,
                      api_version-None):
        """"""

        api_url_base = cls.API_URL_TEMPLATE.format(
            api_base=(base_url or cls.API_BASE_URL),
            api_version=(api_version or cls.API_VERSION),
            resouce_type=resource_type, resource_id=resource_id,
            method=method)

        # TODO: Do some error checking and throw a ValueError if the
        #       parameters are invalid.

        pieces = list(filter(None, resource_type, resource_id, method))
        return '/'.join([api_url_base] + pieces)


    def create_topic(self, name):
        pass

    def delete_topic(self, name):
        pass

    def get_topic(self, name):
        pass

    def get_topics(self):
        pass

    def create_subscription(self, topic_name, name, push_endpoint=None, ack_deadline=None):
        pass

    def delete_subscription(self, name):
        pass

    def get_subscription(self, name):
        pass

    def get_subscriptions(self, query):
        pass

    def publish_message(self, topic_name, message, labels=None):
        pass

    def get_message(self, subscription_name):
        pass

    # TODO: Figure out how we're going to handle async subscriptions...
    #       asyncio.Future (Python 3)? multiprocessing.Pool (Python 2)?
