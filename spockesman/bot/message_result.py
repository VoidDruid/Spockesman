from enum import Enum, auto

from spockesman import AbstractResult


class ResourceType(Enum):
    PICTURE = auto()
    GIF = auto()
    VIDEO = auto()


class Resource:
    def __init__(self, path, resource_type):
        self.path = path
        self.type = resource_type


class Message(AbstractResult):
    def __init__(self, resource, ui=None):
        self.resource = resource
        self.ui = ui
