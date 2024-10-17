from serializers.Serializer import ISerializer
from serializers.xml_serializers.Encoder import Encoder
from serializers.xml_serializers.Decoder import Decoder


class XMLSerializer(ISerializer):
    def __init__(self) -> None:
        super().__init__()
        self.encoder = Encoder()
        self.decoder = Decoder()

    def serialize(self, data) -> str:
        return self.encoder.encode(data)

    def deserialize(self, data: str, cls: type = None) -> any:
        return self.decoder.decode(data, cls)
