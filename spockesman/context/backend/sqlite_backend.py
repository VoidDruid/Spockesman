# access to protected methods in Context objects, it is needed to hide saving/loading from user:
# pylint: disable=W0212,R0904

import sqlite3
from typing import Optional, Iterable, Iterator, Dict

from spockesman.logger import log
from spockesman.context.context import Context
from spockesman.context.backend.abstract import AbstractBackend


class SqliteBackend(AbstractBackend):  # TODO: create base class SQLBackend and inherit from it
    """
    Implementation of abstract backend that uses redis for storage
    """

    @staticmethod
    def bool_from_int(value: int) -> bool:
        if value == 0:
            return False
        if value == 1:
            return True
        raise ValueError(f'Can not convert <int {value}> to bool')

    def __init__(self, db: str) -> None:
        if not db.endswith('.db'):
            db = db + '.db'
        self.__db = sqlite3.connect(db, check_same_thread=False)
        self.__cursor = self.__db.cursor()
        self.__cursor.execute(
            'create table if not exists context'
            '(user_id text, type text, state text, command text, input integer,'
            'data text, additional text)'
        )
        self.__db.commit()

    def deactivate(self) -> bool:
        try:
            self.__db.close()
            return True
        except sqlite3.Error:
            return False

    def __del__(self) -> None:
        self.deactivate()

    def load(self, user_id: str) -> Optional[Context]:
        query = 'select type, state, command, input, data, additional from context where user_id=?'
        values = self.__cursor.execute(query, (user_id,)).fetchone()
        if not values:
            return None
        type_, state, command, input_, data, additional = values
        context = Context.unpickle_type(type_)(user_id, state)
        context.load_data(data)
        context.command = command
        context.input = self.bool_from_int(input_)
        context._set_additional_fields(additional)
        return context

    def save(self, context: Context) -> None:
        data = context.dump_data()
        additional = context._get_additional_fields()
        query = (
            'insert into context'
            '(user_id, type, state, command, input, data, additional) '
            'values (?, ?, ?, ?, ?, ?, ?)'
        )
        state = context.state
        state_name: Optional[str] = None
        if state is not None:
            state_name = state.name
        self.__cursor.execute(
            query,
            (
                context.user_id,
                context.pickled_type,
                state_name,
                context.command,
                int(context.input),
                data,
                additional,
            ),
        )
        self.__db.commit()

    def delete(self, *user_ids: Iterable[str]) -> None:
        query = 'delete from context where user_id=?'
        self.__cursor.executemany(query, user_ids)
        self.__db.commit()

    def delete_all(self) -> None:
        query = 'delete from context where 1'
        self.__cursor.execute(query)
        self.__db.commit()

    def __iter__(self) -> Iterator[Context]:
        query = 'select user_id from context'
        user_ids = self.__cursor.execute(query).fetchall()
        for user_id in user_ids:
            user_id = user_id[0]
            context = self.load(user_id)
            if context:
                yield context


def activate(config: Dict) -> SqliteBackend:
    log.debug('Activating SQLITE context backend')
    return SqliteBackend(config['Name'])
