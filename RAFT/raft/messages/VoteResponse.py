import json


class VoteResponse:
    def __init__(self, term: int = None, vote_granted: bool = None, voter_id: str = None, candidate_id: str = None) -> None:
        self.term = term
        self.vote_granted = vote_granted
        self.voter_id = voter_id
        self.candidate_id = candidate_id

    def __str__(self):
        return f"VoteResponse({self.term}, {self.vote_granted})"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_json(json_str):
        json_dict = json.loads(json_str)
        return VoteResponse(json_dict["term"], json_dict["vote_granted"])

    @classmethod
    def from_dict(cls, data: dict):
        return cls(voter_id=data["voter_id"],
                   candidate_id=data["candidate_id"],
                   term=data["term"],
                   vote_granted=data["vote_granted"])

    def to_dict(self):
        return {
            "message_type": "VoteResponse",
            "term": self.term,
            "vote_granted": self.vote_granted,
            "voter_id": self.voter_id,
            "candidate_id": self.candidate_id
        }

    def to_bytes(self):
        return json.dumps(self.to_dict()).encode()

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_term(self):
        return self.term

    def get_vote_granted(self):
        return self.vote_granted

    def set_term(self, term):
        self.term = term

    def set_vote_granted(self, vote_granted):
        self.vote_granted = vote_granted

    def __eq__(self, other):
        return self.term == other.term and self.vote_granted == other.vote_granted

    def __ne__(self, other):
        return not self.__eq__(other)
