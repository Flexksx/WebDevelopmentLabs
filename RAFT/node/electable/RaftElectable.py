from electable.RaftElectablePeer import RaftElectablePeer
from electable.RaftElectableSocket import RaftElectableUDPSocket
from electable.RaftElectableState import RaftElectableState
from electable.RaftElectableContext import RaftElectableContext
from node.state.FollowerState import FollowerState
from node.state.StateManager import StateManager


class RaftElectable:
    def __init__(self, id: str = None, peers: list[RaftElectablePeer] = None, address: str = None, port: str = None) -> None:
        self.context = RaftElectableContext(
            id=id, peers=peers, state=RaftElectableState.FOLLOWER, socket=RaftElectableUDPSocket(address=address, port=port))
        self.state = StateManager(self.context)
