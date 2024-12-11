from node.electable.RaftElectablePeer import RaftElectablePeer
from node.electable.RaftElectableSocket import RaftElectableUDPSocket
from node.electable.RaftElectableState import RaftElectableState
from node.electable.RaftElectableContext import RaftElectableContext
from node.state.FollowerState import FollowerState
from node.state.StateManager import StateManager


class RaftElectable:
    def __init__(self, id: str = None, peers: list[RaftElectablePeer] = None, address: str = None, port: str = None) -> None:
        # self._socket = RaftElectableUDPSocket(address=address, port=port)
        self.context = RaftElectableContext(
            node_id=id, peers=peers, address=address, port=port)
        self.state = StateManager(self.context)
