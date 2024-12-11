import json
import time
from node.electable.RaftElectableContext import RaftElectableContext
from node.messages.RaftHeartbeat import RaftHeartbeat
from node.state.RaftState import AbstractRaftState


class LeaderState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager=None) -> None:
        super().__init__(context=context, state_manager=state_manager)
        self._last_heartbeat = time.time()

    def on_state_entry(self):
        print(f"Node {self._context.get_id()}: Entered Leader state")
        self._context.set_leader_id(self._context.get_id())
        self._context.set_voted_for(None)
        self._context.reset_votes()
        self._context.increment_term()

    def on_state_exit(self):
        print(f"Node {self._context.get_id()}: Exiting Leader state")

    def send_hearbeat(self):
        self._last_heartbeat = time.time()
        heartbeat = RaftHeartbeat(
            self._context.get_term(), self._context.get_id())
        for peer in self._context.get_peers():
            self._context.get_socket().sendto(
                heartbeat.to_json(), peer)
