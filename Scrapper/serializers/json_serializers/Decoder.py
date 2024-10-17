class Decoder:
    def __init__(self) -> None:
        pass

    def decode(self, data: str, cls: type = None) -> any:
        parsed_data = self.__parse(data)
        if cls:
            return self.__deserialize_object(parsed_data, cls)
        return parsed_data

    def __parse(self, data: str) -> any:
        if data == "null":
            return None
        elif data == "true":
            return True
        elif data == "false":
            return False
        elif data[0] == '"':
            return self.__parse_string(data)
        elif data[0] == "[":
            return self.__parse_list(data)
        elif data[0] == "{":
            return self.__parse_dict(data)
        elif self.__is_number(data):
            return self.__parse_number(data)
        else:
            return self.__parse_value(data)

    def __parse_list(self, data: str) -> list:
        data = data[1:-1]
        if not data:
            return []
        items = data.split(", ")
        return [self.__parse(item) for item in items]

    def __parse_dict(self, data: str) -> dict:
        data = data[1:-1]
        if not data:
            return {}
        items = data.split(", ")
        return {self.__parse(key): self.__parse(value) for key, value in (item.split(": ") for item in items)}

    def __parse_string(self, data: str) -> str:
        return data[1:-1]

    def __parse_number(self, data: str) -> float:
        return float(data)

    def __parse_value(self, data: str) -> any:
        return data

    def __deserialize_object(self, data: dict, cls: type) -> any:
        obj = cls.__new__(cls)
        for key, value in data.items():
            setattr(obj, key, value)
        return obj

    def __parse_bool(self, data: str) -> bool:
        return data == "true"

    def __parse_null(self, data: str) -> None:
        return None

    def __is_number(self, data: str) -> bool:
        try:
            float(data)
            return True
        except ValueError:
            return False
