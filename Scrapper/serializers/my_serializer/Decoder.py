class Decoder:
    def __init__(self) -> None:
        pass

    def decode(self, data: str, cls: type = None) -> any:
        parsed_data = self.__parse(data)
        if cls:
            return self.__deserialize_object(parsed_data, cls)
        return parsed_data

    def __parse(self, data: str) -> any:
        data = data.strip()
        if data == "null":
            return None
        elif data == "true":
            return True
        elif data == "false":
            return False
        elif data.startswith('"') and data.endswith('"'):
            return self.__parse_string(data)
        elif data.startswith("[") and data.endswith("]"):
            return self.__parse_list(data)
        elif data.startswith("{") and data.endswith("}"):
            return self.__parse_dict(data)
        elif self.__is_number(data):
            return self.__parse_number(data)
        else:
            return self.__parse_value(data)

    def __parse_list(self, data: str) -> list:
        """Parses a list from the custom encoded format."""
        data = data[1:-1].strip()
        if not data:
            return []
        items = self.__split_items(data, delimiter="|")
        return [self.__parse(item) for item in items]

    def __parse_dict(self, data: str) -> dict:
        """Parses a dictionary from the custom encoded format."""
        data = data[1:-1].strip()
        if not data:
            return {}

        items = self.__split_items(data, delimiter="|")
        parsed_dict = {}

        for item in items:
            if ' = ' in item:
                key, value = item.split(' = ', 1)
                key = self.__parse(key.strip())
                value = self.__parse(value.strip())
                parsed_dict[key] = value
            else:
                raise ValueError(f"Invalid dictionary entry: {item}")

        return parsed_dict

    def __parse_string(self, data: str) -> str:
        return data[1:-1]

    def __parse_number(self, data: str) -> float | int:
        if '.' in data:
            return float(data)
        return int(data)

    def __parse_value(self, data: str) -> any:
        return data

    def __deserialize_object(self, data: dict, cls: type) -> any:
        obj = cls.__new__(cls)
        for key, value in data.items():
            setattr(obj, key, value)
        return obj

    def __split_items(self, data: str, delimiter: str) -> list:
        """
        Splits items based on the specified delimiter while handling nested structures.
        """
        items = []
        bracket_count = 0
        brace_count = 0
        current_item = []

        for char in data:
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
            elif char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1

            # Split only when at top level (not nested)
            if char == delimiter and bracket_count == 0 and brace_count == 0:
                if current_item:
                    items.append(''.join(current_item).strip())
                    current_item = []
            else:
                current_item.append(char)

        if current_item:
            items.append(''.join(current_item).strip())

        return items

    def __is_number(self, data: str) -> bool:
        try:
            float(data)
            return True
        except ValueError:
            return False
