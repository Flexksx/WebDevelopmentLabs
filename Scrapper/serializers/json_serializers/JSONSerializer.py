from serializers.Serializer import ISerializer
from serializers.json_serializers.Encoder import Encoder
from serializers.json_serializers.Decoder import Decoder


class JSONSerializer(ISerializer):
    def __init__(self):
        self.encoder = Encoder()
        self.decoder = Decoder()

    def serialize(self, obj: any) -> str:
        return self.encoder.encode(obj)

    def deserialize(self, data: str, cls: type = None) -> any:
        return self.decoder.decode(data, cls)
