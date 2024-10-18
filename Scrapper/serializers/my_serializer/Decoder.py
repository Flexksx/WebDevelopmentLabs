class Decoder:
    def __init__(self):
        pass

    def decode(self, encoded_str, cls: type = None):
        lines = encoded_str.strip().split("\n")
        data = self.__decode_lines(lines)

        if cls:  # If a class is provided, instantiate an object
            return self.__deserialize_object(data, cls)
        return data

    def __decode_lines(self, lines):
        data = {}
        stack = [data]  # Stack to handle nested structures
        current_key = None
        current_indent = 0

        for line in lines:
            stripped_line = line.lstrip()
            # Calculate indentation level
            indent_level = len(line) - len(stripped_line)

            # Handle list entries
            if stripped_line.startswith("list ="):
                items = stripped_line[len("list ="):].strip()[1:-1].split(", ")
                stack[-1][current_key] = [self.__parse_value(item)
                                          for item in items]
                continue

            # Handle dictionary entries
            if ":" in stripped_line:
                key, value = stripped_line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if indent_level > current_indent:  # New nested structure
                    current_key = key
                    new_dict = {}
                    stack[-1][key] = new_dict
                    stack.append(new_dict)
                elif indent_level < current_indent:  # Closing nested structure
                    stack.pop()
                    if stack:
                        current_key = None
                else:  # Same level
                    current_key = key

                # Store the value
                if " = " in value:
                    value_type, value_content = value.split(" = ", 1)
                    stack[-1][key] = self.__parse_value(value_content)

            current_indent = indent_level

        return data

    def __parse_value(self, value):
        if value.lower() == "none":
            return None
        elif value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value  # Treat as string if it cannot be converted

    def __deserialize_object(self, data: dict, cls: type):
        obj = cls.__new__(cls)
        for key, value in data.items():
            setattr(obj, key, value)
        return obj
