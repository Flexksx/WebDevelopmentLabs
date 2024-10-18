class Encoder:
    def __init__(self):
        pass

    def encode(self, config):
        return self.__encode_value(config)

    def __encode_value(self, value, indent_level=0):
        if isinstance(value, dict):
            return self.__encode_dict(value, indent_level)
        elif isinstance(value, list):
            return self.__encode_list(value, indent_level)
        elif hasattr(value, '__dict__'):  # Check if it's an object
            return self.__encode_dict(value.__dict__, indent_level)
        elif isinstance(value, str):
            return f"string = {value}"
        elif isinstance(value, bool):
            return f"boolean = {value}"
        elif value is None:
            return "None"
        else:
            return f"{type(value).__name__} = {value}"

    def __encode_dict(self, data, indent_level=0):
        result = []
        indent = "    " * indent_level  # Four spaces for each level of indentation
        for key, value in data.items():
            result.append(f"{indent}{key}: {
                          self.__encode_value(value, indent_level + 1)}")
        return "\n".join(result)

    def __encode_list(self, data, indent_level=0):
        indent = "    " * indent_level  # Four spaces for each level of indentation
        encoded_items = [self.__encode_value(
            item, indent_level) for item in data]
        return f"list = [{', '.join(encoded_items)}]"
