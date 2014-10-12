class Topic(object):

    def __init__(self, connection=None, name=None):
        self.connection = connection
        self.name = name

    @classmethod
    def from_dict(cls, topic_dict, connection=None):
        return cls(connection=connection, name=topic_dict['name'])

    def __repr__(self):  # pragma NO COVER
        return '<Topic: %s>' % self.name

    def delete(self):
        pass

    def subscribe(self, name, *args, **kwargs):
        return self.connection.create_subscription(topic_name=self.name,
                                                   name=name, *args, **kwargs)

    def publish(self, message, labels=None):
        return self.connection.publish_message(topic_name=self.name,
                                               message=message, labels=labels)
