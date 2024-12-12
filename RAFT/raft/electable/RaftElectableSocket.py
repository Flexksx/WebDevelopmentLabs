import socket

from raft.electable.RaftElectablePeer import RaftElectablePeer


class RaftElectableUDPSocket:
    def __init__(self, address: str = None, port: int = None, timeout: float = 0.5) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._address = address
        print(f"Binding to address {self._address}")
        self._port = port
        print(f"Binding to port {self._port}")
        self._sock.bind(("0.0.0.0", self._port))
        self._sock.settimeout(timeout)  # Set timeout to 0.5 seconds

    def recvfrom(self, size: int) -> tuple:
        return self._sock.recvfrom(size)

    def send(self, message: str, addr: tuple) -> None:
        if isinstance(message, str):
            message = message.encode('utf-8')
        if isinstance(addr, RaftElectablePeer):
            addr = (addr.get_address(), addr.get_port())
            print(f"Sending to {addr} the message: {message}")
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
