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
            if start == -1 or end == -1:  # No more tags found
                break

            key = content[start + 1:end]  # Extract the tag
            value_start = end + 1
            value_end = content.find(f'</{key}>', value_start)

            if value_end == -1:  # If closing tag is not found
                break

            value_xml = content[value_start:value_end].strip()

            # Decode the value and store it directly in the items dictionary
            if self.__has_nested_tags(value_xml):
                # Recursively decode if there are nested tags
                items[key] = self.__decode_dict(value_xml)
            else:
                items[key] = self.__decode_value(value_xml)

            # Move to the next key
            content = content[value_end + len(f'</{key}>'):].strip()

        return items

    def __has_nested_tags(self, content: str):
        # Check for any tags in the content
        return '<' in content and '>' in content and content.count('<') > 1

    def __decode_value(self, value: str):
        value = value.strip()  # Remove extra whitespace
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
                return value  # Treat it as a string

    def __deserialize_object(self, data: dict, cls: type):
        obj = cls.__new__(cls)
        for key, value in data.items():
            setattr(obj, key, value)
        return obj
