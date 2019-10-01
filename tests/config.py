COMMANDS = {
    'Echo': None,
    'Passd': None,
    'End': '/end',
    'Start': '/start',
    'Hi': '/hi',
}

# You can change it to redis_backend if you have it running
CONTEXT_BACKEND = {
    'Name': 'example',
    'Type': 'sqlite_backend',
}

STATES = {
    'Main': {
        'Type': 'Basic',
        'Commands': {
            'Start': 'Repeat',
            'Hi': 'Transient',
        },
    },
    'Repeat': {
        'Type': 'Cyclic',
        'Cycle': 'Echo',
        'Commands': {
            'End': 'Main',
        },
    },
    'Transient': {
        'Type': 'Transient',
        'Transition': {
            'Command': {
                'Type': 'COMMAND',
                'Value': 'Passd',
            },
            'State': 'Repeat',
        },
    },
}
