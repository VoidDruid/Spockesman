try:
    import ujson as json
except ImportError:
    import json
import sqlite3

from spockesman.logger import log
from spockesman.context.context import Context
from spockesman.context.backend.abstract import AbstractBackend


class SqliteBackend(AbstractBackend):  # TODO: create base class SQLBackend and inherit from it
    """
    Implementation of abstract backend that uses redis for storage
    """
    @staticmethod
    def bool_from_int(value):
        if value == 0:
            return False
        elif value == 1:
            return True
        else:
            raise ValueError(f'Can not convert <int {value}> to bool')

    def __init__(self, db):
        if not db.endswith('.db'):
            db = db + '.db'
        self.__db = sqlite3.connect(db, check_same_thread=False)
        self.__cursor = self.__db.cursor()
        self.__cursor.execute('create table if not exists context'
                              '(user_id text, state text, command text, input integer, data text)')
        self.__db.commit()

    def load(self, user_id):
        query = 'select state, command, input, data from context where user_id=?'
        values = self.__cursor.execute(query, (user_id,)).fetchone()
        if not values:
            return None
        state, command, input_, data = values
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ValueError(f'User {user_id} data is broken!')
        context = Context(user_id, state, data)
        context.input = self.bool_from_int(input_)
        return context

    def save(self, context):
        data = json.dumps(context.data)
        query = 'insert into context (user_id, state, command, input, data) values (?, ?, ?, ?, ?)'
        state = context.state
        if state is not None:
            state_name = state.name
        else:
            state_name = None
        self.__cursor.execute(query, [context.user_id, state_name, context.command,
                                      int(context.input), data])
        self.__db.commit()

    def delete(self, *user_ids):
        query = 'delete from context where user_id=?'
        self.__cursor.executemany(query, user_ids)
        self.__db.commit()

    def delete_all(self):
        query = 'delete from context where 1'
        self.__cursor.execute(query)
        self.__db.commit()

    def __iter__(self):
        query = 'select user_id from context'
        user_ids = self.__cursor.execute(query).fetchall()
        for user_id in user_ids:
            user_id = user_id[0]
            context = self.load(user_id)
            if context:
                yield context


def activate(config) -> SqliteBackend:
    log.debug('Activating SQLITE context backend')
    return SqliteBackend(config['Name'])
