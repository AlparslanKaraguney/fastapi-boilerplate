from enum import Enum


class Action(Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    SOFT_DELETE = "SOFT_DELETE"
    HARD_DELETE = "HARD_DELETE"

    def get_options(self):
        return [action.value for action in Action]
