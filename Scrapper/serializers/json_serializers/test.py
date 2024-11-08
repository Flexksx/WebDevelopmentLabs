
from serializers.json_serializers.JSONSerializer import JSONSerializer
from models.Product import Product
import unittest


class TestJSONSerializerEncoding(unittest.TestCase):
    def setUp(self):
        self.serializer = JSONSerializer()

    def test_serialize_number(self):
        data = 1
        expected = "1"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_string(self):
        data = "Hello, World!"
        expected = '"Hello, World!"'
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_none(self):
        data = None
        expected = "null"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_bool(self):
        data = True
        expected = "true"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_dict_bool(self):
        data = {"BOOL_KEY": True}
        expected = '{"BOOL_KEY": true}'
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_list(self):
        data = [1, 2, 3, 4, 5]
        expected = "[1, 2, 3, 4, 5]"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_mixed_list(self):
        data = [1, '2', 3, {"key": "value"}, 5]
        expected = '[1, "2", 3, {"key": "value"}, 5]'
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_dict(self):
        data = {"key1": 1, "key2": 2, "key3": 3}
        expected = '{"key1": 1, "key2": 2, "key3": 3}'
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_object(self):
        data = Product("Beer", "some/url", "WhiteBear", 10, 20, 0.5)
        expected = '{"name": "Beer", "url": "some/url", "manufacturer": "WhiteBear", "price": 10, "volume": 20, "abv": 0.5, "currency": "MDL"}'
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)


class TestJSONSerializerDecoding(unittest.TestCase):
    def setUp(self):
        self.serializer = JSONSerializer()

    def test_deserialize_number(self):
        data = "1"
        expected = 1
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)

    def test_deserialize_string(self):
        data = '"Hello, World!"'
        expected = "Hello, World!"
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)

    def test_deserialize_none(self):
        data = "null"
        expected = None
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)

    def test_deserialize_bool(self):
        data = "true"
        expected = True
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)

    def test_deserialize_list(self):
        data = "[1, 2, 3, 4, 5]"
        expected = [1, 2, 3, 4, 5]
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)

    def test_deserialize_dict(self):
        data = '{"key1": 1, "key2": 2, "key3": 3}'
        expected = {"key1": 1, "key2": 2, "key3": 3}
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)

    def test_deserialize_dict_bool(self):
        data = '{"BOOL_KEY": true}'
        expected = {"BOOL_KEY": True}
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)

    def test_deserialize_bool(self):
        data = "true"
        expected = True
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)

    def test_deserialize_mixed_list(self):
        data = '[1, "2", 3, {"key": "value"}, 5]'
        expected = [1, '2', 3, {"key": "value"}, 5]
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)

    def test_deserialize_object(self):
        data = '{"name": "Beer", "url": "some/url", "manufacturer": "WhiteBear", "price": 10, "volume": 20, "abv": 0.5, "currency": "MDL"}'
        expected = Product("Beer", "some/url", "WhiteBear", 10, 20, 0.5)
        actual = self.serializer.deserialize(data, cls=Product)
        print(actual)
        print(expected)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
