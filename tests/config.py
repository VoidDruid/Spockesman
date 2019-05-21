Events:
  Start: [/start]
  End: [/end]
  Echo:
  Hi: [/hi]
  Passd:
  Glob: [/lol]
ContextBackend:
  Type: redis
  Host: localhost
  Port: 6379
  User:
  Password:
  Name: 0
Global: [Globs]
States:
  Main:
    Type: Basic
    Commands:
      Start: Repeat
      Hi: Transient
  Repeat:
    Type: Cyclic
    Cycle: Echo
    Commands:
      End: Main
  Transient:
    Type: Transient
    Transition:
      Command:
        Type: COMMAND
        Value: Passd
      State: Repeat
