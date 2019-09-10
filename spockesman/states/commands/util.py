def default_context_transform(context, state, command):
    """
    Push user to new state and set last command's name
    :param context: Context object
    :param state: state name or State instance
    :param command: name of last command
    :return: None
    """
    context.state = state
    if not isinstance(command, str):
        command = command.name
    context.command = command
