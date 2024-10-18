from serializers.Serializer import ISerializer
from serializers.my_serializer.Encoder import Encoder
from serializers.my_serializer.Decoder import Decoder


class CustomSerializer(ISerializer):
    def __init__(self) -> None:
        super().__init__()
        self.encoder = Encoder()
        self.decoder = Decoder()

    def serialize(self, data) -> str:
        return self.encoder.encode(data)

    def deserialize(self, data, cls=None):
        return self.decoder.decode(data, cls)
