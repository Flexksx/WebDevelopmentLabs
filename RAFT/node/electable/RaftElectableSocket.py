import socket


class RaftElectableUDPSocket:
    def __init__(self, address: str = None, port: int = None, timeout: float = 0.5) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._address = address
        print(f"Binding to address {self._address}")
        self._port = port
        print(f"Binding to port {self._port}")
        self._sock.bind((self._address, self._port))
        self._sock.settimeout(timeout)  # Set timeout to 0.5 seconds

    def recvfrom(self, size: int) -> tuple:
        print(f"Receiving from {self._address}:{self._port}")
        return self._sock.recvfrom(size)

    def sendto(self, message: bytes, addr: tuple) -> None:
        self._sock.sendto(message, addr)

    def close(self) -> None:
        self._sock.close()

    def get_address(self) -> str:
        return self._address

    def get_port(self) -> int:
        return self._port

    def set_address(self, address: str) -> None:
        self._address = address

    def set_port(self, port: int) -> None:
        self._port = port

    def get_sock(self) -> socket.socket:
        return self._sock

    def set_sock(self, sock: socket.socket) -> None:
        self._sock = sock
