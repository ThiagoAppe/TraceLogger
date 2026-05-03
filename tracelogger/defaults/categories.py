from enum import Enum


class DefaultLogCategory(Enum):
    SYSTEM = "system"
    USER = "user"
    AUTH = "auth"
    FILES = "files"
    NOTIFICATION = "notification"