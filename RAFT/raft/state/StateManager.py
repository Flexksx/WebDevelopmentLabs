from raft.electable.RaftElectableContext import RaftElectableContext
from raft.state.CandidateState import CandidateState
from raft.state.FollowerState import FollowerState
from raft.state.LeaderState import LeaderState
from raft.state.RaftState import AbstractRaftState
from raft.electable.RaftElectableState import RaftElectableState


class StateManager:
    def __init__(self, context: RaftElectableContext) -> None:
        self._context = context
        self._states = {
            RaftElectableState.FOLLOWER: FollowerState(
                context=self._context,
                state_manager=self,
            ),
            RaftElectableState.CANDIDATE: CandidateState(context=self._context, state_manager=self),
            RaftElectableState.LEADER: LeaderState(context=self._context, state_manager=self),
        }
        # Initial state
        self._state = self._states[RaftElectableState.FOLLOWER]

    def get_state(self) -> AbstractRaftState:
        """Get the current state."""
        return self._state

    def transition_to(self, state: RaftElectableState):
        """
        Transition to a new state.

        Args:
            state_name (str): The name of the state to transition to.
        """
        print(f"Transitioning from {
              self._state.__class__.__name__} to {str(state)}")
        self._state.on_state_exit()

        self._state = self._states[state]
        self._context.set_state(state)

        self._state.on_state_entry()

    def cleanup_current_state(self):
        """Clean up the current state when shutting down."""
        self._state.on_state_exit()
