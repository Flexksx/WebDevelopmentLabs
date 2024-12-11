from node.electable.RaftElectableContext import RaftElectableContext
from node.messages.RequestVote import RequestVote
from node.state.RaftState import AbstractRaftState
import json


class CandidateState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager=None) -> None:
        super().__init__(context=context, state_manager=state_manager)
        self.votes = 0

    def on_state_entry(self):
        print(f"Node {self._context.get_id()}: Entered Candidate state")
        self._context.increment_term()
        self._context.set_voted_for(self._context.get_id())
        self._context.reset_votes()
        self._context.increment_votes()

    def send_request_vote(self):
        print(f"Node {self._context.get_id()}: Sending RequestVote")
        request_vote = RequestVote(
            self._context.get_term(), self._context.get_id())
        for peer in self._context.get_peers():
            self._context.get_socket().send(request_vote.to_json(), peer)

    def on_state_exit(self):
        print(f"Node {self._context.get_id()}: Exiting Candidate state")
        self._context.reset_votes()
        self._context.set_voted_for(None)
        self._context.set_leader_id(None)
        self._context.set_state("Follower")
        self._context.get_socket().close()

    def on_message(self, message: dict):
        print(f"Node {self._context.get_id()}: Received message {message}")
        if message["type"] == "RequestVote":
            self.on_request_vote(message)
        print(f"Node {self._context.get_id()
                      }: Received invalid message {message}")

    def on_request_vote(self, message: dict):
        print(f"Node {self._context.get_id()}: Received RequestVote")
        request_vote = RequestVote.from_json(json.dumps(message))
        if request_vote.term > self._context.get_term():
            self._context.set_term(request_vote.term)
            self._context.set_state("Follower")
            self._context.get_state().on_message(message)
        if request_vote.term < self._context.get_term():
            return
        if self._context.get_voted_for() is None or self._context.get_voted_for() == request_vote.candidate_id:
            self._context.set_voted_for(request_vote.candidate_id)
            self._context.get_socket().send(request_vote.to_json(), request_vote.candidate_id)
            self._context.increment_votes()

        if self._context.get_votes() > len(self._context.get_peers()) / 2:
            self._context.set_state("Leader")
            self._context.get_state().on_state_entry()
            self._context.get_state().send_heartbeat
