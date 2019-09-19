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
    def __init__(self, host, port, db):
        self.__redis = redis.Redis(db=db, host=host, port=port)

    def load(self, user_id):
        data = self.__redis.get(user_id)
        if data:
            return Context.from_dict(json.loads(data))
        return None

    def save(self, context):
        self.__redis.set(context.user_id, json.dumps(context.to_dict()))

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
