from enum import Enum


class Command(Enum):
    BUILD = 'build'
    RUN = 'run'
    REBUILD = 'rebuild'
    RESTART = 'restart'
    STOP = 'stop'
    REMOVE = 'remove'
    SREMOVE = 'sremove'
    ALL = 'all'
