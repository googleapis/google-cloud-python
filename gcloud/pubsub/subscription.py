class Subscription(object):

    def __init__(self, connection=None, topic=None, name=None):
        self.connection = connection
        self.topic = topic
        self.name = name

    @classmethod
    def from_dict(cls, subscription_dict, connection=None):
        return cls(connection=connection, topic=subscription_dict['topic'],
                   name=subscription_dict['name'])

    def __repr__(self):  # pragma NO COVER
        topic_name = self.topic.name if self.topic else None
        return '<Subscription: %s to topic %s>' % (self.name, topic_name)

    def delete(self):
        pass

    def get_message(self):
        return self.connection.get_message(self.name)
