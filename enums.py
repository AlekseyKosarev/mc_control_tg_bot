from enum import Enum

class FileNamesEnum(Enum):
    SERVER_STATS = "server_stats.json"
    USERS_DATA = "users.json"

class UserRole(Enum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    PENDING_MODERATOR = 'pending_moderator'

    @classmethod
    def __getitem__(self, item):
        try:
            return self.__members__[item]
        except KeyError:
            return self.__members__[item.upper()]