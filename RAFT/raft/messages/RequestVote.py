# In RequestVote.py
import json


class RequestVote:
    def __init__(self, term: int, candidate_id: str):
        self.term = term
        self.candidate_id = candidate_id

    @classmethod
    def from_dict(cls, data: dict):
        return cls(term=data["term"], candidate_id=data["candidate_id"])

    def to_dict(self):
        return {
            "message_type": "RequestVote",
            "term": self.term,
            "candidate_id": self.candidate_id
        }

    def to_bytes(self):
        return json.dumps(self.to_dict()).encode()

    def to_json(self):
        return json.dumps(self.to_dict())
