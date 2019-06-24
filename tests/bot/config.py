COMMANDS = {
    'Echo': None,
    'End': '/end',
    'Glob': '/lol',
    'Hi': '/hi',
    'Passd': None,
    'Start': '/start'
}

CONTEXT_BACKEND = {
    'Host': 'localhost',
    'Name': 0,
    'Password': None,
    'Port': 6379,
    'Type': 'redis',
    'User': None
}

GLOBAL = [
    'Globs'
]

STATES = {
    'Main': {
        'Commands': {
            'Hi': 'Transient',
            'Start': 'Repeat'
        },
        'Type': 'Basic'
    },
    'Repeat': {
        'Commands': {
            'End': 'Main'
        },
        'Cycle': 'Echo',
        'Type': 'Cyclic'
    },
    'Transient': {
        'Transition': {
            'Command': {
                'Type': 'COMMAND',
                'Value': 'Passd'
            },
            'State': 'Repeat'
        },
        'Type': 'Transient'
    }
}
