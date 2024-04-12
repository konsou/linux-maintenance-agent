from typing import Literal, NotRequired, Optional, TypedDict


class FunctionDescription(TypedDict):
  description: NotRequired[str]
  name: str
  parameters: object # JSON Schema object


class Tool(TypedDict):
  type: Literal['function']
  function: FunctionDescription

ToolChoice = Literal['none', 'auto'] | TypedDict('ToolChoice', {
    'type': Literal['function'],
    'function': dict[Literal['name'], str]
})

class Message(TypedDict):
    role: Literal["assistant", "user", "system", "tool"]
    content: str
    tools: NotRequired[list[Tool]]
    tool_choice: NotRequired[ToolChoice]