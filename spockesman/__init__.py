from spockesman.processor import process, NoStateException, CorruptedContextRecord
from spockesman.config import setup
from spockesman.states import *
from spockesman.context import Context
from spockesman.context.backend import BackendNotLoaded
from spockesman.results import ABCResult

__version__ = '0.4.5'

# TODO: move to pytest from unittest
# TODO: do we really need to do 'user_input, call_args = args[:2]' everywhere?
#  Do we even need *args and **kwargs in state's __call__?
# TODO: write more tests
# TODO: remove global variables!
# TODO: generate config file from loaded state machine
# TODO: setup linters
# TODO: setup CI
# TODO: setup code-coverage checks
