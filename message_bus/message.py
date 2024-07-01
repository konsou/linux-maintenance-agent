import dataclasses
import json
from typing import Mapping, Any


class MessageType:
    CHAT_MESSAGE = "CHAT_MESSAGE"
    TEST = "TEST"


ValidMessageValue = (
    int
    | float
    | str
    | bool
    | None
    | list["ValidMessageValue"]
    | dict[str, "ValidMessageValue"]
)


def is_valid_message_value(value: Any) -> bool:
    if isinstance(value, (int, float, str, bool, type(None))):
        return True
    elif isinstance(value, list):
        return all(is_valid_message_value(item) for item in value)
    elif isinstance(value, dict):
        return all(
            isinstance(key, str) and is_valid_message_value(val)
            for key, val in value.items()
        )
    return False


@dataclasses.dataclass
class Message:
    message_type: MessageType
    key: str
    source: str
    target: str
    value: ValidMessageValue

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not isinstance(self.key, str):
            raise TypeError("Key must be a string")
        if not isinstance(self.source, str):
            raise TypeError("Source must be a string")
        if not isinstance(self.target, str):
            raise TypeError("Target must be a string")
        if not is_valid_message_value(self.value):
            raise TypeError("Value must be a ValidMessageValue")

    def as_dict(self) -> dict[str, ValidMessageValue]:
        return dataclasses.asdict(self)

    def as_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.as_dict(), indent=indent)

    @classmethod
    def from_dict(cls, d: Mapping[str, ValidMessageValue]) -> "Message":
        return cls(
            str(d["message_type"]),
            str(d["key"]),
            str(d["source"]),
            str(d["target"]),
            d["value"],
        )

    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        return cls.from_dict(json.loads(json_str))
