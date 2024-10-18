class Decoder:
    def __init__(self):
        pass

    def decode(self, xml_string: str, cls: type = None):
        xml_string = xml_string.strip()
        parsed_data = self.__decode_dict(xml_string)
        if cls:
            first_key = list(parsed_data.keys())[0]
            parsed_data = parsed_data[first_key]
            return self.__deserialize_object(parsed_data, cls)
        return parsed_data

    def __decode_dict(self, content: str):
        items = {}

        while content:
            start = content.find('<')
            end = content.find('>', start)
            if start == -1 or end == -1:
                break
            key = content[start + 1:end]
            value_start = end + 1
            value_end = content.find(f'</{key}>', value_start)
            if value_end == -1:
                break
            value_xml = content[value_start:value_end].strip()

            if self.__has_nested_tags(value_xml):
                items[key] = self.__decode_dict(value_xml)
            else:
                items[key] = self.__decode_value(value_xml)

            content = content[value_end + len(f'</{key}>'):].strip()

        return items

    def __has_nested_tags(self, content: str):
        return '<' in content and '>' in content and content.count('<') > 1

    def __decode_value(self, value: str):
        value = value.strip()
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    def __deserialize_object(self, data: dict, cls: type):
        obj = cls.__new__(cls)
        for key, value in data.items():
            setattr(obj, key, value)
        return obj
