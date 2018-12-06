import logging
import sys
import unittest

logging.basicConfig(level=logging.INFO)

from tests import *

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'bot':
        from tests.bot.main import bot
        # bot.start_method()

    else:
        print('\nWARNING!\n'
              'Full test run requires redis server running on localhost:6379!\n'
              'Otherwise, many tests for "processor.process(...)" will FAIL.\n')
        unittest.main()
