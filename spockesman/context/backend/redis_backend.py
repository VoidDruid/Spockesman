try:
    import ujson as json
except ImportError:
    import json

import redis

from spockesman.logger import log
from spockesman.context.context import Context
from spockesman.context.backend.abstract import AbstractBackend

# TODO: support url connection


class RedisBackend(AbstractBackend):
    """
    Implementation of abstract backend that uses redis for storage
    """
    value_key = 'value'
    type_key = 'type'

    def __init__(self, host, port, db):
        self.__redis = redis.Redis(db=db, host=host, port=port)

    def load(self, user_id):
        data = self.__redis.hget(user_id, self.value_key)
        type_ = self.__redis.hget(user_id, self.type_key)
        if data and type:
            return Context.unpickle_type(type_).from_dict(json.loads(data))
        return None

    def save(self, context):
        self.__redis.hset(context.user_id, self.type_key, context.pickled_type)
        self.__redis.hset(context.user_id, self.value_key, json.dumps(context.to_dict()))

    def delete(self, *user_ids):
        self.__redis.delete(user_ids)

    def delete_all(self):
        self.__redis.flushdb()

    def __iter__(self):
        for key in self.__redis.scan_iter():
            context = self.load(key)
            if context:
                yield context


def activate(config) -> RedisBackend:
    log.debug('Activating REDIS context backend')
    return RedisBackend(config['Host'], int(config['Port']), int(config['Name']))
