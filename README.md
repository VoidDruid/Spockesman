# Spockesman 
![Logo](logo.png)
###### Declarative state-machine - mainly for chat bots

---

Example usage in *examples directory*.

### Roadmap:
- Move to **pytest** from unittest
- Do we really need to do `user_input, call_args = args[:2]` everywhere?
Do we even need `*args` and `**kwargs` in state's `__call__`?
- More **tests**: context backend, state processing, tricky handlers
- Remove global variables! **Make state machine a class**, instead of collection of `COMMANDS` and `STATES`
- #### CI:
    - setup integrate TeamCity
    - setup linters
    - setup code-coverage checks
- #### Ideas:
    - Generate config file from loaded state machine
