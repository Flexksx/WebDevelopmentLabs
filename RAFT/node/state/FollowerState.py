from random import randint
from electable.RaftElectableContext import RaftElectableContext
from node.state.StateManager import StateManager
from state.RaftState import AbstractRaftState
import json


class FollowerState(AbstractRaftState):
    def __init__(self, context: RaftElectableContext = None, state_manager: StateManager = None) -> None:
        super().__init__(context=context, state_manager=state_manager)
        self._heartbeat_timeout = randint(150, 300) / 1000

    def on_state_entry(self):
        print(f"Node {self._context.get_id()}: Entered Follower state")

    def on_state_exit(self):
        print(f"Node {self._context.get_id()}: Exited Follower state")

    def await_heartbeat(self):
        print(f"Node {self._context.get_id()}: Awaiting heartbeat")
        self._context.set_state("Follower")
        self._context.set_leader_id(None)
        self._context.set_voted_for(None)
        self._context.set_term(self._context.get_term() + 1)
