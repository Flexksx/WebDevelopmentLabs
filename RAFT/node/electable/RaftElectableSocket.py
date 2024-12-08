import socket

from node.electable.RaftElectablePeer import RaftElectablePeer


class RaftElectableSocket:
    def __init__(self, address: str = None, port: int = None) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._address = address
        print(f"Binding to address {self._address}")
        self._port = port
        print(f"Binding to port {self._port}")
        self._sock.bind((self._address, self._port))

    def recvfrom(self, size: int) -> tuple:
        return self._sock.recvfrom(size)

    def send(self, message: dict, peer: RaftElectablePeer) -> None:
        self._sock.sendto(message, (peer.get_address(), peer.get_port()))

    def receive(self) -> dict:
        return self._sock.recv(1024)

    def close(self) -> None:
        self._sock.close()

    def get_address(self) -> str:
        return self._address

    def set_address(self, address: str) -> None:
        self._address = address

    def get_port(self) -> int:
        return self._port

    def set_port(self, port: int) -> None:
        self._port = port

    def get_sock(self) -> socket:
        return self._sock

    def set_sock(self, sock: socket) -> None:
        self._sock = sock
