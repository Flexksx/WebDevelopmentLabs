class ISerializer:
    def __init__(self) -> None:
        pass

    def serialize(self, data: any) -> str:
        pass

    def deserialize(self, data: str) -> any:
        pass
