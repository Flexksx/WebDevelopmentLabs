# node/state/FollowerState.py

import json
import threading
import time
from random import uniform
import socket

from raft.electable.RaftElectablePeer import RaftElectablePeer
from raft.electable.RaftElectableContext import RaftElectableContext
from raft.electable.RaftElectableState import RaftElectableState
from raft.messages.RequestVote import RequestVote
from raft.messages.VoteResponse import VoteResponse
from raft.messages.RaftHeartbeat import RaftHeartbeat
from raft.state.RaftState import AbstractRaftState


class FollowerState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager=None) -> None:
        super().__init__(context=context, state_manager=state_manager)
        # Assign different timeout ranges based on node ID to stagger elections
        node_id = self._context.get_id()
        if node_id == "node1":
            self.__heartbeat_timeout = uniform(0.2, 0.7)
        elif node_id == "node2":
            self.__heartbeat_timeout = uniform(0.3, 0.8)
        elif node_id == "node3":
            self.__heartbeat_timeout = uniform(0.4, 0.9)
        else:
            self.__heartbeat_timeout = uniform(0.2, 1.0)  # Default range

        self._last_heartbeat_time = time.time()  # Timestamp of last heartbeat
        self._monitor_thread = None  # Thread for monitoring heartbeat timeouts
        self._listener_thread = None  # Thread for listening for messages
        self._stop_flag = False  # Flag to stop threads gracefully
        address = self._context.get_address()
        port = self._context.get_port()
        # Initialize its own socket
        if address is None or port is None:
            raise ValueError(
                "Address and port must be provided for FollowerState's socket.")
        self._socket = self._context.get_socket()

    def on_state_entry(self):
        """Called when the node enters the Follower state."""
        print(f"Node {self._context.get_id()}: Entered Follower state")
        self._last_heartbeat_time = time.time()
        self._stop_flag = False

        self._monitor_thread = threading.Thread(
            target=self._monitor_heartbeat_timeout, name="HeartbeatMonitor")
        self._monitor_thread.start()

        self._listener_thread = threading.Thread(
            target=self._listen_for_messages, name="MessageListener")
        self._listener_thread.start()

    def on_state_exit(self):
        """Called when the node exits the Follower state."""
        print(f"Node {self._context.get_id()}: Exited Follower state")
        self._stop_flag = True
        current_thread = threading.current_thread()
        # Ensure the threads exit cleanly without joining the current thread
        if self._monitor_thread and self._monitor_thread.is_alive() and self._monitor_thread != current_thread:
            self._monitor_thread.join()
        if self._listener_thread and self._listener_thread.is_alive() and self._listener_thread != current_thread:
            self._listener_thread.join()

    def reset_heartbeat_timer(self):
        """Reset the heartbeat timer (called when a heartbeat is received)."""
        self._last_heartbeat_time = time.time()
        print(f"Node {self._context.get_id()}: Heartbeat timer reset")

    def on_timeout(self):
        """Triggered when the heartbeat timeout occurs."""
        print(f"Node {self._context.get_id()
                      }: Heartbeat timeout, transitioning to Candidate state")
        self._state_manager.transition_to(RaftElectableState.CANDIDATE)

    def on_request_vote(self, request_vote: RequestVote):
        """Handle a RequestVote message in the Follower state."""
        print(f"Node {self._context.get_id()}: Received vote request from {
              request_vote.candidate_id}")

        if request_vote.term > self._context.get_term():
            # Update term and vote for candidate
            self._context.set_term(request_vote.term)
            self._context.set_voted_for(request_vote.candidate_id)
            print(f"Node {self._context.get_id()}: Granting vote to {
                  request_vote.candidate_id} for term {request_vote.term}")
            # Transition to Follower is redundant since already in FollowerState
            # But if needed to reset state, it can be called
            # self._state_manager.transition_to(RaftElectableState.FOLLOWER)
            return VoteResponse(
                voter_id=self._context.get_id(),
                candidate_id=request_vote.candidate_id,
                term=request_vote.term,
                vote_granted=True
            )
        elif request_vote.term < self._context.get_term():
            print(f"Node {self._context.get_id()}: RequestVote term {
                  request_vote.term} < current term {self._context.get_term()}, ignoring.")
            return None
        else:  # request_vote.term == current term
            if (self._context.get_voted_for() is None or
                    self._context.get_voted_for() == request_vote.candidate_id):
                self._context.set_voted_for(request_vote.candidate_id)
                print(f"Node {self._context.get_id()}: Granting vote to {
                      request_vote.candidate_id} for term {request_vote.term}")
                return VoteResponse(
                    voter_id=self._context.get_id(),
                    candidate_id=request_vote.candidate_id,
                    term=request_vote.term,
                    vote_granted=True
                )
            else:
                print(f"Node {self._context.get_id()}: Already voted this term, cannot grant vote to {
                      request_vote.candidate_id}")
                return None

    def on_heartbeat(self, heartbeat: RaftHeartbeat):
        """Handle a received Heartbeat message."""
        print(f"Node {self._context.get_id()}: Received heartbeat from leader {
              heartbeat.leader_id}")
        if heartbeat.term >= self._context.get_term():
            self._context.set_term(heartbeat.term)
            self._context.set_leader_id(heartbeat.leader_id)
            self.reset_heartbeat_timer()

    def _monitor_heartbeat_timeout(self):
        """Monitor heartbeat timeout in a separate thread."""
        while not self._stop_flag:
            time.sleep(0.1)  # Check every 100ms
            elapsed_time = time.time() - self._last_heartbeat_time
            if elapsed_time >= self.__heartbeat_timeout:
                self.on_timeout()
                break  # Exit the thread loop after triggering the timeout

    def _listen_for_messages(self):
        """Listen for incoming messages using its own socket."""
        while not self._stop_flag:
            try:
                print(f"Node {self._context.get_id()}: Listening for messages on {
                      self._socket.get_address()}:{self._socket.get_port()}")
                data, addr = self._socket.recvfrom(1024)
                decoded_message = self._decode_message(data)
                self._handle_message(decoded_message, addr)
            except socket.timeout:
                continue
            except OSError:
                break
            except Exception as e:
                print(f"Node {self._context.get_id()
                              }: Error receiving message: {e}")
                break

    def _decode_message(self, data: bytes) -> dict:
        """Decode an incoming message from bytes to a dictionary."""
        try:
            return json.loads(data.decode())
        except json.JSONDecodeError as e:
            print(f"Node {self._context.get_id()}: JSON decode error: {e}")
            return {}

    def _handle_message(self, message: dict, addr: tuple):
        """Handle an incoming message."""
        print(f"Node {self._context.get_id()}: Received message {message}")
        message_type = message.get("message_type")
        if message_type == "RequestVote":
            # Construct a RequestVote object from the dictionary
            request_vote = RequestVote.from_dict(message)
            response = self.on_request_vote(request_vote)
            if response:
                self._socket.send(response.to_bytes(), addr)
        elif message_type == "Heartbeat":
            # Construct a RaftHeartbeat object from the dictionary
            heartbeat = RaftHeartbeat.from_dict(message)
            self.on_heartbeat(heartbeat)
        else:
            print(f"Node {self._context.get_id()
                          }: Unknown message type {message_type}")
