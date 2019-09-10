COMMANDS = {
    'Echo': None,
    'End': '/end',
    'Start': '/start',
    'Hi': '/hi',
}

# You can change it to sqlite_backend if you do not have redis running
CONTEXT_BACKEND = {
    'Host': 'localhost',
    'Name': 0,
    'Password': None,
    'Port': 6379,
    'Type': 'redis_backend',
    'User': None
}
