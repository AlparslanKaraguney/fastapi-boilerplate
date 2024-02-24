from enum import Enum


class Source(Enum):
    API = "API"
    ADMIN = "ADMIN"

    def get_options(self):
        return [source.value for source in Source]
