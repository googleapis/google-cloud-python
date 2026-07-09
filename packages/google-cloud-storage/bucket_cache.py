import threading

from threading import Lock


class BucketCache(object):
    def __init__(self, client):
        self.cache = LruCache
        self.client = client
        self.lock = Lock()
        self.in_flight_requests = set()
        # TODO: followup, if all threads want the md.,then what ?
        # basically even the fisrst req would change.
        # self.blocking_queue

        pass

    def get_bucket_attributes(self, bucket_name):
        with self.lock:
            if bucket_name in self.cache:
                return self.cache[bucket_name]
            elif bucket_name in self.in_flight_requests:
                # this would be the case of thundering herd, where 'n' threads
                # all of them faced "cache miss" and 1 is in progress to fetch metadata.
                # hence we don't want rest `n - 1`` threads to make the same req
                return None
            else:
                # fire a background thread and get bucket metadata.
                threading.Thread(
                    target=self._get_bucket_md, args=(bucket_name,), daemon=True
                ).start()
                return None

    def _get_bucket_md(self, bucket_name):
        md = self.client.get_bucket(bucket_name)

        self.cache[bucket_name] = md  # parse appropriately
