from electable.RaftElectableContext import RaftElectableContext
from node.state.StateManager import StateManager
from state.RaftState import AbstractRaftState
import json


class CandidateState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager: StateManager = None) -> None:
        super().__init__(context=context, state_manager=state_manager)
        self.votes = 0

    def on_election_timeout(self):
        print(f"Node {self.context.node_id}: Starting new election for term {
              self.context.term + 1}")
        self.context.term += 1
        self.context.voted_for = self.context.node_id
        self.votes = 1  # Vote for self
        self.request_votes()

    def request_votes(self):
        for peer in self.context.peers:
            message = {
                "type": "RequestVote",
                "term": self.context.term,
                "candidate_id": self.context.node_id,
            }
            self.context.sock.sendto(json.dumps(message).encode(), peer)

    def on_receive_vote_request(self, message, addr):
        print(
            f"Node {self.context.node_id}: Ignoring vote request while Candidate")

    def on_receive_heartbeat(self, message):
        if message["term"] >= self.context.term:
            print(
                f"Node {self.context.node_id}: Received heartbeat, reverting to Follower")
            self.context.transition_to("Follower")
