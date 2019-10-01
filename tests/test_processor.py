from .util import BaseTestCase, reload


class ProcessorTest(BaseTestCase):
    user_id = '12345'
    test_input = 'Test input'

    def setUp(self) -> None:
        self.M = reload()

        class Message(self.M.ABCResult):
            def __init__(self, string):
                self.string = string

            def __str__(self):
                return self.string

            def __eq__(self, other):
                return str(other) == self.string
        self.message = Message

    def tearDown(self) -> None:
        self.M.context.backend.database.delete_all()

    def test_base_processing(self):
        with self.assertRaises(self.M.BackendNotLoaded):
            self.M.processor.process(self.user_id, self.test_input)
        self.M.setup('tests/config.yaml')
        with self.assertRaises(self.M.NoStateException):
            self.M.processor.process(self.user_id, self.test_input)
        first_proc = self.M.processor.process(self.user_id, self.test_input, state='Main')
        self.assertIsNone(first_proc)
        with self.assertRaises(self.M.InvalidCommandException):
            self.M.processor.process(self.user_id, self.test_input)
        with self.assertRaises(self.M.NoHandlerException):
            self.M.processor.process(self.user_id, '/start')
        context = self.M.context.backend.database.load(self.user_id)
        self.assertIsNotNone(context)
        self.assertEqual(context.user_id, self.user_id)
        self.assertEqual(context.state.name, 'Main')

    def prepare_context(self):
        self.M.setup('tests/config.yaml')
        self.M.context.backend.database.save(self.M.Context(self.user_id, state='Main'))

    def test_processing_loaded(self):
        self.prepare_context()
        with self.assertRaises(self.M.NoHandlerException):
            self.M.processor.process(self.user_id, '/start')

    def test_processing_errors(self):
        self.prepare_context()

        @self.M.handler(self.M.Command.Start)
        def start(context, user_input):
            return 'string'

        @self.M.handler(self.M.Command.Hi)
        def start(context, user_input):
            return 123

        with self.assertRaises(TypeError):
            self.M.process(self.user_id, '/start')

        with self.assertRaises(TypeError):
            self.M.process(self.user_id, '/hi')

    def test_processing_iterable(self):
        self.prepare_context()

        @self.M.handler(self.M.Command.Start)
        def start(context, user_input):
            return self.message('first'), (self.message('second'), self.message('third'))

        result = self.M.process(self.user_id, '/start')
        self.assertTupleEqual(result, ('first', 'second', 'third'))

    def test_processing_callable(self):
        self.prepare_context()

        def other_callable(context, user_input):
            return self.message(user_input)

        @self.M.handler(self.M.Command.Start)
        def start(context, user_input):
            return other_callable

        result = self.M.process(self.user_id, '/start')
        self.assertEqual(result, '/start')

    def test_processing_global(self):
        self.prepare_context()

        @self.M.global_command(self.M.Command.Glob)
        def start(context, user_input):
            return self.message('help')

        result = self.M.process(self.user_id, '/lol')
        self.assertEqual(result, 'help')
