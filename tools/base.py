from typing import TypedDict, Literal, NotRequired, Callable

JSONSchemaType = Literal["string", "number", "object", "array", "boolean", "null"]


class ToolProperty(TypedDict):
    type: JSONSchemaType
    description: NotRequired[str]
    enum: NotRequired[list]  # allowed values - basically same as Literal


class ToolParameters(TypedDict):
    type: Literal["object"]
    properties: dict[str, ToolProperty]
    required: list[str]  # property names


class FunctionDescription(TypedDict):
    name: str
    description: NotRequired[str]
    parameters: ToolParameters


class ToolDict(TypedDict):
    # "Tool" is a broader category, but right now only tools of type "function" exist
    type: Literal["function"]
    function: FunctionDescription


class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        properties: dict[str, ToolProperty],
        required: list[str],
        callable: Callable[..., str],
    ):
        self.type = "function"
        self.name = name
        self.description = description
        self.parameters = ToolParameters(
            type="object", properties=properties, required=required
        )
        self.function_description = FunctionDescription(
            name=name, description=description, parameters=self.parameters
        )
        self.dict = ToolDict(type="function", function=self.function_description)
        self.callable = callable

    def __call__(self, *args, **kwargs) -> str:
        return self.callable(*args, **kwargs)
