from node.electable.RaftElectableContext import RaftElectableContext
from node.messages.RequestVote import RequestVote
from node.messages.VoteResponse import VoteResponse
from node.state.RaftState import AbstractRaftState
import json


class CandidateState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager=None) -> None:
        super().__init__(context=context, state_manager=state_manager)
        self.votes = 0

    def on_state_entry(self):
        """Called when the node enters the Candidate state."""
        print(f"Node {self._context.get_id()}: Entered Candidate state")
        self._context.increment_term()  # Increment term for the new election
        self._context.set_voted_for(self._context.get_id())  # Vote for itself
        self._context.reset_votes()  # Reset votes for the new election
        self._context.increment_votes()  # Count self-vote
        self.send_request_vote()  # Send RequestVote to all peers

    def send_request_vote(self):
        """Send RequestVote messages to all peers."""
        print(f"Node {self._context.get_id()}: Sending RequestVote")
        request_vote = RequestVote(
            self._context.get_term(), self._context.get_id())
        for peer in self._context.get_peers():
            self._context.get_socket().send(request_vote.to_json(), peer)

    def on_state_exit(self):
        """Called when the node exits the Candidate state."""
        print(f"Node {self._context.get_id()}: Exiting Candidate state")
        self._context.reset_votes()
        self._context.set_voted_for(None)

    def on_message(self, message: dict):
        """Handle incoming messages."""
        print(f"Node {self._context.get_id()}: Received message {message}")
        if message["type"] == "RequestVote":
            self.on_request_vote(message)
        elif message["type"] == "VoteResponse":
            self.on_vote_response(message)
        else:
            print(f"Node {self._context.get_id()
                          }: Ignored invalid message {message}")

    def on_request_vote(self, message: dict):
        """Handle incoming RequestVote messages."""
        print(f"Node {self._context.get_id()}: Received RequestVote")
        request_vote = RequestVote.from_json(json.dumps(message))

        # If the incoming term is greater, transition back to Follower
        if request_vote.term > self._context.get_term():
            print(f"Node {self._context.get_id()
                          }: Higher term detected, becoming Follower")
            self._context.set_term(request_vote.term)
            self._state_manager.transition_to("Follower")
            self._state_manager.get_state().on_message(message)
            return

        # Reject vote requests with stale terms
        if request_vote.term < self._context.get_term():
            return

        # Grant vote if conditions are met
        if self._context.get_voted_for() is None or self._context.get_voted_for() == request_vote.candidate_id:
            self._context.set_voted_for(request_vote.candidate_id)
            vote_response = VoteResponse(
                voter_id=self._context.get_id(),
                term=self._context.get_term(),
                vote_granted=True,
            )
            self._context.get_socket().send(vote_response.to_json(), request_vote.candidate_id)

    def on_vote_response(self, message: dict):
        """Handle incoming VoteResponse messages."""
        print(f"Node {self._context.get_id()}: Received VoteResponse")
        vote_response = VoteResponse.from_json(json.dumps(message))

        # If the response term is higher, transition back to Follower
        if vote_response.term > self._context.get_term():
            print(f"Node {self._context.get_id()
                          }: Higher term detected, becoming Follower")
            self._context.set_term(vote_response.term)
            self._state_manager.transition_to("Follower")
            return

        # Count the vote if granted
        if vote_response.vote_granted:
            self._context.increment_votes()
            print(f"Node {self._context.get_id()}: Current votes: {
                  self._context.get_votes()}")
            # Check if a majority is reached
            if self._context.get_votes() > len(self._context.get_peers()) // 2:
                print(f"Node {self._context.get_id()
                              }: Achieved majority, becoming Leader")
                self._state_manager.transition_to("Leader")
