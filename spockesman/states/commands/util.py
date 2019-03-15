def default_context_transform(context, state, command):
    context.state = state
    if not isinstance(command, str):
        command = command.name
    context.command = command
