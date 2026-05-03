from enum import Enum


class DefaultLogArea(Enum):
    CORE = "core"
    DATABASE = "database"
    MODELS = "models"
    SERVICES = "services"
    ROUTERS = "routers"
    UTILS = "utils"
    GENERAL = "general"