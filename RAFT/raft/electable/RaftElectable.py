from raft.electable.RaftElectablePeer import RaftElectablePeer
from raft.electable.RaftElectableSocket import RaftElectableUDPSocket
from raft.electable.RaftElectableState import RaftElectableState
from raft.electable.RaftElectableContext import RaftElectableContext
from raft.state.FollowerState import FollowerState
from raft.state.StateManager import StateManager


class RaftElectable:
    def __init__(self, id: str = None, peers: list[RaftElectablePeer] = None, address: str = None, port: str = None) -> None:
        # self._socket = RaftElectableUDPSocket(address=address, port=port)
        self.context = RaftElectableContext(
            node_id=id, peers=peers, address=address, port=port)
        self.state = StateManager(self.context)
