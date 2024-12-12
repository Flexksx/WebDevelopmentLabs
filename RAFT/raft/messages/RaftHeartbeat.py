# In RaftHeartbeat.py
import json


class RaftHeartbeat:
    def __init__(self, term: int, leader_id: str):
        self._term = term
        self._leader_id = leader_id

    @classmethod
    def from_dict(cls, data: dict):
        return cls(term=data["term"], leader_id=data["leader_id"])

    def get_term(self) -> int:
        return self._term

    def get_leader_id(self) -> str:
        return self._leader_id

    def to_json(self) -> str:
        return json.dumps({
            "message_type": "Heartbeat",
            "term": self._term,
            "leader_id": self._leader_id
        })
