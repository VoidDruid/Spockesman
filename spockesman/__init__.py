from spockesman.processor import process
from spockesman.config import setup
from spockesman.states import *
from spockesman.context import Context
from spockesman.context.backend import BackendNotLoaded
from spockesman.results import ABCResult

__version__ = '0.1.3'

# TODO: refactor relative imports, change everything to absolute imports
# TODO: move to pytest from unittest
# TODO: do we really need to do 'user_input, call_args = args[:2]' everywhere?
#  Do we even need args and kwargs in state's __call__?
