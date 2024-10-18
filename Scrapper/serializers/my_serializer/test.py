from serializers.my_serializer.CustomSerializer import CustomSerializer
import unittest
from models.Product import Product


class TestCustomSerializerEncoding(unittest.TestCase):
    def setUp(self):
        self.serializer = CustomSerializer()

    def test_serialize_dict(self):
        data = {"name": "product1", "category": "category1", "price": 10.0}
        expected = "name: string = product1\ncategory: string = category1\nprice: float = 10.0"
        actual = self.serializer.serialize(data)
        self.assertEqual(self.serializer.serialize(data), expected)

    def test_serialize_product(self):
        product = Product("product1", "category1", 'aaaa', 120, 123, 32)
        expected = "name: string = product1\nurl: string = category1\nmanufacturer: string = aaaa\nprice: float = 120.0\nvolume: float = 123.0\nabv: float = 32.0\ncurrency: string = MDL"
        self.assertEqual(self.serializer.serialize(product), expected)


class TestCustomSerializerDecoding(unittest.TestCase):
    def setUp(self):
        self.serializer = CustomSerializer()

    def test_deserialize_dict(self):
        data = "name: string = product1\ncategory: string = category1\nprice: float = 10.0"
        expected = {"name": "product1", "category": "category1", "price": 10.0}
        self.assertEqual(self.serializer.deserialize(data), expected)

    def test_deserialize_product(self):
        data = "name: string = product1\nurl: string = category1\nmanufacturer: string = aaaa\nprice: float = 120.0\nvolume: float = 123.0\nabv: float = 32.0\ncurrency: string = MDL"
        expected = Product("product1", "category1", 'aaaa', 120, 123, 32)
        self.assertEqual(self.serializer.deserialize(data, Product), expected)


if __name__ == '__main__':
    unittest.main()
