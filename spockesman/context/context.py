# pylint: disable=W0212,R0904
# Access to protected methods is from Context to other context objects
# Many public methods are needed to create simple interface for end-user

try:
    import ujson as json
except ImportError:
    import json  # type: ignore
import pickle
from copy import deepcopy
from typing import Any, Dict, List, Optional, Union

from spockesman.logger import log
from spockesman.states.base import INITIAL_STATE, STATES
from spockesman.states.base_state import BaseState


# TODO:
#  - input to __input and methods is_input, set_input
#  - custom data classes, store data object class
#  - command to __command and property getter
class Context:
    """
    User context. Contains user's id, state, last command, and arbitrary additional data
    """

    PICKLING_PROTOCOL = 3
    default_fields = ('user_id', 'input', 'command')

    def __init__(
        self, user_id: str, state: Union[str, BaseState] = None, data: Dict = None
    ) -> None:
        self.user_id = user_id
        self.__state: Optional[str] = None
        self.state = state  # type: ignore
        self.input: bool = False
        self.command: Optional[str] = None
        self._data: Dict
        if data is None:
            self._data = {}
        else:
            self._data = data

    @property
    def pickled_type(self) -> bytes:
        return pickle.dumps(type(self), self.PICKLING_PROTOCOL)

    @staticmethod
    def unpickle_type(type_str: bytes) -> type:
        return pickle.loads(type_str)

    @property
    def state(self) -> Optional[BaseState]:
        if self.__state is None:
            return None
        return STATES[self.__state](self)

    @state.setter
    def state(self, state_: Union[None, str, BaseState]) -> None:
        if not state_:
            self.__state = INITIAL_STATE.name
            return
        if isinstance(state_, str):
            state_name = state_
        elif isinstance(state_, type) and issubclass(state_, BaseState):
            state_name = state_.name
        else:
            raise TypeError(
                f'State for context must be either a subclass of BaseState or string, '
                f'not a {type(state_)}'
            )
        if state_name not in STATES:
            raise ValueError(
                f"State {state_} is not registered! Maybe it's a metastate? "
                f'If so, set flag is_meta to False, or user concrete state'
            )
        self.__state = state_name

    def clone(self, context: 'Context') -> None:
        if context.state:
            self.__state = context.state.name
        self.input = context.input
        self.command = context.command
        self._data = deepcopy(context._data)
        self.install_additional_fields(context.prepare_additional_fields())

    def to_dict(self) -> Dict:
        return {
            'state': self.__state,
            'input': self.input,
            'command': self.command,
            'user_id': self.user_id,
            'data': self._data,
            'additional': self._get_additional_fields(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Context':
        context = cls(data['user_id'], data['state'])
        context.input = data.get('input', False)
        context.command = data.get('command', None)
        context._data = data.get('data', {})
        context._set_additional_fields(data.get('additional', None))
        return context

    def store(self, key: str, value: Union[Dict, List, str, int, float, bool]) -> None:
        """
        Add data to context._data. We check that key is a string, because we save _data to json,
        which can break some keys (1 -> '1'), but we do not check value,
        because it can be a dict or a list, and checking it would be too expensive
        and json will raise exception on any errors anyway
        :param key:
        :param value:
        :return:
        """
        if not isinstance(key, str):
            raise TypeError(f'Only strings are allowed as keys to context data, not <type(key)>')
        self._data[key] = value

    def dump_data(self) -> str:
        try:
            return json.dumps(self._data)
        except TypeError as e:
            raise TypeError(f'Error while dumping context data - {e.args[0]}')

    def load_data(self, json_str: str) -> None:
        if self._data:
            raise ValueError('Data can be loaded only into empty context')
        try:
            self._data = json.loads(json_str)
        except json.JSONDecodeError:
            raise ValueError(f'Json representation of data is invalid: {json_str}')

    # Following method allow us to access context data easily:
    #
    # Example:
    #
    # context = Context('user_id')
    # context.store('item', 'Some item')
    # context['item'] == context._data['item'] == 'Some item'
    def __getitem__(self, item: str) -> Any:
        return self._data[item]

    # NOTE: We use json for data and pickle for additional fields,
    # because json is safe and pickle is NOT, so we provide 'data' dict as default storage
    # If user wants to store any objects, we provide the option to use additional fields with pickle
    # But control over it's safety is delegated to user
    # BY DEFAULT: store all public fields
    #
    # Following methods allow users to subclass Context,
    # add fields to it and describe how they should be loaded/stored
    #
    # Example:
    #
    # class CustomContext(Context):
    #     def __init__(self, new_field, *args, **kwargs, ):
    #         super().__init__(*args, **kwargs)
    #         self.new_field = new_field
    #
    #     def prepare_additional_fields(self):
    #         return {'new_field': self.new_field}
    #
    #     def install_additional_fields(self, data):
    #         self.new_field = data['new_field']
    #

    def prepare_additional_fields(self) -> Any:
        """
        Creates object that can be pickled, storing info about additional fields
        :return: object with all additional info that you want to save
        """
        default_fields = {
            key: item
            for key, item in self.__dict__.items()
            if not key.startswith('_') and key not in self.default_fields
        }
        if not default_fields:
            return None
        return default_fields

    def install_additional_fields(self, data: Any) -> None:
        """
        Base method, that user can override to implement loading custom fields for stored 'data'
        :param data: unpickled data object from 'prepare_additional_fields', loaded from backend
        :return: None
        """
        self.__dict__.update(data)

    def _get_additional_fields(self) -> Optional[bytes]:
        try:
            prepared_data = self.prepare_additional_fields()
            if prepared_data is None:
                return None
            return pickle.dumps(prepared_data, self.PICKLING_PROTOCOL)
        except pickle.PicklingError:
            log.exception('Error while pickling additional context fields!')
            raise

    def _set_additional_fields(self, data: bytes) -> None:
        if data is None:
            return
        try:
            self.install_additional_fields(pickle.loads(data))
        except pickle.UnpicklingError:
            log.exception('Error while unpickling additional context element!')
            raise
