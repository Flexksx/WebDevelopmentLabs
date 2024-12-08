import json
import time
from electable.RaftElectableContext import RaftElectableContext
from electable.RaftElectableSocket import RaftElectableSocket
from electable.RaftElectableState import RaftElectableState
from heartbeat.RaftHeartbeat import RaftHeartbeat


class RaftHeartbeatManager():
    def __init__(self, context: RaftElectableContext, socket: RaftElectableSocket) -> None:
        self._context = context
        self._socket = socket

    def send(self):
        while self._context.get_state().is_leader():
            for peer in self._context.get_peers():
                heartbeat = RaftHeartbeat(
                    self._context.get_term(), self._context.get_id())
                self._socket.sendto(heartbeat.to_json(), peer)
                print(f"""Node {self._context.get_id()
                                } sent heartbeat to {peer}""")
            time.sleep(1)

    def receive(self):
        while True:
            data, addr = self._socket.recvfrom(1024)
            heartbeat = RaftHeartbeat.from_json(data.decode())
            if heartbeat.get_term() > self._context.get_term():
                self._context.set_term(heartbeat.get_term())
                self._context.set_state(RaftElectableState.FOLLOWER)
                self._context.set_leader_id(heartbeat.get_leader_id())
                break

    def start(self):
        self.send()
        self.receive()
        self._context.get_state().start_election()
        self._context.get_state().send_heartbeat()
        self._context.get_state().handle_messages()
