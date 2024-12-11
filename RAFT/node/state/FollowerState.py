import json
import threading
import time
from random import randint
import socket

from node.electable.RaftElectablePeer import RaftElectablePeer
from node.electable.RaftElectableContext import RaftElectableContext
from node.electable.RaftElectableSocket import RaftElectableUDPSocket
from node.messages.RequestVote import RequestVote
from node.messages.VoteResponse import VoteResponse
from node.messages.RaftHeartbeat import RaftHeartbeat
from node.state.RaftState import AbstractRaftState


class FollowerState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager=None, address: str = None, port: int = None) -> None:
        super().__init__(context=context, state_manager=state_manager)
        self.__heartbeat_timeout = randint(
            150, 300) / 1000  # Random timeout in seconds
        self._last_heartbeat_time = time.time()  # Timestamp of last heartbeat
        self._monitor_thread = None  # Thread for monitoring heartbeat timeouts
        self._listener_thread = None  # Thread for listening for messages
        self._stop_flag = False  # Flag to stop threads gracefully
        print(address, port)
        # Initialize its own socket
        if address is None or port is None:
            raise ValueError(
                "Address and port must be provided for FollowerState's socket.")
        self._socket = RaftElectableUDPSocket(
            address=address, port=port, timeout=0.5)  # 500ms timeout

    def on_state_entry(self):
        """Called when the node enters the Follower state."""
        print(f"Node {self._context.get_id()}: Entered Follower state")
        self._last_heartbeat_time = time.time()  # Reset heartbeat timer
        self._stop_flag = False  # Reset stop flag for threads

        # Start the heartbeat timeout monitor thread
        self._monitor_thread = threading.Thread(
            target=self._monitor_heartbeat_timeout, name="HeartbeatMonitor")
        self._monitor_thread.start()

        # Start the message listener thread
        self._listener_thread = threading.Thread(
            target=self._listen_for_messages, name="MessageListener")
        self._listener_thread.start()

    def on_state_exit(self):
        """Called when the node exits the Follower state."""
        print(f"Node {self._context.get_id()}: Exited Follower state")
        self._stop_flag = True  # Signal threads to stop

        # Close the socket to unblock recvfrom
        self._socket.close()

        # Ensure the threads exit cleanly
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join()
        if self._listener_thread and self._listener_thread.is_alive():
            self._listener_thread.join()

    def reset_heartbeat_timer(self):
        """Reset the heartbeat timer (called when a heartbeat is received)."""
        self._last_heartbeat_time = time.time()
        print(f"Node {self._context.get_id()}: Heartbeat timer reset")

    def on_timeout(self):
        """Triggered when the heartbeat timeout occurs."""
        print(f"Node {self._context.get_id()
                      }: Heartbeat timeout, transitioning to Candidate state")
        self._state_manager.transition_to("Candidate")

    def on_request_vote(self, request_vote: RequestVote):
        """Handle a vote request."""
        print(f"Node {self._context.get_id()}: Received vote request from {
              request_vote.get_candidate_id()}")
        if self._context.get_term() < request_vote.get_term():
            self._context.set_term(request_vote.get_term())
            self._context.set_voted_for(None)
            self._state_manager.transition_to("Follower")

        if self._context.get_voted_for() is None or self._context.get_voted_for() == request_vote.get_candidate_id():
            if self._context.get_term() == request_vote.get_term():
                self._context.set_voted_for(request_vote.get_candidate_id())
                return VoteResponse(self._context.get_id(), request_vote.get_candidate_id(), request_vote.get_term(), True)

        return VoteResponse(self._context.get_id(), request_vote.get_candidate_id(), request_vote.get_term(), False)

    def on_heartbeat(self, heartbeat: RaftHeartbeat):
        """Handle a received Heartbeat message."""
        print(f"Node {self._context.get_id()}: Received heartbeat from leader {
              heartbeat.get_leader_id()}")
        if heartbeat.get_term() >= self._context.get_term():
            self._context.set_term(heartbeat.get_term())
            self._context.set_leader_id(heartbeat.get_leader_id())
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
                message, addr = self._socket.recvfrom(1024)
                decoded_message = self._decode_message(message)
                self._handle_message(decoded_message, addr)
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

    def _handle_message(self, message: dict, addr: tuple):
        """Handle an incoming message."""
        message_type = message.get("type")
        if message_type == "RequestVote":
            request_vote = RequestVote.from_dict(message)
            response = self.on_request_vote(request_vote)
            if response:
                self._socket.sendto(response.to_bytes(), addr)
        elif message_type == "Heartbeat":
            heartbeat = RaftHeartbeat.from_dict(message)
            self.on_heartbeat(heartbeat)
