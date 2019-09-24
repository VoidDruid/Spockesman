from .util import BaseTestCase


class ContextTest(BaseTestCase):
    user_id = '12345'

    @classmethod
    def setUpClass(cls):
        cls.setUpPackage(cls)
        cls.M.setup('tests/config.yaml')

    @property
    def context(self):
        return self.M.Context(self.user_id)

    def test_basic(self):
        context = self.context
        self.assertDictEqual({
            'state': None,
            'input': False,
            'command': None,
            'user_id': self.user_id,
            'data': {},
            'additional': None
        }, context.to_dict())

    def test_raises_on_unregistered(self):
        class TestUnregisteredState:
            def __init__(self, context_):
                pass
        with self.assertRaises(TypeError):
            self.M.Context(self.user_id, TestUnregisteredState)

    def test_state(self):
        class TestState(self.M.State):
            def __init__(self, context_):
                pass
        context = self.M.Context(self.user_id, TestState)
        self.assertTrue(isinstance(context.state, TestState))
        self.assertDictEqual({
            'state': 'TestState',
            'input': False,
            'command': None,
            'user_id': self.user_id,
            'data': {},
            'additional': None
        }, context.to_dict())

    def test_initial_state(self):
        @self.M.initial
        class TestInitialState(self.M.State):
            def __init__(self, context_):
                pass
        context = self.context
        self.assertTrue(isinstance(context.state, TestInitialState))
        self.assertDictEqual({
            'state': 'TestInitialState',
            'input': False,
            'command': None,
            'user_id': self.user_id,
            'data': {},
            'additional': None
        }, context.to_dict())

    def test_data_access(self):
        context = self.context
        item_1 = 'Some item'
        item_2 = 'Other item'
        context.store('item', item_1)
        self.assertEqual(context['item'], item_1)
        context.store('item', item_2)
        self.assertEqual(context['item'], item_2)

    def test_additional_fields(self):
        class CustomContext(self.M.Context):
            def __init__(self, *args, new_field=None, **kwargs):
                super().__init__(*args, **kwargs)
                self.new_field = new_field

        context = CustomContext(self.user_id, new_field='new_field_value')
        self.assertEqual(context.new_field, 'new_field_value')
        self.assertDictEqual({
            'new_field': 'new_field_value',
        }, context.prepare_additional_fields())

    def test_cloning(self):
        class CustomContext(self.M.Context):
            def __init__(self, *args, new_field=None, **kwargs):
                super().__init__(*args, **kwargs)
                self.new_field = new_field

        context = CustomContext(self.user_id, new_field='new_field_value')
        cloned = CustomContext(self.user_id)
        cloned.clone(context)
        self.assertEqual(cloned.new_field, 'new_field_value')
