import random
from node.electable.RaftElectablePeer import RaftElectablePeer
from node.electable.RaftElectableSocket import RaftElectableSocket
from node.electable.RaftElectableState import RaftElectableState


class RaftElectableContext:
    def __init__(self,
                 id: str = None,
                 term: int = 0,
                 voted_for: str = None,
                 leader_id: str = None,
                 peers: list[RaftElectablePeer] = None,
                 socket: RaftElectableSocket = None
                 ) -> None:
        self._id = id
        self._term = term
        self._voted_for = voted_for
        self._leader_id = leader_id
        self._peers = peers or []
        self._election_timeout = random.randint(150, 300) / 1000
        self._socket = socket

    def get_term(self) -> int:
        return self._term

    def set_term(self, term: int) -> None:
        self._term = term

    def increment_term(self) -> None:
        """Increment the term and reset voted_for."""
        self._term += 1
        self._voted_for = None

    def get_voted_for(self) -> str:
        return self._voted_for

    def set_voted_for(self, voted_for: str) -> None:
        self._voted_for = voted_for

    def get_state(self) -> RaftElectableState:
        return self._state

    def set_state(self, state: RaftElectableState) -> None:
        print(f"Node {self._id} transitioning from {self._state} to {state}")
        self._state = state

    def get_leader_id(self) -> str:
        return self._leader_id

    def set_leader_id(self, leader_id: str) -> None:
        self._leader_id = leader_id

    def get_peers(self) -> list[RaftElectablePeer]:
        return self._peers

    def set_peers(self, peers: list[RaftElectablePeer]) -> None:
        self._peers = peers

    def add_peer(self, peer: RaftElectablePeer) -> None:
        """Add a peer to the list if it's not already present."""
        if peer not in self._peers:
            self._peers.append(peer)
            print(f"Node {self._id} added peer {peer.get_id()}")

    def remove_peer(self, peer_id: str) -> None:
        """Remove a peer by its ID."""
        self._peers = [
            peer for peer in self._peers if peer.get_id() != peer_id]
        print(f"Node {self._id} removed peer {peer_id}")

    def get_id(self) -> str:
        return self._id

    def set_id(self, id: str) -> None:
        self._id = id
