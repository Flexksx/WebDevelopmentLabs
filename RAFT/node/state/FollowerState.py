from random import randint
from node.electable.RaftElectableContext import RaftElectableContext
from node.messages.RequestVote import RequestVote
from node.messages.VoteResponse import VoteResponse
from node.state.RaftState import AbstractRaftState


class FollowerState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager=None) -> None:
        super().__init__(context=context, state_manager=state_manager)
        self.__heartbeat_timeout = randint(150, 300) / 1000
        self._current_timeout = 0

    def on_state_entry(self):
        print(f"Node {self._context.get_id()}: Entered Follower state")

    def on_state_exit(self):
        print(f"Node {self._context.get_id()}: Exited Follower state")

    def on_timeout(self):
        self._state_manager.set_state(
            self._state_manager.transition_to("Candidate"))

    def on_request_vote(self, request_vote: RequestVote):
        print(f"Node {self._context.get_id()}: Received vote request from {
              request_vote.get_candidate_id()}")
        if self._context.get_current_term() < request_vote.get_term():
            self._context.set_current_term(request_vote.get_term())
            self._context.set_voted_for(None)
            self._state_manager.set_state(
                self._state_manager.transition_to("Follower"))
        if self._context.get_voted_for() is None or self._context.get_voted_for() == request_vote.get_candidate_id():
            if self._context.get_current_term() == request_vote.get_term():
                self._context.set_voted_for(request_vote.get_candidate_id())
                return VoteResponse(self._context.get_id(), request_vote.get_candidate_id(), request_vote.get_term(), True)
        return VoteResponse(self._context.get_id(), request_vote.get_candidate_id(), request_vote.get_term(), False)

    def on_vote_response(self, vote_response: VoteResponse):
        print(f"Node {self._context.get_id()}: Received vote response from {
              vote_response.get_voter_id()}")
        if vote_response.get_vote_granted():
            self._context.increment_votes()
            if self._context.get_votes() >= (len(self._context.get_peers()) / 2) + 1:
                self._state_manager.set_state(
                    self._state_manager.transition_to("Leader"))
        else:
            if self._context.get_current_term() < vote_response.get_term():
                self._context.set_current_term(vote_response.get_term())
                self._context.set_voted_for(None)
                self._state_manager.set_state(
                    self._state_manager.transition_to("Follower"))

    def check_timeout(self, delta):
        self._current_timeout += delta
        if self._current_timeout >= self.__heartbeat_timeout:
            self._current_timeout = 0
            self.on_timeout()
        return self._current_timeout
