from .processor import process
from .config import setup
from .states import *
from .context import Context
from .context.backend import BackendNotLoaded
from .results import ABCResult

__version__ = '0.1.2'

# TODO: refactor relative imports, change everything to absolute imports
# TODO: move to pytest from unittest
# TODO: do we really need to do 'user_input, call_args = args[:2]' everywhere?
#  Do we even need args and kwargs in state's __call__?
