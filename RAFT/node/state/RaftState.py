from abc import ABC, abstractmethod

from node.electable.RaftElectableContext import RaftElectableContext
from node.state.StateManager import StateManager


class AbstractRaftState(ABC):
    def __init__(self, context: RaftElectableContext = None, state_manager: StateManager = None) -> None:
        self._state_manager = state_manager
        self._context = context

    @abstractmethod
    def on_state_entry(self):
        """Handle state entry."""
        pass

    @abstractmethod
    def on_election_timeout(self):
        """Handle election timeout."""
        pass

    @abstractmethod
    def on_receive_vote_request(self, message, addr):
        """Handle a RequestVote message."""
        pass

    @abstractmethod
    def on_receive_heartbeat(self, message):
        """Handle a Heartbeat message."""
        pass

    @abstractmethod
    def on_receive_vote_response(self, message):
        """Handle a VoteResponse message."""
        pass

    @abstractmethod
    def on_receive_client_request(self, message):
        """Handle a client request."""
        pass

    @abstractmethod
    def on_receive_client_response(self, message):
        """Handle a client response."""
        pass
