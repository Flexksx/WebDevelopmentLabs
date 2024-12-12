import json
import socket
import threading
import time
from random import uniform
from raft.electable.RaftElectableContext import RaftElectableContext
from raft.electable.RaftElectablePeer import RaftElectablePeer
from raft.electable.RaftElectableState import RaftElectableState
from raft.messages.RequestVote import RequestVote
from raft.messages.VoteResponse import VoteResponse
from raft.state.RaftState import AbstractRaftState


class CandidateState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager=None) -> None:
        super().__init__(context=context, state_manager=state_manager)
        self.votes = 0
        self._listener_thread = None  # Thread for listening for messages
        self._stop_flag = False  # Flag to stop threads gracefully
        # Randomized election timeout to retry elections if no leader is elected
        self._candidate_timeout = uniform(0.3, 1.0)
        self._candidate_timer_thread = None  # Thread to monitor candidate timeout

    def on_state_entry(self):
        """Called when the node enters the Candidate state."""
        print(f"Node {self._context.get_id()}: Entered CANDIDATE state")
        self._context.increment_term()  # Increment term for the new election
        self._context.set_voted_for(self._context.get_id())  # Vote for itself
        self._context.reset_votes()  # Reset votes for the new election
        self._context.increment_votes()  # Count self-vote
        self.votes = 1  # Initialize votes with self-vote
        self.send_request_vote()  # Send RequestVote to all peers

        # Start the message listener thread
        self._listener_thread = threading.Thread(
            target=self._listen_for_messages, name="CandidateMessageListener")
        self._listener_thread.start()

        # Start the candidate election timeout thread
        self._candidate_timer_thread = threading.Thread(
            target=self._monitor_candidate_timeout, name="CandidateTimer")
        self._candidate_timer_thread.start()

    def send_request_vote(self):
        """Send RequestVote messages to all peers."""
        print(f"Node {self._context.get_id()}: Sending RequestVote")
        request_vote = RequestVote(
            term=self._context.get_term(),
            candidate_id=self._context.get_id()
        )
        for peer in self._context.get_peers():
            # Ensure that the peer is not itself
            if peer.get_id() == self._context.get_id():
                continue
            print(f"Node {self._context.get_id()
                          }: Sending RequestVote to {peer.get_id()}")
            request_vote_to_send = request_vote.to_json().encode()
            self._context.get_socket().send(request_vote_to_send, peer)

    def on_state_exit(self):
        """Called when the node exits the Candidate state."""
        print(f"Node {self._context.get_id()}: Exiting CANDIDATE state")
        self._context.reset_votes()
        self._context.set_voted_for(None)
        self._stop_flag = True  # Signal listener thread to stop

        # Ensure the listener thread exits cleanly
        if self._listener_thread and self._listener_thread.is_alive():
            self._listener_thread.join()
        if self._candidate_timer_thread and self._candidate_timer_thread.is_alive():
            self._candidate_timer_thread.join()

    def on_message(self, message: dict):
        """Handle incoming messages."""
        print(f"Node {self._context.get_id()}: Received message {message}")
        if message.get("message_type") == "RequestVote":
            self.on_request_vote(message)
        elif message.get("message_type") == "VoteResponse":
            self.on_vote_response(message)
        else:
            print(f"Node {self._context.get_id()
                          }: Ignored invalid message {message}")

    def on_request_vote(self, message: dict):
        """Handle incoming RequestVote messages while in Candidate state."""
        print(f"Node {self._context.get_id()
                      }: Received RequestVote message {message}")
        request_vote = RequestVote.from_dict(message)

        if request_vote.term > self._context.get_term():
            print(f"Node {self._context.get_id()}: Higher term detected ({
                  request_vote.term} > {self._context.get_term()}), becoming FOLLOWER")
            self._context.set_term(request_vote.term)
            self._context.set_voted_for(None)
            self._state_manager.transition_to(RaftElectableState.FOLLOWER)
            # Re-handle the request as a follower now that we've stepped down
            return self._state_manager.get_state().on_request_vote(request_vote)

        if request_vote.term < self._context.get_term():
            print(f"Node {self._context.get_id()}: RequestVote term {
                  request_vote.term} < current term {self._context.get_term()}, ignoring.")
            return None

        # Same term, already voted for self
        print(f"Node {self._context.get_id()}: Same term request from {
              request_vote.candidate_id}, already voted for self, not granting vote.")
        return None

    def on_vote_response(self, message: dict):
        """Handle incoming VoteResponse messages."""
        print(f"Node {self._context.get_id()}: Received VoteResponse")
        vote_response = VoteResponse.from_dict(message)

        if vote_response.term > self._context.get_term():
            print(f"Node {self._context.get_id()
                          }: Higher term detected, becoming FOLLOWER")
            self._context.set_term(vote_response.term)
            self._state_manager.transition_to(RaftElectableState.FOLLOWER)
            return

        if vote_response.vote_granted:
            self.votes += 1
            self._context.increment_votes()
            print(f"Node {self._context.get_id()}: Current votes: {
                  self._context.get_votes()}")
            if self._context.get_votes() > len(self._context.get_peers()) // 2:
                print(f"Node {self._context.get_id()
                              }: Achieved majority, becoming LEADER")
                self._state_manager.transition_to(RaftElectableState.LEADER)

    def _get_peer_by_id(self, peer_id: str) -> RaftElectablePeer:
        """Helper method to retrieve a peer by its ID."""
        for peer in self._context.get_peers():
            if peer.get_id() == peer_id:
                return peer
        return None

    def _listen_for_messages(self):
        """Listen for incoming messages using the shared socket."""
        while not self._stop_flag:
            try:
                print(f"Node {self._context.get_id()}: Listening for messages on {
                      self._context.get_socket().get_address()}:{self._context.get_socket().get_port()}")
                data, addr = self._context.get_socket().recvfrom(1024)
                decoded_message = self._decode_message(data)
                print(f"Node {self._context.get_id()
                              }: Received message {decoded_message}")
                self.on_message(decoded_message)
            except socket.timeout:
                # Timeout occurred, check stop_flag and continue
                continue
            except OSError:
                # Socket has been closed, exit the loop
                break
            except Exception as e:
                print(f"Node {self._context.get_id()
                              }: Error receiving message: {e}")
                break  # Optionally break on other exceptions

    def _decode_message(self, message: bytes) -> dict:
        """Decode an incoming message from bytes to a dictionary."""
        return json.loads(message.decode())

    def _monitor_candidate_timeout(self):
        """Monitor candidate timeout in a separate thread."""
        start_time = time.time()
        while not self._stop_flag:
            time.sleep(0.1)  # Check every 100ms
            elapsed_time = time.time() - start_time
            if elapsed_time >= self._candidate_timeout:
                print(f"Node {self._context.get_id(
                )}: Candidate timeout elapsed, incrementing term and retrying election")
                self._context.increment_term()
                self._context.set_voted_for(self._context.get_id())
                self._context.reset_votes()
                self._context.increment_votes()
                self.votes = 1
                self.send_request_vote()
                # Reset the timer for the new attempt
                start_time = time.time()
