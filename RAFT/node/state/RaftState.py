from abc import ABC, abstractmethod

from node.electable.RaftElectableContext import RaftElectableContext


class AbstractRaftState(ABC):
    def __init__(self, context: RaftElectableContext = None, state_manager=None) -> None:
        self._state_manager = state_manager
        self._context = context

    @abstractmethod
    def on_state_entry(self):
        """Handle state entry."""
        pass

    @abstractmethod
    def on_state_exit(self):
        """Handle state exit."""
        pass
