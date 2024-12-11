from node.electable.RaftElectableContext import RaftElectableContext
from node.state.CandidateState import CandidateState
from node.state.FollowerState import FollowerState
from node.state.LeaderState import LeaderState
from node.state.RaftState import AbstractRaftState


class StateManager:
    def __init__(self, context: RaftElectableContext) -> None:
        self._context = context
        self._states = {
            "Follower": FollowerState(
                context=self._context,
                state_manager=self,
                address=self._context.get_address(),
                port=self._context.get_port()
            ),
            "Candidate": CandidateState(context=self._context, state_manager=self),
            "Leader": LeaderState(context=self._context, state_manager=self),
        }
        self._state = self._states["Follower"]  # Initial state

    def get_state(self) -> AbstractRaftState:
        """Get the current state."""
        return self._state

    def transition_to(self, state_name: str):
        """
        Transition to a new state.

        Args:
            state_name (str): The name of the state to transition to.
        """
        print(f"Transitioning from {
              self._state.__class__.__name__} to {state_name}")
        self._state.on_state_exit()

        self._state = self._states[state_name]
        self._context.set_state(state_name)

        self._state.on_state_entry()

    def cleanup_current_state(self):
        """Clean up the current state when shutting down."""
        self._state.on_state_exit()
