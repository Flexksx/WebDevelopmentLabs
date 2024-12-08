from node.electable.RaftElectableContext import RaftElectableContext
from node.state.CandidateState import CandidateState
from node.state.FollowerState import FollowerState
from node.state.LeaderState import LeaderState


class StateManager:
    def __init__(self, context: RaftElectableContext) -> None:
        self._context = context
        self._state = FollowerState(context)
        self._states = {
            "Follower": FollowerState(context=self._context, state_manager=self),
            "Candidate": CandidateState(context=self._context, state_manager=self),
            "Leader": LeaderState(context=self._context, state_manager=self),
        }

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def transition_to(self, state_name):
        self._state = self._states[state_name]
        self._context.set_state(state_name)
        self._state.on_state_entry()
        return self._state
