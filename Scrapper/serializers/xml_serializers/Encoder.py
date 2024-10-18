class Encoder:
    def __init__(self) -> None:
        pass

    def encode(self, data: any, root_tag: str = None) -> str:
        if isinstance(data, list):
            return self.__encode_list(data, root_tag)
        elif isinstance(data, dict):
            return self.__encode_dict(data, root_tag)
        elif hasattr(data, "__dict__"):
            return self.__encode_object(data, root_tag)
        else:
            return self.__encode_value(data, root_tag)

    def __encode_list(self, data: list, root_tag: str) -> str:
        items = "".join(f"<item>{self.encode(item)}</item>" for item in data)
        return f"<list>{items}</list>"  # Using the provided root tag for lists

    def __encode_dict(self, data: dict, root_tag: str) -> str:
        items = [f"<{key}>{self.encode(
            value)}</{key}>" for key, value in data.items()]
        return "".join(items)

    def __encode_object(self, obj: object, root_tag: str) -> str:
        # Using the class name of the object as the tag
        items = "".join(f"<{key}>{self.encode(
            value)}</{key}>" for key, value in obj.__dict__.items())
        return f"<{obj.__class__.__name__}>{items}</{obj.__class__.__name__}>"

    def __encode_value(self, value: any, root_tag: str) -> str:
        if isinstance(value, str):
            return value
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            return str(value)
        elif isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return ""
        else:
            raise ValueError(f"Unsupported type: {type(value)}")
