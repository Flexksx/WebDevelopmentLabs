from serializers.xml_serializers.XMLSerializer import XMLSerializer
from models.Product import Product
import unittest


class TestXMLSerializerEncoding(unittest.TestCase):
    def setUp(self) -> None:
        self.serializer = XMLSerializer()

    def test_serialize_list(self) -> None:
        data = [1, 2, 3, 4, 5]
        expected = "<list><item>1</item><item>2</item><item>3</item><item>4</item><item>5</item></list>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_dict(self) -> None:
        data = {"name": "John", "age": 25, "is_student": True}
        expected = "<name>John</name><age>25</age><is_student>true</is_student>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_product(self) -> None:
        data = Product("Beer", "some/url", "WhiteBear", 10, 20, 0.5)
        expected = "<Product><name>Beer</name><url>some/url</url><manufacturer>WhiteBear</manufacturer><price>10</price><volume>20</volume><abv>0.5</abv><currency>MDL</currency></Product>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_nested_objects(self) -> None:
        data = {"name": "John", "age": 25, "is_student": True, "address": {
            "city": "Chisinau", "street": "Stefan cel Mare"}}
        expected = "<name>John</name><age>25</age><is_student>true</is_student><address><city>Chisinau</city><street>Stefan cel Mare</street></address>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_dict_with_list(self) -> None:
        data = {"name": "John", "age": 25,
                "is_student": True, "grades": [9, 10, 8, 9]}
        expected = "<name>John</name><age>25</age><is_student>true</is_student><grades><list><item>9</item><item>10</item><item>8</item><item>9</item></list></grades>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)


class TestXMLSerializerDecoding(unittest.TestCase):
    def setUp(self) -> None:
        self.serializer = XMLSerializer()

    def test_deserialize_dict(self) -> None:
        data = "<name>John</name><age>25</age><is_student>true</is_student>"
        expected = {"name": "John", "age": 25, "is_student": True}
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)

    def test_deserialize_product(self) -> None:
        data = "<Product><name>Beer</name><url>some/url</url><manufacturer>WhiteBear</manufacturer><price>10</price><volume>20</volume><abv>0.5</abv><currency>MDL</currency></Product>"
        expected = Product("Beer", "some/url", "WhiteBear", 10, 20, 0.5)
        actual = self.serializer.deserialize(data, Product)
        self.assertEqual(expected, actual)

    def test_nested_objects(self) -> None:
        data = "<name>John</name><age>25</age><is_student>true</is_student><address><city>Chisinau</city><street>Stefan cel Mare</street></address>"
        expected = {"name": "John", "age": 25, "is_student": True, "address": {
            "city": "Chisinau", "street": "Stefan cel Mare"}}
        actual = self.serializer.deserialize(data)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
