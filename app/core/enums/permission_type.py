from enum import Enum


class PermissionType(Enum):
    READ = "READ"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    def get_options(self):
        return [permission_type.value for permission_type in PermissionType]
