from electable.RaftElectableContext import RaftElectableContext
from node.state.StateManager import StateManager
from state.RaftState import AbstractRaftState
import json


class FollowerState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager: StateManager = None) -> None:
        super().__init__(context=context, state_manager=state_manager)

    def on_state_entry(self):
        print(f"Node {self._context.get_id()}: Entered Follower state")

    def on_election_timeout(self):
        print(
            f"""Node {self._context.get_id()}: Election timeout, becoming Candidate""")
        self._context.transition_to("Candidate")

    def on_receive_vote_request(self, message, addr):
        print(
            f"Node {self._context.get_id()}: Received vote request from {message['candidate_id']}")

        if message["term"] > self._context.get_term():
            self._context.set_term(message["term"])
            self._context.set_voted_for(None)

        if self._context.get_voted_for() is None and message["term"] == self._context.get_term():
            self._context.set_voted_for(message["candidate_id"])
            self._state_manager.get_state().on_vote_granted(
                message["candidate_id"])

        response = {
            "term": self._context.get_term(),
            "vote_granted": self._context.get_voted_for() == message["candidate_id"]
        }

        self._context.get_socket().sendto(
            json.dumps(response).encode(), addr)

    def on_receive_heartbeat(self, message):
        pass
