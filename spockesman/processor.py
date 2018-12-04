from .context.backend import BackendNotLoaded, database
from .logger import log
from .states import WrongCommandException, NoHandlerException


def process(user_id, user_input, context=None):
    log.debug(f"Processing input: '{user_input}', user: '{user_id}'")
    load = not context
    if load:
        try:
            context = database.load(user_id)
        except BackendNotLoaded as e:
            log.error('Tried to process input, but context storage backend was not initialized.')
            log.exception(e)
            return None, None
    try:
        reply, ui = context.state(user_input)
    except WrongCommandException as e:
        log.error(f"Tried to process input, but user's input is neither global command, "
                  f"or a command available in current state: {type(context.state).__name__}")
        log.exception(e)
        return None, None
    except NoHandlerException as e:
        log.error(f"Tried to process input, user's input is a command, but no handler for it was found.")
        log.exception(e)
        return None, None
    if load:
        database.save(user_id, context)
    return reply, ui
