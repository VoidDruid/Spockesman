from .context.backend import database, BackendNotLoaded
from .states import WrongCommandException


def process(user_id, user_input):
    try:
        context = database.load(user_id)
    except BackendNotLoaded:
        return None, None
    try:
        reply, ui = context.state.process_input(user_input)
    except WrongCommandException:
        return None, None
    database.save(user_id, context)
    return reply, ui
