import random
from node.electable.RaftElectablePeer import RaftElectablePeer
from node.electable.RaftElectableSocket import RaftElectableUDPSocket
from node.electable.RaftElectableState import RaftElectableState


class RaftElectableContext:
    """Represents the context of a Raft electable node.
    Used to store properties of a node, rather than putting it all in the node class.
    """

    def __init__(self,
                 node_id: str = None,
                 term: int = 0,
                 voted_for: str = None,
                 leader_id: str = None,
                 peers: list[RaftElectablePeer] = None,
                 address: str = None,
                 port: int = None,
                 ) -> None:
        """
        Args:
            node_id(str): Unique ID for the node.
            term(int): Current term.
            voted_for(str): ID of the candidate this node voted for .
            leader_id(str): ID of the current leader.
            peers(list[RaftElectablePeer]): List of peers in the cluster.
        """
        self._id = node_id
        self._term = term
        self._voted_for = voted_for
        self._leader_id = leader_id
        self._peers = peers or []
        self._votes = 0
        self._state = RaftElectableState.FOLLOWER
        self._address = address
        self._port = port

    def get_address(self) -> str:
        """Get the address of the node."""
        return self._address

    def get_port(self) -> int:
        """Get the port of the node."""
        return self._port

    def get_socket(self) -> RaftElectableUDPSocket:
        """Get the socket of the node."""
        return self._socket

    # Term Management

    def get_term(self) -> int:
        """Get the current term."""
        return self._term

    def set_term(self, term: int) -> None:
        """Set the current term."""
        self._term = term
        self._voted_for = None  # Reset vote for new term

    def increment_term(self) -> None:
        """Increment the term and reset the voted_for field."""
        self._term += 1
        self._voted_for = None

    # Voted For
    def get_voted_for(self) -> str:
        """Get the ID of the candidate this node voted for ."""
        return self._voted_for

    def set_voted_for(self, voted_for: str) -> None:
        """Set the ID of the candidate this node voted for ."""
        self._voted_for = voted_for

    # State Management
    def get_state(self) -> RaftElectableState:
        """Get the current state of the node."""
        return self._state

    def set_state(self, state: RaftElectableState) -> None:
        """Set the current state of the node."""
        if self._state != state:
            print(f"Node {self._id} transitioning from {
                  self._state} to {state}")
        self._state = state

    # Leader Management
    def get_leader_id(self) -> str:
        """Get the ID of the current leader."""
        return self._leader_id

    def set_leader_id(self, leader_id: str) -> None:
        """Set the ID of the current leader."""
        self._leader_id = leader_id

    # Peer Management
    def get_peers(self) -> list[RaftElectablePeer]:
        """Get the list of peers in the cluster."""
        return self._peers

    def set_peers(self, peers: list[RaftElectablePeer]) -> None:
        """Set the list of peers in the cluster."""
        self._peers = peers

    def add_peer(self, peer: RaftElectablePeer) -> None:
        """Add a peer to the cluster."""
        if peer not in self._peers:
            self._peers.append(peer)
            print(f"Node {self._id} added peer {peer.get_id()}")

    def remove_peer(self, peer_id: str) -> None:
        """Remove a peer from the cluster by its ID."""
        self._peers = [
            peer for peer in self._peers if peer.get_id() != peer_id]
        print(f"Node {self._id} removed peer {peer_id}")

    # ID Management
    def get_id(self) -> str:
        """Get the ID of this node."""
        return self._id

    def set_id(self, node_id: str) -> None:
        """Set the ID of this node."""
        self._id = node_id

    # Election Timeout
    def get_election_timeout(self) -> float:
        """Get the election timeout."""
        return self._election_timeout

    def reset_election_timeout(self) -> None:
        """Reset the election timeout to a new randomized value."""
        self._election_timeout = random.uniform(0.15, 0.3)

    # Votes
    def get_votes(self) -> int:
        """Get the number of votes received by this node."""
        return self._votes

    def reset_votes(self) -> None:
        """Reset the vote count."""
        self._votes = 0

    def increment_votes(self) -> None:
        """Increment the vote count by one."""
        self._votes += 1
