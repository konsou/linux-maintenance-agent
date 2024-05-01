from enum import Enum, auto


class Actions(Enum):
    PLAN = auto()
    COMMUNICATE = auto()
    RUN_COMMAND_LINE = auto()
    WRITE_FILE = auto()
    SPAWN_AND_EXECUTE = auto()
    INVALID = auto()


ValidActionValue = (
    int
    | float
    | str
    | bool
    | None
    | list["ValidActionValue"]
    | dict[str, "ValidActionValue"]
)

ActionResponse = dict[str, ValidActionValue]
