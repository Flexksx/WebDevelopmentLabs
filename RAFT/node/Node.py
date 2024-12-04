from .NodeState import NodeState


class Node:
    def __init__(self, id: str = None, peers: list[str] = None, port: str = None) -> None:
        self._id = id
        self._peers = peers
        self._port = port
        self._state = NodeState.FOLLOWER
