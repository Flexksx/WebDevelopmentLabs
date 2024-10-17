from serializers.xml_serializers.XMLSerializer import XMLSerializer
from models.Product import Product
import unittest


class TestXMLSerializerEncoding(unittest.TestCase):
    def setUp(self) -> None:
        self.serializer = XMLSerializer()

    def test_serialize_number(self) -> None:
        data = 1
        expected = "<int>1</int>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_string(self) -> None:
        data = "Hello, World!"
        expected = "<str>Hello, World!</str>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_none(self) -> None:
        data = None
        expected = "<NoneType></NoneType>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_bool(self) -> None:
        data = True
        expected = "<bool>True</bool>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_list(self) -> None:
        data = [1, 2, 3, 4, 5]
        expected = "<list><int>1</int><int>2</int><int>3</int><int>4</int><int>5</int></list>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_dict(self) -> None:
        data = {"key1": 1, "key2": 2, "key3": 3}
        expected = "<dict><key1><int>1</int></key1><key2><int>2</int></key2><key3><int>3</int></key3></dict>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_dict_bool(self) -> None:
        data = {"BOOL_KEY": True}
        expected = "<dict><BOOL_KEY><bool>True</bool></BOOL_KEY></dict>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_mixed_list(self) -> None:
        data = [1, "2", 3, {"key": "value"}, 5]
        expected = "<list><int>1</int><str>2</str><int>3</int><dict><key><str>value</str></key></dict><int>5</int></list>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)

    def test_serialize_product(self) -> None:
        data = Product("Beer", "some/url", "WhiteBear", 10, 20, 0.5)
        expected = "<Product><name>Beer</name><url>some/url</url><brand>WhiteBear</brand><price>10</price><stock>20</stock><volume>0.5</volume></Product>"
        actual = self.serializer.serialize(data)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
