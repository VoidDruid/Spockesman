import json

import redis

from ...logger import log
from ..context import Context
from .abstract import AbstractBackend


class RedisBackend(AbstractBackend):
    def __init__(self, host, port, db):
        self.__redis = redis.Redis(db=db, host=host, port=port)

    def load(self, user_id):
        data = self.__redis.get(user_id)
        if data:
            return Context.from_dict(json.loads(data))
        else:
            return Context(user_id)

    def save(self, user_id, context):
        self.__redis.set(user_id, json.dumps(context.to_dict()))

    def delete(self, *user_id):
        self.__redis.delete(user_id)

    def delete_all(self):
        self.__redis.flushdb()

    def __iter__(self):
        return self.__redis.scan_iter()


def activate(config):
    log.debug('Activating REDIS context backend')
    return RedisBackend(config['Host'], int(config['Port']), int(config['Name']))
