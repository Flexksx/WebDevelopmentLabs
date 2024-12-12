class RaftElectablePeer:
    def __init__(self, id: str = None, address: str = None, port: int = None) -> None:
        self._id = id
        self._address = address
        self._port = port
        print(f"Created peer {self._id} at {self._address}:{self._port}")

    def get_id(self) -> str:
        return self._id

    def set_id(self, id: str) -> None:
        self._id = id

    def get_address(self) -> str:
        return self._address

    def set_address(self, address: str) -> None:
        self._address = address

    def get_port(self) -> int:
        return self._port

    def set_port(self, port: int) -> None:
        self._port = port
