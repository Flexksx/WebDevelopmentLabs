import json
import time
from electable.RaftElectableContext import RaftElectableContext
from node.state.StateManager import StateManager
from state.RaftState import AbstractRaftState


class LeaderState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager: StateManager = None) -> None:
        super().__init__(context=context, state_manager=state_manager)

    def on_election_timeout(self):
        print(f"Node {self.context.node_id}: Leader does not timeout")

    def on_receive_vote_request(self, message, addr):
        print(f"Node {self.context.node_id}: Ignoring vote request while Leader")

    def on_receive_heartbeat(self, message):
        print(
            f"Node {self.context.node_id}: Received heartbeat while Leader (ignoring)")

    def send_heartbeats(self):
        while self.context.state == "Leader":
            for peer in self.context.peers:
                message = {
                    "type": "Heartbeat",
                    "term": self.context.term,
                    "leader_id": self.context.node_id,
                }
                self.context.sock.sendto(json.dumps(message).encode(), peer)
            print(f"Node {self.context.node_id}: Sent heartbeats")
            time.sleep(1)
