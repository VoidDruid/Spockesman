from .environment import STATES


class StateMeta(type):

    def __new__(mcs, name, bases, dct):
        transform = dct.get('transform', [])

        def property_gen(itm):
            item = dct[itm]

            def act_prop(self):
                return item
            return property(act_prop)

        for itm in transform:
            dct[itm] = property_gen(itm)

        cls = super().__new__(mcs, name, bases, dct)
        STATES[cls.__name__] = cls
        return cls
