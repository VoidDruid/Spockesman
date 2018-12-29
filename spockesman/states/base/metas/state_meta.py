from copy import deepcopy

from .environment import STATES


class StateMeta(type):

    def __new__(mcs, name, bases, dct):
        try:
            transform = dct['transform']
        except KeyError:
            transform = tuple()
        if bases:
            last_transform = bases[0].transform
        else:
            last_transform = tuple()

        transform = tuple({*transform, *last_transform})
        dct['transform'] = transform

        def property_gen(requested_key):
            try:
                item = dct[requested_key]
            except KeyError:
                return

            def act_prop():
                # TODO: this is pretty slow, try to find another way
                return deepcopy(item)
            return item, act_prop

        for key in transform:
            attr_pair = property_gen(key)
            if attr_pair:
                dct[f"__{key}"], dct[key] = attr_pair[0], attr_pair[1]

        cls = super().__new__(mcs, name, bases, dct)
        STATES[name] = cls
        return cls
